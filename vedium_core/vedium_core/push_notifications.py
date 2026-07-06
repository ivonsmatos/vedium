# -*- coding: utf-8 -*-
"""
Vedium — Web Push Notifications Backend

Fluxo:
    1. Frontend (push-notifications.js) chama save_subscription() após
       o usuário dar permissão no browser.
    2. O backend armazena a subscription (endpoint + keys) em
       "Vedium Push Subscription" (DocType custom).
    3. Para enviar uma notificação, chamar send_push_notification() —
       pode ser invocado de qualquer job, hook ou endpoint.

Dependência: pywebpush
    Adicionar em requirements.txt:
        pywebpush>=2.0.0

Configuração (site_config.json ou System Settings custom):
    vedium_vapid_private_key  — chave privada VAPID (base64 URL-safe)
    vedium_vapid_public_key   — chave pública VAPID (base64 URL-safe)
    vedium_vapid_email        — mailto: do responsável

Gerar chaves VAPID (rodar 1x no servidor):
    from py_vapid import Vapid
    v = Vapid()
    v.generate_keys()
    print("Private:", v.private_key_urlsafe)
    print("Public:", v.public_key_urlsafe)
"""

import json
import logging

import frappe
from frappe import _

log = logging.getLogger("vedium.push")

_SUB_DOCTYPE = "Vedium Push Subscription"

_SUB_FIELDS = [
    ("user", "Usuário", "Link", {"options": "User", "reqd": 1, "in_list_view": 1}),
    ("endpoint", "Endpoint", "Long Text", {"reqd": 1}),
    ("subscription_json", "Subscription (JSON)", "Long Text", {"reqd": 1}),
    ("active", "Ativa", "Check", {"default": "1", "in_list_view": 1}),
]


def ensure_push_subscription_doctype():
    """Cria o doctype custom 'Vedium Push Subscription' (idempotente)."""
    if frappe.db.exists("DocType", _SUB_DOCTYPE):
        return _SUB_DOCTYPE

    dt = frappe.new_doc("DocType")
    dt.name = _SUB_DOCTYPE
    dt.module = "Vedium Core"
    dt.custom = 1
    dt.autoname = "hash"
    dt.track_changes = 0
    dt.sort_field = "modified"
    dt.sort_order = "DESC"
    for fn, label, ft, extra in _SUB_FIELDS:
        row = {"fieldname": fn, "label": label, "fieldtype": ft}
        row.update(extra)
        dt.append("fields", row)
    for role in ["System Manager"]:
        dt.append("permissions", {
            "role": role, "read": 1, "write": 1, "create": 1, "delete": 1,
            "email": 1, "export": 1, "report": 1, "share": 1, "print": 1,
        })
    dt.insert(ignore_permissions=True)
    frappe.db.commit()
    return _SUB_DOCTYPE


def _safe_doctype_exists(dt):
    return bool(frappe.db.exists("DocType", dt))


# ─────────────────────────────────────────────
# API pública — chamada do browser
# ─────────────────────────────────────────────

@frappe.whitelist()
def get_vapid_public_key():
    """Retorna a VAPID public key para o frontend inicializar o PushManager."""
    key = frappe.db.get_single_value("System Settings", "custom_vedium_vapid_public_key") or ""
    return {"vapid_public_key": key}


@frappe.whitelist()
def save_subscription(subscription_json: str):
    """
    Salva ou atualiza a push subscription do usuário logado.
    Chamado pelo push-notifications.js após Notification.requestPermission().
    """
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para ativar notificações"), frappe.PermissionError)

    try:
        sub_data = json.loads(subscription_json)
    except json.JSONDecodeError:
        frappe.throw(_("Subscription inválida"), frappe.ValidationError)

    endpoint = sub_data.get("endpoint", "")
    if not endpoint:
        frappe.throw(_("Endpoint ausente na subscription"), frappe.ValidationError)

    ensure_push_subscription_doctype()

    # Upsert: um usuário pode ter múltiplos dispositivos
    existing = frappe.db.exists(_SUB_DOCTYPE, {"user": user, "endpoint": endpoint})
    if existing:
        frappe.db.set_value(_SUB_DOCTYPE, existing, {
            "subscription_json": subscription_json,
            "active": 1,
        })
    else:
        frappe.get_doc({
            "doctype": _SUB_DOCTYPE,
            "user": user,
            "endpoint": endpoint,
            "subscription_json": subscription_json,
            "active": 1,
        }).insert(ignore_permissions=True)

    frappe.db.commit()
    return {"status": "ok"}


@frappe.whitelist()
def remove_subscription(endpoint: str):
    """Remove a subscription de um endpoint específico (usuário desativou notificações)."""
    user = frappe.session.user
    if user == "Guest":
        return {"status": "skip"}

    if not _safe_doctype_exists(_SUB_DOCTYPE):
        return {"status": "pending_setup"}

    existing = frappe.db.exists(_SUB_DOCTYPE, {"user": user, "endpoint": endpoint})
    if existing:
        frappe.db.set_value(_SUB_DOCTYPE, existing, "active", 0)
        frappe.db.commit()

    return {"status": "ok"}


# ─────────────────────────────────────────────
# Envio de notificações (uso interno)
# ─────────────────────────────────────────────

def send_push_notification(
    user: str,
    title: str,
    body: str,
    url: str = "/",
    icon: str = "",
    image: str = "",
    tag: str = "vedium",
    actions: list | None = None,
):
    """
    Envia uma Web Push Notification para todos os dispositivos ativos do usuário.

    Exemplo de uso (num job ou hook):
        from vedium_core.push_notifications import send_push_notification
        send_push_notification(
            user="aluno@vediums.com",
            title="Sua aula começa em 10 minutos!",
            body="Inglês Executivo · Turma B2 — Sala virtual aguarda.",
            url="/lms/courses/ingles-executivo",
            tag="class-reminder",
        )
    """
    if not _safe_doctype_exists(_SUB_DOCTYPE):
        return

    subscriptions = frappe.get_all(
        _SUB_DOCTYPE,
        filters={"user": user, "active": 1},
        fields=["name", "subscription_json"],
    )
    if not subscriptions:
        return

    vapid_private = frappe.db.get_single_value(
        "System Settings", "custom_vedium_vapid_private_key"
    )
    vapid_email = frappe.db.get_single_value(
        "System Settings", "custom_vedium_vapid_email"
    ) or "mailto:contato@vediums.com"

    if not vapid_private:
        frappe.log_error("VAPID private key não configurada", "Vedium.Push.send")
        return

    payload = json.dumps({
        "title": title,
        "body": body,
        "url": url,
        "icon": icon or "/assets/vedium_core/vedium_assets/images/favicons/android-chrome-192x192.png?v=icon-v2",
        "image": image,
        "tag": tag,
        "actions": actions or [],
    })

    try:
        from pywebpush import WebPushException, webpush
    except ImportError:
        frappe.log_error(
            "pywebpush não instalado. Execute: pip install pywebpush",
            "Vedium.Push.send",
        )
        return

    for sub in subscriptions:
        try:
            sub_data = json.loads(sub.subscription_json)
            webpush(
                subscription_info=sub_data,
                data=payload,
                vapid_private_key=vapid_private,
                vapid_claims={"sub": vapid_email},
            )
        except Exception as exc:
            err_str = str(exc)
            # Subscription expirada ou inválida — desativar
            if "410" in err_str or "404" in err_str:
                frappe.db.set_value(_SUB_DOCTYPE, sub.name, "active", 0)
                frappe.db.commit()
            else:
                frappe.log_error(
                    f"Erro ao enviar push para {user} ({sub.name}): {exc}",
                    "Vedium.Push.send",
                )


def notify_class_reminder(user: str, course_title: str, course_url: str):
    """Helper: lembrete de aula 10 minutos antes."""
    send_push_notification(
        user=user,
        title="🎓 Sua aula começa em breve!",
        body=f"{course_title} · Sala virtual aguarda você.",
        url=course_url,
        tag="class-reminder",
    )


def notify_certificate_ready(user: str, course_title: str):
    """Helper: certificado disponível após conclusão."""
    send_push_notification(
        user=user,
        title="🏆 Certificado disponível!",
        body=f"Parabéns! Você concluiu {course_title}. Baixe seu certificado.",
        url="/certificado",
        tag="certificate-ready",
    )


def notify_trial_expiring(user: str, course_title: str, days_left: int):
    """Helper: aviso de trial expirando."""
    send_push_notification(
        user=user,
        title=f"⏰ {days_left} dia(s) restantes no trial",
        body=f"Seu período de avaliação de {course_title} está encerrando. Assine agora!",
        url="/planos",
        tag="trial-expiring",
    )
