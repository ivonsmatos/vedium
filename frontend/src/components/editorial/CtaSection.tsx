import { Button } from "@/components/ui/Button";
import { TextLink } from "@/components/ui/TextLink";

interface CtaSectionProps {
  eyebrow?: string;
  title: string;
  text?: string;
  primaryCta: { text: string; href: string };
  secondaryCta?: { text: string; href: string };
  variant?: "section" | "brand" | "brand-full" | "inline";
}

export function CtaSection({ eyebrow, title, text, primaryCta, secondaryCta, variant = "section" }: CtaSectionProps) {
  const onDark = variant === "brand" || variant === "brand-full";
  return (
    <div className={`v2-cta-section${variant !== "section" ? ` v2-cta-section--${variant}` : ""}`}>
      <div>
        {eyebrow ? <p className={`v2-eyebrow${onDark ? " v2-eyebrow--on-dark" : ""}`} style={{ marginBlockEnd: "var(--v2-space-3)" }}>{eyebrow}</p> : null}
        <h2 className="v2-heading v2-h2 v2-cta-section__title">{title}</h2>
        {text ? <p className="v2-body v2-body-lg v2-cta-section__text">{text}</p> : null}
      </div>
      <div className="v2-hero__actions">
        <Button href={primaryCta.href} variant="primary">
          {primaryCta.text}
        </Button>
        {secondaryCta ? (
          <TextLink href={secondaryCta.href} onDark={onDark}>
            {secondaryCta.text}
          </TextLink>
        ) : null}
      </div>
    </div>
  );
}
