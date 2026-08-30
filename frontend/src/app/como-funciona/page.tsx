import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { TextLink } from "@/components/ui/TextLink";
import { HeroEditorial } from "@/components/editorial/HeroEditorial";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { LiveClassExperience } from "@/components/editorial/LiveClassExperience";
import { FeatureMedia } from "@/components/editorial/FeatureMedia";
import { CourseIndexIntro } from "@/components/editorial/CourseIndexIntro";
import { FAQSection } from "@/components/editorial/FAQSection";
import { CtaSection } from "@/components/editorial/CtaSection";

import {
  COURSES_SECTION,
  EVOLUTION,
  FINAL_CTA,
  HOW_IT_WORKS_BREADCRUMB,
  HOW_IT_WORKS_FAQ,
  HOW_IT_WORKS_HERO,
  HOW_IT_WORKS_SEO,
  LANGUAGE_CONTEXT,
  LEVEL_STRUCTURE,
  LIVE_CLASS,
  NEXT_LEVEL,
  OVERVIEW,
  POINT_OF_START,
  STUDY_FORMATS,
  TEACHER_AND_PRACTICE,
} from "@/content/how-it-works";

export const metadata: Metadata = {
  title: HOW_IT_WORKS_SEO.title,
  description: HOW_IT_WORKS_SEO.description,
  alternates: {
    canonical: HOW_IT_WORKS_SEO.canonical,
    languages: HOW_IT_WORKS_SEO.hreflang,
  },
  robots: HOW_IT_WORKS_SEO.robots,
  openGraph: {
    type: "website",
    url: HOW_IT_WORKS_SEO.canonical,
    title: HOW_IT_WORKS_SEO.title,
    description: HOW_IT_WORKS_SEO.description,
    images: [HOW_IT_WORKS_SEO.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: HOW_IT_WORKS_SEO.title,
    description: HOW_IT_WORKS_SEO.description,
    images: [HOW_IT_WORKS_SEO.ogImage],
  },
};

function buildJsonLd() {
  const organization = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Vedium",
    url: "https://vediums.com",
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: HOW_IT_WORKS_BREADCRUMB.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : HOW_IT_WORKS_SEO.canonical,
    })),
  };

  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: HOW_IT_WORKS_FAQ.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };

  return [organization, breadcrumb, faq];
}

export default function HowItWorksPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={HOW_IT_WORKS_HERO.eyebrow}
          headline={HOW_IT_WORKS_HERO.headline}
          support={HOW_IT_WORKS_HERO.support}
          primaryCta={HOW_IT_WORKS_HERO.primaryCta}
          secondaryCta={HOW_IT_WORKS_HERO.secondaryCta}
          media={HOW_IT_WORKS_HERO.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={HOW_IT_WORKS_BREADCRUMB} />
        </div>

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
              {OVERVIEW.eyebrow}
            </p>
            <ProgressionFlow
              title={OVERVIEW.title}
              text={OVERVIEW.text}
              steps={OVERVIEW.steps.map((step) => ({ label: step.label, note: step.note, href: step.href }))}
            />
          </div>
        </section>

        <div id="ponto-de-partida">
          <VediumMethod eyebrow={POINT_OF_START.eyebrow} title={POINT_OF_START.title} intro={POINT_OF_START.intro} items={POINT_OF_START.items} />
        </div>

        <div id="percurso">
          <VediumMethod eyebrow={LEVEL_STRUCTURE.eyebrow} title={LEVEL_STRUCTURE.title} intro={LEVEL_STRUCTURE.text} items={LEVEL_STRUCTURE.rows} />
          <section className="v2-section v2-section--alt">
            <div className="v2-container v2-container--wide">
              <p className="v2-body v2-body-lg v2-text-muted v2-measure">{LEVEL_STRUCTURE.hebrewNote}</p>
              <div style={{ marginBlockStart: "var(--v2-space-4)" }}>
                <TextLink href={LEVEL_STRUCTURE.hebrewCta.href} size="lg">
                  {LEVEL_STRUCTURE.hebrewCta.text}
                </TextLink>
              </div>
            </div>
          </section>
        </div>

        <section className="v2-section v2-section--brand" id="aulas-ao-vivo">
          <div className="v2-container v2-container--wide">
            <LiveClassExperience
              title={LIVE_CLASS.title}
              lead={LIVE_CLASS.lead}
              points={LIVE_CLASS.points}
              imageSrc={LIVE_CLASS.media.src}
              imageAlt={LIVE_CLASS.media.alt}
              onDark
            />
          </div>
        </section>

        <div id="professor">
          <VediumMethod eyebrow={TEACHER_AND_PRACTICE.eyebrow} title={TEACHER_AND_PRACTICE.title} intro={TEACHER_AND_PRACTICE.intro} items={TEACHER_AND_PRACTICE.items} />
        </div>

        <section className="v2-section" id="idioma-e-contexto">
          <div className="v2-container v2-container--wide">
            <FeatureMedia eyebrow={LANGUAGE_CONTEXT.eyebrow} title={LANGUAGE_CONTEXT.title} text={LANGUAGE_CONTEXT.text} media={LANGUAGE_CONTEXT.media} />
          </div>
        </section>

        <section className="v2-section v2-section--warm" id="acompanhamento">
          <div className="v2-container v2-container--wide">
            <FeatureMedia eyebrow={EVOLUTION.eyebrow} title={EVOLUTION.title} text={EVOLUTION.text} media={EVOLUTION.media} reverse />
            <div id="proximo-nivel" className="v2-measure" style={{ marginBlockStart: "var(--v2-space-12)", paddingBlockStart: "var(--v2-space-10)", borderBlockStart: "1px solid var(--v2-color-border)" }}>
              <p className="v2-eyebrow">{NEXT_LEVEL.eyebrow}</p>
              <h3 className="v2-heading v2-h3" style={{ marginBlockStart: "var(--v2-space-3)", marginBlockEnd: "var(--v2-space-3)" }}>
                {NEXT_LEVEL.title}
              </h3>
              <p className="v2-body v2-text-muted">{NEXT_LEVEL.text}</p>
            </div>
          </div>
        </section>

        <VediumMethod eyebrow={STUDY_FORMATS.eyebrow} title={STUDY_FORMATS.title} intro={STUDY_FORMATS.intro} items={STUDY_FORMATS.items} />

        <CourseIndexIntro eyebrow={COURSES_SECTION.eyebrow} title={COURSES_SECTION.title} lead={COURSES_SECTION.lead} courses={COURSES_SECTION.courses} />

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <FAQSection faqId="como-funciona-faq" eyebrow="Dúvidas comuns" title="Perguntas frequentes sobre como estudar na Vedium." items={HOW_IT_WORKS_FAQ} />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection title={FINAL_CTA.headline} text={FINAL_CTA.support} primaryCta={FINAL_CTA.primaryCta} secondaryCta={FINAL_CTA.secondaryCta} variant="brand-full" />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
