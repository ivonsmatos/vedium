(function () {
  var supported = ["pt", "en", "es", "fr", "de", "ru", "zh-CN"];
  var languageMeta = {
    pt: { flag: "🇧🇷", label: "BRASIL | PORTUGUÊS" },
    en: { flag: "🇺🇸", label: "UNITED STATES | ENGLISH" },
    es: { flag: "🇪🇸", label: "SPAIN | ESPAÑOL" },
    fr: { flag: "🇫🇷", label: "FRANCE | FRANÇAIS" },
    de: { flag: "🇩🇪", label: "DACH REGION | DEUTSCH" },
    ru: { flag: "🇷🇺", label: "RUSSIA | РУССКИЙ" },
    "zh-CN": { flag: "🇨🇳", label: "CHINA | 中文" }
  };
  var browserMap = {
    pt: "pt",
    en: "en",
    es: "es",
    fr: "fr",
    de: "de",
    ru: "ru",
    zh: "zh-CN",
    "zh-cn": "zh-CN",
    "zh-hans": "zh-CN"
  };
  var storageKey = "vedium_preferred_language";
  var cookieName = "googtrans";

  function normalize(lang) {
    if (!lang) return "pt";
    var value = String(lang).toLowerCase();
    if (browserMap[value]) return browserMap[value];
    var root = value.split("-")[0];
    return browserMap[root] || "pt";
  }

  function setCookie(lang) {
    var cookieValue = lang === "pt" ? "/pt/pt" : "/pt/" + lang;
    var maxAge = 60 * 60 * 24 * 365;
    document.cookie = cookieName + "=" + cookieValue + ";path=/;max-age=" + maxAge + ";SameSite=Lax";
    if (location.hostname.indexOf(".") > -1) {
      document.cookie = cookieName + "=" + cookieValue + ";path=/;domain=." + location.hostname.replace(/^www\./, "") + ";max-age=" + maxAge + ";SameSite=Lax";
    }
  }

  function loadGoogleTranslate() {
    if (document.querySelector('script[src*="translate_a/element.js"]')) return;
    var script = document.createElement("script");
    script.src = "https://translate.google.com/translate_a/element.js?cb=vediumInitGoogleTranslate";
    script.async = true;
    document.head.appendChild(script);
  }

  function getCurrentLang() {
    var preferred = localStorage.getItem(storageKey);
    if (preferred) return preferred;
    var match = document.cookie.match(/(?:^|;\s*)googtrans=\/pt\/([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "pt";
  }

  function markActive(lang) {
    var meta = languageMeta[lang] || languageMeta.pt;
    document.querySelectorAll("[data-vd-lang]").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-vd-lang") === lang);
    });
    document.querySelectorAll("[data-vd-current-flag]").forEach(function (node) {
      node.textContent = meta.flag;
    });
    document.querySelectorAll("[data-vd-current-label]").forEach(function (node) {
      node.textContent = meta.label;
    });
  }

  function setModalOpen(open) {
    var modal = document.querySelector("[data-vd-language-modal]");
    var openButtons = document.querySelectorAll("[data-vd-language-open]");
    if (!modal) return;
    modal.hidden = !open;
    document.body.classList.toggle("vedium-language-modal-open", open);
    openButtons.forEach(function (button) {
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  function switchLanguage(lang, userSelected) {
    if (supported.indexOf(lang) === -1) return;
    setCookie(lang);
    localStorage.setItem(storageKey, lang);
    if (userSelected) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: "language_selected", language: lang });
    }
    markActive(lang);
    if (lang === "pt") {
      window.location.reload();
      return;
    }
    loadGoogleTranslate();
  }

  window.vediumInitGoogleTranslate = function () {
    if (!window.google || !google.translate || !document.getElementById("google_translate_element")) return;
    new google.translate.TranslateElement({
      pageLanguage: "pt",
      includedLanguages: supported.join(","),
      autoDisplay: false
    }, "google_translate_element");
  };

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-vd-language-open]").forEach(function (button) {
      button.addEventListener("click", function () {
        setModalOpen(true);
      });
    });

    document.querySelectorAll("[data-vd-language-close]").forEach(function (button) {
      button.addEventListener("click", function () {
        setModalOpen(false);
      });
    });

    document.querySelectorAll("[data-vd-lang]").forEach(function (button) {
      button.addEventListener("click", function () {
        switchLanguage(button.getAttribute("data-vd-lang"), true);
      });
    });

    document.addEventListener("click", function (event) {
      var target = event.target && event.target.closest ? event.target : event.target.parentElement;
      var link = target && target.closest ? target.closest('a[href*="wa.me/"], a[href*="api.whatsapp.com/"]') : null;
      if (!link) return;
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: "public_cta_click", location: link.getAttribute("data-vd-location") || "whatsapp_link", cta: "whatsapp" });
      if (window.matchMedia("(hover: none)").matches || window.innerWidth <= 768) {
        event.preventDefault();
        window.location.href = link.href;
      }
    }, true);

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setModalOpen(false);
    });

    var current = localStorage.getItem(storageKey) || getCurrentLang();
    if (!localStorage.getItem(storageKey)) {
      current = normalize(navigator.language || (navigator.languages && navigator.languages[0]));
    }
    markActive(current);
    if (localStorage.getItem(storageKey) && current !== "pt") {
      loadGoogleTranslate();
    }
  });
}());
