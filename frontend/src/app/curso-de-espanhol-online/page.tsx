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

import { spanish } from "@/content/languages/spanish";

export const metadata: Metadata = {
  title: spanish.seo.title,
  description: spanish.seo.description,
  alternates: {
    canonical: spanish.seo.canonical,
    languages: spanish.seo.hreflang,
  },
  robots: spanish.seo.robots,
  openGraph: {
    type: "website",
    url: spanish.seo.canonical,
    title: spanish.seo.title,
    description: spanish.seo.description,
    images: [spanish.seo.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: spanish.seo.title,
    description: spanish.seo.description,
    images: [spanish.seo.ogImage],
  },
};

function buildJsonLd() {
  const course = {
    "@context": "https://schema.org",
    "@type": "Course",
    name: "Curso de Espanhol Online",
    description: spanish.seo.description,
    url: spanish.seo.canonical,
    provider: { "@type": "Organization", name: "Vedium", url: "https://vediums.com" },
    educationalLevel: "Básico ao Avançado (A1 a C1)",
    inLanguage: "pt-BR",
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: spanish.breadcrumb.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : spanish.seo.canonical,
    })),
  };

  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: spanish.faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };

  return [course, breadcrumb, faq];
}

export default function SpanishPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={spanish.hero.eyebrow}
          headline={spanish.hero.headline}
          support={spanish.hero.support}
          primaryCta={spanish.hero.primaryCta}
          secondaryCta={spanish.hero.secondaryCta}
          media={spanish.hero.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={spanish.breadcrumb} />
        </div>

        {spanish.studyPillars ? (
          <VediumMethod eyebrow={spanish.studyPillars.eyebrow} title={spanish.studyPillars.headline} items={spanish.studyPillars.rows} />
        ) : null}

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <LiveClassExperience
              title={spanish.liveClass.title}
              lead={spanish.liveClass.lead}
              points={spanish.liveClass.points}
              imageSrc={spanish.liveClass.media.src}
              imageAlt={spanish.liveClass.media.alt}
              onDark
            />
          </div>
        </section>

        <section className="v2-section v2-section--warm" id="niveis">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow
              title={spanish.levels.title}
              text={spanish.levels.lead}
              steps={spanish.levels.items.map((level, index) => ({
                label: `${String(index + 1).padStart(2, "0")} ${level.publicLabel.toUpperCase()}`,
                note: level.competencySummary,
                href: level.href,
              }))}
            />
          </div>
        </section>

        {spanish.applications ? (
          <VediumMethod eyebrow={spanish.applications.eyebrow} title={spanish.applications.headline} items={spanish.applications.rows} />
        ) : null}

        {spanish.culture ? (
          <section className="v2-section">
            <div className="v2-container v2-container--wide">
              <FeatureMedia
                eyebrow={spanish.culture.eyebrow}
                title={spanish.culture.title}
                text={spanish.culture.description}
                media={spanish.culture.media}
              />
            </div>
          </section>
        ) : null}

        {spanish.insights ? (
          <section className="v2-section v2-section--alt">
            <div className="v2-container v2-container--wide">
              <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
                Conhecimento Vedium
              </p>
              <h2 className="v2-heading v2-insights-intro__title">{spanish.insights.headline}</h2>
              <InsightsEditorial
                featured={spanish.insights.featured}
                secondaryA={spanish.insights.secondary[0]}
                secondaryB={spanish.insights.secondary[1]}
              />
            </div>
          </section>
        ) : null}

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FAQSection
              faqId="espanhol-faq"
              eyebrow="Dúvidas comuns"
              title="Perguntas frequentes sobre o curso de Espanhol."
              items={spanish.faq}
            />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={spanish.finalCta.headline}
              text={spanish.finalCta.support}
              primaryCta={spanish.finalCta.primaryCta}
              secondaryCta={spanish.finalCta.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
