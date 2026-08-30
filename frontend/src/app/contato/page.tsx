import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { Button } from "@/components/ui/Button";
import { TrackedWhatsappLink } from "@/components/ui/TrackedWhatsappLink";
import { ProgressionFlow } from "@/components/editorial/ProgressionFlow";
import { FAQSection } from "@/components/editorial/FAQSection";
import { ContactForm } from "@/components/editorial/ContactForm";
import { CtaSection } from "@/components/editorial/CtaSection";

import {
  B2B_BLOCK,
  CONTACT_BREADCRUMB,
  CONTACT_FAQ,
  CONTACT_FORM_COPY,
  CONTACT_INTRO,
  CONTACT_SEO,
  DIRECT_CONTACT,
  NEXT_STEPS,
  SUBJECTS,
  SUBJECTS_INTRO,
} from "@/content/contact";

export const metadata: Metadata = {
  title: CONTACT_SEO.title,
  description: CONTACT_SEO.description,
  alternates: {
    canonical: CONTACT_SEO.canonical,
    languages: CONTACT_SEO.hreflang,
  },
  robots: CONTACT_SEO.robots,
  openGraph: {
    type: "website",
    url: CONTACT_SEO.canonical,
    title: CONTACT_SEO.title,
    description: CONTACT_SEO.description,
    images: [CONTACT_SEO.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: CONTACT_SEO.title,
    description: CONTACT_SEO.description,
    images: [CONTACT_SEO.ogImage],
  },
};

// Organization minimo com ContactPoint -- mesmo contrato de
// `20-institutional-entity-contract.md` (mesmo telefone/e-mail já
// usados no EducationalOrganization da Home/`/sobre`). Nenhum
// ContactPoint conflitante (missão seção 23).
function buildJsonLd() {
  const organization = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Vedium",
    url: "https://vediums.com",
    contactPoint: {
      "@type": "ContactPoint",
      telephone: "+55-11-91129-3075",
      email: "contato@vediums.com",
      contactType: "Customer Service",
      availableLanguage: ["Portuguese", "English"],
    },
  };

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: CONTACT_BREADCRUMB.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: item.href ? new URL(item.href, "https://vediums.com").toString() : CONTACT_SEO.canonical,
    })),
  };

  return [organization, breadcrumb];
}

export default function ContactPage() {
  const jsonLd = buildJsonLd();

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        {/* Sem overlay -- esta página não tem foto full-bleed atrás do
            header (missão seção 6), então o header sólido normal evita o
            problema de sobreposição que o modo overlay pressupõe (ver
            HeroEditorial, que reserva espaço próprio pro header
            flutuante por cima de uma imagem). */}
        <Header />

        {/* Intro institucional sem foto (missão seção 6: "não precisa de
            Hero fotográfico gigantesco") -- mesma estrutura de markup do
            CtaSection--brand-full (ver CtaSection.tsx), só com H1 real
            (único desta página) no lugar do h2 fixo do componente. */}
        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--content">
            <div className="v2-cta-section v2-cta-section--brand-full">
              <div>
                <p className="v2-eyebrow v2-eyebrow--on-dark" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
                  {CONTACT_INTRO.eyebrow}
                </p>
                <h1 className="v2-heading v2-cta-section__title">{CONTACT_INTRO.headline}</h1>
                <p className="v2-body v2-body-lg v2-cta-section__text">{CONTACT_INTRO.support}</p>
              </div>
              <div className="v2-hero__actions">
                <TrackedWhatsappLink href={CONTACT_INTRO.primaryCta.href} label={CONTACT_INTRO.primaryCta.text} className="v2-btn v2-btn--primary">
                  <span>{CONTACT_INTRO.primaryCta.text}</span>
                </TrackedWhatsappLink>
                <Button href={CONTACT_INTRO.secondaryCta.href} variant="secondary" onDark>
                  {CONTACT_INTRO.secondaryCta.text}
                </Button>
              </div>
            </div>
          </div>
        </section>

        <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
          <Breadcrumb items={CONTACT_BREADCRUMB} />
        </div>

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
              {SUBJECTS_INTRO.eyebrow}
            </p>
            <h2 className="v2-heading v2-h2" style={{ marginBlockEnd: "var(--v2-space-6)", maxWidth: "40rem" }}>
              {SUBJECTS_INTRO.title}
            </h2>
            <div className="v2-b2b-list">
              {SUBJECTS.map((subject) => (
                <div className="v2-b2b-list__item" key={subject.title}>
                  <p className="v2-b2b-list__label">{subject.title}</p>
                  <p className="v2-b2b-list__text">{subject.text}</p>
                  <div style={{ marginBlockStart: "var(--v2-space-3)" }}>
                    <TrackedWhatsappLink href={subject.href} label={`${subject.title}: ${subject.whatsappText}`} className="v2-text-link">
                      <span>{subject.whatsappText}</span>
                    </TrackedWhatsappLink>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="v2-section v2-section--warm" id="whatsapp">
          <div className="v2-container v2-container--content">
            <p className="v2-eyebrow">{DIRECT_CONTACT.eyebrow}</p>
            <h2 className="v2-heading v2-h2" style={{ marginBlockStart: "var(--v2-space-3)", marginBlockEnd: "var(--v2-space-4)" }}>
              {DIRECT_CONTACT.title}
            </h2>
            <p className="v2-body v2-body-lg v2-text-muted v2-measure">{DIRECT_CONTACT.text}</p>
            <div className="v2-hero__actions" style={{ marginBlockStart: "var(--v2-space-6)" }}>
              <TrackedWhatsappLink href={DIRECT_CONTACT.whatsappHref} label={DIRECT_CONTACT.whatsappLabel} className="v2-btn v2-btn--primary">
                <span>WhatsApp: {DIRECT_CONTACT.whatsappLabel}</span>
              </TrackedWhatsappLink>
              <a className="v2-text-link" href={DIRECT_CONTACT.emailHref}>
                <span>{DIRECT_CONTACT.emailLabel}</span>
              </a>
            </div>
          </div>
        </section>

        <section className="v2-section">
          <div className="v2-container v2-container--content">
            <p className="v2-eyebrow">{CONTACT_FORM_COPY.eyebrow}</p>
            <h2 className="v2-heading v2-h2" style={{ marginBlockStart: "var(--v2-space-3)", marginBlockEnd: "var(--v2-space-4)" }}>
              {CONTACT_FORM_COPY.title}
            </h2>
            <p className="v2-body v2-body-lg v2-text-muted v2-measure" style={{ marginBlockEnd: "var(--v2-space-8)" }}>
              {CONTACT_FORM_COPY.text}
            </p>
            <ContactForm />
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--content">
            <CtaSection eyebrow={B2B_BLOCK.eyebrow} title={B2B_BLOCK.title} text={B2B_BLOCK.text} primaryCta={B2B_BLOCK.cta} variant="brand-full" />
          </div>
        </section>

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
              {NEXT_STEPS.eyebrow}
            </p>
            <ProgressionFlow title={NEXT_STEPS.title} text={NEXT_STEPS.text} steps={NEXT_STEPS.steps} />
          </div>
        </section>

        <section className="v2-section">
          <div className="v2-container v2-container--wide">
            <FAQSection faqId="contato-faq" eyebrow="Dúvidas comuns" title="Perguntas frequentes sobre como falar com a Vedium." items={CONTACT_FAQ} />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
