/**
 * Contrato de artigo do Blog (Fase F.5). Ver
 * docs/frontend-v2/25-blog-content-model.md para o racional de cada
 * campo e docs/frontend-v2/26-blog-cadence-and-dates.md para a regra
 * de preservação de datas históricas.
 */

export interface BlogFaqItem {
  question: string;
  answer: string;
}

export interface BlogSection {
  heading: string;
  body: string[]; // HTML controlado (parágrafos, listas, tabelas) -- mesma convenção de blog_content.py
}

export interface BlogCta {
  title: string;
  text: string;
  label: string;
  href: string;
}

export interface BlogRelatedArticle {
  slug: string;
  category: string;
  title: string;
}

export type BlogSchemaType = "Article" | "Course" | "HowTo";
export type BlogFunnelStage = "Atração" | "Consideração" | "Conversão";
export type BlogSearchIntent = "Problema/solução" | "Decisão de curso" | "Informacional" | "Comparação";

export interface BlogArticle {
  slug: string;
  // Categoria = segmento de URL (/blog/<category>/<slug>). Artigos
  // legados sem categoria vivem em /blog/<slug> (ver
  // 24-blog-source-of-truth.md) -- campo fica vazio nesse caso.
  category: string;
  title: string;
  description: string;
  h1: string;
  // Idioma do CONTEÚDO do artigo, não do locale do site (missão seção
  // 26). "pt-BR" mesmo quando o site inteiro é pt-BR por padrão.
  language: string;
  // publishedAt é IMUTÁVEL na migração técnica (correção do usuário,
  // 2026-08-30): nunca gerado por new Date(), nunca a data da migração.
  publishedAt: string; // YYYY-MM-DD, data real original
  publishedAtDisplay: string;
  updatedAt?: string; // só quando houver revisão editorial REAL do conteúdo
  // Autoria institucional -- sem persona fictícia (missão seção 23).
  author: string;
  tag: string; // rótulo editorial exibido (ex.: "Inglês")
  cluster: string; // ver Clusters_e_Pilares
  pillarUrl: string; // página-pilar real já aprovada no Next
  primaryKeyword: string;
  secondaryKeywords: string[];
  searchIntent: BlogSearchIntent;
  funnelStage: BlogFunnelStage;
  schema: BlogSchemaType;
  heroImage?: { src: string; alt: string };
  lead: string;
  sections: BlogSection[];
  faq: BlogFaqItem[];
  cta: BlogCta;
  relatedArticles: BlogRelatedArticle[];
  seo: {
    canonical: string;
    robots: string;
    ogImage: string;
  };
}
