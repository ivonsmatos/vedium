"""Home real (`/`) -- Fase C.1.4: cutover controlado para o Design System V2.

Substitui a implementacao V1 anterior (grade de cursos vinda de `LMS
Course`, sem uso pela Home V2). Reusa a MESMA implementacao real ja
validada em `/_home_v2` desde a Fase C (mesmo template compartilhado
`templates/includes/v2/home_page_content.html`, mesma funcao de dados
`v2_home_data.build_home_v2_context()`) -- "template compartilhado +
context compartilhado, minimo de duplicacao" (secao 5 da missao C.1.4).

Contrato de SEO PRESERVADO do V1 (title/description/keywords/robots/
canonical/hreflang/OG/Twitter/JSON-LD/favicons) -- nenhum valor foi
inventado nesta fase, todos migrados literalmente de www/index.html antes
do cutover (backup em docs/redesign/47-home-v2-cutover-result.md).
`context.canonical_url` (nao `context.canonical`, reservado pelo core do
Frappe -- ver nota completa em www/_home_v2.py) segue o mesmo padrao
estabelecido em 144 arquivos do projeto.

`/_home_v2` continua existindo, noindex/nofollow/fora do sitemap, como
rota tecnica de fallback ate o fim do periodo de estabilizacao (ver
docs/redesign/35-home-v2-rollback-plan.md Cenario B).
"""

import frappe

from vedium_core.v2_home_data import build_home_v2_context


def get_context(context):
    _redirect_app_root_to_login()

    context.title = "Vedium - Cursos Online ao Vivo em Cinco Idiomas"
    context.canonical_url = frappe.utils.get_url("/")

    return build_home_v2_context(context)


def _redirect_app_root_to_login():
    """Keep app.vediums.com as product/login, while vediums.com remains marketing."""
    request = getattr(frappe.local, "request", None)
    host_candidates = [
        frappe.get_request_header("X-Forwarded-Host"),
        frappe.get_request_header("Host"),
        getattr(request, "host", ""),
        getattr(request, "host_url", ""),
    ]
    host = " ".join(str(item or "") for item in host_candidates).lower()
    path = getattr(frappe.local, "path", "") or getattr(request, "path", "") or "/"
    if "app.vediums.com" in host and path in ("", "/"):
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
