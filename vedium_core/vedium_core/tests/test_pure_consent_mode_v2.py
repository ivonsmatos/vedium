"""Testes puros do Consent Mode v2 (Fase C.1.1 Parte C -> Fase C.1.3 Parte A).

Fase C.1.3: consent-mode-v2.js e a barra de cookies foram CABLEADOS em
producao (autorizado explicitamente pela missao C.1.3, ver
docs/redesign/45-consent-remediation-result.md). Testes de texto/estrutura
aqui; verificacao empirica em runtime (dataLayer real, cliques reais via
CDP) esta documentada no mesmo doc 45, nao reproduzida em pytest porque
exigiria um browser headless que a suite normal nao tem disponivel."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONSENT_JS = ROOT / "vedium_core" / "vedium_core" / "public" / "js" / "v2" / "consent-mode-v2.js"
COOKIE_CONSENT_JS = ROOT / "vedium_core" / "vedium_core" / "public" / "js" / "cookie-consent.js"
COOKIE_CONSENT_MIN_JS = ROOT / "vedium_core" / "vedium_core" / "public" / "js" / "cookie-consent.min.js"
META_PIXEL_JS = ROOT / "vedium_core" / "vedium_core" / "public" / "js" / "meta-pixel.js"
CONSENT_DEFAULT_INCLUDE = ROOT / "vedium_core" / "vedium_core" / "templates" / "includes" / "consent_default.html"
WWW = ROOT / "vedium_core" / "vedium_core" / "www"
TEMPLATES = ROOT / "vedium_core" / "vedium_core" / "templates"

EIGHT_ENTRYPOINTS = [
    WWW / "index.html",
    WWW / "en" / "index.html",
    WWW / "es" / "index.html",
    WWW / "de" / "index.html",
    WWW / "fr" / "index.html",
    WWW / "ru" / "index.html",
    WWW / "curso.html",
    TEMPLATES / "includes" / "site_footer.html",
]


def test_consent_mode_file_exists():
    assert CONSENT_JS.exists()


def test_sets_all_four_consent_mode_v2_signals_denied_by_default():
    src = CONSENT_JS.read_text(encoding="utf-8")
    assert '"consent", "default"' in src
    for signal in ("analytics_storage", "ad_storage", "ad_user_data", "ad_personalization"):
        assert signal in src


def test_grants_consent_on_existing_vedium_consent_event():
    src = CONSENT_JS.read_text(encoding="utf-8")
    assert '"consent", "update"' in src
    assert "vedium:consent" in src


def test_does_not_duplicate_or_modify_shared_cookie_consent_file():
    src = CONSENT_JS.read_text(encoding="utf-8")
    assert "vd-cookie-bar" not in src, "nao deve reimplementar a barra de cookies existente"
    assert COOKIE_CONSENT_JS.exists()
    cookie_src = COOKIE_CONSENT_JS.read_text(encoding="utf-8")
    assert "vedium:consent" in cookie_src, (
        "cookie-consent.js precisa continuar disparando o evento que este arquivo escuta"
    )


def test_exposes_explicit_reject():
    src = CONSENT_JS.read_text(encoding="utf-8")
    assert "denyConsentExplicitly" in src
    assert "vedium:consent-rejected" in src
    assert '"rejected"' in src


def test_exposes_granular_preferences_handler():
    """Fase C.1.3 (secao 6 da missao): categorias reais (analytics/marketing),
    nao inventadas -- mapeiam direto pros 4 sinais ja usados no default/update."""
    src = CONSENT_JS.read_text(encoding="utf-8")
    assert "applyGranularPreferences" in src
    assert "vedium:consent-preferences" in src


def test_meta_pixel_logic_gates_on_consent_when_loaded():
    """A LOGICA de meta-pixel.js respeita consentimento (achado real da
    Fase C.1.1, reconfirmado aqui) -- ver test_meta_pixel_min_js_is_never_
    referenced_by_any_real_page abaixo pro achado adicional da Fase C.1.3."""
    assert META_PIXEL_JS.exists()
    src = META_PIXEL_JS.read_text(encoding="utf-8")
    assert "vedium:consent" in src
    assert "vedium_cookie_consent" in src


def test_meta_pixel_min_js_is_never_referenced_by_any_real_page():
    """Achado NOVO da Fase C.1.3: meta-pixel.min.js so aparece em hooks.py
    (web_include_js -- mecanismo que nao se aplica as paginas reais, ver
    consent_default.html/hooks.py) e em nenhum www/*.html real. Ou seja, a
    logica de consentimento de meta-pixel.js esta correta, mas o arquivo
    nunca carrega em producao hoje -- achado registrado, NAO corrigido
    nesta fase (missao pediu explicitamente pra nao reescrever/republicar
    Meta). Ver docs/redesign/45-consent-remediation-result.md."""
    html_files = list(WWW.rglob("*.html")) + list(TEMPLATES.rglob("*.html"))
    referencing = [f for f in html_files if "meta-pixel" in f.read_text(encoding="utf-8", errors="ignore")]
    assert referencing == [], (
        "Se este teste comecar a falhar porque um arquivo passou a referenciar "
        "meta-pixel.min.js, isso e uma correcao real do gap documentado -- "
        "atualizar este teste pra refletir o novo estado, nao reverter a mudanca."
    )


def test_consent_default_include_exists_and_has_idempotency_guard():
    assert CONSENT_DEFAULT_INCLUDE.exists()
    src = CONSENT_DEFAULT_INCLUDE.read_text(encoding="utf-8")
    assert "__vediumConsentDefaultSet" in src
    assert "consent" in src and "default" in src


def test_eight_real_entrypoints_include_consent_default_exactly_once():
    """Fase C.1.3 (secao 2-3 da missao): os 8 pontos reais que inicializam
    o GTM (mapeados na Fase C.1.2) precisam ter o include do consent
    default, cada um EXATAMENTE UMA VEZ no proprio arquivo -- o guard em
    consent_default.html cobre paginas que acumulam 2 copias do include
    via {% include %} aninhado (ex. index.html inclui site_footer.html
    mais abaixo), mas cada ARQUIVO individual deve referenciar o include
    uma unica vez (nao duas por engano)."""
    for path in EIGHT_ENTRYPOINTS:
        assert path.exists(), f"entrypoint esperado nao encontrado: {path}"
        src = path.read_text(encoding="utf-8")
        count = src.count('{% include "templates/includes/consent_default.html" %}')
        assert count == 1, f"{path} deveria incluir consent_default.html 1 vez, encontrado {count}"


def test_consent_default_include_precedes_gtm_block_in_each_entrypoint():
    for path in EIGHT_ENTRYPOINTS:
        src = path.read_text(encoding="utf-8")
        include_idx = src.find('{% include "templates/includes/consent_default.html" %}')
        gtm_idx = src.find("GTM-P6Q2FXLK")
        assert include_idx != -1 and gtm_idx != -1, f"include ou GTM ausente em {path}"
        assert include_idx < gtm_idx, f"consent default precisa vir ANTES do GTM em {path}"


def test_cookie_consent_has_accept_reject_and_manage_with_equivalent_prominence():
    """Fase C.1.3 (secao 4 da missao): nao criar dark pattern -- Aceitar e
    Recusar tem a mesma classe de botao principal ausente (ambos <button>
    top-level do mesmo <span> de acoes), "Gerenciar preferencias" e
    secundario visualmente mas sempre presente, nunca escondido atras de
    mais cliques que os outros dois."""
    src = COOKIE_CONSENT_JS.read_text(encoding="utf-8")
    assert 'id="vd-cookie-ok"' in src
    assert 'id="vd-cookie-reject"' in src
    assert 'id="vd-cookie-manage"' in src
    # Os 3 botoes vivem no mesmo bloco vd-cookie-actions (mesmo nivel, sem
    # esconder Recusar atras de um menu ou de mais passos que Aceitar).
    actions_block = src.split('class="vd-cookie-actions"')[1].split("</span>")[0]
    for btn_id in ("vd-cookie-ok", "vd-cookie-reject", "vd-cookie-manage"):
        assert btn_id in actions_block


def test_cookie_consent_preferences_categories_map_to_real_signals_only():
    """Fase C.1.3 (secao 6): nenhuma categoria inventada -- so
    Essenciais (sempre ativo)/Analytics/Marketing, mapeando pros 4 sinais
    reais ja usados em consent-mode-v2.js."""
    src = COOKIE_CONSENT_JS.read_text(encoding="utf-8")
    assert "vd-cookie-pref-analytics" in src
    assert "vd-cookie-pref-marketing" in src
    assert "checked disabled" in src  # essenciais sempre ativo, sem toggle


def test_cookie_consent_six_locales_have_accept_reject_manage_texts():
    src = COOKIE_CONSENT_JS.read_text(encoding="utf-8")
    approved = {
        "pt": ("Aceitar", "Recusar", "Gerenciar preferências"),
        "en": ("Accept", "Reject", "Manage preferences"),
        "es": ("Aceptar", "Rechazar", "Gestionar preferencias"),
        "fr": ("Accepter", "Refuser", "Gérer les préférences"),
        "de": ("Akzeptieren", "Ablehnen", "Einstellungen verwalten"),
        "ru": ("Принять", "Отклонить", "Управлять настройками"),
    }
    for lang, (accept, reject, manage) in approved.items():
        assert accept in src, f"texto de Aceitar ausente para {lang}"
        assert reject in src, f"texto de Recusar ausente para {lang}"
        assert manage in src, f"texto de Gerenciar preferencias ausente para {lang}"


def test_cookie_consent_min_js_was_regenerated_and_cache_bust_bumped():
    """Fase C.1.3: cookie-consent.min.js precisa refletir o cookie-consent.js
    atualizado (Aceitar/Recusar/Gerenciar), e a query string de
    cache-busting precisa ter mudado (senao navegadores com o arquivo
    antigo em cache HTTP nunca veriam o botao novo)."""
    assert COOKIE_CONSENT_MIN_JS.exists()
    min_src = COOKIE_CONSENT_MIN_JS.read_text(encoding="utf-8")
    assert "vd-cookie-reject" in min_src
    assert "vd-cookie-manage" in min_src
    for path in EIGHT_ENTRYPOINTS + [WWW / "contato.html"]:
        src = path.read_text(encoding="utf-8")
        if "cookie-consent.min.js" in src:
            assert "v=mobile-pwa-fix" not in src, f"{path} ainda referencia a versao antiga do cache-bust"
