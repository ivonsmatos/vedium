/* Vedium — Meta Pixel (Facebook/Instagram Ads)
 * Carregado em todas as páginas públicas via web_include_js (hooks.py).
 * ID: 1539456614495904
 *
 * LGPD: só dispara APÓS o consentimento de cookies. Em visitas onde o
 * usuário já aceitou (localStorage vedium_cookie_consent === "1") carrega
 * de imediato; senão, aguarda o evento "vedium:consent" emitido pela barra
 * de cookies (cookie-consent.js) ao clicar "Aceitar" — assim o pixel
 * dispara na mesma navegação, sem precisar recarregar a página.
 *
 * Obs.: o <noscript><img> do snippet oficial não se aplica aqui — um pixel
 * carregado por JS já não rastreia navegadores sem JS.
 */
(function () {
  function loadPixel() {
    if (window.fbq) return; // evita inicializar duas vezes

    !(function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = "2.0";
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");

    fbq("init", "1539456614495904");
    fbq("track", "PageView");
  }

  var consented = false;
  try {
    var _c = localStorage.getItem("vedium_cookie_consent");
    consented = _c === "1" || _c === "accepted";
  } catch (e) {}

  if (consented) {
    loadPixel();
  } else {
    // dispara assim que o usuário aceitar os cookies (sem recarregar)
    window.addEventListener("vedium:consent", loadPixel, { once: true });
  }
})();
