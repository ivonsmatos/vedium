import Link from "next/link";
import { Icon } from "@/components/ui/Icon";
import type { InsightCard } from "@/content/home/insights";

interface InsightsEditorialProps {
  featured: InsightCard;
  secondaryA: InsightCard;
  secondaryB?: InsightCard;
  ctaLabel?: string;
}

export function InsightsEditorial({ featured, secondaryA, secondaryB, ctaLabel = "Leia o artigo" }: InsightsEditorialProps) {
  return (
    <div className="v2-insights">
      <article className="v2-insights__featured">
        <p className="v2-insights__meta">
          {featured.category ? <span>{featured.category}</span> : null}
          {featured.date ? <span>{featured.date}</span> : null}
        </p>
        <h3 className="v2-insights__featured-title">
          <Link href={featured.href}>{featured.title}</Link>
        </h3>
        <p className="v2-insights__featured-summary">{featured.summary}</p>
        <Link className="v2-insights__cta" href={featured.href}>
          {ctaLabel} <Icon name="arrow-right" size="1em" />
        </Link>
      </article>
      <div className="v2-insights__secondary-col">
        {[secondaryA, secondaryB].filter((item): item is InsightCard => Boolean(item)).map((item) => (
          <article className="v2-insights__secondary" key={item.href}>
            <p className="v2-insights__meta">
              {item.category ? <span>{item.category}</span> : null}
              {item.date ? <span>{item.date}</span> : null}
            </p>
            <h4 className="v2-insights__secondary-title">
              <Link href={item.href}>{item.title}</Link>
            </h4>
            <p className="v2-insights__secondary-summary">{item.summary}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
