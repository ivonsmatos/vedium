"""Preview da pagina B2B V2 -- ferramenta de desenvolvimento.

Fase B.6E (Parte C da missao): preview ISOLADO, nao substitui a pagina
publica real /empresas. Mesmo gate de acesso e mesmo isolamento SEO de
design_system_v2.py (noindex, fora do sitemap, fora da navegacao real,
restrito a developer_mode ou System Manager).

Rota: /design_system_v2_b2b -- NAO /design_system_v2/b2b (a missao sugeriu
essa rota aninhada como "sugestao conceitual", com "ou outra rota segura
coerente com a stack Frappe" como alternativa explicita). Uma subpasta
www/design_system_v2/ colide com o arquivo plano www/design_system_v2.py
ja existente no resolvedor de modulos Python do Frappe -- os dois nao
podem coexistir com o mesmo nome em www/ (bug real encontrado ao tentar:
"ModuleNotFoundError: 'vedium_core.www.design_system_v2' is not a
package", porque o arquivo .py ja ocupa esse nome no namespace). Corrigir
exigiria uma website_route_rule em hooks.py (arquivo de producao
compartilhado, fora do escopo desta fase) ou renomear o arquivo existente
(quebraria a URL /design_system_v2 ja em uso). Rota plana com underscore
escolhida em vez disso -- mesmo padrao ja usado no resto do repo pra
controllers www/ (nunca hifen no nome do arquivo, ver memoria do
projeto).
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
            "Preview da pagina B2B V2 disponivel apenas em developer_mode ou para System Manager.",
            frappe.PermissionError,
        )

    context.title = "Vedium para Empresas -- Preview V2 (dev)"
    context.no_sitemap = 1
    return context
