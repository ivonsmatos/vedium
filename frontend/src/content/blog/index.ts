import type { BlogArticle } from "@/types/blog";
import { AULA_DE_INGLES_ONLINE_AO_VIVO } from "./aula-de-ingles-online-ao-vivo";

/**
 * Registro dos artigos já migrados para o Next. Fase F.5 migra 1 (prova
 * de conceito do template + arquitetura) -- os outros 96 do inventário
 * (docs/frontend-v2/27-blog-url-migration-map.csv) continuam servidos
 * pelo Frappe até uma fase futura de migração em lote, com aprovação
 * humana por artigo (missão seção 6: nunca mesclar/arquivar automático).
 */
export const BLOG_ARTICLES: BlogArticle[] = [AULA_DE_INGLES_ONLINE_AO_VIVO];

export function getArticle(category: string, slug: string): BlogArticle | undefined {
  return BLOG_ARTICLES.find((article) => article.category === category && article.slug === slug);
}

export function getAllArticles(): BlogArticle[] {
  return [...BLOG_ARTICLES].sort((a, b) => (a.publishedAt < b.publishedAt ? 1 : -1));
}
