export interface FooterLink {
  label: string;
  href: string;
}

export const FOOTER_BRAND_SIGNATURE = "Escola de idiomas online com aulas ao vivo e progressão por nível.";

export const FOOTER_COURSE_LINKS: FooterLink[] = [
  { label: "Inglês", href: "/curso-de-ingles-online" },
  { label: "Iorubá", href: "/curso-de-ioruba-online" },
  { label: "Português para Estrangeiros", href: "/portugues-para-estrangeiros" },
  { label: "Espanhol", href: "/curso-de-espanhol-online" },
  { label: "Hebraico", href: "/curso-de-hebraico-online" },
];

export const FOOTER_VEDIUM_LINKS: FooterLink[] = [
  { label: "Sobre", href: "/sobre" },
  { label: "Professores", href: "/professores" },
  { label: "Como funciona", href: "/como-funciona" },
  { label: "Blog", href: "/blog" },
  { label: "Para empresas", href: "/empresas" },
];

export const FOOTER_HELP_LINKS: FooterLink[] = [
  { label: "FAQ", href: "/faq" },
  { label: "Contato", href: "/contato" },
  { label: "Descubra seu nível", href: "/teste-de-nivel" },
];

export const FOOTER_LEGAL_LINKS: FooterLink[] = [
  { label: "Privacidade", href: "/privacidade" },
  { label: "Termos", href: "/termos" },
  { label: "Cancelamento/reembolso", href: "/cancelamento-reembolso" },
];

export const FOOTER_SEO_GROUPS: { heading: string; links: FooterLink[] }[] = [
  {
    heading: "Vedium online para você",
    links: [
      { label: "Curso de inglês online", href: "/curso-de-ingles-online" },
      { label: "Inglês para entrevista", href: "/ingles-para-entrevista" },
      { label: "Inglês para tecnologia", href: "/ingles-para-programadores" },
      { label: "Inglês executivo", href: "/ingles-executivo" },
      { label: "Inglês para viagens", href: "/ingles-para-viagens" },
      { label: "Português para estrangeiros", href: "/portugues-para-estrangeiros" },
      { label: "Curso de iorubá online", href: "/curso-de-ioruba-online" },
      { label: "Preparatório Celpe-Bras", href: "/preparatorio-celpe-bras" },
    ],
  },
  {
    heading: "Conteúdos gratuitos",
    links: [
      { label: "Blog da Vedium", href: "/blog" },
      { label: "Aprender iorubá: língua e cultura", href: "/blog/aprender-ioruba-lingua-e-cultura" },
      { label: "Quanto custa e vale a pena", href: "/quanto-custa-curso-de-idiomas" },
      { label: "Teste de inglês", href: "/teste-de-nivel-ingles" },
    ],
  },
  {
    heading: "Conteúdos e oportunidades",
    links: [
      { label: "Indique a Vedium", href: "/programa-de-indicacao" },
      { label: "Parcerias", href: "/parcerias" },
      { label: "Trabalhe conosco", href: "/carreiras" },
      { label: "Treinamento para empresas", href: "/empresas" },
      { label: "Comunidade por idioma", href: "/comunidade" },
      { label: "Matrícula", href: "/matricula" },
    ],
  },
];

export const FOOTER_SOCIAL_LINKS = [
  { label: "Instagram", href: "https://www.instagram.com/vediumsglobal/", icon: "instagram" },
  { label: "LinkedIn", href: "https://www.linkedin.com/company/vediums", icon: "linkedin" },
];

export const FOOTER_BOTTOM_LEFT =
  "VEDIUM GLOBAL EDUCAÇÃO E TECNOLOGIA LTDA · CNPJ 58.434.869/0001-24 · Brasil · Atendimento 100% Online";
export const FOOTER_WHATSAPP_NUMBER = "+55 (11) 91129-3075";
