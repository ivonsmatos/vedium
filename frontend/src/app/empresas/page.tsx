import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { HeroEditorial } from "@/components/editorial/HeroEditorial";
import { VediumMethod } from "@/components/editorial/VediumMethod";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { B2BHomeFeature } from "@/components/editorial/B2BHomeFeature";
import { FeatureMedia } from "@/components/editorial/FeatureMedia";
import { FAQSection } from "@/components/editorial/FAQSection";
import { CtaSection } from "@/components/editorial/CtaSection";

import { b2b } from "@/content/b2b";

export const metadata: Metadata = {
  title: b2b.seo.title,
  description: b2b.seo.description,
  alternates: {
    canonical: b2b.seo.canonical,
    languages: b2b.seo.hreflang,
  },
  robots: b2b.seo.robots,
  openGraph: {
    type: "website",
    url: b2b.seo.canonical,
    title: b2b.seo.title,
    description: b2b.seo.description,
    images: [b2b.seo.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: b2b.seo.title,
    description: b2b.seo.description,
    images: [b2b.seo.ogImage],
  },
};

function buildJsonLd() {
  const service = {
    "@context": "https://schema.org",
    "@type": "Service",
    name: "Vedium para Empresas",
    serviceType: "Treinamento corporativo de idiomas",
    provider: { "@type": "Organization", name: "Vedium", url: "https://vediums.com" },
    areaServed: "BR",
    description: b2b.seo.description,
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: b2b.breadcrumb.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : b2b.seo.canonical,
    })),
  };

  const faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: b2b.faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };

  return [service, breadcrumb, faq];
}

export default function B2BPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header overlay />

        <HeroEditorial
          eyebrow={b2b.hero.eyebrow}
          headline={b2b.hero.headline}
          support={b2b.hero.support}
          primaryCta={b2b.hero.primaryCta}
          secondaryCta={b2b.hero.secondaryCta}
          media={b2b.hero.media}
        />

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={b2b.breadcrumb} />
        </div>

        <VediumMethod eyebrow={b2b.challenge.eyebrow} title={b2b.challenge.headline} items={b2b.challenge.rows} />

        <section className="v2-section v2-section--warm">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow title={b2b.diagnosis.title} text={b2b.diagnosis.text} steps={b2b.diagnosis.steps} />
          </div>
        </section>

        <section className="v2-section v2-section--brand" id="solucao">
          <div className="v2-container v2-container--wide">
            <B2BHomeFeature
              eyebrow={b2b.solution.eyebrow}
              subEyebrow={b2b.solution.subEyebrow}
              title={b2b.solution.title}
              text={b2b.solution.text}
              text2={b2b.solution.text2}
              proofItems={b2b.solution.proofItems}
              primaryCta={b2b.solution.primaryCta}
              secondaryCta={b2b.solution.secondaryCta}
              imageSrc={b2b.solution.media.src}
              imageAlt={b2b.solution.media.alt}
            />
          </div>
        </section>

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow title={b2b.howItWorks.title} text={b2b.howItWorks.text} steps={b2b.howItWorks.steps} />
          </div>
        </section>

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <FeatureMedia
              eyebrow={b2b.management.eyebrow}
              title={b2b.management.title}
              text={b2b.management.description}
              media={b2b.management.media}
              reverse
            />
          </div>
        </section>

        <VediumMethod eyebrow={b2b.formats.eyebrow} title={b2b.formats.headline} items={b2b.formats.rows} />

        <section className="v2-section v2-section--warm">
          <div className="v2-container v2-container--wide">
            <ProgressionFlow title={b2b.implementation.title} text={b2b.implementation.text} steps={b2b.implementation.steps} />
          </div>
        </section>

        <VediumMethod eyebrow={b2b.whyVedium.eyebrow} title={b2b.whyVedium.headline} items={b2b.whyVedium.rows} />

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={b2b.diagnosisCta.title}
              text={b2b.diagnosisCta.text}
              primaryCta={b2b.diagnosisCta.primaryCta}
              secondaryCta={b2b.diagnosisCta.secondaryCta}
              variant="section"
            />
          </div>
        </section>

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <FAQSection faqId="empresas-faq" eyebrow="Dúvidas comuns" title="Perguntas frequentes sobre Vedium para Empresas." items={b2b.faq} />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={b2b.diagnosisCta.title}
              text={b2b.diagnosisCta.text}
              primaryCta={b2b.diagnosisCta.primaryCta}
              secondaryCta={b2b.diagnosisCta.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
