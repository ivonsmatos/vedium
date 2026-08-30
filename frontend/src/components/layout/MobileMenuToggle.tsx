"use client";

import { useEffect, useRef } from "react";

export function MobileMenuToggle() {
  const buttonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.key !== "Escape") return;
      const header = buttonRef.current?.closest<HTMLElement>("[data-v2-header]");
      if (!header) return;
      header.setAttribute("data-menu-open", "false");
      buttonRef.current?.setAttribute("aria-expanded", "false");
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, []);

  function toggle() {
    const header = buttonRef.current?.closest<HTMLElement>("[data-v2-header]");
    if (!header) return;
    const open = header.getAttribute("data-menu-open") === "true";
    header.setAttribute("data-menu-open", open ? "false" : "true");
    buttonRef.current?.setAttribute("aria-expanded", open ? "false" : "true");
  }

  return (
    <button
      ref={buttonRef}
      type="button"
      className="v2-header__burger"
      aria-label="Abrir menu"
      aria-expanded="false"
      aria-controls="v2-header-mobile-panel"
      onClick={toggle}
    >
      <span className="v2-header__burger-icon" aria-hidden="true" />
    </button>
  );
}
