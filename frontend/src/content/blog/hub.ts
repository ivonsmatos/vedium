import { HEADER_COURSES } from "@/content/site/header";

/**
 * Conteúdo do hub /blog (missão F.5 seção 11). Só 1 artigo migrado nesta
 * fase (ver content/blog/index.ts) -- "últimos conteúdos" mostra o que
 * existe de verdade, sem preencher com placeholders (mesma disciplina de
 * "mostrar menos quando o conteúdo real é escasso" já usada em fases
 * anteriores, ex.: Espanhol com 2 artigos em vez de forçar 3).
 */
export const BLOG_HUB_SEO = {
  title: "Blog da Vedium: idiomas, cultura e aprendizado",
  description:
    "Conteúdos sobre inglês, espanhol, hebraico, iorubá e português para estrangeiros, com dicas práticas, cultura, aprendizagem online e orientação para quem estuda idiomas com aulas ao vivo.",
  canonical: "https://vediums.com/blog",
  robots: "index, follow, max-image-preview:large",
  ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
  hreflang: {
    "pt-br": "https://vediums.com/blog",
    "x-default": "https://vediums.com/blog",
  },
};

export const BLOG_HUB_INTRO = {
  eyebrow: "BLOG DA VEDIUM",
  title: "Idiomas, cultura e aprendizado.",
  support: "Conteúdos práticos sobre inglês, iorubá, português para estrangeiros, espanhol e hebraico, para quem estuda ou está decidindo por onde começar.",
};

export const BLOG_EXPLORE_BY_LANGUAGE = HEADER_COURSES.map((course) => ({ name: course.label, href: course.href }));

export const BLOG_B2B_NOTE = {
  text: "Para empresas, a Vedium também estrutura programas de idiomas voltados ao desenvolvimento de equipes.",
  ctaText: "Conheça a Vedium para Empresas",
  ctaHref: "/empresas",
};

export const BLOG_FINAL_CTA = {
  headline: "Encontre o percurso adequado para você.",
  support: "Conheça os cursos da Vedium e veja como começar de acordo com o idioma e o seu momento de aprendizagem.",
  primaryCta: { text: "Conheça os cursos", href: "/cursos-de-idiomas-online" },
  secondaryCta: { text: "Como funciona", href: "/como-funciona" },
};
