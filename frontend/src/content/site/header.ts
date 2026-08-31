export interface HeaderCourseLink {
  label: string;
  href: string;
}

export interface LocaleOption {
  code: string;
  label: string;
  flag: string;
}

export const WHATSAPP_HREF = "https://wa.me/5511911293075?text=Ol%C3%A1%2C%20quero%20falar%20com%20a%20Vedium";
export const STUDENT_AREA_HREF = "https://app.vediums.com/login";
export const LEVEL_TEST_HREF = "/teste-de-nivel";

export const HEADER_COURSES: HeaderCourseLink[] = [
  { label: "Inglês", href: "/curso-de-ingles-online" },
  { label: "Iorubá", href: "/curso-de-ioruba-online" },
  { label: "Português para Estrangeiros", href: "/portugues-para-estrangeiros" },
  { label: "Espanhol", href: "/curso-de-espanhol-online" },
  { label: "Hebraico", href: "/curso-de-hebraico-online" },
];

export const LOCALE_OPTIONS: LocaleOption[] = [
  { code: "pt-br", label: "Português", flag: "🇧🇷" },
  { code: "en", label: "English", flag: "🌐" },
  { code: "es", label: "Español", flag: "🇪🇸" },
  { code: "fr", label: "Français", flag: "🇫🇷" },
  { code: "de", label: "Deutsch", flag: "🇩🇪" },
  { code: "ru", label: "Русский", flag: "🇷🇺" },
];

export const LOCALE_NAV_URLS: Record<string, string> = {
  "pt-br": "/",
  en: "/en/",
  es: "/es/",
  fr: "/fr/",
  de: "/de/",
  ru: "/ru/",
};

export const HEADER_MEGA_MEDIA_SRC = "/assets/vedium_core/v2/media/home/e02-study-laptop.jpg";

export const HEADER_NAV_TEXT_PT = {
  comoFunciona: "Como funciona",
  professores: "Professores",
  empresas: "Para empresas",
  blog: "Conteúdo",
  cursos: "Cursos",
  sobre: "Sobre",
  aluno: "Área do aluno",
  cursosHeading: "Idiomas",
  atalhosHeading: "Institucional",
  testeNivel: "Fazer teste de nível",
};

export interface PrimaryCtaOverride {
  text: string;
  href: string;
}
