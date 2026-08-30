import Link from "next/link";
import { ReactNode } from "react";
import { Icon } from "./Icon";
import { TrackedWhatsappLink } from "./TrackedWhatsappLink";
import { isWhatsappHref } from "@/lib/analytics/whatsapp";

interface TextLinkProps {
  children: ReactNode;
  href: string;
  size?: "default" | "lg";
  variant?: "brand" | "accent";
  icon?: string;
  onDark?: boolean;
  className?: string;
}

export function TextLink({
  children,
  href,
  size = "default",
  variant = "brand",
  icon = "arrow-right",
  onDark = false,
  className = "",
}: TextLinkProps) {
  const sizeClass = size === "lg" ? "v2-text-link--lg" : "";
  const variantClass = variant === "accent" ? "v2-text-link--accent" : "";
  const darkClass = onDark ? "v2-text-link--on-dark" : "";

  const finalClassName = `v2-text-link ${variantClass} ${darkClass} ${sizeClass} ${className}`.trim();

  const content = (
    <>
      <span>{children}</span>
      <Icon name={icon} size="1em" />
    </>
  );

  if (isWhatsappHref(href)) {
    const label = typeof children === "string" ? children : "WhatsApp";
    return (
      <TrackedWhatsappLink href={href} label={label} className={finalClassName}>
        {content}
      </TrackedWhatsappLink>
    );
  }

  return (
    <Link href={href} className={finalClassName}>
      {content}
    </Link>
  );
}
