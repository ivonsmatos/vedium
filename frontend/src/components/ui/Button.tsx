import Link from "next/link";
import { CSSProperties, ReactNode } from "react";
import { Icon } from "./Icon";
import { TrackedWhatsappLink } from "./TrackedWhatsappLink";
import { isWhatsappHref } from "@/lib/analytics/whatsapp";

interface ButtonProps {
  children: ReactNode;
  href?: string;
  variant?: "primary" | "secondary" | "outline" | "brand";
  size?: "default" | "compact" | "sm" | "lg";
  onDark?: boolean;
  className?: string;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  icon?: string;
  iconPosition?: "start" | "end";
  newTab?: boolean;
  ariaLabel?: string;
  style?: CSSProperties;
}

export function Button({
  children,
  href,
  variant = "primary",
  size = "default",
  onDark = false,
  className = "",
  onClick,
  type = "button",
  icon,
  iconPosition = "end",
  newTab = false,
  ariaLabel,
  style,
}: ButtonProps) {
  const baseClass = `v2-btn v2-btn--${variant}`;
  const sizeClass = size !== "default" ? `v2-btn--${size}` : "";
  const darkClass = onDark ? "v2-btn--on-dark" : "";

  const finalClassName = `${baseClass} ${sizeClass} ${darkClass} ${className}`.trim();

  const content = (
    <>
      {icon && iconPosition === "start" ? <Icon name={icon} /> : null}
      <span>{children}</span>
      {icon && iconPosition === "end" ? <Icon name={icon} /> : null}
    </>
  );

  if (href) {
    if (isWhatsappHref(href)) {
      // Todo CTA de WhatsApp passa por aqui automaticamente (Fase G.2,
      // Parte A, seção 9) -- Button não sabe montar o evento, só decide
      // delegar pro componente que sabe (`lib/analytics/event.ts` é a
      // única fonte do payload).
      const label = typeof children === "string" ? children : ariaLabel || "WhatsApp";
      return (
        <TrackedWhatsappLink href={href} label={label} className={finalClassName} style={style} ariaLabel={ariaLabel}>
          {content}
        </TrackedWhatsappLink>
      );
    }
    return (
      <Link
        href={href}
        className={finalClassName}
        aria-label={ariaLabel}
        style={style}
        {...(newTab ? { target: "_blank", rel: "noopener" } : {})}
      >
        {content}
      </Link>
    );
  }

  return (
    <button type={type} className={finalClassName} onClick={onClick} aria-label={ariaLabel} style={style}>
      {content}
    </button>
  );
}
