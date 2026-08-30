export interface HeroSlide {
  eyebrow: string;
  headline: string;
  support: string;
  ctaLabel: string;
  ctaHref: string;
  imageSrc: string;
  imageAlt: string;
  imageWidth: number;
  imageHeight: number;
  navLabel: string;
}

const MEDIA_BASE = "/assets/vedium_core/v2/media/home/";

export const HERO_SLIDES: HeroSlide[] = [
  {
    eyebrow: "Escola de idiomas online",
    headline: "Aprenda ao vivo. Avance com direção.",
    support:
      "Professores nativos e especialistas, aulas em tempo real e progressão organizada por nível.",
    ctaLabel: "Conheça os cursos",
    ctaHref: "/catalogo",
    imageSrc: MEDIA_BASE + "e06-listening-online-course.jpg",
    imageAlt:
      "Pessoa adulta assiste a uma aula online em um monitor, ouvindo com atenção e fazendo anotações em um caderno.",
    imageWidth: 2000,
    imageHeight: 1333,
    navLabel: "Vedium",
  },
  {
    eyebrow: "Inglês ao vivo",
    headline: "Inglês para avançar com segurança.",
    support: "Do A1 ao C1, com professor, prática e progressão por nível.",
    ctaLabel: "Conheça inglês",
    ctaHref: "/curso-de-ingles-online",
    imageSrc: MEDIA_BASE + "e02-study-laptop.jpg",
    imageAlt:
      "Pessoa adulta concentrada, usando fones de ouvido, estuda em um notebook e faz anotações em um caderno.",
    imageWidth: 2000,
    imageHeight: 1263,
    navLabel: "Inglês",
  },
  {
    eyebrow: "Português para estrangeiros",
    headline: "Portuguese for real life in Brazil.",
    support: "Live Portuguese for work, daily life and integration.",
    ctaLabel: "Discover Portuguese",
    ctaHref: "/portugues-para-estrangeiros",
    imageSrc: MEDIA_BASE + "e10-notes-at-home.jpg",
    imageAlt: "Pessoa adulta com fones de ouvido participa de uma aula online, escrevendo em um caderno.",
    imageWidth: 2000,
    imageHeight: 1333,
    navLabel: "Português",
  },
  {
    eyebrow: "Vedium para empresas",
    headline: "Idiomas para equipes que precisam se comunicar melhor.",
    support: "Programas ao vivo com diagnóstico, organização por nível e acompanhamento.",
    ctaLabel: "Para empresas",
    ctaHref: "/empresas",
    imageSrc: MEDIA_BASE + "e07-hero-videoconference.jpg",
    imageAlt:
      "Profissional adulto participa de uma videochamada em equipe, em um escritório, com colegas visíveis na tela.",
    imageWidth: 2000,
    imageHeight: 1333,
    navLabel: "Empresas",
  },
];
