(function () {
  var localeMeta = {
    "pt-br": { lang: "pt", prefix: "/pt-br/", flag: "https://flagcdn.com/w20/br.png", flag2x: "https://flagcdn.com/w40/br.png 2x", alt: "Brazil", label: "BRASIL | PORTUGUÊS" },
    "en": { lang: "en", prefix: "/en/", flag: "https://flagcdn.com/w20/un.png", flag2x: "https://flagcdn.com/w40/un.png 2x", alt: "Global", label: "GLOBAL | ENGLISH" },
    "en-us": { lang: "en", prefix: "/en-us/", flag: "https://flagcdn.com/w20/us.png", flag2x: "https://flagcdn.com/w40/us.png 2x", alt: "United States", label: "UNITED STATES | ENGLISH" },
    "es-ar": { lang: "es", prefix: "/es-ar/", flag: "https://flagcdn.com/w20/ar.png", flag2x: "https://flagcdn.com/w40/ar.png 2x", alt: "Argentina", label: "ARGENTINA | ESPAÑOL" },
    "fr-ca": { lang: "fr", prefix: "/fr-ca/", flag: "https://flagcdn.com/w20/ca.png", flag2x: "https://flagcdn.com/w40/ca.png 2x", alt: "Canada", label: "CANADA | FRANÇAIS" },
    "es-co": { lang: "es", prefix: "/es-co/", flag: "https://flagcdn.com/w20/co.png", flag2x: "https://flagcdn.com/w40/co.png 2x", alt: "Colombia", label: "COLOMBIA | ESPAÑOL" },
    "fr": { lang: "fr", prefix: "/fr/", flag: "https://flagcdn.com/w20/fr.png", flag2x: "https://flagcdn.com/w40/fr.png 2x", alt: "France", label: "FRANCE | FRANÇAIS" },
    "de": { lang: "de", prefix: "/de/", flag: "https://flagcdn.com/w20/de.png", flag2x: "https://flagcdn.com/w40/de.png 2x", alt: "Germany", label: "DACH REGION | DEUTSCH" },
    "es": { lang: "es", prefix: "/es/", flag: "https://flagcdn.com/w20/es.png", flag2x: "https://flagcdn.com/w40/es.png 2x", alt: "Spain", label: "SPAIN | ESPAÑOL" },
    "ru": { lang: "ru", prefix: "/ru/", flag: "https://flagcdn.com/w20/ru.png", flag2x: "https://flagcdn.com/w40/ru.png 2x", alt: "Russia", label: "RUSSIA | РУССКИЙ" },
    "zh-cn": { lang: "zh-CN", prefix: "/zh-cn/", flag: "https://flagcdn.com/w20/cn.png", flag2x: "https://flagcdn.com/w40/cn.png 2x", alt: "China", label: "CHINA | 中文" },
    "en-au": { lang: "en", prefix: "/en-au/", flag: "https://flagcdn.com/w20/au.png", flag2x: "https://flagcdn.com/w40/au.png 2x", alt: "Australia", label: "AUSTRALIA | ENGLISH" }
  };
  var supported = Object.keys(localeMeta).map(function (locale) { return localeMeta[locale].lang; })
    .filter(function (lang, index, all) { return all.indexOf(lang) === index; });
  var browserMap = {
    pt: "pt-br",
    "pt-br": "pt-br",
    en: "en-us",
    "en-us": "en-us",
    es: "es",
    "es-ar": "es-ar",
    fr: "fr",
    "fr-ca": "fr-ca",
    de: "de",
    ru: "ru",
    zh: "zh-cn",
    "zh-cn": "zh-cn",
    "zh-hans": "zh-cn"
  };
  var storageKey = "vedium_preferred_locale";
  var cookieName = "googtrans";

  function normalize(lang) {
    if (!lang) return "pt-br";
    var value = String(lang).toLowerCase();
    if (browserMap[value]) return browserMap[value];
    var root = value.split("-")[0];
    return browserMap[root] || "pt-br";
  }

  function setCookie(locale) {
    var meta = localeMeta[locale] || localeMeta["pt-br"];
    var cookieValue = meta.lang === "pt" ? "/pt/pt" : "/pt/" + meta.lang;
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
    return match ? normalize(decodeURIComponent(match[1])) : "pt-br";
  }

  function getLocaleFromPath() {
    var firstSegment = location.pathname.split("/").filter(Boolean)[0];
    return localeMeta[firstSegment] ? firstSegment : "";
  }

  function stripLocalePrefix(pathname) {
    var parts = pathname.split("/").filter(Boolean);
    if (parts.length && localeMeta[parts[0]]) {
      parts.shift();
    }
    return "/" + parts.join("/");
  }

  function buildLocaleUrl(locale) {
    var meta = localeMeta[locale] || localeMeta["pt-br"];
    var cleanPath = stripLocalePrefix(location.pathname);
    var path = cleanPath === "/" ? meta.prefix : meta.prefix + cleanPath.replace(/^\//, "");
    return path.replace(/\/{2,}/g, "/") + location.search + location.hash;
  }

  function markActive(locale) {
    var meta = localeMeta[locale] || localeMeta["pt-br"];
    document.querySelectorAll("[data-vd-locale]").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-vd-locale") === locale);
    });
    document.querySelectorAll("[data-vd-current-flag]").forEach(function (node) {
      if (node.tagName && node.tagName.toLowerCase() === "img") {
        node.src = meta.flag;
        node.srcset = meta.flag2x;
        node.alt = meta.alt;
      } else {
        node.textContent = meta.alt;
      }
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

  function selectLocale(locale) {
    var meta = localeMeta[locale];
    if (!meta) return;
    setCookie(locale);
    localStorage.setItem(storageKey, locale);
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: "language_selected", language: meta.lang, locale: locale });
    markActive(locale);
    setModalOpen(false);
    window.location.assign(buildLocaleUrl(locale));
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

    document.querySelectorAll("[data-vd-locale]").forEach(function (button) {
      button.addEventListener("click", function () {
        selectLocale(button.getAttribute("data-vd-locale"));
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

    var current = getLocaleFromPath() || localStorage.getItem(storageKey) || getCurrentLang();
    if (!getLocaleFromPath() && !localStorage.getItem(storageKey)) {
      current = normalize(navigator.language || (navigator.languages && navigator.languages[0]));
    }
    markActive(current);
    if (getLocaleFromPath() && localeMeta[current] && localeMeta[current].lang !== "pt") {
      setCookie(current);
      loadGoogleTranslate();
    }
  });
}());
