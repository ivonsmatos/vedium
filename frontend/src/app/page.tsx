import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { HeroEditorialCarousel } from "@/components/editorial/HeroEditorialCarousel";
import { PathfinderSection } from "@/components/editorial/PathfinderSection";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { CourseIndexIntro } from "@/components/editorial/CourseIndexIntro";
import { CourseFeature } from "@/components/editorial/CourseFeature";
import { LiveClassExperience } from "@/components/editorial/LiveClassExperience";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { B2BHomeFeature } from "@/components/editorial/B2BHomeFeature";
import { InsightsEditorial } from "@/components/editorial/InsightsEditorial";
import { CtaSection } from "@/components/editorial/CtaSection";
import { TextLink } from "@/components/ui/TextLink";

import { HERO_SLIDES } from "@/content/home/hero";
import {
  PATHFINDER_CTA,
  PATHFINDER_EYEBROW,
  PATHFINDER_LANGUAGES,
  PATHFINDER_LANGUAGE_QUESTION,
  PATHFINDER_LEAD,
  PATHFINDER_OBJECTIVES,
  PATHFINDER_OBJECTIVE_QUESTION,
  PATHFINDER_STEPS,
  PATHFINDER_TITLE,
} from "@/content/home/pathfinder";
import { METHOD_EYEBROW, METHOD_INTRO, METHOD_ITEMS, METHOD_TITLE } from "@/content/home/method";
import { COURSE_INDEX_ENTRIES, COURSE_INDEX_EYEBROW, COURSE_INDEX_LEAD, COURSE_INDEX_TITLE, HOME_COURSES } from "@/content/home/courses";
import { LIVE_CLASS_CTA, LIVE_CLASS_LEAD, LIVE_CLASS_POINTS, LIVE_CLASS_TITLE, LIVE_CLASS_VIDEO_POSTER, LIVE_CLASS_VIDEO_SRC } from "@/content/home/liveClass";
import { PROGRESSION_STEPS, PROGRESSION_TEXT, PROGRESSION_TITLE } from "@/content/home/progression";
import {
  B2B_EYEBROW,
  B2B_IMAGE_ALT,
  B2B_IMAGE_SRC,
  B2B_OBJECT_POSITION,
  B2B_PRIMARY_CTA,
  B2B_PROOF_ITEMS,
  B2B_SECONDARY_CTA,
  B2B_SUB_EYEBROW,
  B2B_TEXT,
  B2B_TEXT_2,
  B2B_TITLE,
} from "@/content/home/b2b";
import { INSIGHTS_ALL_HREF, INSIGHTS_ALL_LABEL, INSIGHTS_CTA_LABEL, INSIGHTS_EYEBROW, INSIGHTS_FEATURED, INSIGHTS_SECONDARY, INSIGHTS_TITLE } from "@/content/home/insights";
import { CTA_FINAL_PRIMARY, CTA_FINAL_SECONDARY, CTA_FINAL_TEXT, CTA_FINAL_TITLE } from "@/content/home/ctaFinal";

const TITLE = "Vedium - Cursos Online ao Vivo em Cinco Idiomas";
const DESCRIPTION =
  "Aprenda inglês (níveis A1 a C1) e iorubá com a Vedium: aulas ao vivo com professores qualificados, certificado de conclusão e suporte ao aluno. Comece hoje a sua jornada de fluência.";

export const metadata: Metadata = {
  title: TITLE,
  description: DESCRIPTION,
  keywords: [
    "curso de inglês online ao vivo",
    "curso de iorubá",
    "aulas de idiomas ao vivo",
    "escola de idiomas online",
    "certificado de inglês",
    "inglês A1 a C1",
  ],
  alternates: {
    canonical: "https://vediums.com/",
    languages: {
      "pt-br": "https://vediums.com/",
      en: "https://vediums.com/en",
      es: "https://vediums.com/es",
      fr: "https://vediums.com/fr",
      de: "https://vediums.com/de",
      "x-default": "https://vediums.com/",
    },
  },
  openGraph: {
    type: "website",
    url: "https://vediums.com/",
    title: "Vedium - Cursos Online ao Vivo em Cinco Idiomas",
    description: "Aulas ao vivo de inglês, espanhol, hebraico, iorubá e português para estrangeiros, com professores e certificado.",
    images: ["/assets/vedium_core/vedium_assets/images/logos/logo-color-reta.png"],
  },
  twitter: {
    card: "summary_large_image",
    title: "Vedium - Cursos de Idiomas Online ao Vivo",
    description: "Aulas ao vivo de cinco idiomas, com professores e certificado.",
    images: ["/assets/vedium_core/vedium_assets/images/logos/logo-color-reta.png"],
  },
};

const JSON_LD = {
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  name: "Vedium",
  url: "https://vediums.com",
  logo: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
  description: "Escola de idiomas online com aulas ao vivo: Inglês (A1 a C1) e Iorubá, do básico ao avançado.",
  address: { "@type": "PostalAddress", addressCountry: "BR" },
  contactPoint: {
    "@type": "ContactPoint",
    telephone: "+55-11-91129-3075",
    email: "contato@vediums.com",
    contactType: "Customer Service",
    availableLanguage: ["Portuguese", "English"],
  },
  sameAs: ["https://www.instagram.com/vediumsglobal/", "https://www.linkedin.com/company/vediums"],
};

export default function HomePage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(JSON_LD) }} />
      <main>
        <Header overlay primaryCtaOverride={{ text: "Conheça os cursos", href: "/catalogo" }} />

        <HeroEditorialCarousel slides={HERO_SLIDES} />

        <PathfinderSection
          eyebrow={PATHFINDER_EYEBROW}
          title={PATHFINDER_TITLE}
          lead={PATHFINDER_LEAD}
          steps={PATHFINDER_STEPS}
          languageQuestion={PATHFINDER_LANGUAGE_QUESTION}
          languages={PATHFINDER_LANGUAGES}
          objectiveQuestion={PATHFINDER_OBJECTIVE_QUESTION}
          objectives={PATHFINDER_OBJECTIVES}
          cta={PATHFINDER_CTA}
        />

        <VediumMethod eyebrow={METHOD_EYEBROW} title={METHOD_TITLE} intro={METHOD_INTRO} items={METHOD_ITEMS} />

        <div className="v2-course-feature-stack">
          <CourseIndexIntro
            eyebrow={COURSE_INDEX_EYEBROW}
            title={COURSE_INDEX_TITLE}
            lead={COURSE_INDEX_LEAD}
            courses={COURSE_INDEX_ENTRIES}
          />
          {HOME_COURSES.map((course) => (
            <CourseFeature key={course.slug} course={course} index={course.order} />
          ))}
        </div>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <LiveClassExperience
              title={LIVE_CLASS_TITLE}
              lead={LIVE_CLASS_LEAD}
              points={LIVE_CLASS_POINTS}
              videoSrc={LIVE_CLASS_VIDEO_SRC}
              videoPoster={LIVE_CLASS_VIDEO_POSTER}
              cta={LIVE_CLASS_CTA}
              onDark
            />
          </div>
        </section>

        <section className="v2-section v2-section--warm">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow title={PROGRESSION_TITLE} text={PROGRESSION_TEXT} steps={PROGRESSION_STEPS} />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <B2BHomeFeature
              eyebrow={B2B_EYEBROW}
              subEyebrow={B2B_SUB_EYEBROW}
              title={B2B_TITLE}
              text={B2B_TEXT}
              text2={B2B_TEXT_2}
              proofItems={B2B_PROOF_ITEMS}
              primaryCta={B2B_PRIMARY_CTA}
              secondaryCta={B2B_SECONDARY_CTA}
              imageSrc={B2B_IMAGE_SRC}
              imageAlt={B2B_IMAGE_ALT}
              objectPosition={B2B_OBJECT_POSITION}
            />
          </div>
        </section>

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
              {INSIGHTS_EYEBROW}
            </p>
            <h2 className="v2-heading v2-insights-intro__title">{INSIGHTS_TITLE}</h2>
            <InsightsEditorial
              featured={INSIGHTS_FEATURED}
              secondaryA={INSIGHTS_SECONDARY[0]}
              secondaryB={INSIGHTS_SECONDARY[1]}
              ctaLabel={INSIGHTS_CTA_LABEL}
            />
            <div style={{ marginBlockStart: "var(--v2-space-12)" }}>
              <TextLink href={INSIGHTS_ALL_HREF} size="lg">
                {INSIGHTS_ALL_LABEL}
              </TextLink>
            </div>
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={CTA_FINAL_TITLE}
              text={CTA_FINAL_TEXT}
              primaryCta={CTA_FINAL_PRIMARY}
              secondaryCta={CTA_FINAL_SECONDARY}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
