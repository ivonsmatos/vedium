/* Vedium — Barra de consentimento de cookies/termos (LGPD)
 * Auto-injeta a barra se o usuário ainda não aceitou. Lembra a escolha em localStorage.
 */
(function () {
  "use strict";
  var KEY = "vedium_cookie_consent";
  try {
    if (localStorage.getItem(KEY) === "accepted") return;
  } catch (e) { /* localStorage indisponível: mostra a barra mesmo assim */ }

  var css = ''
    + '#vd-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:2000;'
    + 'background:#0f172a;color:#fff;border-radius:14px;box-shadow:0 10px 40px rgba(0,0,0,.35);'
    + 'padding:18px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap;'
    + "font-family:'Outfit',system-ui,-apple-system,sans-serif;max-width:1100px;margin:0 auto;"
    + 'transform:translateY(140%);transition:transform .4s ease;}'
    + '#vd-consent.vd-show{transform:translateY(0);}'
    + '#vd-consent p{margin:0;flex:1 1 320px;font-size:.95rem;line-height:1.55;color:rgba(255,255,255,.85);}'
    + '#vd-consent a{color:#93c5fd;text-decoration:underline;}'
    + '#vd-consent .vd-actions{display:flex;gap:10px;flex:0 0 auto;}'
    + '#vd-consent button{cursor:pointer;border:none;border-radius:50px;font-weight:600;'
    + 'padding:.7rem 1.4rem;font-size:.9rem;font-family:inherit;}'
    + '#vd-consent .vd-accept{background:#2563eb;color:#fff;}'
    + '#vd-consent .vd-accept:hover{background:#1d4ed8;}'
    + '#vd-consent .vd-reject{background:transparent;color:rgba(255,255,255,.75);border:1px solid rgba(255,255,255,.3);}'
    + '#vd-consent .vd-reject:hover{color:#fff;border-color:#fff;}'
    + '@media(max-width:600px){#vd-consent{flex-direction:column;align-items:stretch;text-align:left;}'
    + '#vd-consent .vd-actions{justify-content:flex-end;}}';

  function inject() {
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    var bar = document.createElement("div");
    bar.id = "vd-consent";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-label", "Aviso de cookies");
    bar.innerHTML =
      '<p>🍪 Usamos cookies e tecnologias similares para melhorar sua experiência e analisar o uso do site. '
      + 'Ao continuar, você concorda com a nossa '
      + '<a href="/privacidade.html">Política de Privacidade</a> e os '
      + '<a href="/termos.html">Termos de Uso</a>.</p>'
      + '<div class="vd-actions">'
      + '<button type="button" class="vd-reject">Só essenciais</button>'
      + '<button type="button" class="vd-accept">Aceitar</button>'
      + '</div>';
    document.body.appendChild(bar);
    requestAnimationFrame(function () { bar.classList.add("vd-show"); });

    function close(value) {
      try { localStorage.setItem(KEY, value); } catch (e) {}
      bar.classList.remove("vd-show");
      setTimeout(function () { bar.remove(); }, 400);
    }
    bar.querySelector(".vd-accept").addEventListener("click", function () { close("accepted"); });
    bar.querySelector(".vd-reject").addEventListener("click", function () { close("essential"); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }
})();
