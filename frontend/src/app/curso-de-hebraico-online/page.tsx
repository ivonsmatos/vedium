import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { HeroEditorial } from "@/components/editorial/HeroEditorial";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { LiveClassExperience } from "@/components/editorial/LiveClassExperience";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { FeatureMedia } from "@/components/editorial/FeatureMedia";
import { EditorialNote } from "@/components/editorial/EditorialNote";
import { InsightsEditorial } from "@/components/editorial/InsightsEditorial";
import { FAQSection } from "@/components/editorial/FAQSection";
import { CtaSection } from "@/components/editorial/CtaSection";

import { hebrew, alefBetSample } from "@/content/languages/hebrew";

export const metadata: Metadata = {
  title: hebrew.seo.title,
  description: hebrew.seo.description,
  alternates: {
    canonical: hebrew.seo.canonical,
    languages: hebrew.seo.hreflang,
  },
  robots: hebrew.seo.robots,
  openGraph: {
    type: "website",
    url: hebrew.seo.canonical,
    title: hebrew.seo.title,
    description: hebrew.seo.description,
    images: [hebrew.seo.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: hebrew.seo.title,
    description: hebrew.seo.description,
    images: [hebrew.seo.ogImage],
  },
};

function buildJsonLd() {
  const course = {
    "@context": "https://schema.org",
    "@type": "Course",
    name: "Curso de Hebraico Online",
    description: hebrew.seo.description,
    url: hebrew.seo.canonical,
    provider: { "@type": "Organization", name: "Vedium", url: "https://vediums.com" },
    educationalLevel: "Alfabetização a A2/B1 (Moderno); Leitura Guiada (Bíblico)",
    inLanguage: "pt-BR",
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: hebrew.breadcrumb.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : hebrew.seo.canonical,
    })),
  };

  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: hebrew.faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };

  return [course, breadcrumb, faq];
}

export default function HebrewPage() {
  const jsonLd = buildJsonLd();
  const [particularNote, teacherNote] = hebrew.editorialNotes ?? [];

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={hebrew.hero.eyebrow}
          headline={hebrew.hero.headline}
          support={hebrew.hero.support}
          primaryCta={hebrew.hero.primaryCta}
          secondaryCta={hebrew.hero.secondaryCta}
          media={hebrew.hero.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={hebrew.breadcrumb} />
        </div>

        {hebrew.tracks ? (
          <div id="percursos">
            <VediumMethod eyebrow={hebrew.tracks.eyebrow} title={hebrew.tracks.headline} items={hebrew.tracks.items} />
          </div>
        ) : null}

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <LiveClassExperience
              title={hebrew.liveClass.title}
              lead={hebrew.liveClass.lead}
              points={hebrew.liveClass.points}
              imageSrc={hebrew.liveClass.media.src}
              imageAlt={hebrew.liveClass.media.alt}
              onDark
            />
          </div>
        </section>

        {hebrew.culture ? (
          <section className="v2-section" id="moderno">
            <div className="v2-container v2-container--wide">
              <FeatureMedia
                eyebrow={hebrew.culture.eyebrow}
                title={hebrew.culture.title}
                text={hebrew.culture.description}
                media={hebrew.culture.media}
              />
              <p className="v2-body-sm v2-text-subtle" style={{ marginBlockStart: "var(--v2-space-4)" }}>
                O alfabeto hebraico:{" "}
                <span lang="he" dir="rtl" style={{ fontSize: "1.1em" }}>
                  {alefBetSample.hebrewScript}
                </span>{" "}
                ({alefBetSample.transliteration}).
              </p>
            </div>
          </section>
        ) : null}

        <section className="v2-section v2-section--warm">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow
              title={hebrew.levels.title}
              text={hebrew.levels.lead}
              steps={hebrew.levels.items.map((level, index) => ({
                label: `${String(index + 1).padStart(2, "0")} ${level.publicLabel}`,
                note: level.competencySummary,
                href: level.href,
              }))}
            />
          </div>
        </section>

        {hebrew.secondaryFeature ? (
          <section className="v2-section" id="biblico">
            <div className="v2-container v2-container--wide">
              <FeatureMedia
                eyebrow={hebrew.secondaryFeature.eyebrow}
                title={hebrew.secondaryFeature.title}
                text={hebrew.secondaryFeature.description}
                media={hebrew.secondaryFeature.media}
                cta={hebrew.secondaryFeature.relatedLink}
                reverse
              />
            </div>
          </section>
        ) : null}

        {particularNote || teacherNote ? (
          <section className="v2-section v2-section--warm" id="particular">
            <div className="v2-container v2-container--wide">
              <div className="v2-notes-pair">
                {particularNote ? (
                  <EditorialNote bare eyebrow={particularNote.eyebrow} title={particularNote.title} text={particularNote.text} cta={particularNote.cta} />
                ) : null}
                {teacherNote ? (
                  <EditorialNote bare eyebrow={teacherNote.eyebrow} title={teacherNote.title} text={teacherNote.text} cta={teacherNote.cta} />
                ) : null}
              </div>
            </div>
          </section>
        ) : null}

        {hebrew.insights ? (
          <section className="v2-section v2-section--alt">
            <div className="v2-container v2-container--wide">
              <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
                Conhecimento Vedium
              </p>
              <h2 className="v2-heading v2-insights-intro__title">{hebrew.insights.headline}</h2>
              <InsightsEditorial
                featured={hebrew.insights.featured}
                secondaryA={hebrew.insights.secondary[0]}
                secondaryB={hebrew.insights.secondary[1]}
              />
            </div>
          </section>
        ) : null}

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FAQSection faqId="hebraico-faq" eyebrow="Dúvidas comuns" title="Perguntas frequentes sobre o curso de Hebraico." items={hebrew.faq} />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={hebrew.finalCta.headline}
              text={hebrew.finalCta.support}
              primaryCta={hebrew.finalCta.primaryCta}
              secondaryCta={hebrew.finalCta.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
