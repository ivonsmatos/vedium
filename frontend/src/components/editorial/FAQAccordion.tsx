"use client";

import { useState } from "react";
import { Icon } from "@/components/ui/Icon";
import type { FaqItem } from "@/types/language";

interface FAQAccordionProps {
  faqId: string;
  items: FaqItem[];
  allowMultiple?: boolean;
}

/**
 * React equivalente do macro `v2_faq_accordion` -- mesmas classes CSS
 * (`.v2-faq*`). Único item aberto por vez por padrão (allowMultiple=false),
 * igual ao comportamento original.
 */
export function FAQAccordion({ faqId, items, allowMultiple = false }: FAQAccordionProps) {
  const [openIndexes, setOpenIndexes] = useState<Set<number>>(new Set());

  function toggle(index: number) {
    setOpenIndexes((current) => {
      const isOpen = current.has(index);
      if (allowMultiple) {
        const next = new Set(current);
        if (isOpen) next.delete(index);
        else next.add(index);
        return next;
      }
      return isOpen ? new Set() : new Set([index]);
    });
  }

  return (
    <div className="v2-faq" id={faqId} data-allow-multiple={allowMultiple ? "true" : "false"}>
      {items.map((item, index) => {
        const itemId = `${faqId}-${index + 1}`;
        const isOpen = openIndexes.has(index);
        return (
          <div className="v2-faq__item" key={item.question}>
            <h3>
              <button
                type="button"
                className="v2-faq__trigger"
                id={`${itemId}-trigger`}
                aria-expanded={isOpen}
                aria-controls={`${itemId}-panel`}
                onClick={() => toggle(index)}
              >
                <span>{item.question}</span>
                <span className="v2-faq__icon" aria-hidden="true">
                  <Icon name="chevron-down" size="0.9em" />
                </span>
              </button>
            </h3>
            <div
              className="v2-faq__panel"
              id={`${itemId}-panel`}
              role="region"
              aria-labelledby={`${itemId}-trigger`}
              data-open={isOpen ? "true" : "false"}
            >
              <div className="v2-faq__panel-inner">{item.answer}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
