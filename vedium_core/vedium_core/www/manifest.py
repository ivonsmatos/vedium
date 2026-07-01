from pathlib import Path

import frappe


no_cache = 1
base_template_path = "www/manifest.html"


def get_context(context):
    manifest_path = Path(__file__).resolve().parents[1] / "public" / "manifest.json"
    content = manifest_path.read_text(encoding="utf-8")

    frappe.response["type"] = "binary"
    frappe.response["filecontent"] = content.encode("utf-8")
    frappe.response["filename"] = "manifest.json"
    frappe.response["content_type"] = "application/manifest+json; charset=utf-8"
    context.no_cache = 1
    return context
