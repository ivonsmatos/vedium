import Script from "next/script";

/**
 * GTM real + Consent Mode v2 no Next (Fase G.2, Parte A). Container único
 * confirmado em produção (`docs/redesign/baseline/analytics-contracts.md`)
 * -- não inventar outro. GA4 (`G-TMBTXVRMLE`) roda 100% de DENTRO do
 * container (tag "GA4 - Base Config"), então este arquivo NUNCA carrega
 * gtag.js/GA4 separadamente -- carregar o container basta.
 *
 * Ordem (P0, missão seção 3): o sinal `consent default` PRECISA rodar
 * antes do GTM. Aqui isso é garantido pela própria semântica do
 * `next/script`, não por convenção de posição no arquivo:
 * `beforeInteractive` é injetado no `<head>` e executa antes de qualquer
 * script `afterInteractive` (GTM incluso) -- ver
 * `node_modules/next/dist/docs/01-app/02-guides/scripts.md`, que cita
 * "cookie consent managers" como o exemplo canônico de `beforeInteractive`
 * e "tag managers" como o exemplo canônico de `afterInteractive`.
 *
 * Snippet do GTM copiado da variante COM guard de dedupe
 * (`d.querySelector('script[src*="'+i+'"]')`), a mesma usada em
 * `templates/includes/site_footer.html` -- não a variante sem guard de
 * `www/index.html`, que é a origem do bug documentado de
 * `<noscript>` duplicado. Escolha deliberada: começar do padrão sem o bug
 * conhecido, não replicá-lo numa base de código nova.
 *
 * `cookie-consent.js` e `consent-mode-v2.js` são cópias vendorizadas
 * byte-a-byte dos arquivos reais de produção (ver comentário de proveniência
 * em cada um, `public/assets/vedium_core/js/`) -- mesmas chaves de
 * localStorage (`vedium_cookie_consent`, `vedium_cookie_preferences`),
 * mesmos eventos (`vedium:consent`, `vedium:consent-rejected`,
 * `vedium:consent-preferences`), para que o consentimento dado num
 * frontend seja respeitado no outro sem duas fontes de verdade
 * (missão seção 4-5; ver `docs/frontend-v2/35-gtm-next-contract.md`).
 */
const GTM_CONTAINER_ID = "GTM-P6Q2FXLK";

export function AnalyticsScripts() {
  return (
    <>
      <Script id="vedium-consent-default" strategy="beforeInteractive">
        {`
window.dataLayer = window.dataLayer || [];
if (!window.__vediumConsentDefaultSet) {
  window.__vediumConsentDefaultSet = true;
  (function () {
    function gtag() { window.dataLayer.push(arguments); }
    gtag('consent', 'default', {
      'analytics_storage': 'denied',
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied',
      'wait_for_update': 500
    });
  })();
}
        `}
      </Script>

      <Script id="vedium-gtm" strategy="afterInteractive">
        {`
(function(w,d,s,l,i){
  w[l]=w[l]||[];
  if (d.querySelector('script[src*="' + i + '"]')) return;
  w[l].push({'gtm.start': new Date().getTime(), event:'gtm.js'});
  var f=d.getElementsByTagName(s)[0], j=d.createElement(s), dl=l!='dataLayer'?'&l='+l:'';
  j.async=true; j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;
  f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','${GTM_CONTAINER_ID}');
        `}
      </Script>

      <noscript>
        <iframe
          src={`https://www.googletagmanager.com/ns.html?id=${GTM_CONTAINER_ID}`}
          height="0"
          width="0"
          style={{ display: "none", visibility: "hidden" }}
          title="Google Tag Manager"
        />
      </noscript>

      <Script src="/assets/vedium_core/js/cookie-consent.js" strategy="afterInteractive" />
      <Script src="/assets/vedium_core/js/v2/consent-mode-v2.js" strategy="afterInteractive" />
    </>
  );
}
