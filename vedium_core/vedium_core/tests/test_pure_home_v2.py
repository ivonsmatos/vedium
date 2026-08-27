"""Testes puros para a Home V2 (Fase C / C.1 / C.1.4) -- rodam sem Frappe/bench.

Cobrem o bloqueador P0 investigado na Fase C.1 (canonical), as garantias
estruturais da rota tecnica /_home_v2 (mantida apos o cutover como
fallback), a matriz do Pathfinder sincronizada entre Python (fonte de
verdade) e JS (espelho client-side), e -- desde a Fase C.1.4 -- que `/`
de fato assumiu a implementacao V2 (cutover controlado e autorizado).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WWW = ROOT / "vedium_core" / "vedium_core" / "www"
TPL = ROOT / "vedium_core" / "vedium_core" / "templates" / "includes"
V2_HOME_DATA = ROOT / "vedium_core" / "vedium_core" / "v2_home_data.py"
V2_JS = ROOT / "vedium_core" / "vedium_core" / "public" / "js" / "v2" / "design-system-v2.js"
HOME_V2_PY = WWW / "_home_v2.py"
HOME_V2_HTML = WWW / "_home_v2.html"
INDEX_PY = WWW / "index.py"
INDEX_HTML = WWW / "index.html"


def test_home_v2_uses_canonical_url_not_reserved_canonical_key():
    """Achado real da Fase C.1: frappe/website/page_renderers/base_template_page.py
    sobrescreve context.canonical INCONDICIONALMENTE com a URL da propria
    pagina (self.path), depois que get_context() roda -- qualquer valor
    setado em context.canonical dentro do controller e descartado antes do
    template renderizar. O padrao REAL e ja estabelecido em todo o site
    (curso.py/curso.html, templates/base.html, 144 arquivos) e usar
    `context.canonical_url` (chave propria, nao reservada) + `{{ canonical_url }}`
    no template -- nunca `context.canonical`/`{{ canonical }}`. """
    py = HOME_V2_PY.read_text(encoding="utf-8")
    html = HOME_V2_HTML.read_text(encoding="utf-8")

    # Remove linhas de comentario (# ...) antes de checar por atribuicao
    # real -- o proprio arquivo comenta o codigo-fonte do Frappe
    # (`self.context.canonical = ...`) a titulo de explicacao, o que nao
    # deve ser confundido com uma atribuicao de verdade neste controller.
    py_code_only = "\n".join(
        line for line in py.splitlines() if not line.strip().startswith("#")
    )

    assert "context.canonical_url" in py, (
        "_home_v2.py precisa setar context.canonical_url (chave real, ver curso.py) -- "
        "context.canonical sozinho e sobrescrito pelo core do Frappe e nunca chega ao template."
    )
    assert re.search(r"(?<!self\.)context\.canonical(?!_url)\s*=", py_code_only) is None, (
        "_home_v2.py nao deve setar context.canonical diretamente -- essa chave e sempre "
        "sobrescrita pelo core do Frappe (base_template_page.py:set_missing_values); "
        "usar context.canonical_url."
    )
    assert '{{ canonical_url }}' in html, (
        "_home_v2.html precisa renderizar {{ canonical_url }} no <link rel=\"canonical\"> "
        "(mesmo padrao de templates/base.html e curso.html)."
    )
    assert re.search(r"\{\{\s*canonical\s*\}\}", html) is None, (
        "_home_v2.html nao deve referenciar {{ canonical }} (valor sempre sobrescrito pelo "
        "core do Frappe para a URL da propria pagina -- usar {{ canonical_url }})."
    )


def test_home_v2_canonical_points_to_real_home_not_itself():
    py = HOME_V2_PY.read_text(encoding="utf-8")
    assert 'frappe.utils.get_url("/")' in py, (
        "canonical_url da rota /_home_v2 precisa apontar pra \"/\" (Home real) -- "
        "nunca para a propria rota tecnica (evita competir com \"/\" por indexacao "
        "mesmo se o noindex for removido por engano no futuro)."
    )


def test_home_v2_is_noindex_and_out_of_sitemap():
    py = HOME_V2_PY.read_text(encoding="utf-8")
    html = HOME_V2_HTML.read_text(encoding="utf-8")
    assert "context.no_sitemap = 1" in py
    assert 'noindex, nofollow' in html


def test_home_v2_does_not_create_a_redirect():
    """Secao 1 da missao da Fase C: "/_home_v2" nao pode ser um redirect
    nem criar um -- e uma pagina real (HTTP 200), nao um alias de "/"."""
    py = HOME_V2_PY.read_text(encoding="utf-8")
    html = HOME_V2_HTML.read_text(encoding="utf-8")
    for forbidden in ("redirect_location", "raise frappe.Redirect", "frappe.local.flags.redirect"):
        assert forbidden not in py
        assert forbidden not in html


def test_real_home_untouched_by_the_v2_integration():
    """Ate a Fase C.1.3, este teste garantia que `/` continuava com o
    canonical hardcoded original e nenhuma referencia as rotas tecnicas V2
    -- correto ENQUANTO o cutover nao era autorizado.

    Fase C.1.4 (cutover controlado, autorizado explicitamente pela missao):
    `/` passou a SER a implementacao V2, reutilizando o mesmo template
    compartilhado de `/_home_v2` (secao 5 da missao: "template
    compartilhado + context compartilhado, minimo de duplicacao"). O teste
    virou o oposto do que era: confirma que o cutover de fato aconteceu
    (canonical via context.canonical_url, nao mais hardcoded; corpo via
    home_page_content.html) e que a rota tecnica /_home_v2 continua
    existindo em paralelo (nao removida, so deixou de ser a UNICA
    implementacao real -- ver docs/redesign/47-home-v2-cutover-result.md)."""
    html = INDEX_HTML.read_text(encoding="utf-8")
    py = INDEX_PY.read_text(encoding="utf-8")
    assert "{{ canonical_url }}" in html, (
        "index.html deveria usar o mecanismo real de canonical_url (nao mais "
        "o valor hardcoded do V1) -- ver www/_home_v2.py pra origem do padrao."
    )
    assert "context.canonical_url" in py
    assert '"templates/includes/v2/home_page_content.html"' in html, (
        "index.html precisa reusar o MESMO corpo compartilhado de /_home_v2, "
        "nao duplicar o HTML (secao 5 da missao C.1.4)."
    )
    assert "build_home_v2_context" in py
    # A rota tecnica continua existindo (nao removida nesta fase).
    assert HOME_V2_PY.exists()
    assert HOME_V2_HTML.exists()


def test_noindex_never_leaks_from_home_v2_route_into_real_home():
    """Fase C.1.4 (secao 6 da missao: "Não deixar noindex vazar para `/`.
    Criar teste específico."). `/` precisa ser index,follow (contrato real
    de producao, preservado do V1); `/_home_v2` precisa continuar
    noindex/nofollow/fora do sitemap -- os dois nunca podem trocar de
    lugar por engano."""
    index_html = INDEX_HTML.read_text(encoding="utf-8")
    index_py = INDEX_PY.read_text(encoding="utf-8")
    home_v2_html = HOME_V2_HTML.read_text(encoding="utf-8")
    home_v2_py = HOME_V2_PY.read_text(encoding="utf-8")

    assert 'content="index, follow' in index_html, "/ precisa continuar indexavel"
    assert "noindex" not in index_html, "/ nunca pode ter noindex"
    assert "context.robots" not in index_py, "/ nao deve setar robots=noindex via context"
    assert "no_sitemap" not in index_py, "/ precisa continuar no sitemap"

    assert 'content="noindex, nofollow"' in home_v2_html, "/_home_v2 precisa continuar noindex"
    assert 'context.robots = "noindex, nofollow"' in home_v2_py
    assert "context.no_sitemap = 1" in home_v2_py, "/_home_v2 precisa continuar fora do sitemap"


def test_pathfinder_matrix_languages_match_between_python_and_js():
    """A matriz de encaminhamento do Pathfinder existe em DOIS lugares
    (Python, fonte de verdade documentada, e JS, espelho client-side --
    JS nao executa Python em tempo de navegacao). As duas precisam ter
    exatamente as mesmas 5 chaves de idioma, ou a documentacao e o
    comportamento real divergem silenciosamente."""
    py_src = V2_HOME_DATA.read_text(encoding="utf-8")
    js_src = V2_JS.read_text(encoding="utf-8")

    expected_languages = [
        "Inglês", "Iorubá", "Português para Estrangeiros", "Espanhol", "Hebraico",
    ]
    for lang in expected_languages:
        assert f'"{lang}"' in py_src or f"'{lang}'" in py_src, f"{lang} ausente em PATHFINDER_MATRIX (Python)"
        assert f'"{lang}"' in js_src, f"{lang} ausente em PATHFINDER_MATRIX (JS)"

    assert "PATHFINDER_MATRIX" in py_src
    assert "PATHFINDER_MATRIX" in js_src
    assert "initPathfinderRouting" in js_src


def test_pathfinder_matrix_has_no_fabricated_urls():
    """Toda URL na matriz precisa corresponder a um arquivo www/ real
    (ou ser a pagina-pilar, ja confirmada em fases anteriores) -- nunca
    um slug inventado. Checagem estrutural (existencia de arquivo), nao
    HTTP (isso e feito manualmente/via script CDP, documentado em
    docs/redesign/27-home-v2-link-contract.md)."""
    py_src = V2_HOME_DATA.read_text(encoding="utf-8")
    urls = set(re.findall(r'"(/[a-z0-9\-]+)"', py_src))
    known_pillars = {
        "/curso-de-ingles-online", "/curso-de-ioruba-online", "/portugues-para-estrangeiros",
        "/curso-de-espanhol-online", "/curso-de-hebraico-online",
    }
    known_objective_pages = {
        "/ingles-executivo", "/ingles-para-viagens", "/ioruba-cultura-e-ancestralidade",
        "/portugues-para-executivos", "/preparatorio-celpe-bras",
    }
    for url in urls & (known_pillars | known_objective_pages | {"/teste-de-nivel", "/blog"}):
        if url in known_objective_pages or url in known_pillars:
            slug = url.strip("/")
            assert (WWW / f"{slug}.html").exists(), f"URL {url} na matriz do Pathfinder nao tem arquivo www/ real"


def test_v2_home_data_module_does_not_touch_shared_production_files():
    """v2_home_data.py precisa so LER blog_content.py (import), nunca
    escrever nele -- garante isolamento (arquivo novo, nao modifica
    producao compartilhada)."""
    src = V2_HOME_DATA.read_text(encoding="utf-8")
    assert "import" in src and "blog_content" in src
    # so leitura via .items(), nunca escrita indexada nova
    assert "BLOG_POSTS[" not in src.replace("BLOG_POSTS[slug]", "")
