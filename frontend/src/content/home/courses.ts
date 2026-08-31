export interface HomeCourse {
  slug: string;
  displayName: string;
  levelSummary: string;
  headline: string;
  description: string;
  url: string;
  ctaLabel: string;
  mediaSrc: string;
  mediaAlt: string;
  order: number;
  reverse: boolean;
  bandTone: "white" | "warm" | "alt";
  objectPosition: string;
}

const MEDIA_BASE = "/media/";

/**
 * Fonte editorial/curada -- espelha vedium_core/vedium_core/home_course_collection.py
 * (HOME_COURSE_COLLECTION). Mesma cópia/URLs/mídia já validados na fonte.
 */
export const HOME_COURSES: HomeCourse[] = [
  {
    slug: "ingles",
    displayName: "Inglês",
    levelSummary: "Do A1 ao C1",
    headline: "Inglês para avançar no trabalho, nos estudos e na comunicação.",
    description: "Aulas ao vivo com professor, prática de conversação e progressão clara por nível.",
    url: "/curso-de-ingles-online",
    ctaLabel: "Conheça o curso",
    mediaSrc: MEDIA_BASE + "e02-study-laptop.jpg",
    mediaAlt: "Pessoa adulta concentrada, usando fones de ouvido, estuda em um notebook e faz anotações em um caderno.",
    order: 1,
    reverse: false,
    bandTone: "white",
    objectPosition: "center",
  },
  {
    slug: "ioruba",
    displayName: "Iorubá",
    levelSummary: "Básico ao avançado",
    headline: "Língua, oralidade, literatura e história.",
    description:
      "Iorubá ensinado com profundidade linguística e seriedade cultural, do primeiro contato à leitura avançada.",
    url: "/curso-de-ioruba-online",
    ctaLabel: "Conheça o curso",
    mediaSrc: MEDIA_BASE + "e11-ioruba-learning.jpg",
    mediaAlt: "Pessoa adulta negra, em ambiente profissional, digita em um notebook.",
    order: 2,
    reverse: true,
    bandTone: "warm",
    objectPosition: "center 15%",
  },
  {
    slug: "portugues-para-estrangeiros",
    displayName: "Português para Estrangeiros",
    levelSummary: "Portuguese for life in Brazil",
    headline: "Português para viver, trabalhar, estudar e se comunicar no Brasil.",
    description: "Aulas ao vivo para quem precisa se comunicar em português no dia a dia brasileiro.",
    url: "/portugues-para-estrangeiros",
    ctaLabel: "Explore o programa",
    mediaSrc: MEDIA_BASE + "e14-ple-headphones-home.jpg",
    mediaAlt:
      "Pessoa adulta usando fones de ouvido escreve em um caderno em frente a um notebook, em um ambiente doméstico claro.",
    order: 3,
    reverse: false,
    bandTone: "alt",
    objectPosition: "center 20%",
  },
  {
    slug: "espanhol",
    displayName: "Espanhol",
    levelSummary: "Comunicação com precisão",
    headline: "Do desenvolvimento inicial à comunicação profissional e cotidiana.",
    description:
      "Espanhol para quem quer sair do português misturado com espanhol e comunicar com clareza e confiança.",
    url: "/curso-de-espanhol-online",
    ctaLabel: "Conheça o curso",
    mediaSrc: MEDIA_BASE + "e12-espanhol-professora.jpg",
    mediaAlt: "Pessoa adulta de cabelo cacheado usa óculos, concentrada, olhando para baixo.",
    order: 4,
    reverse: true,
    bandTone: "white",
    objectPosition: "center 20%",
  },
  {
    slug: "hebraico",
    displayName: "Hebraico",
    levelSummary: "Escolha sua trilha",
    headline: "Alfabetização, Hebraico Moderno e leitura bíblica orientada.",
    description: "Aulas particulares e trilhas específicas conforme seu objetivo com o idioma.",
    url: "/curso-de-hebraico-online",
    ctaLabel: "Conheça as trilhas",
    mediaSrc: MEDIA_BASE + "e13-hebraico-headphones.jpg",
    mediaAlt: "Pessoa adulta usando fones de ouvido participa de uma aula online, sorrindo, em frente a um notebook.",
    order: 5,
    reverse: false,
    bandTone: "alt",
    objectPosition: "center",
  },
];

export const COURSE_INDEX_ENTRIES = HOME_COURSES.map((course) => ({
  name: course.displayName,
  href: course.url,
}));

export const COURSE_INDEX_EYEBROW = "Nossos cursos";
export const COURSE_INDEX_TITLE = "Cinco idiomas. Cursos organizados por nível e objetivo.";
export const COURSE_INDEX_LEAD = "Escolha o idioma e conheça os níveis, formatos e possibilidades de aprendizagem.";
