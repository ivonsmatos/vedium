# -*- coding: utf-8 -*-
"""Integração Vedium ↔ Raven.

Este módulo é deliberadamente uma camada fina e segura:

- se o Raven não estiver instalado, tudo vira no-op;
- a fonte da verdade de acesso é o ``LMS Enrollment`` + ``custom_vedium_status``;
- canais são vinculados a ``LMS Course`` / ``LMS Batch`` via campos nativos do
  Raven (``linked_doctype`` / ``linked_document``);
- membros sincronizados recebem ``is_synced=1`` para auditoria/reconciliação.

Assim conseguimos instalar/customizar Raven sem acoplar regra pedagógica dentro
do app de terceiros.
"""

from __future__ import annotations

import re

import frappe

WORKSPACE_NAME = "Vedium"
STATUS_FIELD = "custom_vedium_status"
ACTIVE_STATUSES = {"Active", "Trial"}
INACTIVE_STATUSES = {"Cancelled", "Ended", "Expired", "Suspended"}


def raven_available() -> bool:
    return all(
        frappe.db.exists("DocType", doctype)
        for doctype in (
            "Raven User",
            "Raven Workspace",
            "Raven Workspace Member",
            "Raven Channel",
            "Raven Channel Member",
        )
    )


def is_active_enrollment(enrollment) -> bool:
    status = (getattr(enrollment, STATUS_FIELD, None) or "Active").strip()
    return status in ACTIVE_STATUSES


def sync_enrollment(doc, method=None):
    """Hook de LMS Enrollment.

    Mantém canais Raven coerentes com matrícula/status. Não lança exceção para
    nunca quebrar checkout, migração ou edição administrativa de matrícula.
    """
    if not raven_available():
        return

    try:
        _sync_enrollment(doc)
        frappe.db.commit()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.communication.sync_enrollment")


def remove_enrollment_membership(doc, method=None):
    if not raven_available():
        return
    try:
        raven_user = frappe.db.get_value("Raven User", {"user": doc.member}, "name")
        if not raven_user:
            return
        for channel in _channels_for_enrollment(doc):
            if channel:
                _remove_channel_member(channel, raven_user)
        frappe.db.commit()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.communication.remove_enrollment_membership"
        )


def _sync_enrollment(enrollment):
    if not getattr(enrollment, "member", None):
        return

    raven_user = ensure_raven_user(enrollment.member)
    if not raven_user:
        return

    workspace = ensure_workspace()
    ensure_workspace_member(workspace, raven_user)

    channels = _channels_for_enrollment(enrollment, create=True)

    if is_active_enrollment(enrollment):
        for channel in channels:
            ensure_channel_member(channel, raven_user, enrollment.doctype, enrollment.name)
    else:
        for channel in channels:
            _remove_channel_member(channel, raven_user)


def _channels_for_enrollment(enrollment, create=False):
    channels = []
    if getattr(enrollment, "course", None):
        channels.append(
            ensure_course_channel(enrollment.course) if create else _find_linked_channel("LMS Course", enrollment.course)
        )
    batch = getattr(enrollment, "enrollment_from_batch", None)
    if batch:
        channels.append(
            ensure_batch_channel(batch) if create else _find_linked_channel("LMS Batch", batch)
        )
    return [c for c in channels if c]


def ensure_raven_user(user: str) -> str | None:
    if not user or user in ("Guest", "Administrator"):
        return None
    if not frappe.db.exists("User", user):
        return None

    existing = frappe.db.get_value("Raven User", {"user": user}, "name")
    user_doc = frappe.get_doc("User", user)

    if not _user_has_role(user_doc, "Raven User"):
        user_doc.append("roles", {"role": "Raven User"})
        user_doc.save(ignore_permissions=True)

    if existing:
        frappe.db.set_value(
            "Raven User",
            existing,
            {
                "enabled": 1 if user_doc.enabled else 0,
                "full_name": user_doc.full_name or user_doc.first_name or user,
                "first_name": user_doc.first_name,
            },
        )
        return existing

    raven_user = frappe.get_doc(
        {
            "doctype": "Raven User",
            "user": user,
            "type": "User",
            "enabled": 1 if user_doc.enabled else 0,
            "full_name": user_doc.full_name or user_doc.first_name or user,
            "first_name": user_doc.first_name,
        }
    )
    raven_user.insert(ignore_permissions=True)
    return raven_user.name


def ensure_workspace() -> str:
    if frappe.db.exists("Raven Workspace", WORKSPACE_NAME):
        return WORKSPACE_NAME

    workspace = frappe.get_doc(
        {
            "doctype": "Raven Workspace",
            "workspace_name": WORKSPACE_NAME,
            "type": "Private",
            "can_only_join_via_invite": 1,
            "only_admins_can_create_channels": 1,
            "description": "Comunicação oficial da Vedium, sincronizada com LMS.",
        }
    )
    workspace.insert(ignore_permissions=True)
    return workspace.name


def ensure_workspace_member(workspace: str, raven_user: str, is_admin: bool = False) -> str:
    existing = frappe.db.exists(
        "Raven Workspace Member", {"workspace": workspace, "user": raven_user}
    )
    if existing:
        return existing
    member = frappe.get_doc(
        {
            "doctype": "Raven Workspace Member",
            "workspace": workspace,
            "user": raven_user,
            "is_admin": 1 if is_admin else 0,
        }
    )
    member.insert(ignore_permissions=True)
    return member.name


def ensure_course_channel(course: str) -> str:
    title = frappe.db.get_value("LMS Course", course, "title") or course
    return _ensure_linked_channel(
        linked_doctype="LMS Course",
        linked_document=course,
        channel_name=f"curso-{_slug(title or course)}",
        description=f"Canal do curso {title}",
    )


def ensure_batch_channel(batch: str) -> str:
    title = frappe.db.get_value("LMS Batch", batch, "title") or batch
    return _ensure_linked_channel(
        linked_doctype="LMS Batch",
        linked_document=batch,
        channel_name=f"turma-{_slug(title or batch)}",
        description=f"Canal da turma {title}",
    )


def _ensure_linked_channel(linked_doctype, linked_document, channel_name, description=None) -> str:
    existing = _find_linked_channel(linked_doctype, linked_document)
    if existing:
        return existing

    channel = frappe.get_doc(
        {
            "doctype": "Raven Channel",
            "type": "Private",
            "channel_name": channel_name,
            "channel_description": description,
            "workspace": ensure_workspace(),
            "linked_doctype": linked_doctype,
            "linked_document": linked_document,
            "is_synced": 1,
        }
    )
    channel.flags.do_not_add_member = True
    channel.insert(ignore_permissions=True)
    return channel.name


def _find_linked_channel(linked_doctype, linked_document):
    return frappe.db.get_value(
        "Raven Channel",
        {
            "linked_doctype": linked_doctype,
            "linked_document": linked_document,
            "workspace": WORKSPACE_NAME,
            "is_archived": 0,
        },
        "name",
    )


def ensure_channel_member(channel: str, raven_user: str, linked_doctype=None, linked_document=None) -> str:
    existing = frappe.db.exists(
        "Raven Channel Member", {"channel_id": channel, "user_id": raven_user}
    )
    if existing:
        return existing

    member = frappe.get_doc(
        {
            "doctype": "Raven Channel Member",
            "channel_id": channel,
            "user_id": raven_user,
            "is_admin": 0,
            "last_visit": frappe.utils.now_datetime(),
            "allow_notifications": 1,
            "linked_doctype": linked_doctype,
            "linked_document": linked_document,
            "is_synced": 1,
        }
    )
    member.insert(ignore_permissions=True)
    return member.name


def _remove_channel_member(channel: str, raven_user: str):
    for row in frappe.get_all(
        "Raven Channel Member",
        filters={"channel_id": channel, "user_id": raven_user, "is_synced": 1},
        pluck="name",
    ):
        frappe.delete_doc("Raven Channel Member", row, ignore_permissions=True, force=True)


def reconcile_enrollment_channels(limit: int | None = None):
    """Job manual/scheduler para corrigir divergências LMS ↔ Raven."""
    if not raven_available():
        return {"raven_available": False, "synced": 0}

    enrollments = frappe.get_all(
        "LMS Enrollment",
        fields=["name"],
        limit_page_length=limit or 0,
        order_by="modified desc",
    )
    synced = 0
    for row in enrollments:
        doc = frappe.get_doc("LMS Enrollment", row.name)
        _sync_enrollment(doc)
        synced += 1
    frappe.db.commit()
    return {"raven_available": True, "synced": synced}


def _user_has_role(user_doc, role: str) -> bool:
    return role in {row.role for row in user_doc.get("roles", [])}


def _slug(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "canal"
