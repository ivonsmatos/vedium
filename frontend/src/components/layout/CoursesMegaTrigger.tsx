"use client";

import { useRef } from "react";
import { Icon } from "@/components/ui/Icon";

interface CoursesMegaTriggerProps {
  label: string;
}

export function CoursesMegaTrigger({ label }: CoursesMegaTriggerProps) {
  const buttonRef = useRef<HTMLButtonElement>(null);

  function onClick(event: React.MouseEvent<HTMLButtonElement>) {
    const item = buttonRef.current?.closest<HTMLElement>("[data-v2-nav-item]");
    if (!item) return;
    // Em telas com hover real, deixa o CSS (:hover) resolver -- só
    // intercepta o click quando o dispositivo não tem hover (touch), igual
    // ao comportamento original em design-system-v2.js.
    if (window.matchMedia && window.matchMedia("(hover: hover)").matches) return;
    event.preventDefault();
    const isOpen = item.getAttribute("data-mega-open") === "true";
    item.setAttribute("data-mega-open", isOpen ? "false" : "true");
    buttonRef.current?.setAttribute("aria-expanded", isOpen ? "false" : "true");
  }

  return (
    <button
      ref={buttonRef}
      type="button"
      className="v2-header__nav-link"
      aria-haspopup="true"
      aria-expanded="false"
      onClick={onClick}
    >
      {label} <Icon name="chevron-down" size="0.8em" />
    </button>
  );
}
