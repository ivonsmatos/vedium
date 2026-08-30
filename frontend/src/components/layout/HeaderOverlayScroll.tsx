"use client";

import { useEffect } from "react";

/**
 * Header overlay -- fixed sobre o Hero, transparente até a base do Hero
 * cruzar a base do header durante o scroll; a partir dali ganha fundo
 * sólido ("is-solid"). Espelha initHeaderOverlay em design-system-v2.js.
 * Não renderiza nada -- só o efeito de scroll.
 */
export function HeaderOverlayScroll() {
  useEffect(() => {
    const wrap = document.querySelector<HTMLElement>("[data-v2-header-overlay]");
    const hero = document.querySelector<HTMLElement>(".v2-editorial-hero");
    if (!wrap || !hero) return;

    let ticking = false;
    function update() {
      const solid = hero!.getBoundingClientRect().bottom <= wrap!.getBoundingClientRect().bottom;
      wrap!.classList.toggle("is-solid", solid);
      ticking = false;
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", update);
    update();

    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", update);
    };
  }, []);

  return null;
}
