"""Brevo contact and event synchronization for Vedium.

The integration is intentionally optional: when ``BREVO_API_KEY`` is absent
or ``BREVO_ENABLED`` is false, document hooks become no-ops. All outbound
requests run in background jobs so CRM/LMS writes are never blocked by Brevo.

Configuration lives in the Frappe site config, never in source control:

    bench --site app.vediums.com set-config BREVO_API_KEY "xkeysib-..."
    bench --site app.vediums.com set-config BREVO_ENABLED 1
    bench --site app.vediums.com set-config BREVO_CONTACT_LIST_IDS "[12]"

Use a regular Brevo API key here, not an MCP token.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

import frappe
import requests
from frappe.utils import cint, now_datetime


BREVO_API_BASE_URL = "https://api.brevo.com/v3"
DEFAULT_TIMEOUT_SECONDS = 20

# Attributes created by setup_brevo_schema(). They are deliberately text
# attributes so course/status identifiers can evolve without a destructive
# enumeration migration inside Brevo.
#
# Dois grupos:
# 1) Os nomes que os MODELOS do kit de e-mail leem diretamente no corpo
#    (COURSE/LEVEL/COMPANY) + os de segmentação sugeridos no README
#    (ENROLLMENT_STATUS/LIFECYCLE_STAGE/COMMUNICATION_LANGUAGE). Sem estes,
#    `{{ contact.COURSE }}` etc. renderizam vazio — ver
#    Cliente/Vedium/emailmkt/README.md ("enviar em COURSE, não COURSE_INTEREST").
# 2) Os VEDIUM_* legados/técnicos, mantidos para auditoria e segmentação fina
#    sem colidir com os nomes canônicos do kit.
CONTACT_ATTRIBUTES = {
    # Lidos pelos modelos do kit (nomes exatos, ver campos-brevo.txt)
    "COURSE": "text",
    "LEVEL": "text",
    "COMPANY": "text",
    "ENROLLMENT_STATUS": "text",
    "LIFECYCLE_STAGE": "text",
    "COMMUNICATION_LANGUAGE": "text",
    # Legados/técnicos Vedium
    "VEDIUM_USER_ID": "text",
    "VEDIUM_COURSE_ID": "text",
    "VEDIUM_COURSE": "text",
    "VEDIUM_STATUS": "text",
    "VEDIUM_TRIAL_END": "text",
    "VEDIUM_BILLING_PERIOD": "text",
    "VEDIUM_PAYMENT_CURRENCY": "text",
    "VEDIUM_CRM_STATUS": "text",
    "VEDIUM_SOURCE": "text",
}

# Área do aluno e portal de cobrança (links estáveis usados como params.* dos
# fluxos operacionais/transacionais do kit — A08 onboarding, A20 cobrança).
# O portal de cobrança é um redirect whitelisted que exige login e cria uma
# sessão fresca do Stripe Billing Portal no clique (ver
# stripe_billing.billing_portal_redirect) — por isso pode ir num evento que o
# Brevo guarda e envia depois, ao contrário de uma URL de sessão de curta vida.
STUDENT_PORTAL_URL = "https://app.vediums.com/lms/courses"
BILLING_PORTAL_URL = (
    "https://app.vediums.com/api/method/"
    "vedium_core.stripe_billing.billing_portal_redirect"
)

STATUS_EVENTS = {
    "Active": "enrollment_activated",
    "Trial": "trial_started",
    "Cancellation Requested": "cancellation_requested",
    "Pending Review": "enrollment_pending_review",
    "Suspended": "enrollment_suspended",
    "Cancelled": "enrollment_cancelled",
    "Ended": "enrollment_ended",
    "Expired": "trial_expired",
}


class BrevoAPIError(RuntimeError):
    """Raised when Brevo rejects or cannot process an API request."""


def _config(*names: str, default: Any = None) -> Any:
    for name in names:
        value = frappe.conf.get(name)
        if value not in (None, ""):
            return value
    return default


def is_enabled() -> bool:
    enabled = _config("BREVO_ENABLED", "brevo_enabled", default=1)
    api_key = _config("BREVO_API_KEY", "brevo_api_key")
    return bool(cint(enabled) and api_key)


def lifecycle_owned_by_brevo() -> bool:
    """Quando True, o Brevo é o dono dos e-mails de ciclo de vida do aluno
    (boas-vindas/onboarding A08, cobrança A20, marcos A10…) e o Frappe NÃO
    deve enviar os e-mails equivalentes por `frappe.sendmail` — evita e-mail em
    dobro.

    Enquanto o setup do Brevo não estiver 100% no ar, deixe
    ``BREVO_LIFECYCLE_LIVE`` desligado (padrão): o Frappe continua sendo o
    remetente interino de boas-vindas/dunning/nudge. Ao concluir o setup do
    Brevo (modelos importados, automações mapeando os eventos, domínio
    autenticado), ligue a chave num único comando e o Frappe se cala sozinho:

        bench --site app.vediums.com set-config BREVO_LIFECYCLE_LIVE 1

    Deliberadamente separado de ``is_enabled()``: a sincronização de contato/
    evento (a "fonte de verdade" que alimenta o Brevo) deve rodar MUITO antes
    de o Brevo assumir o envio — para que, no dia do corte, os contatos já
    estejam corretos e os fluxos tenham histórico de eventos.
    """
    live = _config("BREVO_LIFECYCLE_LIVE", "brevo_lifecycle_live", default=0)
    return bool(is_enabled() and cint(live))


def _api_key() -> str:
    key = (_config("BREVO_API_KEY", "brevo_api_key") or "").strip()
    if not key:
        raise BrevoAPIError("BREVO_API_KEY não configurada no site_config.")
    return key


def _timeout() -> int:
    return max(
        5,
        cint(
            _config(
                "BREVO_TIMEOUT_SECONDS",
                "brevo_timeout_seconds",
                default=DEFAULT_TIMEOUT_SECONDS,
            )
        ),
    )


def _list_ids() -> list[int]:
    raw = _config("BREVO_CONTACT_LIST_IDS", "brevo_contact_list_ids", default=[])
    if isinstance(raw, (list, tuple, set)):
        values = raw
    elif isinstance(raw, str):
        text = raw.strip()
        if not text:
            return []
        try:
            parsed = json.loads(text)
            values = parsed if isinstance(parsed, list) else [parsed]
        except json.JSONDecodeError:
            values = [part.strip() for part in text.split(",")]
    else:
        values = [raw]

    result: list[int] = []
    for value in values:
        try:
            list_id = int(value)
        except (TypeError, ValueError):
            continue
        if list_id > 0 and list_id not in result:
            result.append(list_id)
    return result


def _request(method: str, path: str, payload: dict | None = None) -> Any:
    url = f"{BREVO_API_BASE_URL}{path}"
    response = requests.request(
        method=method,
        url=url,
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": _api_key(),
        },
        json=payload,
        timeout=_timeout(),
    )
    if response.status_code >= 400:
        # Never log request headers or payloads: both may contain secrets/PII.
        detail = (response.text or "").strip().replace("\n", " ")[:300]
        raise BrevoAPIError(
            f"Brevo {method.upper()} {path} retornou HTTP {response.status_code}: {detail}"
        )
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def test_connection() -> dict:
    """Validate the API key and return a minimal, non-sensitive account summary."""
    account = _request("GET", "/account") or {}
    return {
        "connected": True,
        "company": account.get("companyName"),
        "email": account.get("email"),
        "enterprise": bool(account.get("enterprise")),
    }


def setup_brevo_schema() -> dict:
    """Create missing Vedium contact attributes in Brevo.

    Existing attributes are never changed or deleted. Run once after saving the
    API key, and again safely whenever the schema evolves.
    """
    existing = _request("GET", "/contacts/attributes") or {}
    names = {
        str(item.get("name") or "").upper()
        for item in existing.get("attributes", [])
        if item.get("name")
    }
    created: list[str] = []
    for name, attribute_type in CONTACT_ATTRIBUTES.items():
        if name in names:
            continue
        _request(
            "POST",
            f"/contacts/attributes/normal/{name}",
            {"type": attribute_type},
        )
        created.append(name)
    return {"created": created, "existing": sorted(names)}


def _clean_phone(value: Any) -> str | None:
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    if raw.startswith("00"):
        raw = "+" + raw[2:]
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return None
    if raw.startswith("+"):
        return "+" + digits

    default_country = str(
        _config("BREVO_DEFAULT_COUNTRY_CODE", "brevo_default_country_code", default="")
    ).strip()
    if default_country:
        country_digits = re.sub(r"\D", "", default_country)
        if country_digits:
            return "+" + country_digits + digits
    return None


def _as_iso(value: Any) -> str | None:
    if not value:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _user_data(email_or_user: str) -> dict:
    if not email_or_user:
        return {}
    user = frappe.db.get_value(
        "User",
        email_or_user,
        ["name", "email", "first_name", "last_name", "full_name", "mobile_no", "phone"],
        as_dict=True,
    )
    if not user and "@" in email_or_user:
        user = frappe.db.get_value(
            "User",
            {"email": email_or_user},
            ["name", "email", "first_name", "last_name", "full_name", "mobile_no", "phone"],
            as_dict=True,
        )
    return dict(user or {})


def _base_contact_payload(
    *,
    email: str,
    ext_id: str | None,
    first_name: str | None,
    last_name: str | None,
    phone: str | None,
    attributes: dict | None = None,
) -> dict:
    attrs: dict[str, Any] = {}
    if first_name:
        attrs["FIRSTNAME"] = first_name
    if last_name:
        attrs["LASTNAME"] = last_name
    clean_phone = _clean_phone(phone)
    if clean_phone:
        attrs["SMS"] = clean_phone
    for key, value in (attributes or {}).items():
        if value not in (None, ""):
            attrs[key] = value

    payload: dict[str, Any] = {
        "email": email,
        "attributes": attrs,
        "updateEnabled": True,
    }
    if ext_id:
        payload["ext_id"] = ext_id
    list_ids = _list_ids()
    if list_ids:
        payload["listIds"] = list_ids
    return payload


def upsert_contact(payload: dict) -> Any:
    return _request("POST", "/contacts", payload)


def track_event(
    event_name: str,
    email: str,
    *,
    contact_properties: dict | None = None,
    event_properties: dict | None = None,
    event_date: str | None = None,
) -> Any:
    payload: dict[str, Any] = {
        "event_name": event_name,
        "identifiers": {"email_id": email},
    }
    if event_date:
        payload["event_date"] = event_date
    if contact_properties:
        payload["contact_properties"] = contact_properties
    if event_properties:
        payload["event_properties"] = event_properties
    return _request("POST", "/events", payload)


def emit_contact_event(
    email: str,
    event_name: str,
    *,
    event_properties: dict | None = None,
    contact_properties: dict | None = None,
) -> dict:
    """Dispara um evento de contato pro Brevo, guardado e best-effort.

    No-op se a integração estiver desligada; nunca lança (falha só loga). Usado
    por emissores pontuais de evento fora do fluxo de matrícula (ex.: marcos de
    progresso A10 em gamification.py, ativação em student_onboarding.py) — NÃO
    faz dedup durável (o chamador é responsável pela idempotência via um marcador
    próprio, ex.: custom_last_progress_milestone)."""
    if not is_enabled() or not email or email in ("Guest", "Administrator"):
        return {"skipped": True}
    try:
        track_event(
            event_name,
            email,
            event_properties=event_properties or None,
            contact_properties=contact_properties or None,
        )
        return {"sent": event_name}
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Vedium.Brevo.event.{event_name}")
        return {"error": True}


# Catálogo canônico de eventos de ciclo de vida que o Frappe emite. Usado para
# "primar" a lista de gatilhos do Brevo: o Brevo SÓ mostra no dropdown de
# "evento personalizado" eventos que já foram recebidos ao menos uma vez. NÃO
# inclui `enrollment_created` (já aparece e já tem a automação A08 ativa —
# dispará-lo pro contato-semente entraria no onboarding).
LIFECYCLE_EVENTS = (
    "student_not_activated", "student_absent", "student_inactive",
    "progress_milestone", "monthly_evolution",
    "checkout_started", "payment_failed", "payment_recovered", "payment_due_soon",
    "trial_started", "trial_expired",
    "enrollment_activated", "enrollment_suspended", "enrollment_cancelled",
    "cancellation_requested", "enrollment_pending_review", "enrollment_ended",
    "lead_created", "lead_updated", "lead_stale",
    "lead_status_changed", "lead_converted",
)


@frappe.whitelist()
def seed_event_catalog(email: str = "brevo-seed@vediums.com") -> dict:
    """Dispara cada evento de LIFECYCLE_EVENTS UMA vez para um contato-semente,
    para que apareçam no dropdown de gatilhos do Brevo. Seguro: nenhum desses
    eventos tem automação ainda, e automações do Brevo disparam em eventos
    FUTUROS (não no seed). Rode uma vez; depois o contato-semente pode ser
    apagado do Brevo. Restrito à gestão."""
    if not set(frappe.get_roles()) & {"System Manager", "Administrator", "Vedium Ops"}:
        frappe.throw("Acesso restrito à equipe.", frappe.PermissionError)
    if not is_enabled():
        return {"skipped": "disabled"}
    upsert_contact({
        "email": email,
        "attributes": {"FIRSTNAME": "Seed", "COURSE": "Seed"},
        "updateEnabled": True,
    })
    # Superset de params, para o Brevo também aprender as chaves usadas nos modelos.
    params = {
        "course": "Seed", "course_level": "Seed", "milestone": 25,
        "progress_percent": 25, "amount": "R$ 0,00", "due_date": "01/01/2027",
        "days_idle": 7, "absences": 3, "checkout_url": STUDENT_PORTAL_URL,
        "billing_url": BILLING_PORTAL_URL, "payment_update_url": BILLING_PORTAL_URL,
        "student_portal_url": STUDENT_PORTAL_URL, "onboarding_url": STUDENT_PORTAL_URL,
        "progress_url": STUDENT_PORTAL_URL, "support_checkin_url": STUDENT_PORTAL_URL,
        "attendance_rate": "100%", "activities_summary": "seed", "seed": True,
    }
    fired = []
    for name in LIFECYCLE_EVENTS:
        try:
            track_event(name, email, event_properties=params,
                        contact_properties={"COURSE": "Seed"})
            fired.append(name)
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"Vedium.Brevo.seed.{name}")
    return {"fired": fired, "count": len(fired), "contact": email}


def _event_key(*parts: Any) -> str:
    raw = "|".join(str(part or "") for part in parts)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:40]
    return f"brevo-{digest}"


def _claim_event(key: str, description: str) -> bool:
    row = frappe.db.get_value(
        "Integration Request",
        key,
        ["status", "custom_vedium_attempts"],
        as_dict=True,
    )
    now = now_datetime()
    if row and row.status == "Completed":
        return False
    if row:
        frappe.db.set_value(
            "Integration Request",
            key,
            {
                "status": "Queued",
                "error": None,
                "custom_vedium_attempts": cint(row.custom_vedium_attempts) + 1,
                "custom_vedium_last_attempt_on": now,
            },
        )
    else:
        frappe.get_doc(
            {
                "doctype": "Integration Request",
                "name": key,
                "request_id": key,
                "integration_request_service": "Brevo API",
                "is_remote_request": 1,
                "request_description": description[:140],
                "status": "Queued",
                "custom_vedium_attempts": 1,
                "custom_vedium_last_attempt_on": now,
            }
        ).insert(ignore_permissions=True)
    frappe.db.commit()
    return True


def _mark_event(key: str, status: str, error: str | None = None) -> None:
    values: dict[str, Any] = {"status": status}
    if status == "Completed":
        values.update({"output": "processed", "error": None})
    elif error:
        values["error"] = error[:140]
    frappe.db.set_value("Integration Request", key, values)
    frappe.db.commit()


def _course_data(course_name: str | None) -> dict:
    if not course_name:
        return {}
    course = frappe.db.get_value(
        "LMS Course",
        course_name,
        ["name", "title", "category"],
        as_dict=True,
    )
    return dict(course or {"name": course_name, "title": course_name})


def _enrollment_snapshot(doc) -> dict:
    user = _user_data(getattr(doc, "member", None))
    course = _course_data(getattr(doc, "course", None))
    return {
        "doctype": "LMS Enrollment",
        "name": doc.name,
        "modified": _as_iso(getattr(doc, "modified", None) or now_datetime()),
        "member": getattr(doc, "member", None),
        "email": user.get("email") or getattr(doc, "member", None),
        "user_id": user.get("name") or getattr(doc, "member", None),
        "first_name": user.get("first_name") or "",
        "last_name": user.get("last_name") or "",
        "phone": user.get("mobile_no") or user.get("phone") or "",
        "course_id": course.get("name") or getattr(doc, "course", None),
        "course": course.get("title") or getattr(doc, "course", None),
        "course_category": course.get("category") or "",
        "status": getattr(doc, "custom_vedium_status", None) or "Active",
        "trial_end": _as_iso(getattr(doc, "custom_trial_end", None)),
        "billing_period": getattr(doc, "custom_billing_period", None),
        "payment_currency": getattr(doc, "custom_payment_currency", None),
        "contract_amount": getattr(doc, "custom_contract_monthly_amount", None),
        "contract_currency": (
            getattr(doc, "custom_contract_currency", None)
            or getattr(doc, "custom_payment_currency", None)
        ),
        "payment_failed_on": _as_iso(getattr(doc, "custom_payment_failed_on", None)),
        "status_reason": getattr(doc, "custom_vedium_status_reason", None),
    }


def _format_amount(amount: Any, currency: str | None) -> str | None:
    """Formata o valor pro corpo do e-mail (params.amount). Usa currency.py
    quando disponível; senão, um fallback simples. Nunca lança."""
    if amount in (None, ""):
        return None
    try:
        from vedium_core.currency import format_amount

        return format_amount(float(amount), (currency or "BRL").upper())
    except Exception:
        try:
            return f"{(currency or 'BRL').upper()} {float(amount):,.2f}"
        except Exception:
            return None


def _lifecycle_event_params(snapshot: dict) -> dict:
    """Monta os ``params.*`` que os fluxos operacionais/transacionais do kit
    Brevo leem no corpo (ver Cliente/Vedium/emailmkt/brevo/campos-brevo.txt).

    Só inclui o que o Frappe consegue prover com confiança; todo o resto tem
    ``|default`` no modelo. Os nomes das chaves batem EXATAMENTE com os tokens
    dos modelos, pra qualquer mapeamento de evento→params no Brevo funcionar.
    """
    course = snapshot.get("course") or "seu curso"
    params = {
        "student_portal_url": STUDENT_PORTAL_URL,
        "onboarding_url": STUDENT_PORTAL_URL,
        "progress_url": STUDENT_PORTAL_URL,
        "course_url": STUDENT_PORTAL_URL,
        "billing_url": BILLING_PORTAL_URL,
        "payment_update_url": BILLING_PORTAL_URL,
        "course": course,
        "course_level": course,
    }
    amount = _format_amount(snapshot.get("contract_amount"), snapshot.get("contract_currency"))
    if amount:
        params["amount"] = amount
    return params


def _previous_snapshot(doc) -> dict:
    before = doc.get_doc_before_save() if hasattr(doc, "get_doc_before_save") else None
    if not before:
        return {}
    return {
        "status": getattr(before, "custom_vedium_status", None) or "Active",
        "payment_failed_on": _as_iso(getattr(before, "custom_payment_failed_on", None)),
    }


def _transition_events(snapshot: dict, previous: dict, method: str | None) -> list[str]:
    status = snapshot.get("status") or "Active"
    if method == "after_insert":
        return ["trial_started" if status == "Trial" else "enrollment_created"]

    events: list[str] = []
    previous_status = previous.get("status")
    if previous_status and previous_status != status:
        event_name = STATUS_EVENTS.get(status)
        if event_name:
            events.append(event_name)

    previous_failure = previous.get("payment_failed_on")
    current_failure = snapshot.get("payment_failed_on")
    if not previous_failure and current_failure:
        events.append("payment_failed")
    elif previous_failure and not current_failure:
        events.append("payment_recovered")
    return events


def on_enrollment(doc, method: str | None = None) -> None:
    """LMS Enrollment hook: queue contact upsert and transition events."""
    if not is_enabled():
        return
    snapshot = _enrollment_snapshot(doc)
    if not snapshot.get("email") or snapshot.get("email") in {"Guest", "Administrator"}:
        return
    events = _transition_events(snapshot, _previous_snapshot(doc), method)
    frappe.enqueue(
        "vedium_core.brevo.process_enrollment_snapshot",
        queue="short",
        enqueue_after_commit=True,
        snapshot=snapshot,
        event_names=events,
    )


def process_enrollment_snapshot(snapshot: dict, event_names: list[str] | None = None) -> dict:
    if not is_enabled():
        return {"skipped": "disabled"}

    email = snapshot.get("email")
    if not email:
        return {"skipped": "missing_email"}

    attributes = {
        # Nomes que os modelos do kit leem no corpo
        "COURSE": snapshot.get("course"),
        "ENROLLMENT_STATUS": snapshot.get("status"),
        # Legados/técnicos (segmentação e auditoria)
        "VEDIUM_USER_ID": snapshot.get("user_id"),
        "VEDIUM_COURSE_ID": snapshot.get("course_id"),
        "VEDIUM_COURSE": snapshot.get("course"),
        "VEDIUM_STATUS": snapshot.get("status"),
        "VEDIUM_TRIAL_END": snapshot.get("trial_end"),
        "VEDIUM_BILLING_PERIOD": snapshot.get("billing_period"),
        "VEDIUM_PAYMENT_CURRENCY": snapshot.get("payment_currency"),
        "VEDIUM_SOURCE": "Frappe LMS",
    }
    contact_payload = _base_contact_payload(
        email=email,
        ext_id=snapshot.get("user_id"),
        first_name=snapshot.get("first_name"),
        last_name=snapshot.get("last_name"),
        phone=snapshot.get("phone"),
        attributes=attributes,
    )

    processed: list[str] = []
    for event_name in event_names or []:
        key = _event_key(
            snapshot.get("doctype"),
            snapshot.get("name"),
            snapshot.get("modified"),
            event_name,
        )
        if not _claim_event(key, event_name):
            continue
        try:
            upsert_contact(contact_payload)
            event_properties = {
                "enrollment_id": snapshot.get("name"),
                "course_id": snapshot.get("course_id"),
                "course_category": snapshot.get("course_category"),
                "status": snapshot.get("status"),
                "status_reason": snapshot.get("status_reason"),
                "billing_period": snapshot.get("billing_period"),
                "payment_currency": snapshot.get("payment_currency"),
                "trial_end": snapshot.get("trial_end"),
            }
            # params.* que os fluxos do kit renderizam no corpo (links da área
            # do aluno, portal de cobrança, valor, nome do curso). Vão por
            # último para que course/course_level tenham o rótulo humano.
            event_properties.update(_lifecycle_event_params(snapshot))
            track_event(
                event_name,
                email,
                event_date=snapshot.get("modified"),
                contact_properties=attributes,
                event_properties=event_properties,
            )
            _mark_event(key, "Completed")
            processed.append(event_name)
        except Exception as exc:
            frappe.db.rollback()
            _mark_event(key, "Failed", type(exc).__name__)
            frappe.log_error(
                f"Brevo enrollment sync failed: {type(exc).__name__}",
                "Vedium.Brevo.enrollment",
            )
            raise

    # Status-neutral saves still keep the contact current without creating
    # another automation event.
    if not event_names:
        upsert_contact(contact_payload)
    return {"processed": processed, "contact": email}


def _lead_snapshot(doc) -> dict:
    email = getattr(doc, "email", None) or getattr(doc, "email_id", None)
    return {
        "doctype": "CRM Lead",
        "name": doc.name,
        "modified": _as_iso(getattr(doc, "modified", None) or now_datetime()),
        "email": email,
        "first_name": getattr(doc, "first_name", None) or "",
        "last_name": getattr(doc, "last_name", None) or "",
        "phone": getattr(doc, "mobile_no", None) or getattr(doc, "phone", None) or "",
        "status": getattr(doc, "status", None) or "",
        "source": getattr(doc, "source", None) or "",
        "company": getattr(doc, "organization", None) or getattr(doc, "company_name", None) or "",
        "course": getattr(doc, "custom_curso_interesse", None) or "",
    }


def on_crm_lead(doc, method: str | None = None) -> None:
    """CRM Lead hook: mirror leads to Brevo and trigger lead events."""
    if not is_enabled():
        return
    snapshot = _lead_snapshot(doc)
    if not snapshot.get("email"):
        return
    event_name = "lead_created" if method == "after_insert" else "lead_updated"
    before = doc.get_doc_before_save() if hasattr(doc, "get_doc_before_save") else None
    if before and getattr(before, "status", None) != snapshot.get("status"):
        if str(snapshot.get("status") or "").lower() == "converted":
            event_name = "lead_converted"
        else:
            event_name = "lead_status_changed"
    frappe.enqueue(
        "vedium_core.brevo.process_lead_snapshot",
        queue="short",
        enqueue_after_commit=True,
        snapshot=snapshot,
        event_name=event_name,
    )


def process_lead_snapshot(snapshot: dict, event_name: str) -> dict:
    if not is_enabled():
        return {"skipped": "disabled"}
    email = snapshot.get("email")
    attributes = {
        "COMPANY": snapshot.get("company"),
        "COURSE": snapshot.get("course"),
        "VEDIUM_CRM_STATUS": snapshot.get("status"),
        "VEDIUM_SOURCE": snapshot.get("source") or "Frappe CRM",
    }
    contact_payload = _base_contact_payload(
        email=email,
        ext_id=f"crm:{snapshot.get('name')}",
        first_name=snapshot.get("first_name"),
        last_name=snapshot.get("last_name"),
        phone=snapshot.get("phone"),
        attributes=attributes,
    )
    key = _event_key(
        snapshot.get("doctype"),
        snapshot.get("name"),
        snapshot.get("modified"),
        event_name,
    )
    if not _claim_event(key, event_name):
        return {"duplicate": True}
    try:
        upsert_contact(contact_payload)
        track_event(
            event_name,
            email,
            event_date=snapshot.get("modified"),
            contact_properties=attributes,
            event_properties={
                "lead_id": snapshot.get("name"),
                "status": snapshot.get("status"),
                "source": snapshot.get("source"),
            },
        )
        _mark_event(key, "Completed")
        return {"processed": event_name, "contact": email}
    except Exception as exc:
        frappe.db.rollback()
        _mark_event(key, "Failed", type(exc).__name__)
        frappe.log_error(
            f"Brevo lead sync failed: {type(exc).__name__}",
            "Vedium.Brevo.lead",
        )
        raise


def enqueue_full_sync(limit: int = 5000) -> dict:
    """Queue a one-time backfill of existing CRM leads and LMS enrollments."""
    if not is_enabled():
        raise BrevoAPIError("Integração Brevo desativada ou sem API key.")

    enrollment_names = frappe.get_all(
        "LMS Enrollment", order_by="modified asc", limit_page_length=cint(limit), pluck="name"
    )
    for name in enrollment_names:
        doc = frappe.get_doc("LMS Enrollment", name)
        frappe.enqueue(
            "vedium_core.brevo.process_enrollment_snapshot",
            queue="long",
            snapshot=_enrollment_snapshot(doc),
            event_names=[],
        )

    lead_names: list[str] = []
    if frappe.db.exists("DocType", "CRM Lead"):
        lead_names = frappe.get_all(
            "CRM Lead", order_by="modified asc", limit_page_length=cint(limit), pluck="name"
        )
        for name in lead_names:
            doc = frappe.get_doc("CRM Lead", name)
            frappe.enqueue(
                "vedium_core.brevo.process_lead_snapshot",
                queue="long",
                snapshot=_lead_snapshot(doc),
                event_name="lead_imported",
            )
    return {"enrollments_queued": len(enrollment_names), "leads_queued": len(lead_names)}
