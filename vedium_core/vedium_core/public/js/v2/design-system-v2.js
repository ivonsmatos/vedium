/*
 * VEDIUM DESIGN SYSTEM V2 -- JS progressivo (vanilla, sem jQuery/dependencia
 * nova). So roda dentro de .v2-scope. Isolado -- nao e incluido em
 * web_include_js, so carregado explicitamente pela pagina de preview.
 *
 * Cobre: menu mobile do Header v2, accordion do FAQ, modal base, e o
 * padrao tablist acessivel do LevelJourney (Fase B.3).
 * Tudo funciona sem JS (menu mobile fica sempre visivel sem JS -- ver
 * fallback <noscript> no macro do header; FAQ sem JS mostra todas as
 * respostas abertas via <details>/<summary> nativo; LevelJourney sem JS
 * mostra todos os paineis empilhados -- ver nota no macro v2_level_journey).
 */
(function () {
  "use strict";

  function onReady(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function initHeaderMenu(scope) {
    scope.querySelectorAll("[data-v2-header]").forEach(function (header) {
      var burger = header.querySelector("[data-v2-burger]");
      if (!burger) return;
      burger.addEventListener("click", function () {
        var open = header.getAttribute("data-menu-open") === "true";
        header.setAttribute("data-menu-open", open ? "false" : "true");
        burger.setAttribute("aria-expanded", open ? "false" : "true");
      });

      // Mega menu acessivel por teclado/touch (hover ja cobre desktop via CSS).
      header.querySelectorAll("[data-v2-mega-trigger]").forEach(function (trigger) {
        trigger.addEventListener("click", function (event) {
          var item = trigger.closest("[data-v2-nav-item]");
          if (!item) return;
          var mega = item.querySelector("[data-v2-mega]");
          if (!mega) return;
          // Em telas com hover real, deixa o CSS (:hover) resolver; so
          // intercepta o click quando o dispositivo não tem hover (touch).
          if (window.matchMedia && window.matchMedia("(hover: hover)").matches) return;
          event.preventDefault();
          var isOpen = item.getAttribute("data-mega-open") === "true";
          header.querySelectorAll("[data-v2-nav-item]").forEach(function (i) {
            i.setAttribute("data-mega-open", "false");
          });
          item.setAttribute("data-mega-open", isOpen ? "false" : "true");
        });
      });

      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
          header.setAttribute("data-menu-open", "false");
          if (burger) burger.setAttribute("aria-expanded", "false");
        }
      });
    });
  }

  function setFaqPanelHeight(panel) {
    var inner = panel.querySelector("[data-v2-faq-inner]");
    if (!inner) return;
    panel.style.setProperty("--v2-faq-panel-height", inner.scrollHeight + "px");
  }

  function initFaqAccordion(scope) {
    scope.querySelectorAll("[data-v2-faq]").forEach(function (faq) {
      var allowMultiple = faq.getAttribute("data-allow-multiple") === "true";
      faq.querySelectorAll("[data-v2-faq-trigger]").forEach(function (trigger) {
        var panelId = trigger.getAttribute("aria-controls");
        var panel = panelId ? document.getElementById(panelId) : null;
        if (!panel) return;

        trigger.addEventListener("click", function () {
          var isOpen = trigger.getAttribute("aria-expanded") === "true";

          if (!allowMultiple) {
            faq.querySelectorAll("[data-v2-faq-trigger]").forEach(function (otherTrigger) {
              if (otherTrigger === trigger) return;
              var otherPanelId = otherTrigger.getAttribute("aria-controls");
              var otherPanel = otherPanelId ? document.getElementById(otherPanelId) : null;
              otherTrigger.setAttribute("aria-expanded", "false");
              if (otherPanel) otherPanel.setAttribute("data-open", "false");
            });
          }

          trigger.setAttribute("aria-expanded", isOpen ? "false" : "true");
          if (!isOpen) setFaqPanelHeight(panel);
          panel.setAttribute("data-open", isOpen ? "false" : "true");
        });
      });
    });

    // Recalcula altura ao redimensionar (texto pode quebrar em mais linhas
    // em telas estreitas ou com fontes de idiomas mais largas).
    var resizeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        scope.querySelectorAll('[data-v2-faq-panel][data-open="true"]').forEach(setFaqPanelHeight);
      }, 150);
    });
  }

  function trapFocus(modal, event) {
    var focusable = modal.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable.length) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function initModals(scope) {
    var lastTrigger = null;

    function openModal(overlay) {
      lastTrigger = document.activeElement;
      overlay.hidden = false;
      var modal = overlay.querySelector("[data-v2-modal]");
      var focusable = modal ? modal.querySelector("a[href], button, input, select, textarea") : null;
      if (focusable) focusable.focus();
    }

    function closeModal(overlay) {
      overlay.hidden = true;
      if (lastTrigger) lastTrigger.focus();
    }

    scope.querySelectorAll("[data-v2-modal-trigger]").forEach(function (trigger) {
      var targetId = trigger.getAttribute("data-v2-modal-trigger");
      var overlay = document.getElementById(targetId);
      if (!overlay) return;
      trigger.addEventListener("click", function () {
        openModal(overlay);
      });
    });

    scope.querySelectorAll("[data-v2-modal-overlay]").forEach(function (overlay) {
      overlay.addEventListener("click", function (event) {
        if (event.target === overlay) closeModal(overlay);
      });
      overlay.querySelectorAll("[data-v2-modal-close]").forEach(function (closeBtn) {
        closeBtn.addEventListener("click", function () {
          closeModal(overlay);
        });
      });
      overlay.addEventListener("keydown", function (event) {
        if (event.key === "Escape") closeModal(overlay);
        if (event.key === "Tab") trapFocus(overlay, event);
      });
    });
  }

  /*
   * LevelJourney (Fase B.3) -- padrao tablist ARIA com "ativacao automatica"
   * (setas movem foco E trocam o painel, igual ao padrao WAI-ARIA Authoring
   * Practices para tabs). Sem JS, todo painel fica visivel (fallback
   * seguro definido no macro); aqui o JS confirma que rodou escondendo os
   * paineis que nao sao o selecionado.
   */
  function initLevelJourney(scope) {
    scope.querySelectorAll("[data-v2-journey]").forEach(function (timeline) {
      var tabs = Array.prototype.slice.call(timeline.querySelectorAll("[data-v2-journey-tab]"));
      if (!tabs.length) return;
      var container = timeline.parentElement;
      if (!container) return;
      var panels = Array.prototype.slice.call(container.querySelectorAll("[data-v2-journey-panel]"));

      function selectTab(tab, moveFocus) {
        tabs.forEach(function (t) {
          var selected = t === tab;
          t.setAttribute("aria-selected", selected ? "true" : "false");
          t.setAttribute("tabindex", selected ? "0" : "-1");
        });
        panels.forEach(function (panel) {
          var isTarget = panel.id === tab.getAttribute("aria-controls");
          if (isTarget) panel.removeAttribute("hidden");
          else panel.setAttribute("hidden", "");
        });
        if (moveFocus) tab.focus();
      }

      tabs.forEach(function (tab, index) {
        tab.addEventListener("click", function () {
          selectTab(tab, false);
        });
        tab.addEventListener("keydown", function (event) {
          var targetIndex = null;
          if (event.key === "ArrowRight" || event.key === "ArrowDown") targetIndex = (index + 1) % tabs.length;
          else if (event.key === "ArrowLeft" || event.key === "ArrowUp") targetIndex = (index - 1 + tabs.length) % tabs.length;
          else if (event.key === "Home") targetIndex = 0;
          else if (event.key === "End") targetIndex = tabs.length - 1;
          if (targetIndex === null) return;
          event.preventDefault();
          selectTab(tabs[targetIndex], true);
        });
      });

      // Confirma que o JS rodou: esconde os paineis marcados como nao-atuais
      // pelo macro (data-v2-journey-hidden) -- ate aqui, todos ficavam
      // visiveis (fallback sem JS).
      panels.forEach(function (panel) {
        if (panel.hasAttribute("data-v2-journey-hidden")) panel.setAttribute("hidden", "");
      });
    });
  }

  /*
   * HeroEditorialCarousel (Fase B.6A, hero full-bleed inspirado no
   * Bain.com) -- autoplay com pausa (hover/foco/aba oculta/prefers-reduced-
   * motion), troca de slide, barra de progresso por tab, Ken Burns
   * reiniciado a cada slide. Sem JS, o CSS ja deixa so o slide 1 visivel
   * (ver nota no macro v2_hero_editorial_carousel) -- este script so
   * adiciona a rotacao automatica e a navegacao manual por cima disso.
   */
  function initHeroCarousel(scope) {
    scope.querySelectorAll("[data-v2-hero-carousel]").forEach(function (hero) {
      var slides = Array.prototype.slice.call(hero.querySelectorAll(".v2-editorial-hero__slide"));
      var tabs = Array.prototype.slice.call(hero.querySelectorAll("[data-v2-hero-tab]"));
      if (!slides.length || !tabs.length) return;

      var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var autoplayMs = parseFloat(getComputedStyle(hero).getPropertyValue("--v2-hero-autoplay")) * 1000 || 9000;
      var current = 0;
      var timer = null;
      var paused = false;

      function restartDrift(slide) {
        var img = slide.querySelector(".v2-editorial-hero__media img");
        if (!img) return;
        img.style.animation = "none";
        // eslint-disable-next-line no-unused-expressions
        img.offsetWidth; // força reflow -- reinicia a animacao no proximo frame
        img.style.animation = "";
      }

      function goTo(index) {
        if (index === current) return;
        var prevSlide = slides[current];
        var prevTab = tabs[current];
        current = (index + slides.length) % slides.length;
        var nextSlide = slides[current];
        var nextTab = tabs[current];

        prevSlide.classList.remove("is-active");
        prevSlide.setAttribute("aria-hidden", "true");
        prevTab.classList.remove("is-active");
        prevTab.setAttribute("aria-selected", "false");
        prevTab.setAttribute("tabindex", "-1");

        nextSlide.classList.add("is-active");
        nextSlide.removeAttribute("aria-hidden");
        nextTab.classList.add("is-active");
        nextTab.setAttribute("aria-selected", "true");
        nextTab.setAttribute("tabindex", "0");

        if (!reducedMotion) restartDrift(nextSlide);
      }

      function scheduleNext() {
        clearTimeout(timer);
        if (reducedMotion || paused) return;
        timer = setTimeout(function () {
          goTo(current + 1);
          scheduleNext();
        }, autoplayMs);
      }

      tabs.forEach(function (tab, index) {
        tab.addEventListener("click", function () {
          goTo(index);
          scheduleNext();
        });
        tab.addEventListener("keydown", function (event) {
          var targetIndex = null;
          if (event.key === "ArrowRight") targetIndex = (index + 1) % tabs.length;
          else if (event.key === "ArrowLeft") targetIndex = (index - 1 + tabs.length) % tabs.length;
          else if (event.key === "Home") targetIndex = 0;
          else if (event.key === "End") targetIndex = tabs.length - 1;
          if (targetIndex === null) return;
          event.preventDefault();
          tabs[targetIndex].focus();
          goTo(targetIndex);
          scheduleNext();
        });
      });

      function pause() {
        paused = true;
        clearTimeout(timer);
      }
      function resume() {
        if (!paused) return;
        paused = false;
        scheduleNext();
      }

      hero.addEventListener("mouseenter", pause);
      hero.addEventListener("mouseleave", resume);
      hero.addEventListener("focusin", pause);
      hero.addEventListener("focusout", function (event) {
        if (!hero.contains(event.relatedTarget)) resume();
      });
      document.addEventListener("visibilitychange", function () {
        if (document.hidden) pause();
        else resume();
      });

      if (!reducedMotion) scheduleNext();
    });
  }

  /*
   * Header overlay (Fase B.6A) -- fixed sobre o Hero, transparente ate a
   * base do Hero cruzar a base do header durante o scroll; a partir dali
   * ganha fundo solido ("is-solid") pra continuar legivel sobre o resto da
   * Home. rAF-throttled, sem biblioteca de scroll.
   */
  function initHeaderOverlay(scope) {
    var wrap = scope.querySelector("[data-v2-header-overlay]");
    var hero = scope.querySelector(".v2-editorial-hero");
    if (!wrap || !hero) return;

    /*
     * A ferramenta de preview tem sua propria barra fixa/sticky no topo
     * (.dstool-banner sempre, .dstool-toc so em debug mode) -- FORA de
     * .v2-scope, nunca existe na producao real. Sem esse ajuste, o header
     * fixed (top:0) fica exatamente atras dessa barra (mesmo z-index de
     * topo de pagina), escondendo a utility bar por baixo dela. Medido em
     * runtime (nao hardcoded) pra continuar correto se o dev-tool mudar de
     * altura entre Presentation e Debug mode.
     */
    var devToolOffset = 0;
    document.querySelectorAll(".dstool-banner, .dstool-toc").forEach(function (el) {
      devToolOffset += el.getBoundingClientRect().height;
    });
    if (devToolOffset > 0) {
      wrap.style.top = devToolOffset + "px";
      // Mesmo valor tambem encolhe o min-height:100svh do Hero (ver
      // --v2-devtool-offset em components-editorial.css) -- sem isso o
      // Hero + a barra do dev-tool juntos passavam de uma tela, empurrando
      // a navegacao de slides do rodape pra fora da viewport inicial.
      document.documentElement.style.setProperty("--v2-devtool-offset", devToolOffset + "px");
    }

    var ticking = false;
    function update() {
      var solid = hero.getBoundingClientRect().bottom <= wrap.getBoundingClientRect().bottom;
      wrap.classList.toggle("is-solid", solid);
      ticking = false;
    }
    window.addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(update);
      },
      { passive: true }
    );
    window.addEventListener("resize", update);
    update();
  }

  /*
   * LiveClassExperience video (Fase B.6C, secao 17 da missao) -- o video e
   * didatico (fala explicando gramatica), entao usa <video controls> real
   * SEM autoplay (secao 16: "se o vídeo tiver conteúdo didático que
   * precise ser assistido: usar controls e NÃO autoplay") -- isso ja
   * satisfaz "prefers-reduced-motion -> não autoplay, mostrar poster"
   * estruturalmente, sem precisar de logica extra. O unico comportamento
   * de performance que ainda cabe aqui (a missao pede "pause quando sair
   * significativamente da viewport"): se o visitante der play e depois
   * rolar a secao pra fora da tela, pausa sozinho -- nao continua tocando
   * (com audio) fora de vista.
   */
  function initLiveClassVideo(scope) {
    var video = scope.querySelector(".v2-live-class__media video");
    if (!video || !("IntersectionObserver" in window)) return;
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting && !video.paused) video.pause();
        });
      },
      { threshold: 0.1 }
    );
    observer.observe(video);
  }

  /*
   * Locale menu (Fase B.6E, Parte D) -- disclosure simples (botao + lista
   * de links), nao um modal. A resolucao das URLs reais por locale (com
   * fallback en->pt-br, nunca troca de prefixo cega) e feita por
   * vedium-language.js (updateLocaleLinks(), lido via data-vd-locale /
   * data-vd-nav-urls / data-vd-nav-current no elemento [data-v2-locale-root]
   * -- mesmo contrato do header de producao, ver ui-contracts.md). Este
   * bloco so cuida de abrir/fechar o painel -- nao reimplementa nem
   * substitui a logica de resolucao de URL real.
   */
  function initLocaleMenu(scope) {
    scope.querySelectorAll("[data-v2-locale-root]").forEach(function (root) {
      var toggle = root.querySelector("[data-v2-locale-toggle]");
      var menu = root.querySelector("[data-v2-locale-menu]");
      if (!toggle || !menu) return;

      function isOpen() {
        return toggle.getAttribute("aria-expanded") === "true";
      }

      function open() {
        menu.hidden = false;
        toggle.setAttribute("aria-expanded", "true");
      }

      function close(focusToggle) {
        menu.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        if (focusToggle) toggle.focus();
      }

      toggle.addEventListener("click", function () {
        if (isOpen()) close(false);
        else open();
      });

      document.addEventListener("click", function (event) {
        if (!isOpen()) return;
        if (root.contains(event.target)) return;
        close(false);
      });

      root.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && isOpen()) close(true);
      });
    });
  }

  /*
   * Pathfinder routing (Fase C, secao 8-9; refeito na Fase C.2, secao 7 --
   * "resolve_learning_path" compartilhado) -- progressive enhancement. SEM
   * JS, o <form> nativo (v2_pathfinder, method="get") ja funciona: submete
   * pra "/teste-de-nivel" (fallback seguro e util pra qualquer combinacao).
   * COM JS, intercepta o submit e troca o destino pela URL real mais
   * especifica pra aquela combinacao idioma+objetivo -- nunca uma URL
   * inventada, tudo confirmado HTTP 200 (ver docs/redesign/26-home-v2-integration.md).
   *
   * Fase C.2: a matriz deixou de estar hardcoded aqui -- le do data island
   * <script type="application/json" id="vedium-webmcp-course-data"> (ver
   * webmcp_course_data.py), o MESMO bloco que webmcp.js usa pra
   * recommend_learning_path. window.VediumPathfinder.resolve() e a UNICA
   * funcao de resolucao -- a UI humana chama ela aqui, a tool WebMCP chama
   * ela em webmcp.js. Ausencia do data island (pagina sem Pathfinder, ou
   * falha de parse) preserva o fallback seguro: nenhuma correspondencia,
   * form submete nativo pro action original.
   */
  function readWebMcpCourseData() {
    var el = document.getElementById("vedium-webmcp-course-data");
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return null;
    }
  }

  function resolveLearningPath(languageDisplayName, goal) {
    var data = readWebMcpCourseData();
    if (!data) return null;
    var matrix = data.pathfinder_matrix_by_display_name || {};
    var entry = matrix[languageDisplayName];
    if (!entry) return null;
    return entry[goal] || entry._pillar || null;
  }

  window.VediumPathfinder = { resolve: resolveLearningPath };

  function pushDataLayer(payload) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
  }

  function initPathfinderRouting(scope) {
    scope.querySelectorAll(".v2-pathfinder").forEach(function (form) {
      var languageInputs = form.querySelectorAll('input[name="pathfinder-idioma"]');
      var goalInputs = form.querySelectorAll('input[name="pathfinder-objetivo"]');

      languageInputs.forEach(function (input) {
        input.addEventListener("change", function () {
          if (input.checked) pushDataLayer({ event: "pathfinder_language_select", language: input.value });
        });
      });
      goalInputs.forEach(function (input) {
        input.addEventListener("change", function () {
          if (input.checked) pushDataLayer({ event: "pathfinder_goal_select", goal: input.value });
        });
      });

      form.addEventListener("submit", function (event) {
        var language = form.querySelector('input[name="pathfinder-idioma"]:checked');
        var goal = form.querySelector('input[name="pathfinder-objetivo"]:checked');
        language = language ? language.value : "";
        goal = goal ? goal.value : "";

        var destination = resolveLearningPath(language, goal) || "";

        pushDataLayer({ event: "pathfinder_submit", language: language, goal: goal, destination: destination || null });

        // Sem correspondencia conhecida: deixa o <form> submeter normal
        // (GET nativo pra "/teste-de-nivel", o fallback seguro do action).
        if (!destination) return;

        event.preventDefault();
        window.location.href = destination;
      });
    });
  }

  onReady(function () {
    var scope = document;
    initHeaderMenu(scope);
    initFaqAccordion(scope);
    initModals(scope);
    initLevelJourney(scope);
    initHeroCarousel(scope);
    initHeaderOverlay(scope);
    initLiveClassVideo(scope);
    initLocaleMenu(scope);
    initPathfinderRouting(scope);
  });
})();
