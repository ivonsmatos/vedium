"""Preview do VEDIUM DESIGN SYSTEM V2 -- ferramenta de desenvolvimento.

Isolado da producao por desenho: noindex, fora do sitemap.py, fora de
site_navbar.html/site_footer.html, e restrito a developer_mode ou a um
usuario com papel "System Manager" (ver PREVIEW_ROLE abaixo). Nao consome
nenhum dado real de curso/professor/preco -- so os tokens/macros do proprio
design system, mais a foto ja publicamente autorizada do Prof. Almir
(vedium_core/public/vedium_assets/images/instructors/) como unico exemplo
de "REAL VEDIUM" no card de professor.

Ver docs/redesign/10-design-system-v2-implementation.md.
"""

import frappe

PREVIEW_ROLE = "System Manager"


def get_context(context):
    context.no_cache = 1

    is_dev = bool(frappe.conf.get("developer_mode"))
    is_authorized_user = frappe.session.user != "Guest" and PREVIEW_ROLE in frappe.get_roles(
        frappe.session.user
    )
    if not (is_dev or is_authorized_user):
        frappe.throw(
            "Preview do Design System V2 disponível apenas em developer_mode ou para System Manager.",
            frappe.PermissionError,
        )

    context.title = "Vedium Design System V2 -- Preview (dev)"
    context.no_sitemap = 1
    return context
