export interface InsightCard {
  title: string;
  summary: string;
  href: string;
  category: string;
  date: string;
}

export const INSIGHTS_EYEBROW = "Conhecimento Vedium";
export const INSIGHTS_TITLE = "Aprenda também fora da aula.";
export const INSIGHTS_CTA_LABEL = "Leia o artigo";
export const INSIGHTS_ALL_LABEL = "Ver todos os conteúdos";
export const INSIGHTS_ALL_HREF = "/blog";

/**
 * Snapshot da seleção real e vigente em vediums.com/ (Conhecimento Vedium):
 * mais recente em destaque + 2 secundários com categorias diferentes --
 * mesma regra determinística de vedium_core/vedium_core/v2_home_data.py
 * (get_insights_selection). Conteúdo real já publicado, não inventado.
 */
export const INSIGHTS_FEATURED: InsightCard = {
  title: "Curso de inglês com professor ao vivo: o que muda na evolução da fala",
  summary:
    "Entenda como um curso de inglês com professor ao vivo acelera a fala, corrige travas e melhora a conversação.",
  href: "/blog/ingles/curso-de-ingles-com-professor-ao-vivo-o-que-muda-na-evolucao-da-fala",
  category: "Inglês",
  date: "15 de julho de 2026",
};

export const INSIGHTS_SECONDARY: InsightCard[] = [
  {
    title: "Plano de 30 dias para começar iorubá com base sólida",
    summary:
      "Um roteiro para começar iorubá em 30 dias com fundamentos sólidos, respeito cultural e prática ao vivo.",
    href: "/blog/ioruba/plano-de-30-dias-para-comecar-ioruba-com-base-solida",
    category: "Iorubá",
    date: "3 de julho de 2026",
  },
  {
    title: "Como funciona a alfabetização em hebraico do zero",
    summary:
      "Entenda como funciona a alfabetização em hebraico do zero, com letras, sons, direção da leitura e aula ao vivo.",
    href: "/blog/hebraico/como-funciona-a-alfabetizacao-em-hebraico-do-zero",
    category: "Hebraico",
    date: "23 de abril de 2025",
  },
];
