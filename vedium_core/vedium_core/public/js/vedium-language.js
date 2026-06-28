(function () {
  var supported = ["pt", "en", "es", "fr", "de", "ru", "zh-CN"];
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
  var autoKey = "vedium_language_autodetected";
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

  function getCurrentLang() {
    var preferred = localStorage.getItem(storageKey);
    if (preferred) return preferred;
    var match = document.cookie.match(/(?:^|;\s*)googtrans=\/pt\/([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "pt";
  }

  function markActive(lang) {
    document.querySelectorAll("[data-vd-lang]").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-vd-lang") === lang);
    });
  }

  function switchLanguage(lang, userSelected) {
    if (supported.indexOf(lang) === -1) return;
    setCookie(lang);
    localStorage.setItem(storageKey, lang);
    if (userSelected) {
      localStorage.setItem(autoKey, "1");
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: "language_selected", language: lang });
    }
    markActive(lang);
    window.location.reload();
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
    document.querySelectorAll("[data-vd-lang]").forEach(function (button) {
      button.addEventListener("click", function () {
        switchLanguage(button.getAttribute("data-vd-lang"), true);
      });
    });

    var current = getCurrentLang();
    markActive(current);

    if (!localStorage.getItem(autoKey) && !localStorage.getItem(storageKey)) {
      var detected = normalize(navigator.language || (navigator.languages && navigator.languages[0]));
      localStorage.setItem(autoKey, "1");
      if (detected !== "pt") {
        switchLanguage(detected, false);
        return;
      }
    }

    if (!document.querySelector('script[src*="translate_a/element.js"]')) {
      var script = document.createElement("script");
      script.src = "https://translate.google.com/translate_a/element.js?cb=vediumInitGoogleTranslate";
      script.async = true;
      document.head.appendChild(script);
    }
  });
}());
