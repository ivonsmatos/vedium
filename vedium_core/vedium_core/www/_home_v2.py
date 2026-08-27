"""Home V2 integrada -- rota paralela, NAO indexavel (Fase C da missao).

Nao substitui `/` (Home atual, intacta). Consome os MESMOS templates/macros
V2 aprovados (via templates/includes/v2/home_body.html, compartilhado com
www/design_system_v2.py) com DADOS REAIS (v2_home_data.py: artigos reais
do blog, matriz de encaminhamento do Pathfinder com URLs reais).

Nome do arquivo com underscore (nao hifen) por decisao deliberada desta
fase: Frappe converte hifen->underscore ao montar o nome do MODULO Python
a partir do nome do arquivo www/<slug>.py, e um controller cujo arquivo
tem hifen nunca roda (bug real, silencioso, ja documentado/corrigido em
~20 controllers deste app em fase anterior -- ver memoria do projeto:
"Controller www = underscore SEMPRE"). "_home-v2" (sugestao conceitual da
missao) teria exatamente esse problema; "_home_v2" (este arquivo) evita.

SEO desta rota tecnica (secao 22 da missao): noindex+nofollow via meta
tag, no_sitemap=1 (nao aparece em www/sitemap.py), canonical apontando pra
`/` (nunca compete por indexacao com a Home real -- se o noindex algum dia
for removido por engano, o canonical ainda protege). Nenhum hreflang
apontando pra esta rota. Guest-acessivel (sem gate de developer_mode/role
-- diferente do preview em design_system_v2.py, que e ferramenta interna
de QA; esta rota precisa ser revisavel por qualquer pessoa com o link,
sem exigir login no Frappe).
"""

import frappe

from vedium_core.v2_home_data import build_home_v2_context

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.no_sitemap = 1

    # Fase C (secao 22 da missao) / Fase C.1 (secao 2, investigacao P0):
    # noindex/nofollow + canonical seguro apontando pra "/" -- nunca compete
    # com a Home real por indexacao.
    #
    # ORIGEM REAL DO PROBLEMA (investigado a fundo na Fase C.1, nao so
    # contornado): o core do Frappe
    # (frappe/website/page_renderers/base_template_page.py, metodo
    # set_missing_values(), chamado por post_process_context() DEPOIS de
    # get_context() rodar) faz
    #     self.context.canonical = frappe.utils.get_url(frappe.utils.escape_html(self.path))
    # INCONDICIONALMENTE -- nao e um "set se nao existir" apesar do nome do
    # metodo, e nao ha nenhum jeito de um controller www/*.py fazer esse
    # valor "grudar" via context.canonical. Isso NAO e um bug so desta
    # pagina: e a razao pela qual TODO O RESTO do site real ja usa uma
    # chave PROPRIA (nao reservada) pra canonical custom -- confirmado
    # lendo curso.py/curso.html e templates/base.html
    # (`{% if canonical_url %}<link rel="canonical" href="{{ canonical_url }}">{% endif %}`),
    # usado em 144 arquivos do app. Aqui seguimos o MESMO padrao real
    # (context.canonical_url, nao mais um nome v2-especifico) -- essa e a
    # solucao correta, nao um workaround ad hoc: e o jeito estabelecido no
    # proprio projeto de expressar "este canonical e diferente da URL
    # literal da pagina". Teste de regressao: tests/test_pure_home_v2.py.
    context.robots = "noindex, nofollow"
    context.canonical_url = frappe.utils.get_url("/")

    context.title = "Vedium -- Home V2 (prévia interna, não indexada)"
    context.metatags = {
        "title": context.title,
        "robots": context.robots,
        "og:title": context.title,
    }

    # Fase C.1.4 (secao 5 da missao): dados (insights + HomeCourseCollection)
    # agora vem de uma funcao compartilhada com www/index.py -- so os campos
    # de SEO acima (robots/canonical_url/title) continuam especificos desta
    # rota tecnica.
    return build_home_v2_context(context)
