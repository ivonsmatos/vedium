"use client";

import { useEffect, useRef, useState } from "react";
import { Icon } from "@/components/ui/Icon";
import type { LocaleOption } from "@/content/site/header";

interface LocaleSwitcherProps {
  options: LocaleOption[];
  navUrls: Record<string, string>;
  currentLocale: string;
}

export function LocaleSwitcher({ options, navUrls, currentLocale }: LocaleSwitcherProps) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const toggleRef = useRef<HTMLButtonElement>(null);
  const current = options.find((option) => option.code === currentLocale) ?? options[0];

  useEffect(() => {
    if (!open) return;

    function onDocumentClick(event: MouseEvent) {
      if (rootRef.current?.contains(event.target as Node)) return;
      setOpen(false);
    }
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setOpen(false);
        toggleRef.current?.focus();
      }
    }
    document.addEventListener("click", onDocumentClick);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("click", onDocumentClick);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  return (
    <div className="v2-hdr-locale" data-v2-locale-root ref={rootRef}>
      <button
        ref={toggleRef}
        type="button"
        className="v2-hdr-utility__locale"
        aria-haspopup="true"
        aria-expanded={open}
        aria-controls="v2-hdr-locale-menu"
        onClick={() => setOpen((value) => !value)}
      >
        <span className="v2-hdr-utility__locale-flag" aria-hidden="true">
          {current.flag}
        </span>
        <span>{current.code === "pt-br" ? "PT" : current.code.toUpperCase()}</span>
        <Icon name="chevron-down" size="0.7em" />
      </button>
      <ul className="v2-hdr-locale-menu" id="v2-hdr-locale-menu" role="menu" hidden={!open}>
        {options.map((option) => (
          <li role="none" key={option.code}>
            <a
              role="menuitem"
              className={`v2-hdr-locale-menu__link${option.code === currentLocale ? " is-active" : ""}`}
              href={navUrls[option.code] ?? "/"}
              aria-current={option.code === currentLocale ? "true" : undefined}
            >
              <span className="v2-hdr-locale-menu__flag" aria-hidden="true">
                {option.flag}
              </span>
              <span>{option.label}</span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
