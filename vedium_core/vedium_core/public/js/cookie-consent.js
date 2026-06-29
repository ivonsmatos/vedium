/* Vedium — barra de consentimento de cookies (LGPD) */
(function () {
  try {
    var saved = localStorage.getItem("vedium_cookie_consent");
    if (saved === "1" || saved === "accepted" || saved === "essential") return;
  } catch (e) { return; }

  function injectStyles() {
    if (document.getElementById("vd-cookie-style")) return;
    var style = document.createElement("style");
    style.id = "vd-cookie-style";
    style.textContent = [
      "#vd-cookie-bar{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;background:#11161d;color:#fff;padding:16px 20px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:center;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.5;box-shadow:0 -2px 16px rgba(0,0,0,.3);}",
      "#vd-cookie-bar p{max-width:780px;margin:0;color:#fff;}",
      "#vd-cookie-bar a{color:#93c5fd;text-decoration:underline;}",
      "#vd-cookie-bar .vd-cookie-actions{display:flex;gap:10px;align-items:center;}",
      "#vd-cookie-bar button{background:#2E6DA4;color:#fff;border:none;padding:11px 24px;border-radius:8px;font-weight:700;cursor:pointer;font-size:14px;}",
      "#vd-cookie-bar .vd-cookie-more{background:transparent;color:#cbd5e1;border:1px solid #475569;padding:10px 18px;border-radius:8px;font-weight:600;text-decoration:none;font-size:14px;}",
      "@media(max-width:767px){#vd-cookie-bar{top:12px;left:12px;right:12px;bottom:auto;border-radius:12px;padding:10px 12px;justify-content:flex-start;font-size:12px;line-height:1.35;box-shadow:0 10px 30px rgba(0,0,0,.22);}#vd-cookie-bar p{max-width:none;flex:1 1 100%;}#vd-cookie-bar .vd-cookie-actions{width:100%;justify-content:flex-end;}#vd-cookie-bar button,#vd-cookie-bar .vd-cookie-more{padding:8px 12px;font-size:12px;border-radius:7px;}}"
    ].join("");
    document.head.appendChild(style);
  }

  function show() {
    if (document.getElementById("vd-cookie-bar")) return;
    injectStyles();
    var bar = document.createElement("div");
    bar.id = "vd-cookie-bar";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-label", "Aviso de cookies");
    bar.innerHTML =
      '<p>Usamos cookies para melhorar a sua experiência e analisar o uso do site. ' +
      'Ao continuar navegando, você concorda com a nossa ' +
      '<a href="/privacidade">Política de Privacidade</a>.</p>' +
      '<span class="vd-cookie-actions">' +
      '<button id="vd-cookie-ok" type="button">Aceitar</button>' +
      '<a class="vd-cookie-more" href="/privacidade">Saiba mais</a>' +
      '</span>';
    document.body.appendChild(bar);
    var btn = document.getElementById("vd-cookie-ok");
    if (btn) btn.addEventListener("click", function () {
      try { localStorage.setItem("vedium_cookie_consent", "1"); } catch (e) {}
      // avisa os trackers (ex.: meta-pixel.js) para dispararem nesta navegação
      try { window.dispatchEvent(new Event("vedium:consent")); } catch (e) {}
      if (bar.parentNode) bar.parentNode.removeChild(bar);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", show);
  } else {
    show();
  }
})();
