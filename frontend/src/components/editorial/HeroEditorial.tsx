import { Button } from "@/components/ui/Button";
import type { CtaLink, HeroMedia } from "@/types/language";

interface HeroEditorialProps {
  eyebrow: string;
  headline: string;
  support: string;
  primaryCta: CtaLink;
  secondaryCta?: CtaLink;
  media: HeroMedia;
}

/**
 * Versão de 1 slide do HeroEditorialCarousel da Home -- mesmas classes CSS
 * (`.v2-editorial-hero*`), mesmo overlay/tipografia/comportamento com o
 * HeaderOverlayScroll (que procura `.v2-editorial-hero` no DOM). Sem
 * carousel: nenhuma tab, nenhum autoplay, 100% Server Component.
 */
export function HeroEditorial({ eyebrow, headline, support, primaryCta, secondaryCta, media }: HeroEditorialProps) {
  return (
    <section className="v2-editorial-hero" aria-label={eyebrow}>
      <div className="v2-editorial-hero__slides">
        <div className="v2-editorial-hero__slide is-active" role="group">
          <div className="v2-editorial-hero__media">
            <img src={media.src} alt={media.alt} width={media.width} height={media.height} loading="eager" fetchPriority="high" />
          </div>
          <div className="v2-editorial-hero__overlay" aria-hidden="true" />
          <div className="v2-editorial-hero__content">
            <div className="v2-container v2-container--wide">
              <div className="v2-editorial-hero__copy">
                {eyebrow ? <p className="v2-eyebrow v2-eyebrow--on-dark v2-editorial-hero__eyebrow">{eyebrow}</p> : null}
                <h1 className="v2-heading v2-editorial-hero__title">{headline}</h1>
                <p className="v2-body v2-editorial-hero__support">{support}</p>
                <div className="v2-hero__actions">
                  <Button href={primaryCta.href} variant="primary">
                    {primaryCta.text}
                  </Button>
                  {secondaryCta ? (
                    <Button href={secondaryCta.href} variant="secondary" onDark newTab={secondaryCta.href.startsWith("http")}>
                      {secondaryCta.text}
                    </Button>
                  ) : null}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
