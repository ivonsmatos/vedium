import type { LanguagePillarContent } from "@/types/language";
import { WHATSAPP_HREF } from "@/content/site/header";

const MEDIA_BASE = "/media/";

/**
 * Conteúdo real e validado para `/portugues-para-estrangeiros` (PLE).
 *
 * Fontes:
 * - SEO (title/description/canonical/hreflang/OG/JSON-LD) e 4 FAQs:
 *   página pública atual `https://vediums.com/portugues-para-estrangeiros`
 *   (snapshot verificado nesta sessão -- ver
 *   docs/frontend-v2/10-ple-seo-parity.md). Achado importante: `x-default`
 *   aponta pra versão EN (`/en/learn-portuguese-brazil`), não pt-BR --
 *   decisão real já em produção pra aquisição internacional, preservada.
 * - Níveis (3, Básico/Intermediário/Avançado -- sem CEFR granular por
 *   nível, embora o Course schema real diga "A1 a B2" como faixa geral):
 *   `course_urls.py` (`PLE_COURSE_TRACK` + `PLE_COURSE_NAV_I18N`),
 *   confirmado contra o HTML real das 3 páginas de nível.
 * - Teste de nível: PT usa a rota genérica `/teste-de-nivel` (PLE NÃO tem
 *   teste próprio em português -- só em outros locales,
 *   `PLE_LEVEL_TEST_URLS`), confirmado em `course_urls.py`.
 * - Hero/seções editoriais: copy dada literalmente pela missão da Fase D.3.
 *
 * SEM seção "Conhecimento Vedium": `blog_content.py` não tem NENHUM post
 * em pt-BR marcado pra português-para-estrangeiros -- o único conteúdo
 * real do tema está em EN (2 posts, categoria "Brazilian Portuguese") e FR
 * (1 post). Misturar idioma do blog com o locale da página violaria a
 * regra da própria missão (seção 3: "não misturar idiomas aleatoriamente
 * na mesma versão") e a regra geral de insights (nunca preencher com
 * conteúdo de outro idioma). `insights` fica ausente aqui de propósito --
 * ver docs/frontend-v2/10-ple-seo-parity.md.
 *
 * SEM seção de professor nomeado (mesma decisão já aplicada a Iorubá/
 * Inglês) -- mensagem institucional genérica entra como apoio da seção
 * "Aulas ao vivo".
 */
export const portugueseForForeigners: LanguagePillarContent = {
  languageKey: "portuguese_for_foreigners",
  displayName: "Português para Estrangeiros",

  seo: {
    title: "Português para Estrangeiros | Vedium",
    description: "Português para estrangeiros com aulas ao vivo para morar, trabalhar, estudar e se comunicar melhor no Brasil.",
    canonical: "https://vediums.com/portugues-para-estrangeiros",
    robots: "index, follow, max-image-preview:large",
    ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    hreflang: {
      "pt-br": "https://vediums.com/portugues-para-estrangeiros",
      en: "https://vediums.com/en/learn-portuguese-brazil",
      es: "https://vediums.com/es/portugues-para-extranjeros",
      fr: "https://vediums.com/fr/portugais-pour-etrangers",
      de: "https://vediums.com/de/portugiesisch-fuer-auslaender",
      ru: "https://vediums.com/ru/portugalskiy-dlya-inostrantsev",
      // x-default -> EN (não pt-BR): decisão real de produção, PLE é a
      // página com foco em aquisição internacional (mission seção 3).
      "x-default": "https://vediums.com/en/learn-portuguese-brazil",
    },
  },

  breadcrumb: [
    { label: "Início", href: "/" },
    { label: "Cursos de Idiomas", href: "/cursos-de-idiomas-online" },
    { label: "Português para Estrangeiros", href: null },
  ],

  hero: {
    eyebrow: "PORTUGUÊS PARA ESTRANGEIROS",
    headline: "Português para viver, trabalhar e se comunicar no Brasil.",
    support:
      "Aulas ao vivo para estrangeiros que querem desenvolver o português com prática, orientação e contato com situações reais da vida no Brasil.",
    primaryCta: { text: "Conheça o curso", href: "#niveis" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
    media: {
      src: MEDIA_BASE + "e14-ple-headphones-home.jpg",
      alt: "Pessoa adulta usando fones de ouvido estuda em um notebook, com uma estante de livros ao fundo.",
      width: 2000,
      height: 1263,
    },
  },

  studyPillars: {
    eyebrow: "PORTUGUÊS PARA A VIDA REAL",
    headline: "Aprender o idioma também é aprender a participar das situações do dia a dia.",
    rows: [
      { title: "CONVERSAS DO COTIDIANO", text: "Comunicar-se em situações reais com mais clareza." },
      { title: "TRABALHO", text: "Participar de reuniões, conversas e situações profissionais." },
      { title: "VIDA NO BRASIL", text: "Compreender usos, expressões e situações que fazem parte da rotina." },
      { title: "PROGRESSÃO", text: "Desenvolver competências passo a passo, de acordo com o seu nível." },
    ],
  },

  liveClass: {
    title: "Português ao vivo, com interação e orientação.",
    lead: "Aulas conduzidas por professores preparados para orientar estrangeiros no desenvolvimento do português em situações reais.",
    points: [
      { label: "CONVERSAÇÃO", text: "Prática do idioma durante a aula." },
      { label: "PRONÚNCIA", text: "Orientação para desenvolver clareza na comunicação." },
      { label: "COMPREENSÃO", text: "Escuta e interpretação em diferentes situações." },
      { label: "USO REAL", text: "Vocabulário e estruturas aplicados ao cotidiano no Brasil." },
    ],
    media: {
      src: MEDIA_BASE + "e14-ple-headphones-home.jpg",
      alt: "Pessoa adulta usando fones de ouvido escreve em um caderno em frente a um notebook, em um ambiente doméstico claro.",
      width: 1125,
      height: 2000,
    },
  },

  levels: {
    title: "Seu percurso em português.",
    lead: "Do primeiro contato à comunicação avançada, em três níveis confirmados contra a página real de cada curso.",
    sequential: true,
    items: [
      {
        code: "basico",
        publicLabel: "Básico",
        title: "Português para Estrangeiros: Nível Básico (PLE)",
        competencySummary: "Para quem está começando do zero. Aprenda saudações, vocabulário essencial e comunicação básica do português brasileiro com imersão cultural.",
        focuses: [],
        href: "/curso/portugues-para-estrangeiros-basico",
      },
      {
        code: "intermediario",
        publicLabel: "Intermediário",
        title: "Português para Estrangeiros: Nível Intermediário (PLE)",
        competencySummary: "Para estrangeiros que já têm base no português. Ganhe fluência em conversas sociais, profissionais e situações reais da vida no Brasil.",
        focuses: [],
        href: "/curso/portugues-para-estrangeiros-intermediario",
      },
      {
        code: "avancado",
        publicLabel: "Avançado",
        title: "Português para Estrangeiros: Nível Avançado (PLE)",
        competencySummary: "Para estrangeiros que já falam português e querem refinamento. Aperfeiçoe fluência, vocabulário, escrita, leitura e comunicação profissional.",
        focuses: [],
        href: "/curso/portugues-para-estrangeiros-avancado",
      },
    ],
  },

  culture: {
    eyebrow: "IDIOMA + CONTEXTO",
    title: "Português para compreender não apenas o que se diz, mas como o idioma é usado no Brasil.",
    description:
      "Trabalhamos formas de tratamento, situações cotidianas, registros mais formais e informais, expressões, comunicação profissional e leitura de situações sociais, sempre com rigor e profundidade, nunca como curiosidade turística.",
    media: {
      src: MEDIA_BASE + "e07-hero-videoconference.jpg",
      alt: "Pessoa adulta sorri conversando ao telefone, com um notebook aberto, em um ambiente urbano ao ar livre.",
      width: 2000,
      height: 1333,
    },
  },

  // "Aplicações" (mission seção 12) -- mesmo formato EditorialRows de
  // studyPillars (title+text), renderizado com o mesmo VediumMethod.
  applications: {
    eyebrow: "ONDE O PORTUGUÊS ENTRA NA SUA ROTINA",
    headline: "Situações reais em que o português faz diferença.",
    rows: [
      { title: "TRABALHO", text: "Comunicar-se com colegas, clientes e equipes." },
      { title: "SERVIÇOS E ROTINA", text: "Resolver situações cotidianas com mais autonomia." },
      { title: "ESTUDOS", text: "Participar de aulas, leituras e atividades acadêmicas quando aplicável." },
      { title: "RELAÇÕES SOCIAIS", text: "Compreender melhor conversas e formas de interação." },
    ],
  },

  // Sem `insights` -- ver nota grande no topo do arquivo (nenhum artigo
  // real em pt-BR pra este tema).

  // 4 primeiras: reais e indexadas na página atual (inclui "As aulas podem
  // ter apoio em inglês?", a pergunta que resolve diretamente a distinção
  // site-locale vs course-language pedida na missão). 4 últimas:
  // construídas só com fatos já confirmados em outras partes desta mesma
  // página/site (aulas ao vivo, conversação, nível básico do zero).
  faq: [
    {
      question: "As aulas podem ter apoio em inglês?",
      answer: "Sim. O professor pode usar apoio em inglês quando necessário, aumentando a prática em português progressivamente.",
    },
    {
      question: "É português do Brasil?",
      answer: "Sim. O foco é o português como falado no Brasil.",
    },
    {
      question: "Dá para me preparar para situações de trabalho?",
      answer: "Sim. Podemos incluir reuniões, e-mails, apresentações e vocabulário profissional do dia a dia.",
    },
    {
      question: "Preciso fazer o teste de nível?",
      answer: "O teste gratuito ajuda a estimar seu nível antes de recomendarmos uma trilha.",
    },
    {
      question: "As aulas são ao vivo?",
      answer: "Sim, sempre com professor em tempo real; não são videoaulas gravadas.",
    },
    {
      question: "O curso é voltado especificamente para estrangeiros?",
      answer: "Sim. A trilha é desenhada para quem aprende português como língua adicional, não para quem já é falante nativo.",
    },
    {
      question: "Vou praticar conversação?",
      answer: "Sim. A conversação faz parte das aulas ao vivo, junto com pronúncia, compreensão e uso real do idioma no cotidiano.",
    },
    {
      question: "Preciso já saber português para começar?",
      answer: "Não. O nível Básico foi desenhado para quem está começando do zero, com saudações e vocabulário essencial.",
    },
  ],

  finalCta: {
    headline: "Use o português com mais segurança na vida real.",
    support: "Conheça o curso ou fale com a Vedium para entender qual percurso faz sentido para você.",
    primaryCta: { text: "Conheça o curso", href: "#niveis" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
  },
};
