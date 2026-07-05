# -*- coding: utf-8 -*-
"""
Vedium — Módulo de Compliance LGPD/GDPR

Implementa os direitos dos titulares de dados conforme:
- Lei Geral de Proteção de Dados (LGPD) — Lei 13.709/2018
- General Data Protection Regulation (GDPR) — Regulation 2016/679

Endpoints expostos via api.py:
    vedium_core.lgpd.request_data_export(user)
    vedium_core.lgpd.request_data_deletion(user)
    vedium_core.lgpd.record_consent(user, purpose, scope)
    vedium_core.lgpd.get_consent_status(user)

DocTypes necessários (criar via Frappe UI ou migrate):
    - Vedium Consent Record   (criado aqui via frappe.get_doc)
    - Vedium Data Request     (criado aqui via frappe.get_doc)

Esses DocTypes são opcionais — o módulo usa _safe_get para não quebrar
se ainda não existirem no banco.
"""

from datetime import datetime

import frappe
from frappe import _

from vedium_core.vedium_core.exceptions import LGPDError

# DocTypes gerenciados por este módulo
_CONSENT_DOCTYPE = "Vedium Consent Record"
_REQUEST_DOCTYPE = "Vedium Data Request"


def _safe_doctype_exists(doctype: str) -> bool:
    return bool(frappe.db.exists("DocType", doctype))


# ─────────────────────────────────────────────
# 1. EXPORTAÇÃO DE DADOS (Art. 18 LGPD / Art. 20 GDPR)
# ─────────────────────────────────────────────

@frappe.whitelist()
def request_data_export():
    """
    Enfileira pedido de exportação dos dados pessoais do usuário logado.
    Retorna um ticket de requisição. Os dados são enviados por e-mail em até 72h.
    """
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para solicitar exportação de dados"), LGPDError)

    # Evita múltiplos pedidos pendentes
    if _safe_doctype_exists(_REQUEST_DOCTYPE):
        pending = frappe.db.exists(
            _REQUEST_DOCTYPE,
            {"user": user, "request_type": "Export", "status": "Pending"},
        )
        if pending:
            frappe.throw(
                _("Você já possui uma solicitação de exportação em andamento"),
                LGPDError,
            )

    ticket = _create_data_request(user, request_type="Export")

    # Enfileira job para coletar e enviar dados (não bloqueia a resposta)
    frappe.enqueue(
        "vedium_core.lgpd._process_data_export",
        user=user,
        ticket=ticket,
        queue="long",
        now=frappe.flags.in_test,
    )

    return {
        "ticket": ticket,
        "message": _("Seu pedido foi registrado. Você receberá os dados por e-mail em até 72 horas."),
    }


def _process_data_export(user: str, ticket: str):
    """
    Job assíncrono: coleta todos os dados do usuário e envia por e-mail.
    Rodado pelo worker 'long'.
    """
    try:
        data = _collect_user_data(user)
        import json

        data_json = json.dumps(data, ensure_ascii=False, indent=2, default=str)

        # Envia por e-mail
        frappe.sendmail(
            recipients=[user],
            subject=_("Seus dados pessoais — Vedium"),
            message=_(
                "<p>Olá!</p>"
                "<p>Conforme solicitado, segue abaixo a exportação dos seus dados pessoais na plataforma Vedium.</p>"
                "<pre>{0}</pre>"
                "<p>Se você não fez esta solicitação, entre em contato com nossa equipe.</p>"
            ).format(frappe.utils.escape_html(data_json[:50000])),  # limite seguro de e-mail
            now=True,
        )
        _update_request_status(ticket, "Completed")

    except Exception as e:
        frappe.log_error(f"Erro ao exportar dados de {user}: {e}", "Vedium.LGPD.export")
        _update_request_status(ticket, "Failed")


def _collect_user_data(user: str) -> dict:
    """Agrega todos os dados pessoais do usuário em um dicionário."""
    data = {}

    # Perfil
    user_doc = frappe.db.get_value(
        "User", user,
        ["full_name", "email", "mobile_no", "birth_date", "creation"],
        as_dict=True,
    )
    data["profile"] = user_doc or {}

    # Matrículas
    data["enrollments"] = frappe.get_all(
        "LMS Enrollment",
        filters={"member": user},
        fields=["course", "status", "creation", "payment_gateway", "amount"],
    )

    # Certificados
    data["certificates"] = frappe.get_all(
        "LMS Certificate",
        filters={"member": user},
        fields=["course", "issue_date", "verification_code"],
    )

    # Pagamentos (se existir DocType)
    if _safe_doctype_exists("Vedium Payment"):
        data["payments"] = frappe.get_all(
            "Vedium Payment",
            filters={"user": user},
            fields=["course", "amount", "currency", "gateway", "creation"],
        )

    # Consentimentos
    if _safe_doctype_exists(_CONSENT_DOCTYPE):
        data["consents"] = frappe.get_all(
            _CONSENT_DOCTYPE,
            filters={"user": user},
            fields=["purpose", "scope", "consented", "creation"],
        )

    return data


# ─────────────────────────────────────────────
# 2. EXCLUSÃO DE DADOS (Art. 18 LGPD / Art. 17 GDPR)
# ─────────────────────────────────────────────

@frappe.whitelist()
def request_data_deletion():
    """
    Enfileira pedido de exclusão (direito ao esquecimento) dos dados do usuário.
    Requer confirmação manual pela equipe Vedium (processo irreversível).
    """
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para solicitar exclusão de dados"), LGPDError)

    # Exclusão não pode ter pedido duplicado
    if _safe_doctype_exists(_REQUEST_DOCTYPE):
        existing = frappe.db.exists(
            _REQUEST_DOCTYPE,
            {"user": user, "request_type": "Deletion"},
        )
        if existing:
            frappe.throw(
                _("Você já possui uma solicitação de exclusão registrada"),
                LGPDError,
            )

    ticket = _create_data_request(user, request_type="Deletion")

    # Notifica o time de compliance (exclusão requer revisão manual)
    _notify_compliance_team(user, ticket, request_type="Deletion")

    return {
        "ticket": ticket,
        "message": _(
            "Seu pedido de exclusão foi registrado. "
            "Nossa equipe entrará em contato em até 15 dias úteis."
        ),
    }


# ─────────────────────────────────────────────
# 3. CONSENTIMENTO (Art. 7 e 8 LGPD / Art. 6 GDPR)
# ─────────────────────────────────────────────

@frappe.whitelist()
def record_consent(purpose: str, scope: str, consented: bool = True):
    """
    Registra ou revoga o consentimento do usuário para uma finalidade específica.

    Args:
        purpose: Finalidade (ex: "marketing", "analytics", "ai_training")
        scope:   Escopo (ex: "email_campaigns", "usage_data")
        consented: True = consentimento dado, False = revogado
    """
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para gerenciar seu consentimento"), LGPDError)

    VALID_PURPOSES = {"marketing", "analytics", "ai_training", "third_party_sharing", "newsletter"}
    if purpose not in VALID_PURPOSES:
        frappe.throw(_("Finalidade inválida: {0}").format(purpose), LGPDError)

    if not _safe_doctype_exists(_CONSENT_DOCTYPE):
        # DocType ainda não criado — logar e retornar graciosamente
        frappe.log_error(
            f"DocType {_CONSENT_DOCTYPE} não existe — consentimento não registrado",
            "Vedium.LGPD.consent",
        )
        return {"status": "pending_setup"}

    # Upsert: atualiza se já existe, cria se não existe
    existing = frappe.db.exists(
        _CONSENT_DOCTYPE, {"user": user, "purpose": purpose, "scope": scope}
    )
    if existing:
        frappe.db.set_value(
            _CONSENT_DOCTYPE, existing,
            {"consented": int(consented), "modified": datetime.now()},
        )
        frappe.db.commit()
    else:
        doc = frappe.get_doc({
            "doctype": _CONSENT_DOCTYPE,
            "user": user,
            "purpose": purpose,
            "scope": scope,
            "consented": int(consented),
        })
        doc.insert(ignore_permissions=True)

    action = "dado" if consented else "revogado"
    return {
        "status": "ok",
        "message": _("Consentimento {0} para {1}").format(action, purpose),
    }


@frappe.whitelist()
def get_consent_status():
    """Retorna todos os consentimentos do usuário logado."""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para ver seu consentimento"), LGPDError)

    if not _safe_doctype_exists(_CONSENT_DOCTYPE):
        return []

    return frappe.get_all(
        _CONSENT_DOCTYPE,
        filters={"user": user},
        fields=["purpose", "scope", "consented", "modified"],
        order_by="modified desc",
    )


# ─────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────

def _create_data_request(user: str, request_type: str) -> str:
    """Cria um registro de requisição LGPD. Retorna o nome do documento."""
    if not _safe_doctype_exists(_REQUEST_DOCTYPE):
        # DocType não existe ainda: retorna um UUID temporário e loga
        import uuid
        ticket = f"LGPD-{uuid.uuid4().hex[:8].upper()}"
        frappe.log_error(
            f"DocType {_REQUEST_DOCTYPE} não existe — ticket {ticket} não persistido",
            "Vedium.LGPD.create_request",
        )
        return ticket

    doc = frappe.get_doc({
        "doctype": _REQUEST_DOCTYPE,
        "user": user,
        "request_type": request_type,
        "status": "Pending",
        "requested_at": datetime.now(),
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def _update_request_status(ticket: str, status: str):
    """Atualiza o status de uma requisição LGPD."""
    if _safe_doctype_exists(_REQUEST_DOCTYPE) and frappe.db.exists(_REQUEST_DOCTYPE, ticket):
        frappe.db.set_value(_REQUEST_DOCTYPE, ticket, "status", status)
        frappe.db.commit()


def _notify_compliance_team(user: str, ticket: str, request_type: str):
    """Envia e-mail ao time de compliance sobre uma nova requisição."""
    try:
        compliance_email = frappe.db.get_single_value(
            "System Settings", "support_email"
        ) or frappe.db.get_single_value("Email Account", "email_id")

        if compliance_email:
            frappe.sendmail(
                recipients=[compliance_email],
                subject=f"[LGPD] Nova solicitação de {request_type} — {user}",
                message=(
                    f"<p>Um usuário solicitou <strong>{request_type}</strong> dos seus dados.</p>"
                    f"<p><strong>Usuário:</strong> {frappe.utils.escape_html(user)}</p>"
                    f"<p><strong>Ticket:</strong> {ticket}</p>"
                    f"<p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"
                    f"<p>Prazo legal: 15 dias úteis (LGPD Art. 18 §3).</p>"
                ),
                now=True,
            )
    except Exception as e:
        frappe.log_error(f"Erro ao notificar compliance: {e}", "Vedium.LGPD.notify")
