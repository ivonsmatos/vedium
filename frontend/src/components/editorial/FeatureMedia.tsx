import { TextLink } from "@/components/ui/TextLink";
import type { CtaLink, HeroMedia } from "@/types/language";

interface FeatureMediaProps {
  eyebrow?: string;
  title: string;
  text: string;
  media: HeroMedia;
  reverse?: boolean;
  cta?: CtaLink;
  objectPosition?: string;
}

/**
 * React equivalente do macro `v2_feature_media` (55/45, mídia + conteúdo,
 * CTA textual) -- já existia na folha de estilo compartilhada
 * (`.v2-feature-media*`), sem uso ainda por nenhuma página Next até agora.
 */
export function FeatureMedia({ eyebrow, title, text, media, reverse = false, cta, objectPosition = "center" }: FeatureMediaProps) {
  return (
    <div className={`v2-feature-media${reverse ? " v2-feature-media--reverse" : ""}`}>
      <div className="v2-feature-media__media">
        <img src={media.src} alt={media.alt} width={800} height={600} loading="lazy" style={{ objectPosition }} />
      </div>
      <div className="v2-feature-media__content">
        {eyebrow ? <p className="v2-eyebrow">{eyebrow}</p> : null}
        <h2 className="v2-heading v2-h2 v2-feature-media__title">{title}</h2>
        <p className="v2-body v2-text-muted v2-feature-media__text">{text}</p>
        {cta ? (
          <TextLink href={cta.href} size="lg">
            {cta.text}
          </TextLink>
        ) : null}
      </div>
    </div>
  );
}
