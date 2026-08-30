import type { Metadata } from "next";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { TextLink } from "@/components/ui/TextLink";
import { FeatureMedia } from "@/components/editorial/FeatureMedia";
import { CourseIndexIntro } from "@/components/editorial/CourseIndexIntro";
import { CtaSection } from "@/components/editorial/CtaSection";
import { getAllArticles } from "@/content/blog";
import { BLOG_B2B_NOTE, BLOG_EXPLORE_BY_LANGUAGE, BLOG_FINAL_CTA, BLOG_HUB_INTRO, BLOG_HUB_SEO } from "@/content/blog/hub";

export const metadata: Metadata = {
  title: BLOG_HUB_SEO.title,
  description: BLOG_HUB_SEO.description,
  alternates: { canonical: BLOG_HUB_SEO.canonical, languages: BLOG_HUB_SEO.hreflang },
  robots: BLOG_HUB_SEO.robots,
  openGraph: {
    type: "website",
    url: BLOG_HUB_SEO.canonical,
    title: BLOG_HUB_SEO.title,
    description: BLOG_HUB_SEO.description,
    images: [BLOG_HUB_SEO.ogImage],
  },
  twitter: {
    card: "summary_large_image",
    title: BLOG_HUB_SEO.title,
    description: BLOG_HUB_SEO.description,
    images: [BLOG_HUB_SEO.ogImage],
  },
};

function buildJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Início", item: "https://vediums.com/" },
      { "@type": "ListItem", position: 2, name: "Blog", item: BLOG_HUB_SEO.canonical },
    ],
  };
}

export default function BlogHubPage() {
  const articles = getAllArticles();
  const featured = articles[0];
  const jsonLd = buildJsonLd();

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <main>
        <Header />

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--content">
            <div className="v2-cta-section v2-cta-section--brand-full">
              <div>
                <p className="v2-eyebrow v2-eyebrow--on-dark" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
                  {BLOG_HUB_INTRO.eyebrow}
                </p>
                <h1 className="v2-heading v2-cta-section__title">{BLOG_HUB_INTRO.title}</h1>
                <p className="v2-body v2-body-lg v2-cta-section__text">{BLOG_HUB_INTRO.support}</p>
              </div>
            </div>
          </div>
        </section>

        {featured ? (
          <section className="v2-section">
            <div className="v2-container v2-container--wide">
              <p className="v2-eyebrow" style={{ marginBlockEnd: "var(--v2-space-6)" }}>
                ARTIGO EM DESTAQUE
              </p>
              <FeatureMedia
                eyebrow={featured.tag}
                title={featured.title}
                text={featured.lead}
                media={{
                  src: featured.heroImage?.src || "",
                  alt: featured.heroImage?.alt || "",
                  width: 1100,
                  height: 560,
                }}
                cta={{ text: "Ler artigo completo", href: `/blog/${featured.category}/${featured.slug}` }}
              />
            </div>
          </section>
        ) : null}

        <CourseIndexIntro
          eyebrow="EXPLORAR POR IDIOMA"
          title="Cada idioma, seu próprio percurso."
          lead="Escolha o idioma para conhecer o curso e os níveis disponíveis."
          courses={BLOG_EXPLORE_BY_LANGUAGE}
        />

        <section className="v2-section v2-section--alt">
          <div className="v2-container v2-container--wide">
            <p className="v2-body v2-body-lg v2-text-muted v2-measure">
              {BLOG_B2B_NOTE.text}{" "}
              <TextLink href={BLOG_B2B_NOTE.ctaHref} size="lg">
                {BLOG_B2B_NOTE.ctaText}
              </TextLink>
            </p>
          </div>
        </section>

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--wide">
            <CtaSection
              title={BLOG_FINAL_CTA.headline}
              text={BLOG_FINAL_CTA.support}
              primaryCta={BLOG_FINAL_CTA.primaryCta}
              secondaryCta={BLOG_FINAL_CTA.secondaryCta}
              variant="brand-full"
            />
          </div>
        </section>

        <Footer />
      </main>
    </>
  );
}
