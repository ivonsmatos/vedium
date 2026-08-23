"""Disable Frappe's daily Event digest and enforce 24-hour time display.

This migration is intentionally idempotent. It disables reminders on existing
Events, opts every enabled System User out of Event Reminder emails, changes
the default for new Events, and configures the site for Sao Paulo / HH:mm.

Run:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.configure_calendar_notifications.run
"""

from __future__ import annotations

import json

import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


TIME_ZONE = "America/Sao_Paulo"
TIME_FORMAT = "HH:mm"


def _disable_user_event_reminders() -> tuple[int, int]:
    created = 0
    updated = 0
    users = frappe.get_all(
        "User",
        filters={"enabled": 1, "user_type": "System User"},
        pluck="name",
    )

    for user in users:
        if not frappe.db.exists("Notification Settings", user):
            settings = frappe.new_doc("Notification Settings")
            settings.name = user
            settings.user = user
            settings.enable_email_event_reminders = 0
            settings.insert(ignore_permissions=True)
            created += 1
            continue

        if frappe.db.get_value(
            "Notification Settings", user, "enable_email_event_reminders"
        ):
            frappe.db.set_value(
                "Notification Settings",
                user,
                "enable_email_event_reminders",
                0,
                update_modified=False,
            )
            updated += 1

    return created, updated


def _disable_new_event_reminders_by_default() -> str:
    filters = {
        "doc_type": "Event",
        "field_name": "send_reminder",
        "property": "default",
    }
    setter = frappe.db.get_value("Property Setter", filters, "name")

    if setter:
        frappe.db.set_value(
            "Property Setter",
            setter,
            {"value": "0", "property_type": "Check"},
            update_modified=False,
        )
        return setter

    return make_property_setter(
        "Event",
        "send_reminder",
        "default",
        "0",
        "Check",
    ).name


def _remove_pending_event_digests() -> int:
    communications = frappe.get_all(
        "Communication",
        filters={"subject": "Upcoming Events for Today"},
        pluck="name",
        limit_page_length=1000,
    )
    if not communications:
        return 0

    digests = frappe.get_all(
        "Email Queue",
        filters={
            "status": ("in", ["Not Sent", "Partially Sent"]),
            "communication": ("in", communications),
        },
        pluck="name",
        limit_page_length=1000,
    )
    for name in digests:
        frappe.delete_doc("Email Queue", name, ignore_permissions=True, force=True)
    return len(digests)


def run() -> dict[str, object]:
    print("Auditing current calendar configuration...", flush=True)
    settings_before = frappe.db.get_value(
        "System Settings", "System Settings", ["time_zone", "time_format"], as_dict=True
    )

    events = frappe.get_all("Event", filters={"send_reminder": 1}, pluck="name")
    if events:
        event_table = frappe.qb.DocType("Event")
        (
            frappe.qb.update(event_table)
            .set(event_table.send_reminder, 0)
            .where(event_table.send_reminder == 1)
        ).run()
    print(f"Disabled reminders on {len(events)} Events.", flush=True)

    created, updated = _disable_user_event_reminders()
    print(
        f"Notification Settings: {created} created, {updated} updated.",
        flush=True,
    )
    property_setter = _disable_new_event_reminders_by_default()
    print(f"Event default updated through {property_setter}.", flush=True)
    pending_digests_removed = _remove_pending_event_digests()
    print(f"Removed {pending_digests_removed} pending Event digests.", flush=True)

    frappe.db.set_single_value("System Settings", "time_zone", TIME_ZONE)
    frappe.db.set_single_value("System Settings", "time_format", TIME_FORMAT)
    frappe.clear_cache()
    frappe.db.commit()
    print("Committed calendar configuration.", flush=True)

    result = {
        "events_disabled": len(events),
        "notification_settings_created": created,
        "notification_settings_updated": updated,
        "event_default_property_setter": property_setter,
        "pending_event_digests_removed": pending_digests_removed,
        "settings_before": settings_before,
        "settings_after": {"time_zone": TIME_ZONE, "time_format": TIME_FORMAT},
    }
    print(json.dumps(result, indent=2, default=str))
    return result
