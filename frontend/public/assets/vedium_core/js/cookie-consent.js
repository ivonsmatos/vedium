/* Vedium — barra de consentimento de cookies (LGPD)
 *
 * CÓPIA VENDORIZADA (Fase G.2, Parte A) do arquivo real de produção
 * `vedium_core/vedium_core/public/js/cookie-consent.js` -- byte-a-byte, sem
 * reescrever nenhuma linha de lógica. Objetivo: o Next usa o MESMO
 * contrato de consentimento que o Frappe (mesmas chaves de localStorage,
 * mesmos eventos, mesmo texto, mesmo comportamento de acessibilidade), sem
 * inventar uma barra nova (missão G.2, seção 5: "Next deve respeitar o
 * mesmo contrato sempre que tecnicamente possível... Não criar duas
 * preferências independentes"). Qualquer correção futura deve ser aplicada
 * nos DOIS lugares (ou substituída por um pacote compartilhado) -- não
 * diverja este arquivo do original sem atualizar lá também.
 *
 * Fase C.1.3 (original): Aceitar / Recusar / Gerenciar preferências, com
 * facilidade de acesso equivalente entre Aceitar e Recusar (nenhum dark
 * pattern -- os 2 botões principais tem o mesmo estilo visual, "Gerenciar
 * preferências" e secundário mas sempre visível, nunca escondido atrás de
 * mais cliques que os outros dois). Categorias do painel de preferências
 * mapeiam DIRETO pros sinais reais do Consent Mode v2 (nenhuma categoria
 * inventada):
 *   Essenciais  -> sempre ativo (sessão/CSRF do Frappe, indispensável
 *                  tecnicamente, nao e um cookie de rastreamento)
 *   Analytics   -> analytics_storage
 *   Marketing   -> ad_storage + ad_user_data + ad_personalization
 *                  (Meta Pixel + tags de anúncio viajam juntas aqui)
 */
(function () {
  var language = ((document.documentElement.lang || "pt-BR").toLowerCase().split("-")[0]);
  var messages = {
    pt: {
      aria: "Aviso de cookies", prefsAria: "Gerenciar preferências de cookies",
      text: "Usamos cookies para melhorar a sua experiência e analisar o uso do site. Ao continuar navegando, você concorda com a nossa ",
      privacy: "Política de Privacidade", accept: "Aceitar", reject: "Recusar", manage: "Gerenciar preferências", more: "Saiba mais",
      essential: "Essenciais", essentialDesc: "Necessários para o funcionamento do site (sessão, segurança). Sempre ativos.",
      analytics: "Analytics", analyticsDesc: "Nos ajuda a entender como o site é usado.",
      marketing: "Marketing", marketingDesc: "Usado para medir e personalizar anúncios.",
      save: "Salvar preferências"
    },
    en: {
      aria: "Cookie notice", prefsAria: "Manage cookie preferences",
      text: "We use cookies to improve your experience and analyze website usage. By continuing to browse, you agree to our ",
      privacy: "Privacy Policy", accept: "Accept", reject: "Reject", manage: "Manage preferences", more: "Learn more",
      essential: "Essential", essentialDesc: "Required for the site to work (session, security). Always active.",
      analytics: "Analytics", analyticsDesc: "Helps us understand how the site is used.",
      marketing: "Marketing", marketingDesc: "Used to measure and personalize ads.",
      save: "Save preferences"
    },
    es: {
      aria: "Aviso de cookies", prefsAria: "Gestionar preferencias de cookies",
      text: "Usamos cookies para mejorar tu experiencia y analizar el uso del sitio. Al continuar navegando, aceptas nuestra ",
      privacy: "Política de Privacidad", accept: "Aceptar", reject: "Rechazar", manage: "Gestionar preferencias", more: "Más información",
      essential: "Esenciales", essentialDesc: "Necesarios para el funcionamiento del sitio (sesión, seguridad). Siempre activos.",
      analytics: "Analytics", analyticsDesc: "Nos ayuda a entender cómo se usa el sitio.",
      marketing: "Marketing", marketingDesc: "Usado para medir y personalizar anuncios.",
      save: "Guardar preferencias"
    },
    fr: {
      aria: "Avis relatif aux cookies", prefsAria: "Gérer les préférences de cookies",
      text: "Nous utilisons des cookies pour améliorer votre expérience et analyser l'utilisation du site. En poursuivant votre navigation, vous acceptez notre ",
      privacy: "Politique de confidentialité", accept: "Accepter", reject: "Refuser", manage: "Gérer les préférences", more: "En savoir plus",
      essential: "Essentiels", essentialDesc: "Nécessaires au fonctionnement du site (session, sécurité). Toujours actifs.",
      analytics: "Analytics", analyticsDesc: "Nous aide à comprendre comment le site est utilisé.",
      marketing: "Marketing", marketingDesc: "Utilisé pour mesurer et personnaliser les publicités.",
      save: "Enregistrer les préférences"
    },
    de: {
      aria: "Cookie-Hinweis", prefsAria: "Cookie-Einstellungen verwalten",
      text: "Wir verwenden Cookies, um Ihre Erfahrung zu verbessern und die Nutzung der Website zu analysieren. Wenn Sie weitersurfen, stimmen Sie unserer ",
      privacy: "Datenschutzerklärung", accept: "Akzeptieren", reject: "Ablehnen", manage: "Einstellungen verwalten", more: "Mehr erfahren",
      essential: "Essenziell", essentialDesc: "Für den Betrieb der Website erforderlich (Sitzung, Sicherheit). Immer aktiv.",
      analytics: "Analytics", analyticsDesc: "Hilft uns zu verstehen, wie die Website genutzt wird.",
      marketing: "Marketing", marketingDesc: "Wird verwendet, um Werbung zu messen und zu personalisieren.",
      save: "Einstellungen speichern"
    },
    ru: {
      aria: "Уведомление о файлах cookie", prefsAria: "Управление настройками cookie",
      text: "Мы используем файлы cookie, чтобы улучшить работу сайта и анализировать его использование. Продолжая просмотр, вы соглашаетесь с нашей ",
      privacy: "Политикой конфиденциальности", accept: "Принять", reject: "Отклонить", manage: "Управлять настройками", more: "Подробнее",
      essential: "Необходимые", essentialDesc: "Необходимы для работы сайта (сессия, безопасность). Всегда активны.",
      analytics: "Аналитика", analyticsDesc: "Помогает понять, как используется сайт.",
      marketing: "Маркетинг", marketingDesc: "Используется для измерения и персонализации рекламы.",
      save: "Сохранить настройки"
    }
  };
  var copy = messages[language] || messages.pt;

  function readPreferences() {
    try {
      var raw = localStorage.getItem("vedium_cookie_preferences");
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function persistDecision(analytics, marketing) {
    try {
      localStorage.setItem("vedium_cookie_preferences", JSON.stringify({ analytics: analytics, marketing: marketing }));
      localStorage.setItem("vedium_cookie_consent", marketing ? "1" : "rejected");
    } catch (e) {}
    // Ordem importa: os eventos "genericos" (que o Meta Pixel e o handler
    // simples do consent-mode-v2.js escutam) disparam primeiro; o evento
    // granular "vedium:consent-preferences" dispara por ULTIMO, pra ter a
    // palavra final sobre os 4 sinais do Google quando a escolha for mista
    // (ex.: analytics=true, marketing=false -- sem isso, o handler generico
    // de "vedium:consent-rejected" negaria analytics_storage tambem).
    if (marketing) {
      try { window.dispatchEvent(new Event("vedium:consent")); } catch (e) {}
    } else {
      try { window.dispatchEvent(new Event("vedium:consent-rejected")); } catch (e) {}
    }
    try {
      window.dispatchEvent(new CustomEvent("vedium:consent-preferences", { detail: { analytics: analytics, marketing: marketing } }));
    } catch (e) {}
  }

  try {
    var saved = localStorage.getItem("vedium_cookie_consent");
    if (saved === "1" || saved === "accepted" || saved === "essential" || saved === "rejected") return;
  } catch (e) { return; }

  function injectStyles() {
    if (document.getElementById("vd-cookie-style")) return;
    var style = document.createElement("style");
    style.id = "vd-cookie-style";
    style.textContent = [
      "#vd-cookie-bar{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;background:#11161d;color:#fff;padding:16px 20px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:center;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.5;box-shadow:0 -2px 16px rgba(0,0,0,.3);}",
      "#vd-cookie-bar p{max-width:780px;margin:0;color:#fff;}",
      "#vd-cookie-bar a{color:#93c5fd;text-decoration:underline;}",
      "#vd-cookie-bar .vd-cookie-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;}",
      "#vd-cookie-bar button{background:#2E6DA4;color:#fff;border:none;padding:11px 24px;border-radius:8px;font-weight:700;cursor:pointer;font-size:14px;}",
      "#vd-cookie-bar button.vd-cookie-secondary{background:transparent;color:#cbd5e1;border:1px solid #475569;font-weight:600;}",
      "#vd-cookie-bar .vd-cookie-more{background:transparent;color:#cbd5e1;border:1px solid #475569;padding:10px 18px;border-radius:8px;font-weight:600;text-decoration:none;font-size:14px;}",
      "#vd-cookie-prefs{position:fixed;inset:0;z-index:2147483001;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;padding:16px;}",
      "#vd-cookie-prefs .vd-cookie-prefs-panel{background:#fff;color:#11161d;border-radius:12px;max-width:480px;width:100%;padding:24px;font-family:Arial,Helvetica,sans-serif;}",
      "#vd-cookie-prefs h2{margin:0 0 16px;font-size:18px;}",
      "#vd-cookie-prefs .vd-cookie-row{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;padding:12px 0;border-top:1px solid #e2e8f0;}",
      "#vd-cookie-prefs .vd-cookie-row:first-of-type{border-top:none;}",
      "#vd-cookie-prefs .vd-cookie-row strong{display:block;font-size:14px;}",
      "#vd-cookie-prefs .vd-cookie-row p{margin:4px 0 0;font-size:12px;color:#475569;}",
      "#vd-cookie-prefs .vd-cookie-prefs-actions{display:flex;justify-content:flex-end;gap:10px;margin-top:20px;}",
      "@media(max-width:767px){#vd-cookie-bar{top:12px;left:12px;right:12px;bottom:auto;border-radius:12px;padding:10px 12px;justify-content:flex-start;font-size:12px;line-height:1.35;box-shadow:0 10px 30px rgba(0,0,0,.22);}#vd-cookie-bar p{max-width:none;flex:1 1 100%;}#vd-cookie-bar .vd-cookie-actions{width:100%;justify-content:flex-end;}#vd-cookie-bar button,#vd-cookie-bar .vd-cookie-more{padding:8px 12px;font-size:12px;border-radius:7px;}}"
    ].join("");
    document.head.appendChild(style);
  }

  function closeBar(bar) {
    if (bar && bar.parentNode) bar.parentNode.removeChild(bar);
  }

  function showPreferencesPanel(bar) {
    var existing = readPreferences();
    var overlay = document.createElement("div");
    overlay.id = "vd-cookie-prefs";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-label", copy.prefsAria);
    overlay.innerHTML =
      '<div class="vd-cookie-prefs-panel">' +
      '<h2>' + copy.manage + '</h2>' +
      '<div class="vd-cookie-row"><div><strong>' + copy.essential + '</strong><p>' + copy.essentialDesc + '</p></div>' +
      '<input type="checkbox" checked disabled aria-label="' + copy.essential + '" /></div>' +
      '<div class="vd-cookie-row"><div><strong>' + copy.analytics + '</strong><p>' + copy.analyticsDesc + '</p></div>' +
      '<input type="checkbox" id="vd-cookie-pref-analytics" aria-label="' + copy.analytics + '"' +
      (existing && existing.analytics ? " checked" : "") + ' /></div>' +
      '<div class="vd-cookie-row"><div><strong>' + copy.marketing + '</strong><p>' + copy.marketingDesc + '</p></div>' +
      '<input type="checkbox" id="vd-cookie-pref-marketing" aria-label="' + copy.marketing + '"' +
      (existing && existing.marketing ? " checked" : "") + ' /></div>' +
      '<div class="vd-cookie-prefs-actions">' +
      '<button type="button" id="vd-cookie-prefs-save">' + copy.save + '</button>' +
      '</div></div>';
    document.body.appendChild(overlay);
    var saveBtn = document.getElementById("vd-cookie-prefs-save");
    if (saveBtn) saveBtn.addEventListener("click", function () {
      var analyticsChecked = document.getElementById("vd-cookie-pref-analytics").checked;
      var marketingChecked = document.getElementById("vd-cookie-pref-marketing").checked;
      persistDecision(analyticsChecked, marketingChecked);
      if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
      closeBar(bar);
    });
  }

  function show() {
    if (document.getElementById("vd-cookie-bar")) return;
    injectStyles();
    var bar = document.createElement("div");
    bar.id = "vd-cookie-bar";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-label", copy.aria);
    bar.innerHTML =
      '<p>' + copy.text +
      '<a href="/privacidade">' + copy.privacy + '</a>.</p>' +
      '<span class="vd-cookie-actions">' +
      '<button id="vd-cookie-ok" type="button">' + copy.accept + '</button>' +
      '<button id="vd-cookie-reject" class="vd-cookie-secondary" type="button">' + copy.reject + '</button>' +
      '<button id="vd-cookie-manage" class="vd-cookie-secondary" type="button">' + copy.manage + '</button>' +
      '<a class="vd-cookie-more" href="/privacidade">' + copy.more + '</a>' +
      '</span>';
    document.body.appendChild(bar);

    var acceptBtn = document.getElementById("vd-cookie-ok");
    if (acceptBtn) acceptBtn.addEventListener("click", function () {
      persistDecision(true, true);
      closeBar(bar);
    });

    var rejectBtn = document.getElementById("vd-cookie-reject");
    if (rejectBtn) rejectBtn.addEventListener("click", function () {
      persistDecision(false, false);
      closeBar(bar);
    });

    var manageBtn = document.getElementById("vd-cookie-manage");
    if (manageBtn) manageBtn.addEventListener("click", function () {
      showPreferencesPanel(bar);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", show);
  } else {
    show();
  }
})();
