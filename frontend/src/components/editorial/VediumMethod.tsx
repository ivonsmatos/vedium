import { TextLink } from "@/components/ui/TextLink";

interface VediumMethodProps {
  eyebrow: string;
  title: string;
  intro?: string;
  items: { title: string; text: string; href?: string; ctaLabel?: string }[];
  cta?: { text: string; href: string };
}

export function VediumMethod({ eyebrow, title, intro, items, cta }: VediumMethodProps) {
  return (
    <section className="v2-vedium-method">
      <div className="v2-vedium-method__intro">
        <div className="v2-vedium-method__intro-inner">
          <p className="v2-eyebrow v2-eyebrow--on-dark">{eyebrow}</p>
          <h2 className="v2-heading v2-h2 v2-vedium-method__title">{title}</h2>
          {intro ? <p className="v2-body v2-vedium-method__lead">{intro}</p> : null}
          {cta ? (
            <div style={{ marginBlockStart: "var(--v2-space-6)" }}>
              <TextLink href={cta.href} size="lg" onDark>
                {cta.text}
              </TextLink>
            </div>
          ) : null}
        </div>
      </div>
      <div className="v2-vedium-method__list-wrap">
        <ol className="v2-vedium-method__list">
          {items.slice(0, 4).map((item, index) => (
            <li className="v2-vedium-method__item" key={item.title}>
              <span className="v2-vedium-method__item-num">{String(index + 1).padStart(2, "0")}</span>
              <div>
                <h3 className="v2-vedium-method__item-label">{item.title}</h3>
                <p className="v2-vedium-method__item-text">{item.text}</p>
                {item.href ? (
                  <div style={{ marginBlockStart: "var(--v2-space-3)" }}>
                    <TextLink href={item.href}>{item.ctaLabel ?? "Conheça"}</TextLink>
                  </div>
                ) : null}
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
