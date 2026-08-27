"""Preview do VEDIUM DESIGN SYSTEM V2 -- ferramenta de desenvolvimento.

Isolado da producao por desenho: noindex, fora do sitemap.py, fora de
site_navbar.html/site_footer.html, e restrito a developer_mode ou a um
usuario com papel "System Manager" (ver PREVIEW_ROLE abaixo). Nao consome
nenhum dado real de curso/professor/preco -- so os tokens/macros do proprio
design system, mais a foto ja publicamente autorizada do Prof. Almir
(vedium_core/public/vedium_assets/images/instructors/) como unico exemplo
de "REAL VEDIUM" no card de professor.

Fase B.3 (2026-08-24): dois modos de apresentacao na MESMA rota, definidos
so pela query string (nenhuma logica nova de locale/permissao):
  - /design_system_v2            -> Presentation mode (padrao). So a
    experiencia visual -- sem nomes tecnicos de componente, sem nota de
    implementacao, sem borda de debug.
  - /design_system_v2?debug=1    -> Debug mode. Mostra tambem a secao
    "Component Library" (biblioteca atomica completa, nomes tecnicos,
    notas de QA) abaixo da experiencia de Presentation mode.

Ver docs/redesign/10-design-system-v2-implementation.md e
docs/redesign/14-art-direction-v2.md.
"""

import frappe

from vedium_core.v2_home_data import get_insights_selection, to_insight_macro_dict
from vedium_core.home_course_collection import get_home_course_collection, get_course_index_entries

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
    context.debug_mode = frappe.form_dict.get("debug") in ("1", "true", "yes")

    # Fase C (secao 16 da missao): "Conhecimento Vedium" usa artigos REAIS
    # (mesma selecao dinamica que a Home V2 integrada, ver v2_home_data.py e
    # docs/redesign/26-home-v2-integration.md) -- nao mais 3 titulos
    # hardcoded no template.
    featured, secondary = get_insights_selection()
    context.insights_featured = to_insight_macro_dict(featured)
    context.insights_secondary = [to_insight_macro_dict(c) for c in secondary]

    # Fase C.1.1 (Parte B da missao): mesma HomeCourseCollection real usada
    # pela Home V2 integrada (ver www/_home_v2.py e
    # docs/redesign/38-home-course-collection-contract.md).
    context.home_courses = get_home_course_collection()
    context.course_index_entries = get_course_index_entries()
    return context
