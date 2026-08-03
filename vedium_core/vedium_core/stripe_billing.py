"""Recurring Stripe billing and durable LMS access synchronization."""

from __future__ import annotations

import re
from datetime import timedelta

import frappe
from frappe import _
from frappe.utils import add_months, cint, get_datetime, getdate, now_datetime, today

from vedium_core.frequency_pricing_rules import (
    FREQUENCY_DISCOUNT_PERCENT,
    frequency_discount_percent,
    frequency_quote,
    normalize_classes_per_week,
)
from vedium_core.stripe_billing_rules import (
    ACTIVE_ENROLLMENT_STATUSES,
    GRACE_DAYS,
    SUPPORTED_CURRENCIES,
    build_checkout_params,
    cancellation_status,
    invoice_subscription_id,
    minimum_term_months,
    normalize_period,
    refund_access_status,
)


ACTIVE_STRIPE_STATUSES = {"active", "trialing"}
INACTIVE_STRIPE_STATUSES = {"canceled", "unpaid", "incomplete_expired", "paused"}
EVENT_PROCESSING_TIMEOUT_MINUTES = 5
EVENT_ID_PATTERN = re.compile(r"^evt_[A-Za-z0-9]+$")
DEFAULT_FREQUENCY_COUPON_ID = "vedium-frequency-10"


def get_subscription_plan(course, period):
    period = normalize_period(period)
    field = (
        "custom_stripe_annual_plan"
        if period == "annual"
        else "custom_stripe_monthly_plan"
    )
    plan_name = getattr(course, field, None)
    if not plan_name:
        frappe.throw(_("O curso ainda não possui plano Stripe {0} vinculado.").format(period))

    plan = frappe.get_doc("Subscription Plan", plan_name)
    price_id = (getattr(plan, "product_price_id", None) or "").strip()
    if not price_id.startswith("price_"):
        frappe.throw(_("O plano {0} não possui Product Price ID válido.").format(plan_name))

    currency = (getattr(plan, "currency", None) or "").upper()
    if currency not in SUPPORTED_CURRENCIES:
        frappe.throw(_("O plano {0} usa uma moeda não suportada.").format(plan_name))

    interval = (getattr(plan, "billing_interval", None) or "").strip().lower()
    interval_count = cint(getattr(plan, "billing_interval_count", None) or 1)
    if interval not in {"month", "monthly"} or interval_count != 1:
        frappe.throw(_("O plano {0} não está configurado para cobrança mensal.").format(plan_name))

    gateway = getattr(plan, "payment_gateway", None)
    if not gateway:
        frappe.throw(_("O plano {0} não possui um gateway de pagamento vinculado.").format(plan_name))

    meta = frappe.get_meta("Subscription Plan")
    field = meta.get_field("payment_gateway")
    target_doctype = field.options if field else None

    controller = ""
    account_currency = None

    if target_doctype == "Payment Gateway Account":
        acc = frappe.db.get_value(
            "Payment Gateway Account",
            gateway,
            ["payment_gateway", "currency"],
            as_dict=True,
        )
        if acc:
            account_currency = acc.get("currency")
            if acc.get("payment_gateway"):
                controller = (
                    frappe.db.get_value(
                        "Payment Gateway",
                        acc.get("payment_gateway"),
                        "gateway_controller",
                    )
                    or ""
                )
    elif target_doctype == "Payment Gateway":
        controller = (
            frappe.db.get_value("Payment Gateway", gateway, "gateway_controller") or ""
        )

    if "stripe" not in controller.lower():
        frappe.throw(_("O plano {0} não está vinculado a um gateway Stripe válido.").format(plan_name))

    if account_currency and account_currency.upper() != currency:
        frappe.throw(_("O plano {0} usa um gateway Stripe configurado para a moeda incorreta.").format(plan_name))

    return plan


def get_subscription_price(course, period):
    return get_subscription_plan(course, period).product_price_id


def _retrieve_and_validate_price(stripe, course, plan, display_currency=None):
    price = stripe.Price.retrieve(plan.product_price_id)
    if not price.get("active") or price.get("type") != "recurring":
        frappe.throw(_("O Price Stripe vinculado não está ativo e recorrente."))

    recurring = price.get("recurring") or {}
    if recurring.get("interval") != "month" or int(recurring.get("interval_count") or 1) != 1:
        frappe.throw(_("O Price Stripe precisa ter recorrência mensal."))

    stripe_currency = (price.get("currency") or "").upper()
    plan_currency = (plan.currency or "").upper()
    course_currency = (getattr(course, "currency", None) or plan_currency).upper()
    requested_currency = (display_currency or plan_currency).upper()
    if not stripe_currency or stripe_currency != plan_currency:
        frappe.throw(_("A moeda do Price Stripe diverge da moeda do plano."))
    if course_currency != plan_currency or requested_currency != plan_currency:
        frappe.throw(_("A moeda exibida, o curso e o plano Stripe precisam ser iguais."))

    unit_amount = price.get("unit_amount")
    plan_cost = float(getattr(plan, "cost", 0) or 0)
    if plan_cost and unit_amount is not None and int(round(plan_cost * 100)) != int(unit_amount):
        frappe.throw(_("O valor do Price Stripe diverge do valor cadastrado no plano."))
    return price


def _frequency_coupon_id(stripe):
    """Return a reusable 10% forever coupon, creating it once per Stripe account."""
    coupon_id = (
        frappe.conf.get("STRIPE_FREQUENCY_COUPON_ID")
        or frappe.conf.get("stripe_frequency_coupon_id")
        or DEFAULT_FREQUENCY_COUPON_ID
    )
    try:
        coupon = stripe.Coupon.retrieve(coupon_id)
    except stripe.error.InvalidRequestError:
        try:
            coupon = stripe.Coupon.create(
                id=coupon_id,
                percent_off=float(FREQUENCY_DISCOUNT_PERCENT),
                duration="forever",
                name="Vedium 10% frequência",
                metadata={
                    "vedium_discount_type": "weekly_frequency",
                    "site": frappe.local.site,
                },
            )
        except stripe.error.InvalidRequestError:
            # Handles a concurrent request that created the deterministic ID first.
            coupon = stripe.Coupon.retrieve(coupon_id)

    if (
        not coupon.get("valid", True)
        or coupon.get("duration") != "forever"
        or float(coupon.get("percent_off") or 0) != float(FREQUENCY_DISCOUNT_PERCENT)
    ):
        frappe.throw(_("O cupom Stripe de frequência está configurado incorretamente."))
    return coupon.id


def create_subscription_checkout(
    course,
    user,
    coupon_code=None,
    billing_period=None,
    display_currency=None,
    classes_per_week=1,
):
    """Create a validated subscription Checkout for 1 to 5 weekly classes."""
    import stripe

    try:
        frequency = normalize_classes_per_week(classes_per_week)
    except ValueError as exc:
        frappe.throw(_(str(exc)))

    period = normalize_period(billing_period)
    plan = get_subscription_plan(course, period)
    price = _retrieve_and_validate_price(stripe, course, plan, display_currency)
    price_id = plan.product_price_id
    email = frappe.db.get_value("User", user, "email") or user
    base_url = frappe.utils.get_url()
    quote = frequency_quote((price.get("unit_amount") or 0) / 100, frequency)
    recurring_frequency_discount = float(frequency_discount_percent(frequency))
    metadata = {
        "course_name": str(course.name),
        "user": str(user),
        "site": str(frappe.local.site),
        "coupon_code": coupon_code or "",
        "billing_period": period,
        "minimum_term_months": str(minimum_term_months(period)),
        "price_id": price_id,
        "classes_per_week": str(frequency),
        "frequency_discount_percent": str(recurring_frequency_discount),
        "unit_amount": str(quote["unit_amount"]),
        "monthly_subtotal": str(quote["subtotal"]),
        "monthly_final_amount": str(quote["amount"]),
    }
    params = build_checkout_params(
        price_id,
        email,
        f"{course.name}|{user}",
        base_url,
        course.name,
        metadata,
    )
    params["line_items"][0]["quantity"] = frequency

    promotional_discount = _discount_percent(coupon_code, user)
    if recurring_frequency_discount and promotional_discount:
        frappe.throw(
            _(
                "O desconto por frequência não é cumulativo com cupons promocionais. "
                "Remova o cupom para continuar."
            )
        )
    if recurring_frequency_discount:
        params["discounts"] = [{"coupon": _frequency_coupon_id(stripe)}]
    elif promotional_discount:
        stripe_coupon = stripe.Coupon.create(
            percent_off=promotional_discount,
            duration="once",
            name=f"Vedium {coupon_code}",
            metadata={"vedium_coupon_code": coupon_code, "site": frappe.local.site},
        )
        params["discounts"] = [{"coupon": stripe_coupon.id}]

    session = stripe.checkout.Session.create(**params)
    return session.url


def _discount_percent(coupon_code, user):
    if not coupon_code:
        return 0
    coupon = frappe.db.get_value(
        "Coupon",
        coupon_code,
        ["discount_percent", "active", "max_uses", "used_count", "valid_from", "valid_to"],
        as_dict=True,
    )
    now = now_datetime()
    if coupon:
        valid = (
            coupon.active
            and (not coupon.valid_from or coupon.valid_from <= now)
            and (not coupon.valid_to or coupon.valid_to >= now)
        )
        available = not coupon.max_uses or (coupon.used_count or 0) < coupon.max_uses
        return float(coupon.discount_percent or 0) if valid and available else 0

    from vedium_core.referrals import validate_referral_code

    referral = validate_referral_code(coupon_code, referee=user)
    return float(referral.discount_percent or 0) if referral else 0


def _event_log_name(event_id):
    if not event_id or not EVENT_ID_PATTERN.fullmatch(str(event_id)):
        frappe.throw(_("Stripe event ID inválido"), frappe.AuthenticationError)
    return f"stripe-{event_id}"


def _claim_event(event_id, event_type):
    name = _event_log_name(event_id)
    row = frappe.db.get_value(
        "Integration Request",
        name,
        ["status", "modified", "custom_vedium_attempts"],
        as_dict=True,
    )
    now = now_datetime()
    if row:
        if row.status == "Completed":
            return None
        if row.status == "Queued" and get_datetime(row.modified) > now - timedelta(
            minutes=EVENT_PROCESSING_TIMEOUT_MINUTES
        ):
            return None
        frappe.db.set_value(
            "Integration Request",
            name,
            {
                "status": "Queued",
                "error": None,
                "custom_vedium_attempts": cint(row.custom_vedium_attempts) + 1,
                "custom_vedium_last_attempt_on": now,
            },
        )
    else:
        doc = frappe.get_doc(
            {
                "doctype": "Integration Request",
                "name": name,
                "request_id": event_id,
                "integration_request_service": "Stripe Webhook",
                "is_remote_request": 1,
                "request_description": str(event_type or "unknown")[:140],
                "status": "Queued",
                "custom_vedium_attempts": 1,
                "custom_vedium_last_attempt_on": now,
            }
        )
        try:
            doc.insert(ignore_permissions=True)
        except frappe.DuplicateEntryError:
            return None
    # Persist the claim so a handler rollback cannot erase the idempotency key.
    frappe.db.commit()
    return name


def _mark_event(name, status, failure_code=None):
    if not name:
        return
    values = {"status": status}
    if status == "Completed":
        values.update({"output": "processed", "error": None})
    elif failure_code:
        values["error"] = str(failure_code)[:140]
    frappe.db.set_value("Integration Request", name, values)


def handle_stripe_event(event):
    """Process a signed Stripe event once, with a durable retryable audit row."""
    event_id = event.get("id")
    event_type = event.get("type")
    log_name = _claim_event(event_id, event_type)
    if not log_name:
        return {"duplicate": True}
    try:
        _dispatch_event(event_type, event.get("data", {}).get("object", {}))
        _mark_event(log_name, "Completed")
        return {"processed": True}
    except Exception as exc:
        frappe.db.rollback()
        _mark_event(log_name, "Failed", type(exc).__name__)
        frappe.db.commit()
        frappe.log_error(
            f"Stripe event {event_id} failed ({type(exc).__name__})",
            "Vedium.payments.stripe_webhook",
        )
        raise


def _dispatch_event(event_type, obj):
    if event_type == "checkout.session.completed":
        _checkout_completed(obj)
    elif event_type == "invoice.paid":
        _invoice_paid(obj)
    elif event_type == "invoice.payment_failed":
        _invoice_failed(obj)
    elif event_type == "customer.subscription.updated":
        _subscription_updated(obj)
    elif event_type == "customer.subscription.deleted":
        _apply_cancellation(obj.get("id"), "Assinatura cancelada na Stripe")
    elif event_type == "charge.refunded":
        _charge_refunded(obj)
    elif event_type == "charge.dispute.created":
        _dispute_created(obj)


def _checkout_completed(session):
    if session.get("mode") != "subscription":
        return
    if session.get("payment_status") not in {"paid", "no_payment_required"}:
        frappe.throw(_("Checkout de assinatura ainda não foi pago."))

    metadata = session.get("metadata") or {}
    course_name, user = _validated_reference(session, metadata)
    period = normalize_period(metadata.get("billing_period"))
    try:
        frequency = normalize_classes_per_week(metadata.get("classes_per_week"))
    except ValueError as exc:
        frappe.throw(_(str(exc)), frappe.AuthenticationError)
    course = frappe.get_doc("LMS Course", course_name)
    subscription_id = session.get("subscription")
    if not subscription_id:
        frappe.throw(_("Checkout sem assinatura Stripe"))

    import stripe

    subscription = stripe.Subscription.retrieve(subscription_id)
    _validate_subscription(subscription, session, course, user, period)

    from vedium_core.api import create_enrollment_if_paid

    name = frappe.db.exists("LMS Enrollment", {"course": course_name, "member": user})
    if not name:
        create_enrollment_if_paid(
            course_name,
            user,
            "stripe",
            subscription_id,
            (session.get("amount_total") or 0) / 100,
            (session.get("currency") or course.currency or "brl").upper(),
            metadata.get("coupon_code") or None,
        )
        name = frappe.db.exists("LMS Enrollment", {"course": course_name, "member": user})
    if not name:
        frappe.throw(_("Não foi possível criar a matrícula Stripe."))

    _save_enrollment(
        name,
        {
            "custom_stripe_customer_id": session.get("customer"),
            "custom_stripe_subscription_id": subscription_id,
            "custom_stripe_price_id": metadata.get("price_id"),
            "custom_billing_period": period,
            "custom_classes_per_week": frequency,
            "custom_frequency_discount_percent": float(
                frequency_discount_percent(frequency)
            ),
            "custom_contract_monthly_amount": (session.get("amount_total") or 0) / 100,
            "custom_minimum_term_ends_on": add_months(today(), minimum_term_months(period)),
            "custom_payment_failed_on": None,
            "custom_vedium_status": "Active",
            "custom_vedium_status_changed_on": now_datetime(),
            "custom_vedium_status_reason": "Assinatura Stripe ativa",
        },
    )


def _validated_reference(session, metadata):
    try:
        course_name, user = (session.get("client_reference_id") or "").split("|", 1)
    except ValueError:
        frappe.throw(_("Referência Stripe inválida"), frappe.AuthenticationError)
    checks = (("site", frappe.local.site), ("course_name", course_name), ("user", user))
    if any(not metadata.get(key) or metadata.get(key) != expected for key, expected in checks):
        frappe.throw(_("Metadados Stripe inválidos"), frappe.AuthenticationError)
    if not frappe.db.exists("User", user) or not frappe.db.exists("LMS Course", course_name):
        frappe.throw(_("Referência Stripe inexistente"), frappe.AuthenticationError)
    return course_name, user


def _validate_subscription(subscription, session, course, user, period):
    if subscription.get("id") != session.get("subscription"):
        frappe.throw(_("Assinatura Stripe divergente"), frappe.AuthenticationError)
    if subscription.get("status") not in ACTIVE_STRIPE_STATUSES:
        frappe.throw(_("Assinatura Stripe não está ativa"), frappe.AuthenticationError)
    if subscription.get("customer") != session.get("customer"):
        frappe.throw(_("Cliente Stripe divergente"), frappe.AuthenticationError)

    metadata = subscription.get("metadata") or {}
    try:
        frequency = normalize_classes_per_week(metadata.get("classes_per_week"))
    except ValueError as exc:
        frappe.throw(_(str(exc)), frappe.AuthenticationError)
    expected = {
        "course_name": str(course.name),
        "user": str(user),
        "site": str(frappe.local.site),
        "billing_period": period,
        "classes_per_week": str(frequency),
        "frequency_discount_percent": str(float(frequency_discount_percent(frequency))),
    }
    if any(metadata.get(key) != value for key, value in expected.items()):
        frappe.throw(_("Metadados da assinatura Stripe inválidos"), frappe.AuthenticationError)

    session_metadata = session.get("metadata") or {}
    if any(session_metadata.get(key) != value for key, value in expected.items()):
        frappe.throw(_("Metadados do Checkout Stripe inválidos"), frappe.AuthenticationError)

    plan = get_subscription_plan(course, period)
    items = ((subscription.get("items") or {}).get("data") or [])
    price_ids = {
        (item.get("price") or {}).get("id")
        for item in items
        if isinstance(item.get("price"), dict)
    }
    quantities = [int(item.get("quantity") or 0) for item in items]
    if (
        price_ids != {plan.product_price_id}
        or metadata.get("price_id") != plan.product_price_id
        or len(items) != 1
        or quantities != [frequency]
    ):
        frappe.throw(_("Itens da assinatura Stripe inválidos"), frappe.AuthenticationError)


def _find_enrollment(subscription_id):
    if not subscription_id:
        return None
    return frappe.db.get_value(
        "LMS Enrollment", {"custom_stripe_subscription_id": subscription_id}, "name"
    )


def _invoice_enrollment(invoice):
    subscription_id = invoice_subscription_id(invoice)
    name = _find_enrollment(subscription_id)
    if not name:
        return None
    enrollment = frappe.get_doc("LMS Enrollment", name)
    customer = invoice.get("customer")
    if customer and customer != enrollment.custom_stripe_customer_id:
        frappe.throw(_("Cliente da fatura Stripe inválido"), frappe.AuthenticationError)
    lines = ((invoice.get("lines") or {}).get("data") or [])
    line_price_ids = {
        (line.get("price") or {}).get("id")
        for line in lines
        if isinstance(line.get("price"), dict) and (line.get("price") or {}).get("id")
    }
    if line_price_ids and enrollment.custom_stripe_price_id not in line_price_ids:
        frappe.throw(_("Price da fatura Stripe inválido"), frappe.AuthenticationError)

    expected_frequency = cint(getattr(enrollment, "custom_classes_per_week", 0) or 0)
    matching_quantities = [
        int(line.get("quantity") or 0)
        for line in lines
        if isinstance(line.get("price"), dict)
        and (line.get("price") or {}).get("id") == enrollment.custom_stripe_price_id
    ]
    if expected_frequency and matching_quantities and expected_frequency not in matching_quantities:
        frappe.throw(_("Quantidade da fatura Stripe inválida"), frappe.AuthenticationError)
    return enrollment


def _invoice_paid(invoice):
    enrollment = _invoice_enrollment(invoice)
    if not enrollment:
        return
    requested = bool(enrollment.custom_cancellation_requested_on)
    _save_enrollment(
        enrollment.name,
        {
            "custom_payment_failed_on": None,
            "custom_vedium_status": "Cancellation Requested" if requested else "Active",
            "custom_vedium_status_changed_on": now_datetime(),
            "custom_vedium_status_reason": "Mensalidade confirmada pela Stripe",
            "custom_stripe_last_invoice_id": invoice.get("id"),
            "custom_payment_reference": invoice.get("payment_intent") or invoice.get("id"),
        },
    )


def _invoice_failed(invoice):
    enrollment = _invoice_enrollment(invoice)
    if enrollment and not enrollment.custom_payment_failed_on:
        _save_enrollment(
            enrollment.name,
            {
                "custom_payment_failed_on": now_datetime(),
                "custom_vedium_status_reason": (
                    f"Falha de pagamento; tolerância de {GRACE_DAYS} dias iniciada"
                ),
            },
        )


def _subscription_updated(subscription):
    subscription_id = subscription.get("id")
    status = subscription.get("status")
    if status in ACTIVE_STRIPE_STATUSES:
        if subscription.get("cancel_at_period_end"):
            _set_access(
                subscription_id,
                "Cancellation Requested",
                "Cancelamento agendado ao fim do período",
                cancellation_requested=True,
            )
        else:
            name = _find_enrollment(subscription_id)
            requested = bool(
                name
                and frappe.db.get_value(
                    "LMS Enrollment", name, "custom_cancellation_requested_on"
                )
            )
            _set_access(
                subscription_id,
                "Cancellation Requested" if requested else "Active",
                (
                    "Cancelamento antecipado pendente de análise"
                    if requested
                    else "Assinatura ativa na Stripe"
                ),
                True,
            )
    elif status == "canceled":
        _apply_cancellation(subscription_id, "Assinatura cancelada na Stripe")
    elif status in INACTIVE_STRIPE_STATUSES:
        _set_access(subscription_id, "Suspended", f"Assinatura Stripe: {status}")


def _apply_cancellation(subscription_id, reason):
    name = _find_enrollment(subscription_id)
    if not name:
        return
    minimum_term = frappe.db.get_value(
        "LMS Enrollment", name, "custom_minimum_term_ends_on"
    )
    status = cancellation_status(minimum_term, getdate(today()))
    _save_enrollment(
        name,
        {
            "custom_vedium_status": status,
            "custom_vedium_status_changed_on": now_datetime(),
            "custom_vedium_status_reason": (
                "Cancelamento antecipado pendente de análise"
                if status == "Cancellation Requested"
                else reason
            ),
            "custom_cancellation_requested_on": now_datetime(),
        },
    )


def _charge_refunded(charge):
    status = refund_access_status(charge.get("amount_refunded"), charge.get("amount"))
    reason = (
        "Pagamento integralmente reembolsado"
        if status == "Suspended"
        else "Reembolso parcial pendente de análise"
    )
    _charge_event(charge, status, reason)


def _dispute_created(dispute):
    charge_id = dispute.get("charge")
    if not charge_id:
        return
    import stripe

    charge = stripe.Charge.retrieve(charge_id)
    _charge_event(charge, "Suspended", "Pagamento em contestação")


def _charge_event(charge, status, reason):
    if not charge.get("invoice"):
        return
    import stripe

    invoice = stripe.Invoice.retrieve(charge.get("invoice"))
    enrollment = _invoice_enrollment(invoice)
    if enrollment:
        _save_enrollment(
            enrollment.name,
            {
                "custom_vedium_status": status,
                "custom_vedium_status_changed_on": now_datetime(),
                "custom_vedium_status_reason": reason,
            },
        )


def _set_access(
    subscription_id,
    status,
    reason,
    clear_failure=False,
    cancellation_requested=False,
):
    name = _find_enrollment(subscription_id)
    if not name:
        return
    values = {
        "custom_vedium_status": status,
        "custom_vedium_status_changed_on": now_datetime(),
        "custom_vedium_status_reason": reason,
    }
    if clear_failure:
        values["custom_payment_failed_on"] = None
    if cancellation_requested:
        values["custom_cancellation_requested_on"] = now_datetime()
    _save_enrollment(name, values)


def _save_enrollment(name, values):
    """Use Document.save so access/Raven hooks run on every status transition."""
    enrollment = frappe.get_doc("LMS Enrollment", name)
    valid = {
        key: value
        for key, value in values.items()
        if frappe.get_meta("LMS Enrollment").has_field(key)
    }
    enrollment.update(valid)
    enrollment.save(ignore_permissions=True)
    return enrollment


def suspend_overdue_enrollments():
    cutoff = now_datetime() - timedelta(days=GRACE_DAYS)
    active_labels = [status.title() for status in ACTIVE_ENROLLMENT_STATUSES]
    names = frappe.get_all(
        "LMS Enrollment",
        filters={
            "custom_payment_failed_on": ["<=", cutoff],
            "custom_vedium_status": ["in", active_labels],
        },
        pluck="name",
    )
    for name in names:
        _save_enrollment(
            name,
            {
                "custom_vedium_status": "Suspended",
                "custom_vedium_status_changed_on": now_datetime(),
                "custom_vedium_status_reason": (
                    f"Pagamento não regularizado após {GRACE_DAYS} dias"
                ),
            },
        )
    return len(names)


@frappe.whitelist()
def request_subscription_cancellation(enrollment_name):
    """Record an early request; schedule Stripe only after the minimum term."""
    enrollment = frappe.get_doc("LMS Enrollment", enrollment_name)
    user = frappe.session.user
    if user != enrollment.member and "System Manager" not in frappe.get_roles(user):
        frappe.throw(_("Sem permissão para cancelar esta assinatura."), frappe.PermissionError)
    if not enrollment.custom_stripe_subscription_id:
        frappe.throw(_("Esta matrícula não possui assinatura Stripe."))

    if not enrollment.custom_minimum_term_ends_on:
        frappe.throw(_("A permanência mínima da assinatura não está registrada."))
    minimum_term = getdate(enrollment.custom_minimum_term_ends_on)
    now = now_datetime()
    if getdate(today()) < minimum_term:
        _save_enrollment(
            enrollment.name,
            {
                "custom_vedium_status": "Cancellation Requested",
                "custom_vedium_status_changed_on": now,
                "custom_vedium_status_reason": "Cancelamento antecipado pendente de análise",
                "custom_cancellation_requested_on": now,
            },
        )
        return {"status": "pending_review", "minimum_term_ends_on": minimum_term}

    import stripe

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        frappe.throw(_("STRIPE_SECRET_KEY não configurada."))
    stripe.Subscription.modify(
        enrollment.custom_stripe_subscription_id,
        cancel_at_period_end=True,
    )
    _save_enrollment(
        enrollment.name,
        {
            "custom_vedium_status": "Cancellation Requested",
            "custom_vedium_status_changed_on": now,
            "custom_vedium_status_reason": "Cancelamento agendado ao fim do período",
            "custom_cancellation_requested_on": now,
        },
    )
    return {"status": "scheduled"}
