/* Vedium -- Google Consent Mode v2 (Fase C.1.1, Parte C da missao;
 * cableado em producao na Fase C.1.3).
 *
 * Carregado sitewide via <script> hardcoded logo apos cookie-consent.js em
 * 120 arquivos www/*.html (mesmo padrao ja usado por aquele arquivo --
 * achado real: hooks.py `web_include_js` NAO se aplica a essas paginas,
 * que nao extendem templates/base.html; ver nota em hooks.py e
 * docs/redesign/45-consent-remediation-result.md). Tres partes:
 *
 * 1) setDefaultDeniedConsent() -- REDE DE SEGURANCA, nao a fonte primaria.
 *    A fonte primaria do sinal `default` e o snippet inline em
 *    templates/includes/consent_default.html, incluido nos 8 pontos reais
 *    que inicializam o GTM (Fase C.1.3, ver
 *    docs/redesign/45-consent-remediation-result.md), sempre ANTES do
 *    bloco GTM correspondente -- esse arquivo carrega tarde demais (perto
 *    do fim do <body>) pra ser a fonte primaria, ver medicao empirica na
 *    Fase C.1.2. Aqui, so chama setDefaultDeniedConsent() se o guard
 *    `window.__vediumConsentDefaultSet` (mesmo guard do include acima)
 *    ainda nao tiver sido setado -- cobre qualquer pagina que por engano
 *    nao tenha o include, sem duplicar o `default` nas que ja tem.
 *
 * 2) grantConsentFromAcceptance()/denyConsentExplicitly() -- decisao
 *    BINARIA (Aceitar tudo / Recusar tudo), disparada pelos eventos
 *    "vedium:consent"/"vedium:consent-rejected" que cookie-consent.js ja
 *    despacha nos botoes Aceitar/Recusar.
 *
 * 3) applyGranularPreferences(analytics, marketing) -- decisao GRANULAR,
 *    disparada pelo evento "vedium:consent-preferences" (painel "Gerenciar
 *    preferencias", Fase C.1.3). Mapeia direto pros 4 sinais reais, sem
 *    inventar categoria nova: analytics -> analytics_storage; marketing ->
 *    ad_storage + ad_user_data + ad_personalization (Meta Pixel + tags de
 *    anuncio viajam juntas aqui). Restaura o estado granular salvo em
 *    localStorage.vedium_cookie_preferences a cada carregamento de pagina
 *    (persistencia entre reload/navegacao/troca de locale).
 *
 * Sinais mapeados (secao 14 da missao C.1.2): analytics_storage, ad_storage,
 * ad_user_data, ad_personalization -- os 4 exigidos pelo Consent Mode v2
 * do Google desde marco/2024 pra contas que servem EEE/UK (Vedium serve
 * publico internacional via /en /es /fr /de /ru, entao os 4 se aplicam,
 * nao so os 2 legados de analytics/ads_storage).
 */
(function () {
  "use strict";

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }

  function setDefaultDeniedConsent() {
    gtag("consent", "default", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      wait_for_update: 500,
    });
  }

  function grantConsentFromAcceptance() {
    gtag("consent", "update", {
      analytics_storage: "granted",
      ad_storage: "granted",
      ad_user_data: "granted",
      ad_personalization: "granted",
    });
  }

  function denyConsentExplicitly() {
    try {
      window.localStorage.setItem("vedium_cookie_consent", "rejected");
    } catch (e) {}
    gtag("consent", "update", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
  }

  function applyGranularPreferences(analytics, marketing) {
    gtag("consent", "update", {
      analytics_storage: analytics ? "granted" : "denied",
      ad_storage: marketing ? "granted" : "denied",
      ad_user_data: marketing ? "granted" : "denied",
      ad_personalization: marketing ? "granted" : "denied",
    });
  }

  function alreadyAccepted() {
    try {
      var saved = window.localStorage.getItem("vedium_cookie_consent");
      return saved === "1" || saved === "accepted" || saved === "essential";
    } catch (e) {
      return false;
    }
  }

  function readStoredPreferences() {
    try {
      var raw = window.localStorage.getItem("vedium_cookie_preferences");
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  if (!window.__vediumConsentDefaultSet) {
    window.__vediumConsentDefaultSet = true;
    setDefaultDeniedConsent();
  }

  var storedPreferences = readStoredPreferences();
  if (storedPreferences) {
    // Restaura a escolha granular salva (Fase C.1.3) -- prioridade sobre
    // o binario simples, cobre o caso "analytics sim, marketing nao" que
    // alreadyAccepted() sozinho nao distingue.
    applyGranularPreferences(!!storedPreferences.analytics, !!storedPreferences.marketing);
  } else if (alreadyAccepted()) {
    grantConsentFromAcceptance();
  }

  window.addEventListener("vedium:consent", grantConsentFromAcceptance);
  window.addEventListener("vedium:consent-rejected", denyConsentExplicitly);
  window.addEventListener("vedium:consent-preferences", function (evt) {
    if (evt && evt.detail) {
      applyGranularPreferences(!!evt.detail.analytics, !!evt.detail.marketing);
    }
  });

  window.VediumConsentMode = {
    setDefaultDeniedConsent: setDefaultDeniedConsent,
    grantConsentFromAcceptance: grantConsentFromAcceptance,
    denyConsentExplicitly: denyConsentExplicitly,
    applyGranularPreferences: applyGranularPreferences,
  };
})();
