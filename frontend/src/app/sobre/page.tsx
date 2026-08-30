import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { TextLink } from "@/components/ui/TextLink";
import { HeroEditorial } from "@/components/editorial/HeroEditorial";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { FeatureMedia } from "@/components/editorial/FeatureMedia";
import { CourseIndexIntro } from "@/components/editorial/CourseIndexIntro";
import { CtaSection } from "@/components/editorial/CtaSection";

import {
  ABOUT_BREADCRUMB,
  ABOUT_FINAL_CTA,
  ABOUT_HERO,
  ABOUT_SEO,
  CULTURAL_RIGOR,
  EXPERIENCE,
  PEDAGOGICAL_GUIDANCE,
  PORTFOLIO,
  PRINCIPLES,
  WHAT_WE_BELIEVE,
  WHO_WE_ARE,
  WHY_WE_EXIST,
} from "@/content/about";

export const metadata: Metadata = {
  title: ABOUT_SEO.title,
  description: ABOUT_SEO.description,
  alternates: {
    canonical: ABOUT_SEO.canonical,
    languages: ABOUT_SEO.hreflang,
  },
  robots: ABOUT_SEO.robots,
  openGraph: {
    type: "website",
    url: ABOUT_SEO.canonical,
    title: ABOUT_SEO.title,
    description: ABOUT_SEO.description,
    images: [ABOUT_SEO.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: ABOUT_SEO.title,
    description: ABOUT_SEO.description,
    images: [ABOUT_SEO.ogImage],
  },
};

// Mesmo contrato global de EducationalOrganization já usado em `/`
// (app/page.tsx) -- mesmos campos, sem inventar sameAs/foundingDate/
// founder/award (missão seção 25). `/sobre` é a página que mais faz
// sentido reforçar essa entidade, sem duplicar dado conflitante.
function buildJsonLd() {
  const organization = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    name: "Vedium",
    url: "https://vediums.com",
    logo: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    description: ABOUT_SEO.description,
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

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: ABOUT_BREADCRUMB.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : ABOUT_SEO.canonical,
    })),
  };

  return [organization, breadcrumb];
}

export default function AboutPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={ABOUT_HERO.eyebrow}
          headline={ABOUT_HERO.headline}
          support={ABOUT_HERO.support}
          primaryCta={ABOUT_HERO.primaryCta}
          secondaryCta={ABOUT_HERO.secondaryCta}
          media={ABOUT_HERO.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={ABOUT_BREADCRUMB} />
        </div>

        <VediumMethod eyebrow={WHO_WE_ARE.eyebrow} title={WHO_WE_ARE.title} intro={WHO_WE_ARE.text} items={WHO_WE_ARE.items} />

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--content">
            <p className="v2-eyebrow">{WHY_WE_EXIST.eyebrow}</p>
            <h2 className="v2-heading v2-h2" style={{ marginBlockStart: "var(--v2-space-3)", marginBlockEnd: "var(--v2-space-4)" }}>
              {WHY_WE_EXIST.title}
            </h2>
            <p className="v2-body v2-body-lg v2-text-muted v2-measure">{WHY_WE_EXIST.text}</p>
            <p className="v2-body v2-body-lg v2-measure" style={{ marginBlockStart: "var(--v2-space-5)", fontWeight: 600 }}>
              {WHY_WE_EXIST.closing}
            </p>
          </div>
        </section>

        <VediumMethod eyebrow={WHAT_WE_BELIEVE.eyebrow} title={WHAT_WE_BELIEVE.title} items={WHAT_WE_BELIEVE.items} />

        {/* Selo visual entre 2 VediumMethod seguidos (ambos navy em tela
            larga) -- sem isso, as duas secoes se fundem numa unica mancha
            azul continua, sem indicar onde uma capitulo termina e o outro
            comeca. */}
        <div aria-hidden="true" style={{ height: 2, background: "var(--v2-color-brand-300)", opacity: 0.4 }} />

        <VediumMethod eyebrow={EXPERIENCE.eyebrow} title={EXPERIENCE.title} items={EXPERIENCE.items} />

        <section className="v2-section v2-section--warm">
          <div className="v2-container v2-container--wide">
            <FeatureMedia eyebrow={PEDAGOGICAL_GUIDANCE.eyebrow} title={PEDAGOGICAL_GUIDANCE.title} text={PEDAGOGICAL_GUIDANCE.text} media={PEDAGOGICAL_GUIDANCE.media} />
          </div>
        </section>

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FeatureMedia eyebrow={CULTURAL_RIGOR.eyebrow} title={CULTURAL_RIGOR.title} text={CULTURAL_RIGOR.text} media={CULTURAL_RIGOR.media} reverse />
          </div>
        </section>

        <CourseIndexIntro eyebrow={PORTFOLIO.eyebrow} title={PORTFOLIO.title} lead={PORTFOLIO.lead} courses={PORTFOLIO.courses} />

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <p className="v2-body v2-body-lg v2-text-muted v2-measure">
              {PORTFOLIO.b2bText}{" "}
              <TextLink href={PORTFOLIO.b2bCta.href} size="lg">
                {PORTFOLIO.b2bCta.text}
              </TextLink>
            </p>
          </div>
        </section>

        <VediumMethod eyebrow={PRINCIPLES.eyebrow} title={PRINCIPLES.title} items={PRINCIPLES.items} />

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={ABOUT_FINAL_CTA.headline}
              text={ABOUT_FINAL_CTA.support}
              primaryCta={ABOUT_FINAL_CTA.primaryCta}
              secondaryCta={ABOUT_FINAL_CTA.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
