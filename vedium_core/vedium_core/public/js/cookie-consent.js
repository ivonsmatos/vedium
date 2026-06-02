/* Vedium — barra de consentimento de cookies (LGPD) */
(function () {
  try {
    if (localStorage.getItem("vedium_cookie_consent") === "1") return;
  } catch (e) { return; }

  function show() {
    if (document.getElementById("vd-cookie-bar")) return;
    var bar = document.createElement("div");
    bar.id = "vd-cookie-bar";
    bar.setAttribute("style",
      "position:fixed;left:0;right:0;bottom:0;z-index:2147483000;background:#11161d;color:#fff;" +
      "padding:16px 20px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:center;" +
      "font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.5;box-shadow:0 -2px 16px rgba(0,0,0,.3);");
    bar.innerHTML =
      '<span style="max-width:780px;">🍪 Usamos cookies para melhorar a sua experiência e analisar o uso do site. ' +
      'Ao continuar navegando, você concorda com a nossa ' +
      '<a href="/privacidade" style="color:#93c5fd;text-decoration:underline;">Política de Privacidade</a>.</span>' +
      '<span style="display:flex;gap:10px;">' +
      '<button id="vd-cookie-ok" style="background:#2E6DA4;color:#fff;border:none;padding:11px 24px;border-radius:8px;font-weight:700;cursor:pointer;font-size:14px;">Aceitar</button>' +
      '<a href="/privacidade" style="background:transparent;color:#cbd5e1;border:1px solid #475569;padding:11px 18px;border-radius:8px;font-weight:600;text-decoration:none;font-size:14px;">Saiba mais</a>' +
      '</span>';
    document.body.appendChild(bar);
    var btn = document.getElementById("vd-cookie-ok");
    if (btn) btn.addEventListener("click", function () {
      try { localStorage.setItem("vedium_cookie_consent", "1"); } catch (e) {}
      if (bar.parentNode) bar.parentNode.removeChild(bar);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", show);
  } else {
    show();
  }
})();
