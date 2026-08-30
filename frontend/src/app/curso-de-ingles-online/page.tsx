import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { HeroEditorial } from "@/components/editorial/HeroEditorial";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { LiveClassExperience } from "@/components/editorial/LiveClassExperience";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { CourseIndexIntro } from "@/components/editorial/CourseIndexIntro";
import { InsightsEditorial } from "@/components/editorial/InsightsEditorial";
import { FAQSection } from "@/components/editorial/FAQSection";
import { CtaSection } from "@/components/editorial/CtaSection";

import { english } from "@/content/languages/english";

export const metadata: Metadata = {
  title: english.seo.title,
  description: english.seo.description,
  alternates: {
    canonical: english.seo.canonical,
    languages: english.seo.hreflang,
  },
  robots: english.seo.robots,
  openGraph: {
    type: "website",
    url: english.seo.canonical,
    title: english.seo.title,
    description: english.seo.description,
    images: [english.seo.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: english.seo.title,
    description: english.seo.description,
    images: [english.seo.ogImage],
  },
};

function buildJsonLd() {
  const course = {
    "@context": "https://schema.org",
    "@type": "Course",
    name: "Curso de inglês online ao vivo do A1 ao C1",
    description: english.seo.description,
    url: english.seo.canonical,
    provider: { "@type": "Organization", name: "Vedium", url: "https://vediums.com" },
    educationalLevel: "A1 a C1 (CEFR)",
    inLanguage: "pt-BR",
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: english.breadcrumb.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : english.seo.canonical,
    })),
  };

  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: english.faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };

  return [course, breadcrumb, faq];
}

export default function EnglishPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={english.hero.eyebrow}
          headline={english.hero.headline}
          support={english.hero.support}
          primaryCta={english.hero.primaryCta}
          secondaryCta={english.hero.secondaryCta}
          media={english.hero.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={english.breadcrumb} />
        </div>

        {english.studyPillars ? (
          <VediumMethod
            eyebrow={english.studyPillars.eyebrow}
            title={english.studyPillars.headline}
            intro={english.studyPillars.lead}
            items={english.studyPillars.rows}
            cta={english.studyPillars.cta}
          />
        ) : null}

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <LiveClassExperience
              title={english.liveClass.title}
              lead={english.liveClass.lead}
              points={english.liveClass.points}
              videoSrc={english.liveClass.media.src}
              videoPoster="/assets/vedium_core/v2/media/home/e16-liveclass-teacher-poster.jpg"
              onDark
            />
          </div>
        </section>

        <section className="v2-section v2-section--warm" id="niveis">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow
              title={english.levels.title}
              text={english.levels.lead}
              steps={english.levels.items.map((level, index) => ({
                label: `${String(index + 1).padStart(2, "0")} ${level.publicLabel}`,
                note: level.competencySummary,
                href: level.href,
              }))}
            />
          </div>
        </section>

        {english.objectives ? (
          <CourseIndexIntro
            eyebrow={english.objectives.eyebrow}
            title={english.objectives.title}
            lead={english.objectives.lead}
            courses={english.objectives.items}
          />
        ) : null}

        {english.progressionConcept ? (
          <section className="v2-section">
            <div className="v2-container v2-container--wide">
              <ProgressionFlow
                title={english.progressionConcept.title}
                text={english.progressionConcept.text}
                steps={english.progressionConcept.steps}
              />
            </div>
          </section>
        ) : null}

        {english.insights ? (
        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
              Conhecimento Vedium
            </p>
            <h2 className="v2-heading v2-insights-intro__title">{english.insights.headline}</h2>
            <InsightsEditorial
              featured={english.insights.featured}
              secondaryA={english.insights.secondary[0]}
              secondaryB={english.insights.secondary[1]}
            />
          </div>
        </section>
        ) : null}

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FAQSection faqId="ingles-faq" eyebrow="Dúvidas comuns" title="Perguntas frequentes sobre o curso de Inglês." items={english.faq} />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={english.finalCta.headline}
              text={english.finalCta.support}
              primaryCta={english.finalCta.primaryCta}
              secondaryCta={english.finalCta.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
