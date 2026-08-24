/*
 * VEDIUM DESIGN SYSTEM V2 -- JS progressivo (vanilla, sem jQuery/dependencia
 * nova). So roda dentro de .v2-scope. Isolado -- nao e incluido em
 * web_include_js, so carregado explicitamente pela pagina de preview.
 *
 * Cobre: menu mobile do Header v2, accordion do FAQ, modal base.
 * Tudo funciona sem JS (menu mobile fica sempre visivel sem JS -- ver
 * fallback <noscript> no macro do header; FAQ sem JS mostra todas as
 * respostas abertas via <details>/<summary> nativo).
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

  onReady(function () {
    var scope = document;
    initHeaderMenu(scope);
    initFaqAccordion(scope);
    initModals(scope);
  });
})();
