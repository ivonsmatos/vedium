import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { Button } from "@/components/ui/Button";
import { FAQSection } from "@/components/editorial/FAQSection";
import type { BlogArticle } from "@/types/blog";
import type { BreadcrumbItem } from "@/types/language";

interface ArticleTemplateProps {
  article: BlogArticle;
}

/**
 * Template único e reutilizável de artigo (missão F.5 seção 8) --
 * mesmo Design System das páginas institucionais, nenhum sistema visual
 * novo. Estrutura: breadcrumbs -> cabeçalho do artigo (eyebrow, H1,
 * resumo/resposta direta, data/autor) -> imagem principal -> conteúdo ->
 * FAQ (bloco GEO) -> CTA contextual. `Header`/`Footer` ficam na página
 * (app/blog/[category]/[slug]/page.tsx), não aqui, pra este componente
 * poder ser reusado igual em qualquer rota de artigo futura.
 */
export function ArticleTemplate({ article }: ArticleTemplateProps) {
  const breadcrumb: BreadcrumbItem[] = [
    { label: "Início", href: "/" },
    { label: "Blog", href: "/blog" },
    { label: article.tag, href: null },
  ];

  return (
    <>
      <div className="v2-container v2-container--wide" style={{ paddingBlock: "var(--v2-space-6)" }}>
        <Breadcrumb items={breadcrumb} />
      </div>

      <article>
        <header className="v2-section" style={{ paddingBlockEnd: 0 }}>
          <div className="v2-container v2-container--reading">
            <p className="v2-eyebrow">{article.tag}</p>
            <h1 className="v2-heading v2-h1" style={{ marginBlockStart: "var(--v2-space-3)", marginBlockEnd: "var(--v2-space-4)" }}>
              {article.h1}
            </h1>
            <p className="v2-body v2-body-lg v2-text-muted">{article.lead}</p>
            <div className="v2-article-meta">
              <span>{article.publishedAtDisplay}</span>
              <span aria-hidden="true">·</span>
              <span>{article.author}</span>
              {article.updatedAt ? (
                <>
                  <span aria-hidden="true">·</span>
                  <span>Atualizado em {article.updatedAt}</span>
                </>
              ) : null}
            </div>
          </div>
        </header>

        {article.heroImage ? (
          <div className="v2-section" style={{ paddingBlockStart: 0 }}>
            <div className="v2-container v2-container--reading">
              <div className="v2-article-hero-image">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={article.heroImage.src} alt={article.heroImage.alt} width={1100} height={560} loading="eager" />
              </div>
            </div>
          </div>
        ) : null}

        <section className="v2-section" style={{ paddingBlockStart: 0 }}>
          <div className="v2-container v2-container--reading">
            <div className="v2-article-body">
              {article.sections.map((section, index) => (
                <div key={index}>
                  {section.heading ? (
                    <h2 className="v2-heading v2-h2" style={{ marginBlock: "var(--v2-space-10) var(--v2-space-4)" }}>
                      {section.heading}
                    </h2>
                  ) : null}
                  {section.body.map((html, i) => (
                    <div key={i} dangerouslySetInnerHTML={{ __html: html }} />
                  ))}
                </div>
              ))}
            </div>
          </div>
        </section>

        {article.faq.length > 0 ? (
          <section className="v2-section v2-section--alt">
            <div className="v2-container v2-container--reading">
              <FAQSection
                faqId={`${article.slug}-faq`}
                eyebrow="Dúvidas comuns"
                title="Perguntas frequentes"
                items={article.faq.map((item) => ({ question: item.question, answer: item.answer }))}
              />
            </div>
          </section>
        ) : null}

        <section className="v2-section v2-section--brand">
          <div className="v2-container v2-container--reading" style={{ textAlign: "center" }}>
            <div className="v2-cta-section v2-cta-section--brand-full">
              <div>
                <h2 className="v2-heading v2-cta-section__title">{article.cta.title}</h2>
                <p className="v2-body v2-body-lg v2-cta-section__text">{article.cta.text}</p>
              </div>
              <div className="v2-hero__actions">
                <Button href={article.cta.href} variant="primary">
                  {article.cta.label}
                </Button>
              </div>
            </div>
          </div>
        </section>
      </article>
    </>
  );
}
