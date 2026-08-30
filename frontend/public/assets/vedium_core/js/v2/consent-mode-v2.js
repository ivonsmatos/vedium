/* Vedium — Google Consent Mode v2
 *
 * CÓPIA VENDORIZADA (Fase G.2, Parte A) do arquivo real de produção
 * `vedium_core/vedium_core/public/js/v2/consent-mode-v2.js` -- byte-a-byte,
 * sem reescrever nenhuma linha de lógica. Ver nota equivalente em
 * `cookie-consent.js` deste mesmo diretório.
 *
 * 1) setDefaultDeniedConsent() -- REDE DE SEGURANCA, nao a fonte primaria.
 *    A fonte primaria do sinal `default` no Next e o script inline
 *    `beforeInteractive` em `components/analytics/AnalyticsScripts.tsx`
 *    (equivalente ao `templates/includes/consent_default.html` da
 *    produção), que sempre executa antes de qualquer script
 *    `afterInteractive` (GTM incluso) -- ver documentação da estratégia do
 *    `next/script`. Aqui, so chama setDefaultDeniedConsent() se o guard
 *    `window.__vediumConsentDefaultSet` (mesmo guard do script inline)
 *    ainda nao tiver sido setado.
 *
 * 2) grantConsentFromAcceptance()/denyConsentExplicitly() -- decisao
 *    BINARIA (Aceitar tudo / Recusar tudo), disparada pelos eventos
 *    "vedium:consent"/"vedium:consent-rejected" que cookie-consent.js ja
 *    despacha nos botoes Aceitar/Recusar.
 *
 * 3) applyGranularPreferences(analytics, marketing) -- decisao GRANULAR,
 *    disparada pelo evento "vedium:consent-preferences" (painel "Gerenciar
 *    preferencias"). Mapeia direto pros 4 sinais reais, sem inventar
 *    categoria nova: analytics -> analytics_storage; marketing ->
 *    ad_storage + ad_user_data + ad_personalization (Meta Pixel + tags de
 *    anuncio viajam juntas aqui). Restaura o estado granular salvo em
 *    localStorage.vedium_cookie_preferences a cada carregamento de pagina
 *    (persistencia entre reload/navegacao/troca de idioma).
 *
 * Sinais mapeados: analytics_storage, ad_storage, ad_user_data,
 * ad_personalization -- os 4 exigidos pelo Consent Mode v2 do Google desde
 * marco/2024 pra contas que servem EEE/UK.
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
    // Restaura a escolha granular salva -- prioridade sobre o binario
    // simples, cobre o caso "analytics sim, marketing nao" que
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
