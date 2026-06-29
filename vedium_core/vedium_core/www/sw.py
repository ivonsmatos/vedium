from pathlib import Path

import frappe


no_cache = 1
base_template_path = "www/sw.html"


def get_context(context):
    sw_path = Path(__file__).resolve().parents[1] / "public" / "js" / "sw.js"
    content = sw_path.read_text(encoding="utf-8")

    frappe.response["type"] = "binary"
    frappe.response["filecontent"] = content.encode("utf-8")
    frappe.response["filename"] = "sw.js"
    frappe.response["content_type"] = "application/javascript; charset=utf-8"
    context.no_cache = 1
    return context
