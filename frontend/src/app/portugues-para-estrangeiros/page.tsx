import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { HeroEditorial } from "@/components/editorial/HeroEditorial";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { LiveClassExperience } from "@/components/editorial/LiveClassExperience";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { FeatureMedia } from "@/components/editorial/FeatureMedia";
import { FAQSection } from "@/components/editorial/FAQSection";
import { CtaSection } from "@/components/editorial/CtaSection";

import { portugueseForForeigners as ple } from "@/content/languages/portuguese-for-foreigners";

export const metadata: Metadata = {
  title: ple.seo.title,
  description: ple.seo.description,
  alternates: {
    canonical: ple.seo.canonical,
    languages: ple.seo.hreflang,
  },
  robots: ple.seo.robots,
  openGraph: {
    type: "website",
    url: ple.seo.canonical,
    title: ple.seo.title,
    description: ple.seo.description,
    images: [ple.seo.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: ple.seo.title,
    description: ple.seo.description,
    images: [ple.seo.ogImage],
  },
};

function buildJsonLd() {
  const course = {
    "@context": "https://schema.org",
    "@type": "Course",
    name: "Português para Estrangeiros",
    description: ple.seo.description,
    url: ple.seo.canonical,
    provider: { "@type": "Organization", name: "Vedium", url: "https://vediums.com" },
    educationalLevel: "A1 a B2",
    inLanguage: "pt-BR",
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: ple.breadcrumb.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : ple.seo.canonical,
    })),
  };

  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: ple.faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };

  return [course, breadcrumb, faq];
}

export default function PortugueseForForeignersPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={ple.hero.eyebrow}
          headline={ple.hero.headline}
          support={ple.hero.support}
          primaryCta={ple.hero.primaryCta}
          secondaryCta={ple.hero.secondaryCta}
          media={ple.hero.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={ple.breadcrumb} />
        </div>

        {ple.studyPillars ? (
          <VediumMethod eyebrow={ple.studyPillars.eyebrow} title={ple.studyPillars.headline} items={ple.studyPillars.rows} />
        ) : null}

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <LiveClassExperience
              title={ple.liveClass.title}
              lead={ple.liveClass.lead}
              points={ple.liveClass.points}
              imageSrc={ple.liveClass.media.src}
              imageAlt={ple.liveClass.media.alt}
              onDark
            />
          </div>
        </section>

        <section className="v2-section v2-section--warm" id="niveis">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow
              title={ple.levels.title}
              text={ple.levels.lead}
              steps={ple.levels.items.map((level, index) => ({
                label: `${String(index + 1).padStart(2, "0")} ${level.publicLabel.toUpperCase()}`,
                note: level.competencySummary,
                href: level.href,
              }))}
            />
          </div>
        </section>

        {ple.culture ? (
          <section className="v2-section">
            <div className="v2-container v2-container--wide">
              <FeatureMedia
                eyebrow={ple.culture.eyebrow}
                title={ple.culture.title}
                text={ple.culture.description}
                media={ple.culture.media}
                reverse
              />
            </div>
          </section>
        ) : null}

        {ple.applications ? (
          <VediumMethod eyebrow={ple.applications.eyebrow} title={ple.applications.headline} items={ple.applications.rows} />
        ) : null}

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FAQSection
              faqId="ple-faq"
              eyebrow="Dúvidas comuns"
              title="Perguntas frequentes sobre português para estrangeiros."
              items={ple.faq}
            />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={ple.finalCta.headline}
              text={ple.finalCta.support}
              primaryCta={ple.finalCta.primaryCta}
              secondaryCta={ple.finalCta.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
