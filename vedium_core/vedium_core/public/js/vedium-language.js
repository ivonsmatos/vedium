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
  var localeCopy = {
    en: {
      "Início": "Home",
      "Como funciona": "How it works",
      "Sobre": "About",
      "Cursos": "Courses",
      "FAQ": "FAQ",
      "Contato": "Contact",
      "Entrar": "Log in",
      "Registrar": "Sign up",
      "Teste grátis": "Free test",
      "Fale conosco": "Contact us",
      "Select your region and language": "Select your region and language",
      "Links Úteis": "Useful links",
      "Sobre Nós": "About us",
      "Nossos Cursos": "Our courses",
      "Trabalhe Conosco": "Work with us",
      "Termos": "Terms",
      "Privacidade": "Privacy",
      "Brasil — Atendimento 100% Online": "Brazil — 100% online service",
      "Fazer teste de nível grátis": "Take the free placement test",
      "Falar no WhatsApp": "Talk on WhatsApp",
      "Fluência além das palavras": "Fluency beyond words",
      "Acelere sua Fluência": "Accelerate your fluency",
      "Aulas ao vivo de Inglês e Iorubá, com professores qualificados e foco na sua fluência.": "Live English and Yoruba classes with qualified teachers focused on real fluency.",
      "Professores Nativos": "Native teachers",
      "Aprenda no seu ritmo": "Learn at your own pace",
      "Método que Transforma": "A method that transforms",
      "Aulas ao vivo, exercícios interativos e imersão cultural com professores nativos certificados.": "Live classes, interactive practice and cultural immersion with qualified teachers.",
      "Método Exclusivo": "Exclusive method",
      "Sem fronteiras linguísticas": "No language borders",
      "Conecte-se ao Mundo": "Connect with the world",
      "Inglês e Iorubá — aprenda ao vivo, de onde estiver, com professores de verdade.": "English and Yoruba — learn live, wherever you are, with real teachers.",
      "Aulas ao Vivo": "Live classes",
      "Por que Vedium?": "Why Vedium?",
      "Benefícios de Aprender com a Gente": "Benefits of learning with us",
      "Na Vedium você aprende com aulas ao vivo, turmas pequenas e professores que acompanham a sua evolução de perto — do primeiro contato com o idioma até a fluência.": "At Vedium, you learn through live classes, small groups and teachers who follow your progress closely, from your first contact with the language to fluency.",
      "Aprenda com professores que dominam o idioma": "Learn with teachers who master the language",
      "Aulas 100% ao vivo e online": "100% live online classes",
      "Materiais e exercícios incluídos": "Materials and exercises included",
      "Certificado de conclusão a cada nível": "Completion certificate for each level",
      "Aulas ao vivo, do seu jeito": "Live classes, your way",
      "Do nosso blog": "From our blog",
      "Dicas e Conteúdo": "Tips and content",
      "Conteúdo da trilha": "Program content",
      "O que você vai aprender": "What you will learn",
      "Diagnóstico da necessidade": "Needs diagnosis",
      "Método Vedium": "Vedium method",
      "Como funciona na prática": "How it works in practice",
      "Formato": "Format",
      "O que esperar das aulas": "What to expect from classes",
      "Dúvidas comuns": "Common questions",
      "Perguntas frequentes": "Frequently asked questions",
      "Comece sem compromisso": "Start with no commitment",
      "Descubra seu nível antes de escolher o plano": "Find your level before choosing a plan"
    },
    es: {
      "Início": "Inicio",
      "Como funciona": "Cómo funciona",
      "Sobre": "Acerca de",
      "Cursos": "Cursos",
      "FAQ": "FAQ",
      "Contato": "Contacto",
      "Entrar": "Entrar",
      "Registrar": "Registrarse",
      "Teste grátis": "Prueba gratis",
      "Fale conosco": "Contáctanos",
      "Links Úteis": "Enlaces útiles",
      "Sobre Nós": "Sobre nosotros",
      "Nossos Cursos": "Nuestros cursos",
      "Trabalhe Conosco": "Trabaja con nosotros",
      "Termos": "Términos",
      "Privacidade": "Privacidad",
      "Brasil — Atendimento 100% Online": "Brasil — Atención 100% online",
      "Fazer teste de nível grátis": "Hacer prueba de nivel gratis",
      "Falar no WhatsApp": "Hablar por WhatsApp",
      "Fluência além das palavras": "Fluidez más allá de las palabras",
      "Acelere sua Fluência": "Acelera tu fluidez",
      "Aulas ao vivo de Inglês e Iorubá, com professores qualificados e foco na sua fluência.": "Clases en vivo de inglés y yoruba con profesores calificados y foco en tu fluidez.",
      "Professores Nativos": "Profesores nativos",
      "Aprenda no seu ritmo": "Aprende a tu ritmo",
      "Método que Transforma": "Método que transforma",
      "Aulas ao vivo, exercícios interativos e imersão cultural com professores nativos certificados.": "Clases en vivo, ejercicios interactivos e inmersión cultural con profesores calificados.",
      "Método Exclusivo": "Método exclusivo",
      "Sem fronteiras linguísticas": "Sin fronteras lingüísticas",
      "Conecte-se ao Mundo": "Conéctate con el mundo",
      "Inglês e Iorubá — aprenda ao vivo, de onde estiver, com professores de verdade.": "Inglés y yoruba — aprende en vivo, estés donde estés, con profesores reales.",
      "Aulas ao Vivo": "Clases en vivo",
      "Por que Vedium?": "¿Por qué Vedium?",
      "Benefícios de Aprender com a Gente": "Beneficios de aprender con nosotros",
      "Aulas 100% ao vivo e online": "Clases 100% en vivo y online",
      "Materiais e exercícios incluídos": "Materiales y ejercicios incluidos",
      "Certificado de conclusão a cada nível": "Certificado de finalización por nivel",
      "Dicas e Conteúdo": "Consejos y contenido",
      "O que você vai aprender": "Lo que vas a aprender",
      "Perguntas frequentes": "Preguntas frecuentes"
    },
    fr: {
      "Início": "Accueil",
      "Como funciona": "Fonctionnement",
      "Sobre": "À propos",
      "Cursos": "Cours",
      "FAQ": "FAQ",
      "Contato": "Contact",
      "Entrar": "Connexion",
      "Registrar": "S'inscrire",
      "Teste grátis": "Test gratuit",
      "Fale conosco": "Contactez-nous",
      "Fazer teste de nível grátis": "Faire le test de niveau gratuit",
      "Falar no WhatsApp": "Parler sur WhatsApp",
      "Acelere sua Fluência": "Accélérez votre aisance",
      "Fluência além das palavras": "L'aisance au-delà des mots",
      "O que você vai aprender": "Ce que vous allez apprendre",
      "Perguntas frequentes": "Questions fréquentes"
    },
    de: {
      "Início": "Start",
      "Como funciona": "So funktioniert es",
      "Sobre": "Über uns",
      "Cursos": "Kurse",
      "FAQ": "FAQ",
      "Contato": "Kontakt",
      "Entrar": "Einloggen",
      "Registrar": "Registrieren",
      "Teste grátis": "Gratis-Test",
      "Fale conosco": "Kontakt",
      "Fazer teste de nível grátis": "Kostenlosen Einstufungstest machen",
      "Falar no WhatsApp": "Über WhatsApp sprechen",
      "Acelere sua Fluência": "Beschleunigen Sie Ihre Sprachkompetenz",
      "Fluência além das palavras": "Sprachkompetenz über Wörter hinaus",
      "O que você vai aprender": "Was Sie lernen werden",
      "Perguntas frequentes": "Häufige Fragen"
    },
    ru: {
      "Início": "Главная",
      "Como funciona": "Как это работает",
      "Sobre": "О нас",
      "Cursos": "Курсы",
      "FAQ": "FAQ",
      "Contato": "Контакты",
      "Entrar": "Войти",
      "Registrar": "Регистрация",
      "Teste grátis": "Бесплатный тест",
      "Fale conosco": "Свяжитесь с нами",
      "Fazer teste de nível grátis": "Пройти бесплатный тест уровня",
      "Falar no WhatsApp": "Написать в WhatsApp",
      "Acelere sua Fluência": "Ускорьте свою беглость",
      "O que você vai aprender": "Что вы изучите",
      "Perguntas frequentes": "Частые вопросы"
    },
    "zh-CN": {
      "Início": "首页",
      "Como funciona": "如何运作",
      "Sobre": "关于我们",
      "Cursos": "课程",
      "FAQ": "常见问题",
      "Contato": "联系",
      "Entrar": "登录",
      "Registrar": "注册",
      "Teste grátis": "免费测试",
      "Fale conosco": "联系我们",
      "Fazer teste de nível grátis": "参加免费水平测试",
      "Falar no WhatsApp": "通过 WhatsApp 联系",
      "Acelere sua Fluência": "提升你的流利度",
      "O que você vai aprender": "你将学习什么",
      "Perguntas frequentes": "常见问题"
    }
  };

  function clearLegacyTranslateCookie() {
    ["googtrans", "googtransopt"].forEach(function (name) {
      document.cookie = name + "=;path=/;max-age=0;SameSite=Lax";
      if (location.hostname.indexOf(".") > -1) {
        document.cookie = name + "=;path=/;domain=." + location.hostname.replace(/^www\./, "") + ";max-age=0;SameSite=Lax";
      }
    });
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

  function updateLocaleLinks() {
    var cleanPath = stripLocalePrefix(location.pathname);
    document.querySelectorAll("[data-vd-locale]").forEach(function (link) {
      var locale = link.getAttribute("data-vd-locale");
      var meta = localeMeta[locale];
      if (!meta || !link.setAttribute) return;
      var path = cleanPath === "/" ? meta.prefix : meta.prefix + cleanPath.replace(/^\//, "");
      link.setAttribute("href", path.replace(/\/{2,}/g, "/") + location.search + location.hash);
    });
  }

  function normalizedText(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function translateTextNodes(lang) {
    var copy = localeCopy[lang];
    if (!copy) return;
    var skip = "SCRIPT,STYLE,NOSCRIPT,IFRAME,SVG";
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || !normalizedText(node.nodeValue)) return NodeFilter.FILTER_REJECT;
        if (node.parentElement && node.parentElement.closest(skip)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var node;
    while ((node = walker.nextNode())) {
      var original = normalizedText(node.nodeValue);
      if (copy[original]) {
        node.nodeValue = node.nodeValue.replace(original, copy[original]);
      }
    }
  }

  function localizePage(locale) {
    var meta = localeMeta[locale] || localeMeta["pt-br"];
    document.documentElement.lang = meta.lang === "zh-CN" ? "zh-CN" : meta.lang;
    if (meta.lang !== "pt") {
      translateTextNodes(meta.lang);
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: "language_selected", language: meta.lang, locale: locale });
    }
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

  document.addEventListener("DOMContentLoaded", function () {
    clearLegacyTranslateCookie();
    updateLocaleLinks();

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

    var current = getLocaleFromPath() || "pt-br";
    markActive(current);
    localizePage(current);
  });
}());
