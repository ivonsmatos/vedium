import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { HeroEditorial } from "@/components/editorial/HeroEditorial";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { LiveClassExperience } from "@/components/editorial/LiveClassExperience";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { FeatureMedia } from "@/components/editorial/FeatureMedia";
import { InsightsEditorial } from "@/components/editorial/InsightsEditorial";
import { FAQSection } from "@/components/editorial/FAQSection";
import { CtaSection } from "@/components/editorial/CtaSection";

import { yoruba } from "@/content/languages/yoruba";

export const metadata: Metadata = {
  title: yoruba.seo.title,
  description: yoruba.seo.description,
  alternates: {
    canonical: yoruba.seo.canonical,
    languages: yoruba.seo.hreflang,
  },
  robots: yoruba.seo.robots,
  openGraph: {
    type: "website",
    url: yoruba.seo.canonical,
    title: yoruba.seo.title,
    description: yoruba.seo.description,
    images: [yoruba.seo.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: yoruba.seo.title,
    description: yoruba.seo.description,
    images: [yoruba.seo.ogImage],
  },
};

function buildJsonLd() {
  const course = {
    "@context": "https://schema.org",
    "@type": "Course",
    name: "Curso de Iorubá Online",
    description: yoruba.seo.description,
    url: yoruba.seo.canonical,
    provider: { "@type": "Organization", name: "Vedium", url: "https://vediums.com" },
    educationalLevel: "Iniciante",
    inLanguage: "pt-BR",
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: yoruba.breadcrumb.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : yoruba.seo.canonical,
    })),
  };

  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: yoruba.faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };

  return [course, breadcrumb, faq];
}

export default function IorubaPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={yoruba.hero.eyebrow}
          headline={yoruba.hero.headline}
          support={yoruba.hero.support}
          primaryCta={yoruba.hero.primaryCta}
          secondaryCta={yoruba.hero.secondaryCta}
          media={yoruba.hero.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={yoruba.breadcrumb} />
        </div>

        {yoruba.studyPillars ? (
          <VediumMethod
            eyebrow={yoruba.studyPillars.eyebrow}
            title={yoruba.studyPillars.headline}
            items={yoruba.studyPillars.rows}
          />
        ) : null}

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <LiveClassExperience
              title={yoruba.liveClass.title}
              points={yoruba.liveClass.points}
              imageSrc={yoruba.liveClass.media.src}
              imageAlt={yoruba.liveClass.media.alt}
              onDark
            />
          </div>
        </section>

        <section className="v2-section v2-section--warm" id="niveis">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow
              title={yoruba.levels.title}
              text={yoruba.levels.lead}
              steps={yoruba.levels.items.map((level, index) => ({
                label: `${String(index + 1).padStart(2, "0")} ${level.publicLabel.toUpperCase()}`,
                note: level.competencySummary,
                href: level.href,
              }))}
            />
          </div>
        </section>

        {yoruba.culture ? (
        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FeatureMedia
              eyebrow={yoruba.culture.eyebrow}
              title={yoruba.culture.title}
              text={yoruba.culture.description}
              media={yoruba.culture.media}
              cta={yoruba.culture.relatedLink}
            />
          </div>
        </section>
        ) : null}

        {yoruba.insights ? (
        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
              Conhecimento Vedium
            </p>
            <h2 className="v2-heading v2-insights-intro__title">{yoruba.insights.headline}</h2>
            <InsightsEditorial
              featured={yoruba.insights.featured}
              secondaryA={yoruba.insights.secondary[0]}
              secondaryB={yoruba.insights.secondary[1]}
            />
          </div>
        </section>
        ) : null}

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FAQSection faqId="ioruba-faq" eyebrow="Dúvidas comuns" title="Perguntas frequentes sobre o curso de Iorubá." items={yoruba.faq} />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={yoruba.finalCta.headline}
              text={yoruba.finalCta.support}
              primaryCta={yoruba.finalCta.primaryCta}
              secondaryCta={yoruba.finalCta.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
