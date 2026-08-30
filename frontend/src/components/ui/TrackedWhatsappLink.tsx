"use client";

import { CSSProperties, ReactNode } from "react";
import { trackPublicCtaClick } from "@/lib/analytics/event";

interface TrackedWhatsappLinkProps {
  href: string;
  label: string;
  className?: string;
  style?: CSSProperties;
  ariaLabel?: string;
  children: ReactNode;
}

/**
 * Reaproveita o contrato de analytics real já em produção
 * (`templates/includes/public_intent_page.html`): um clique num link de
 * WhatsApp dispara `dataLayer.push({event:'public_cta_click', cta,
 * location})`. Nenhum nome de evento novo (missão F.3 seção 9; reafirmado
 * na Fase G.2). `Button`/`TextLink` renderizam este componente sempre que
 * o `href` for WhatsApp (ver `lib/analytics/whatsapp.ts`), então cobrir
 * este único componente cobre todo CTA de WhatsApp do site -- um clique,
 * uma emissão, sem listener global duplicado (o bug de duplicidade
 * histórica documentado em `docs/redesign/baseline/analytics-contracts.md`
 * vem de um listener global + onclick local coexistindo; aqui só existe o
 * mecanismo explícito por componente).
 */
export function TrackedWhatsappLink({ href, label, className, style, ariaLabel, children }: TrackedWhatsappLinkProps) {
  function handleClick() {
    trackPublicCtaClick(label, window.location.pathname);
  }

  return (
    <a href={href} target="_blank" rel="noopener" className={className} style={style} aria-label={ariaLabel} onClick={handleClick}>
      {children}
    </a>
  );
}
