import type { MetadataRoute } from "next";
import { getAllArticles } from "@/content/blog";

/**
 * Sitemap real (Fase G.1 seção 7). Só as URLs que este Next realmente
 * serve com 200/indexável -- nenhuma rota de curso individual, blog
 * article ainda não migrado, locale `/en/` etc. (essas continuam sendo
 * responsabilidade do Frappe até uma fase de migração maior, ver
 * `24-blog-source-of-truth.md` e `31-global-route-inventory.csv`).
 *
 * `lastModified` só quando existe um dado editorial real por trás --
 * para o artigo do blog, é `updatedAt` (se houve revisão) ou
 * `publishedAt` (data original, nunca a data de execução deste build).
 * Páginas institucionais sem histórico de revisão rastreado ficam sem
 * `lastModified` (Next omite o campo do XML) em vez de inventar uma
 * data "de hoje".
 */
const BASE_URL = "https://vediums.com";

const STATIC_ROUTES = [
  { path: "/", priority: 1.0, changeFrequency: "weekly" as const },
  { path: "/curso-de-ingles-online", priority: 0.9, changeFrequency: "monthly" as const },
  { path: "/curso-de-ioruba-online", priority: 0.9, changeFrequency: "monthly" as const },
  { path: "/portugues-para-estrangeiros", priority: 0.9, changeFrequency: "monthly" as const },
  { path: "/curso-de-espanhol-online", priority: 0.9, changeFrequency: "monthly" as const },
  { path: "/curso-de-hebraico-online", priority: 0.9, changeFrequency: "monthly" as const },
  { path: "/empresas", priority: 0.8, changeFrequency: "monthly" as const },
  { path: "/como-funciona", priority: 0.7, changeFrequency: "monthly" as const },
  { path: "/sobre", priority: 0.6, changeFrequency: "monthly" as const },
  { path: "/contato", priority: 0.6, changeFrequency: "yearly" as const },
  { path: "/privacidade", priority: 0.3, changeFrequency: "yearly" as const },
  { path: "/termos", priority: 0.3, changeFrequency: "yearly" as const },
  { path: "/cancelamento-reembolso", priority: 0.3, changeFrequency: "yearly" as const },
  { path: "/blog", priority: 0.7, changeFrequency: "weekly" as const },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const staticEntries: MetadataRoute.Sitemap = STATIC_ROUTES.map((route) => ({
    url: `${BASE_URL}${route.path}`,
    changeFrequency: route.changeFrequency,
    priority: route.priority,
  }));

  const articleEntries: MetadataRoute.Sitemap = getAllArticles().map((article) => ({
    url: `${BASE_URL}/blog/${article.category}/${article.slug}`,
    lastModified: article.updatedAt || article.publishedAt,
    changeFrequency: "yearly" as const,
    priority: 0.5,
  }));

  return [...staticEntries, ...articleEntries];
}
