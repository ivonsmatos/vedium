# -*- coding: utf-8 -*-
"""
Vedium — Assinaturas Recorrentes Stripe (mode=subscription)

Responsabilidades deste módulo:
  1. Criar sessão de checkout em mode=subscription usando o price_id
     cadastrado no Frappe (LMS Course.custom_stripe_price_id_semestral /
     custom_stripe_price_id_anual).
  2. Processar os 7 eventos de webhook do ciclo de vida completo:
       checkout.session.completed  → matrícula + contrato
       invoice.paid                → reativa se estava suspenso
       invoice.payment_failed      → registra data da 1ª falha; suspende após 10d
       customer.subscription.updated → sincroniza status
       customer.subscription.deleted → cancela matrícula
       charge.refunded             → revoga acesso
       charge.dispute.created      → alerta admin (não revoga automaticamente)
  3. Scheduler diário: suspende matrículas em falha há > 10 dias.
  4. Funções utilitárias de permanência mínima.

Regras comerciais implementadas (documentadas aqui para referência):
  - Plano semestral: acesso por 6 meses de contrato.
  - Plano anual   : acesso por 12 meses de contrato.
  - Inadimplência : tolerância de 10 dias corridos desde a 1ª falha de
    cobrança antes de suspender o acesso.
  - Cancelamento antecipado: gera status=CancellationRequested; o acesso
    continua até o fim da permanência mínima. Nenhuma multa é cobrada
    automaticamente — decisão comercial exclusiva do administrador.
  - Reembolso aprovado: suspende o acesso imediatamente.
  - Contestação: alerta admin via log; sem revogação automática.

Compatibilidade:
  - Frappe Framework v16 / ERPNext v16 / Frappe LMS 2.x
  - Python 3.14 (produção) / 3.11 (CI)
  - stripe SDK ≥ 7.x

Segurança:
  - Chaves lidas de frappe.conf (nunca hardcoded).
  - Webhook secret obrigatório em produção.
  - Idempotência por custom_last_invoice_id (invoice.paid/failed).
  - Idempotência por custom_stripe_subscription_id (checkout.session.completed).
"""

from __future__ import annotations

from datetime import timedelta

import frappe
from frappe import _

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
GRACE_PERIOD_DAYS = 10          # Dias de inadimplência antes da suspensão
SEMESTRAL_MONTHS = 6
ANUAL_MONTHS = 12
STATUS_FIELD = "custom_vedium_status"

# Opções do campo Select (devem bater com custom_setup.py)
STATUS_ACTIVE = "Active"
STATUS_SUSPENDED = "Suspended"
STATUS_CANCELLED = "Cancelled"


# ---------------------------------------------------------------------------
# Utilitários internos
# ---------------------------------------------------------------------------

def _get_stripe():
    """Retorna o módulo stripe com api_key configurada."""
    import stripe  # lazy — não importa no nível de módulo

    key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not key:
        frappe.throw(_("STRIPE_SECRET_KEY não configurado no site_config.json"))
    stripe.api_key = key
    return stripe


def _now():
    return frappe.utils.now_datetime()


def _add_months(dt, months: int):
    """Adiciona N meses a um datetime de forma segura."""
    import calendar

    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def _set_enrollment_status(enrollment_name: str, status: str, reason: str = ""):
    """Atualiza custom_vedium_status + timestamp em uma única chamada SQL."""
    frappe.db.set_value(
        "LMS Enrollment",
        enrollment_name,
        {
            STATUS_FIELD: status,
            "custom_vedium_status_changed_on": _now(),
            "custom_vedium_status_reason": reason[:500] if reason else "",
        },
        update_modified=False,
    )


def _find_enrollment_by_subscription(subscription_id: str):
    """Localiza LMS Enrollment pelo Stripe Subscription ID."""
    if not subscription_id:
        return None
    return frappe.db.get_value(
        "LMS Enrollment",
        {"custom_stripe_subscription_id": subscription_id},
        "name",
    )


def _find_enrollment_by_payment_intent(payment_intent_id: str):
    """Localiza LMS Enrollment pelo payment_reference (usado em pagamentos únicos/invoices)."""
    if not payment_intent_id:
        return None
    return frappe.db.get_value(
        "LMS Enrollment",
        {"payment_reference": payment_intent_id},
        "name",
    )


def _log(msg: str, title: str = "Vedium.stripe_subscriptions"):
    frappe.log_error(msg, title)


# ---------------------------------------------------------------------------
# Checkout — mode=subscription com price_id do Frappe
# ---------------------------------------------------------------------------

def create_subscription_checkout(
    course_name: str,
    user: str,
    billing_period: str,
    display_currency: str | None = None,
    coupon_code: str | None = None,
) -> str:
    """
    Cria sessão Stripe Checkout em mode=subscription usando o price_id
    cadastrado no campo custom_stripe_price_id_semestral ou custom_stripe_price_id_anual
    do LMS Course.

    Retorna a URL da sessão de checkout.

    Raises frappe.ValidationError se o course não tiver o price_id configurado.
    """
    stripe = _get_stripe()

    billing_period = (billing_period or "semestral").strip().lower()
    if billing_period not in ("semestral", "anual"):
        billing_period = "semestral"

    course = frappe.get_doc("LMS Course", course_name)

    price_field = (
        "custom_stripe_price_id_anual"
        if billing_period == "anual"
        else "custom_stripe_price_id_semestral"
    )
    price_id = getattr(course, price_field, None) or frappe.db.get_value(
        "LMS Course", course_name, price_field
    )

    if not price_id or not str(price_id).startswith("price_"):
        frappe.throw(
            _(
                "O curso {0} não possui o Stripe Price ID configurado para o plano {1}. "
                "Acesse o Desk → LMS Course → {0} e preencha o campo '{2}'."
            ).format(course_name, billing_period, price_field),
            frappe.ValidationError,
        )

    user_email = frappe.db.get_value("User", user, "email") or user
    base_url = frappe.utils.get_url()

    # Boleto NÃO é suportado em mode=subscription pelo Stripe.
    # Apenas cartão de crédito (válido para BRL e USD).
    payment_method_types = ["card"]

    session_params = {
        "payment_method_types": payment_method_types,
        "line_items": [{"price": price_id, "quantity": 1}],
        "mode": "subscription",
        "customer_email": user_email,
        "client_reference_id": f"{course_name}|{user}",
        "success_url": (
            f"{base_url}/lms/courses/{course_name}"
            "?payment=success&session_id={CHECKOUT_SESSION_ID}"
        ),
        "cancel_url": f"{base_url}/lms/courses/{course_name}?payment=cancelled",
        "metadata": {
            "course_name": str(course_name),
            "user": str(user),
            "site": str(frappe.local.site),
            "billing_period": billing_period,
            "coupon_code": coupon_code or "",
        },
    }

    # Cupom Stripe (discount nativo): se houver Stripe coupon ID, passa direto.
    # Para cupons Vedium (desconto percentual calculado internamente), a lógica
    # fica no create_checkout do api.py — aqui não aplicamos desconto duplo.
    try:
        session = stripe.checkout.Session.create(**session_params)
    except Exception as e:
        _log(f"Erro ao criar sessão Stripe: {e}", "Vedium.stripe_subscriptions.checkout")
        frappe.throw(_("Não foi possível criar o checkout do Stripe. Tente novamente."))

    return session.url


# ---------------------------------------------------------------------------
# Handlers de Webhook
# ---------------------------------------------------------------------------

def handle_checkout_session_completed(event_obj: dict):
    """
    Evento: checkout.session.completed (mode=subscription)

    Ações:
      - Cria LMS Enrollment com status Active
      - Registra subscription_id, billing_period, contract_start/end
      - Idempotente: ignora se enrollment já existir para esta subscription
    """
    session = event_obj.get("data", {}).get("object", {})

    if session.get("mode") != "subscription":
        # Pagamentos únicos (mode=payment) são tratados pelo handler legado
        # em api.StripeGateway.handle_webhook — não processamos aqui.
        return

    if session.get("payment_status") not in ("paid", "no_payment_required"):
        _log(
            f"checkout.session.completed ignorado: payment_status={session.get('payment_status')}",
            "Vedium.stripe_subscriptions.checkout_completed",
        )
        return

    metadata = session.get("metadata") or {}
    site = metadata.get("site", "")
    if site and site != frappe.local.site:
        frappe.throw(
            _("Stripe session site inválido"), frappe.AuthenticationError
        )

    ref = session.get("client_reference_id", "")
    try:
        course_name, user = ref.split("|", 1)
    except ValueError:
        _log(
            f"checkout.session.completed: client_reference_id inválido: {ref}",
            "Vedium.stripe_subscriptions.checkout_completed",
        )
        return

    subscription_id = session.get("subscription") or ""
    billing_period = metadata.get("billing_period", "semestral")
    coupon_code = metadata.get("coupon_code") or None
    commitment_months = ANUAL_MONTHS if billing_period == "anual" else SEMESTRAL_MONTHS

    # Idempotência: enrollment já existe para esta subscription?
    if subscription_id and _find_enrollment_by_subscription(subscription_id):
        return

    # Enrollment já existe pelo curso+aluno (ex.: re-checkout)?
    existing = frappe.db.get_value(
        "LMS Enrollment",
        {"course": course_name, "member": user},
        "name",
    )
    if existing:
        # Apenas atualiza a subscription_id se ainda não tiver
        if not frappe.db.get_value(
            "LMS Enrollment", existing, "custom_stripe_subscription_id"
        ):
            now = _now()
            frappe.db.set_value(
                "LMS Enrollment",
                existing,
                {
                    "custom_stripe_subscription_id": subscription_id,
                    "custom_billing_period": billing_period,
                    "custom_contract_start": now,
                    "custom_contract_end": _add_months(now, commitment_months),
                },
                update_modified=False,
            )
        return

    now = _now()
    contract_end = _add_months(now, commitment_months)

    try:
        enrollment = frappe.get_doc(
            {
                "doctype": "LMS Enrollment",
                "course": course_name,
                "member": user,
                "status": "Enrolled",
                "payment_gateway": "stripe",
                "payment_reference": session.get("payment_intent") or subscription_id,
                "purchased_certificate": 1,
                STATUS_FIELD: STATUS_ACTIVE,
                "custom_vedium_status_changed_on": now,
                "custom_stripe_subscription_id": subscription_id,
                "custom_billing_period": billing_period,
                "custom_contract_start": now,
                "custom_contract_end": contract_end,
            }
        )
        enrollment.insert(ignore_permissions=True)
    except Exception as e:
        _log(
            f"Erro ao criar enrollment: {e}",
            "Vedium.stripe_subscriptions.checkout_completed",
        )
        raise

    # Cupom Vedium
    if coupon_code and frappe.db.exists("Coupon", coupon_code):
        frappe.db.sql(
            "UPDATE `tabCoupon` SET used_count = COALESCE(used_count,0)+1 WHERE name=%s",
            (coupon_code,),
        )
    elif coupon_code and frappe.db.exists("Referral", coupon_code):
        try:
            from vedium_core.referrals import record_referral_conversion
            record_referral_conversion(coupon_code, user, course_name, enrollment.name)
        except Exception:
            _log(frappe.get_traceback(), "Vedium.stripe_subscriptions.referral")

    # E-mail de boas-vindas (nunca bloqueia a matrícula)
    _send_welcome_email(user, course_name, billing_period, contract_end)

    # Sync CRM
    try:
        frappe.enqueue(
            "vedium_core.integrations.sync_student_to_crm",
            user=user,
            enqueue_after_commit=True,
        )
    except Exception:
        pass


def handle_invoice_paid(event_obj: dict):
    """
    Evento: invoice.paid

    Ações:
      - Se enrollment estava Suspended → reativa (status = Active)
      - Limpa custom_payment_failure_since
      - Idempotente por custom_last_invoice_id
    """
    invoice = event_obj.get("data", {}).get("object", {})
    subscription_id = invoice.get("subscription") or ""
    invoice_id = invoice.get("id") or ""

    enrollment_name = _find_enrollment_by_subscription(subscription_id)
    if not enrollment_name:
        return

    # Idempotência: já processamos este invoice?
    last_invoice = frappe.db.get_value(
        "LMS Enrollment", enrollment_name, "custom_last_invoice_id"
    )
    if last_invoice == invoice_id:
        return

    updates = {
        "custom_last_invoice_id": invoice_id,
        "custom_payment_failure_since": None,
    }

    current_status = frappe.db.get_value(
        "LMS Enrollment", enrollment_name, STATUS_FIELD
    )
    if current_status == STATUS_SUSPENDED:
        updates[STATUS_FIELD] = STATUS_ACTIVE
        updates["custom_vedium_status_changed_on"] = _now()
        updates["custom_vedium_status_reason"] = "Pagamento recuperado — acesso reativado"

    frappe.db.set_value(
        "LMS Enrollment", enrollment_name, updates, update_modified=False
    )


def handle_invoice_payment_failed(event_obj: dict):
    """
    Evento: invoice.payment_failed

    Ações:
      - Registra custom_payment_failure_since (apenas na 1ª falha)
      - Idempotente por custom_last_invoice_id
      - A suspensão efetiva ocorre no scheduler diário (após 10 dias)
    """
    invoice = event_obj.get("data", {}).get("object", {})
    subscription_id = invoice.get("subscription") or ""
    invoice_id = invoice.get("id") or ""

    enrollment_name = _find_enrollment_by_subscription(subscription_id)
    if not enrollment_name:
        return

    last_invoice = frappe.db.get_value(
        "LMS Enrollment", enrollment_name, "custom_last_invoice_id"
    )
    if last_invoice == invoice_id:
        return

    now = _now()
    failure_since = frappe.db.get_value(
        "LMS Enrollment", enrollment_name, "custom_payment_failure_since"
    )

    updates = {"custom_last_invoice_id": invoice_id}
    if not failure_since:
        # Primeira falha: registra o início do período de inadimplência
        updates["custom_payment_failure_since"] = now

    frappe.db.set_value(
        "LMS Enrollment", enrollment_name, updates, update_modified=False
    )


def handle_subscription_updated(event_obj: dict):
    """
    Evento: customer.subscription.updated

    Ações:
      - Sincroniza o status: se o Stripe retornar status="active" e o
        enrollment estiver Suspended, reativa.
      - Se status="past_due" e grace period já passou, suspende.
      - Não toca em matrículas já Cancelled.
    """
    subscription = event_obj.get("data", {}).get("object", {})
    subscription_id = subscription.get("id") or ""
    stripe_status = (subscription.get("status") or "").lower()

    enrollment_name = _find_enrollment_by_subscription(subscription_id)
    if not enrollment_name:
        return

    current_status = frappe.db.get_value(
        "LMS Enrollment", enrollment_name, STATUS_FIELD
    )
    if current_status == STATUS_CANCELLED:
        return

    if stripe_status == "active":
        if current_status == STATUS_SUSPENDED:
            _set_enrollment_status(
                enrollment_name,
                STATUS_ACTIVE,
                "Assinatura Stripe reativada",
            )
            frappe.db.set_value(
                "LMS Enrollment",
                enrollment_name,
                "custom_payment_failure_since",
                None,
                update_modified=False,
            )
    elif stripe_status in ("past_due", "unpaid"):
        # Verifica se o grace period já expirou
        failure_since = frappe.db.get_value(
            "LMS Enrollment", enrollment_name, "custom_payment_failure_since"
        )
        if failure_since:
            from datetime import datetime
            if isinstance(failure_since, str):
                failure_since = frappe.utils.get_datetime(failure_since)
            if (_now() - failure_since).days >= GRACE_PERIOD_DAYS:
                _set_enrollment_status(
                    enrollment_name,
                    STATUS_SUSPENDED,
                    f"Assinatura {stripe_status} — inadimplência > {GRACE_PERIOD_DAYS} dias",
                )


def handle_subscription_deleted(event_obj: dict):
    """
    Evento: customer.subscription.deleted

    Ações:
      - Marca a matrícula como Cancelled.
      - Se ainda estiver dentro da permanência mínima: registra
        custom_cancellation_requested_on e mantém Active até o fim do contrato.
      - Se fora da permanência: cancela imediatamente.
    """
    subscription = event_obj.get("data", {}).get("object", {})
    subscription_id = subscription.get("id") or ""

    enrollment_name = _find_enrollment_by_subscription(subscription_id)
    if not enrollment_name:
        return

    now = _now()
    contract_end = frappe.db.get_value(
        "LMS Enrollment", enrollment_name, "custom_contract_end"
    )

    within_commitment = False
    if contract_end:
        if isinstance(contract_end, str):
            contract_end = frappe.utils.get_datetime(contract_end)
        within_commitment = contract_end > now

    if within_commitment:
        # Cancelamento solicitado antes do prazo: acesso até fim do contrato
        frappe.db.set_value(
            "LMS Enrollment",
            enrollment_name,
            {
                STATUS_FIELD: STATUS_ACTIVE,          # continua ativo
                "custom_vedium_status_reason": (
                    "Cancelamento solicitado — acesso garantido até fim da permanência mínima"
                ),
                "custom_cancellation_requested_on": now,
                "custom_vedium_status_changed_on": now,
            },
            update_modified=False,
        )
    else:
        # Fora da permanência: cancela imediatamente
        _set_enrollment_status(
            enrollment_name,
            STATUS_CANCELLED,
            "Assinatura cancelada pelo Stripe",
        )


def handle_charge_refunded(event_obj: dict):
    """
    Evento: charge.refunded

    Ações:
      - Suspende o acesso imediatamente (não cancela, pois pode ser reembolso
        parcial — decisão final cabe ao admin).
      - Registra o motivo como "Reembolso aprovado".
    """
    charge = event_obj.get("data", {}).get("object", {})
    payment_intent = charge.get("payment_intent") or ""

    enrollment_name = _find_enrollment_by_payment_intent(payment_intent)
    if not enrollment_name:
        # Tenta via subscription (assinaturas recorrentes)
        subscription_id = (
            charge.get("invoice_details", {}).get("invoice", {}).get("subscription")
            or charge.get("metadata", {}).get("subscription_id")
            or ""
        )
        if subscription_id:
            enrollment_name = _find_enrollment_by_subscription(subscription_id)

    if not enrollment_name:
        _log(
            f"charge.refunded: enrollment não encontrado para payment_intent={payment_intent}",
            "Vedium.stripe_subscriptions.refund",
        )
        return

    _set_enrollment_status(
        enrollment_name,
        STATUS_SUSPENDED,
        "Reembolso aprovado — acesso suspenso (admin pode reativar se parcial)",
    )


def handle_charge_dispute_created(event_obj: dict):
    """
    Evento: charge.dispute.created

    Ações:
      - Loga o alerta no Frappe Error Log para o admin avaliar.
      - NÃO revoga o acesso automaticamente (pode ser fraude do usuário ou
        erro do banco — o admin decide).
    """
    dispute = event_obj.get("data", {}).get("object", {})
    charge_id = dispute.get("charge") or ""
    amount = (dispute.get("amount") or 0) / 100
    currency = (dispute.get("currency") or "").upper()
    reason = dispute.get("reason") or "unknown"

    # Não logamos dados pessoais do titular do cartão.
    _log(
        f"ALERTA: contestação (chargeback) recebida.\n"
        f"charge_id={charge_id} | amount={amount} {currency} | reason={reason}\n"
        f"Acesse o Stripe Dashboard → Disputes para responder dentro do prazo.",
        "Vedium.stripe_subscriptions.dispute",
    )


# ---------------------------------------------------------------------------
# Dispatcher principal (chamado pelo endpoint stripe_webhook em api.py)
# ---------------------------------------------------------------------------

SUBSCRIPTION_EVENT_HANDLERS = {
    "checkout.session.completed": handle_checkout_session_completed,
    "invoice.paid": handle_invoice_paid,
    "invoice.payment_failed": handle_invoice_payment_failed,
    "customer.subscription.updated": handle_subscription_updated,
    "customer.subscription.deleted": handle_subscription_deleted,
    "charge.refunded": handle_charge_refunded,
    "charge.dispute.created": handle_charge_dispute_created,
}


def dispatch_stripe_event(event):
    """
    Recebe um evento Stripe verificado e despacha para o handler correto.
    Eventos desconhecidos são ignorados silenciosamente (não geram erro).
    """
    event_type = event.get("type") if isinstance(event, dict) else getattr(event, "type", None)
    handler = SUBSCRIPTION_EVENT_HANDLERS.get(event_type)
    if handler:
        event_dict = dict(event) if not isinstance(event, dict) else event
        try:
            handler(event_dict)
        except frappe.AuthenticationError:
            raise
        except Exception as e:
            _log(
                f"Erro ao processar evento {event_type}: {e}\n{frappe.get_traceback()}",
                f"Vedium.stripe_subscriptions.{event_type}",
            )
            raise


# ---------------------------------------------------------------------------
# Scheduler — suspensão por inadimplência após 10 dias
# ---------------------------------------------------------------------------

def suspend_overdue_subscriptions():
    """
    Executado diariamente pelo scheduler do Frappe.
    Suspende matrículas com falha de pagamento há mais de GRACE_PERIOD_DAYS dias.
    Seguro: opera apenas em matrículas Active com custom_payment_failure_since preenchido.
    """
    if not frappe.db.exists("DocType", "LMS Enrollment"):
        return

    cutoff = _now() - timedelta(days=GRACE_PERIOD_DAYS)

    overdue = frappe.db.get_all(
        "LMS Enrollment",
        filters={
            STATUS_FIELD: STATUS_ACTIVE,
            "custom_payment_failure_since": ["<", cutoff],
            "custom_stripe_subscription_id": ["is", "set"],
        },
        fields=["name", "member", "course", "custom_payment_failure_since"],
        limit=500,   # processa em lotes para não travar o scheduler
    )

    for enrollment in overdue:
        try:
            _set_enrollment_status(
                enrollment.name,
                STATUS_SUSPENDED,
                f"Inadimplência > {GRACE_PERIOD_DAYS} dias — acesso suspenso automaticamente",
            )
            frappe.log_error(
                f"Matrícula {enrollment.name} suspensa por inadimplência "
                f"(falha desde {enrollment.custom_payment_failure_since})",
                "Vedium.stripe_subscriptions.scheduler",
            )
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                f"Vedium.stripe_subscriptions.scheduler.{enrollment.name}",
            )

    # Cancela matrículas com cancelamento_solicitado que já passaram do prazo
    _cancel_expired_commitments()

    frappe.db.commit()


def _cancel_expired_commitments():
    """
    Cancela matrículas onde:
      - O cancelamento foi solicitado (custom_cancellation_requested_on preenchido)
      - E a permanência mínima já expirou (custom_contract_end < agora)
    """
    now = _now()
    pending_cancel = frappe.db.get_all(
        "LMS Enrollment",
        filters={
            STATUS_FIELD: STATUS_ACTIVE,
            "custom_cancellation_requested_on": ["is", "set"],
            "custom_contract_end": ["<", now],
        },
        fields=["name"],
        limit=200,
    )
    for enrollment in pending_cancel:
        try:
            _set_enrollment_status(
                enrollment.name,
                STATUS_CANCELLED,
                "Permanência mínima concluída — cancelamento efetivado",
            )
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                f"Vedium.stripe_subscriptions.cancel_commitment.{enrollment.name}",
            )


# ---------------------------------------------------------------------------
# E-mail de boas-vindas
# ---------------------------------------------------------------------------

def _send_welcome_email(user: str, course_name: str, billing_period: str, contract_end):
    """Envia e-mail de boas-vindas após assinatura criada. Nunca bloqueia."""
    try:
        course_title = frappe.db.get_value("LMS Course", course_name, "title") or course_name
        user_email = frappe.db.get_value("User", user, "email") or user
        first_name = frappe.db.get_value("User", user, "first_name") or ""

        periodo_label = "anual (12 meses)" if billing_period == "anual" else "semestral (6 meses)"
        contract_end_str = (
            contract_end.strftime("%d/%m/%Y") if hasattr(contract_end, "strftime") else str(contract_end)
        )

        frappe.sendmail(
            recipients=[user_email],
            subject=f"Assinatura confirmada — {course_title} | Vedium",
            message=f"""
                <h3>Bem-vindo(a){', ' + frappe.utils.escape_html(first_name) if first_name else ''}!</h3>
                <p>Sua assinatura <strong>{frappe.utils.escape_html(periodo_label)}</strong>
                do curso <strong>{frappe.utils.escape_html(course_title)}</strong> está ativa.</p>
                <p>Permanência mínima garantida até: <strong>{contract_end_str}</strong></p>
                <p><a href="https://app.vediums.com/lms/courses/{course_name}">
                Acessar o curso agora</a></p>
                <p>Qualquer dúvida, responda este e-mail ou escreva para contato@vediums.com.</p>
                <p>— Equipe Vedium</p>
            """,
        )
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.stripe_subscriptions.welcome_email"
        )
