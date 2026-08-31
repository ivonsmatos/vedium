import type { LanguagePillarContent } from "@/types/language";
import { WHATSAPP_HREF } from "@/content/site/header";

const MEDIA_BASE = "/media/";

/**
 * Único trecho em escrita hebraica real da página -- "alef-bet" (o nome
 * do próprio alfabeto), usado na seção "Hebraico Moderno". Marcado com
 * lang="he" dir="rtl" SÓ neste span (missão seção 34); a página inteira
 * continua LTR/pt-BR. Não é um tipo do contrato genérico
 * (LanguagePillarContent) porque é específico de idiomas com escrita
 * própria -- não reutilizável por Iorubá/Inglês/PLE/Espanhol.
 */
export const alefBetSample = { hebrewScript: "אלף־בית", transliteration: "alef-bet" };

/**
 * Conteúdo real e validado para `/curso-de-hebraico-online`.
 *
 * ACHADO IMPORTANTE (ver docs/frontend-v2/12-hebrew-seo-parity.md):
 * a página-pilar atual em produção está desatualizada em relação ao
 * catálogo real. O FAQPage ao vivo hoje responde "Existe hebraico
 * bíblico na Vedium?" com "Ainda não; o piloto atual é só Hebraico
 * Moderno A1" -- mas as 5 páginas de curso abaixo estão TODAS live,
 * completas e reais (HTTP 200, título/H1/description próprios,
 * confirmado nesta sessão):
 *   - /curso/hebraico-a0-alfabetizacao
 *   - /curso/hebraico-moderno-a1
 *   - /curso/hebraico-moderno-a2-b1
 *   - /curso/hebraico-biblico-leitura-guiada
 *   - /curso/hebraico-particular
 * Este arquivo reflete o catálogo REAL (5 páginas confirmadas), não o
 * FAQ desatualizado da página-pilar antiga -- é uma correção, não uma
 * invenção (toda trilha usada aqui tem página própria, ao vivo, HTTP 200).
 *
 * `course_urls.py` confirma que Hebraico NÃO é uma trilha sequencial
 * única: são produtos distintos (Alfabetização / Moderno A1 / Moderno
 * A2-B1 / Bíblico / Particular). A progressão sequencial real (A0→A1→
 * A2/B1) existe SÓ dentro do percurso Moderno -- Bíblico e Particular são
 * percursos paralelos, não "níveis" depois do A2/B1.
 *
 * SEM seção de professor nomeado (mesma decisão de Iorubá/Inglês/PLE/
 * Espanhol) -- mas esta página TEM uma seção institucional curta e
 * genérica (`editorialNotes`), pedida explicitamente pela missão como
 * capítulo próprio "Professores/Abordagem", sem nome/foto/credencial
 * inventada.
 */
export const hebrew: LanguagePillarContent = {
  languageKey: "hebrew",
  displayName: "Hebraico",

  seo: {
    // title/description recuperados literalmente da página pública atual
    // (mesmos "recuperados ou superados" das páginas anteriores) --
    // mesmo estando parcialmente desatualizados quanto ao catálogo (não
    // mencionam Bíblico/Particular), preservam o sinal já indexado; o
    // H1 e o conteúdo visível é que trazem a cobertura completa e real.
    title: "Curso de Hebraico Online ao Vivo (com Alfabetização) | Vedium",
    description: "Curso de hebraico moderno online ao vivo da Vedium: alfabetização incluída, turma pequena, professor especialista. A partir de R$ 397/mês.",
    canonical: "https://vediums.com/curso-de-hebraico-online",
    robots: "index, follow, max-image-preview:large",
    ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    // Mesmo contrato mínimo já aprovado no Espanhol -- nenhum locale
    // internacional existe hoje para Hebraico.
    hreflang: {
      "pt-br": "https://vediums.com/curso-de-hebraico-online",
      "x-default": "https://vediums.com/curso-de-hebraico-online",
    },
  },

  breadcrumb: [
    { label: "Início", href: "/" },
    { label: "Cursos de Idiomas", href: "/cursos-de-idiomas-online" },
    { label: "Curso de Hebraico Online", href: null },
  ],

  hero: {
    eyebrow: "CURSO DE HEBRAICO ONLINE",
    headline: "Hebraico para diferentes percursos de estudo.",
    support:
      "Aulas ao vivo para quem quer começar pelo alfabeto, desenvolver Hebraico Moderno, avançar na leitura ou seguir um percurso de Hebraico Bíblico.",
    primaryCta: { text: "Conheça os percursos", href: "#percursos" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
    media: {
      // e13 (hebraico-headphones) é retrato nativo (1080x1920) -- num hero
      // full-bleed ficaria estourado/borrado (mesmo achado já corrigido no
      // Hero de Iorubá). Paisagem nativa 2000x1336, sem upscale.
      src: MEDIA_BASE + "e13-hebraico-headphones.jpg",
      alt: "Pessoa adulta concentrada faz a leitura de um livro aberto, em um ambiente doméstico iluminado e aconchegante.",
      width: 2000,
      height: 1336,
    },
  },

  // "Escolha seu percurso" -- a seção mais importante da página (missão
  // seção 8). 4 opções reais, cada uma com página própria (exceto
  // "Hebraico Moderno", que é um conceito com 2 níveis -- aponta para a
  // âncora #moderno desta mesma página, não para uma URL só).
  tracks: {
    eyebrow: "ESCOLHA SEU PERCURSO",
    headline: "O ponto de partida depende do que você quer desenvolver em Hebraico.",
    items: [
      {
        title: "PRIMEIRO CONTATO",
        text: "Para quem precisa começar pelo alfabeto, sons e leitura inicial.",
        href: "/curso/hebraico-a0-alfabetizacao",
        ctaLabel: "Conheça a Alfabetização (A0)",
      },
      {
        title: "HEBRAICO MODERNO",
        text: "Para desenvolver compreensão, leitura e comunicação no idioma contemporâneo.",
        href: "#moderno",
        ctaLabel: "Conheça o percurso Moderno",
      },
      {
        title: "HEBRAICO BÍBLICO",
        text: "Para quem busca um percurso de leitura orientada de textos bíblicos.",
        href: "#biblico",
        ctaLabel: "Conheça o Hebraico Bíblico",
      },
      {
        title: "AULA PARTICULAR",
        text: "Para objetivos, ritmo ou necessidades que pedem acompanhamento individual.",
        href: "#particular",
        ctaLabel: "Conheça o Hebraico Particular",
      },
    ],
  },

  liveClass: {
    title: "Hebraico ao vivo, com orientação durante cada etapa.",
    lead: "Professores preparados para orientar leitura, pronúncia e progressão em Hebraico, do primeiro contato ao percurso avançado.",
    points: [
      { label: "LEITURA", text: "Desenvolvimento progressivo do reconhecimento e leitura do idioma." },
      { label: "PRONÚNCIA", text: "Orientação sobre sons, palavras e produção oral." },
      { label: "ESTRUTURA", text: "Compreensão das formas e construções do idioma." },
      { label: "ACOMPANHAMENTO", text: "Correção e orientação ao longo do percurso." },
    ],
    media: {
      src: MEDIA_BASE + "e13-hebraico-headphones.jpg",
      alt: "Pessoa adulta com fones de ouvido participa de uma aula online, escrevendo em um caderno.",
      width: 2000,
      height: 1333,
    },
  },

  // "Hebraico Moderno" -- capítulo editorial próprio (missão seção 10).
  // O alef-bet (אלף-בית) é citado no idioma original, marcado com
  // lang="he" dir="rtl" só no trecho (missão seção 34) -- sem RTL na
  // página inteira.
  culture: {
    eyebrow: "HEBRAICO MODERNO",
    title: "Do alfabeto ao uso contemporâneo do idioma.",
    description:
      "O percurso de Hebraico Moderno cobre o alfabeto, leitura, vocabulário, compreensão e estruturas da língua, avançando para comunicação em situações contemporâneas. É um percurso distinto do Hebraico Bíblico, com a mesma raiz mas usos diferentes.",
    media: {
      src: MEDIA_BASE + "e02-study-laptop.jpg",
      alt: "Pessoa adulta concentrada, usando fones de ouvido, estuda em um notebook e faz anotações em um caderno.",
      width: 2000,
      height: 1263,
    },
  },

  levels: {
    title: "Progressão do Hebraico Moderno.",
    lead: "Do primeiro contato com o alfabeto à comunicação com maior autonomia, em três etapas confirmadas contra a página real de cada curso.",
    sequential: true,
    items: [
      {
        code: "a0",
        publicLabel: "A0",
        title: "Hebraico A0 Alfabetização",
        competencySummary: "Para quem nunca leu hebraico. Aprenda o alef-bet, reconheça letras e sons, leia palavras iniciais e dê o primeiro passo com segurança.",
        focuses: [],
        href: "/curso/hebraico-a0-alfabetizacao",
      },
      {
        code: "a1",
        publicLabel: "A1",
        title: "Hebraico Moderno Nível A1",
        competencySummary: "Para começar no hebraico moderno. Desenvolva leitura inicial, pronúncia, vocabulário essencial e frases simples do cotidiano com professor ao vivo.",
        focuses: [],
        href: "/curso/hebraico-moderno-a1",
      },
      {
        code: "a2-b1",
        publicLabel: "A2/B1",
        title: "Hebraico Moderno Nível A2/B1",
        competencySummary: "Para quem já tem base no hebraico. Amplie leitura, vocabulário, conversação e autonomia para falar de experiências, planos e situações reais.",
        focuses: [],
        href: "/curso/hebraico-moderno-a2-b1",
      },
    ],
  },

  // "Hebraico Bíblico" -- capítulo separado (missão seção 13). Nome
  // oficial confirmado: "Hebraico Bíblico -- Leitura Guiada". Nenhuma
  // promessa de exegese/interpretação teológica (não confirmado no
  // material da página real).
  secondaryFeature: {
    eyebrow: "HEBRAICO BÍBLICO",
    title: "Leitura orientada para quem quer estudar textos bíblicos em Hebraico.",
    description:
      "O percurso Hebraico Bíblico – Leitura Guiada trabalha vocabulário, estrutura, leitura guiada e contexto linguístico de textos bíblicos, de forma responsável. É um percurso de estudo linguístico, separado do Hebraico Moderno. Nenhum dos dois é \"mais correto\" ou superior ao outro; cada um atende a objetivos diferentes.",
    media: {
      src: MEDIA_BASE + "e16-liveclass-teacher-poster.jpg",
      alt: "Pessoa adulta lê um livro à mesa, com uma aula online aberta no notebook ao lado, em um escritório com estante de livros.",
      width: 1672,
      height: 941,
    },
    relatedLink: { text: "Conheça o Hebraico Bíblico – Leitura Guiada", href: "/curso/hebraico-biblico-leitura-guiada" },
  },

  // A comparação "Moderno x Bíblico" (missão seção 14) foi retirada como
  // secao isolada: com so 2 itens, o VediumMethod (feito pra ate 4) sobrava
  // muito espaco vazio na coluna direita (feedback do usuario, 2026-08-29).
  // O conteudo da comparacao continua coberto, sem perda de informacao, em
  // `culture.description` + `secondaryFeature.description` (cada trilha ja
  // se define em relacao a outra) e na FAQ ("Qual a diferenca entre
  // Hebraico Moderno e Hebraico Biblico?").

  insights: {
    headline: "Aprenda também fora da aula.",
    featured: {
      title: "Como funciona a alfabetização em hebraico do zero",
      summary: "Entenda como funciona a alfabetização em hebraico do zero, com letras, sons, direção da leitura e aula ao vivo.",
      href: "/blog/hebraico/como-funciona-a-alfabetizacao-em-hebraico-do-zero",
      category: "Hebraico",
      date: "23 de abril de 2025",
    },
    secondary: [
      {
        title: "Hebraico moderno x hebraico bíblico: entenda a diferença",
        summary: "Entenda a diferença entre hebraico moderno e bíblico, quando estudar cada um e como a aula ao vivo ajuda iniciantes.",
        href: "/blog/hebraico/hebraico-moderno-x-hebraico-biblico-entenda-a-diferenca",
        category: "Hebraico",
        date: "14 de março de 2025",
      },
    ],
  },

  // "Hebraico Particular" (missão seção 15, capítulo curto, sem preço) e
  // "Professores/Abordagem" (missão seção 16, institucional, sem nome).
  editorialNotes: [
    {
      eyebrow: "HEBRAICO PARTICULAR",
      title: "Um percurso individual para objetivos específicos.",
      text: "Aulas 1:1 com acompanhamento individual, ajustadas a objetivos, ritmo e necessidades específicas: alfabetização, Hebraico Moderno, leitura ou conversação, conforme o seu percurso dentro do que a Vedium oferece hoje.",
      cta: { text: "Conheça o Hebraico Particular", href: "/curso/hebraico-particular" },
    },
    {
      eyebrow: "PROFESSORES E ABORDAGEM",
      title: "Orientação preparada para cada etapa do percurso.",
      text: "As aulas são conduzidas por professores preparados para orientar leitura, pronúncia, estrutura e progressão, do primeiro contato com o alfabeto ao percurso de Hebraico Bíblico ou Moderno mais avançado.",
    },
  ],

  // 4 primeiras: reais, indexadas na página atual -- exceto a de Bíblico,
  // corrigida (ver nota grande no topo do arquivo: a resposta antiga
  // dizia "ainda não", desatualizada frente ao catálogo real de 5 cursos
  // live). 4 últimas: construídas só com fatos confirmados nesta mesma
  // página.
  faq: [
    {
      question: "Preciso saber o alfabeto antes de começar?",
      answer: "Não. A alfabetização (leitura do alef-bet) está incluída na turma de Hebraico Moderno A1, ou você pode começar pelo curso específico de Alfabetização (A0).",
    },
    {
      question: "O curso é religioso?",
      answer: "Não. A proposta é linguística e cultural; hebraico moderno como língua viva, sem viés religioso ou político.",
    },
    {
      question: "As aulas são ao vivo?",
      answer: "Sim, sempre com professor em tempo real e turma pequena.",
    },
    {
      question: "Qual a diferença entre Hebraico Moderno e Hebraico Bíblico?",
      answer: "Hebraico Moderno foca no idioma contemporâneo (leitura, compreensão, comunicação). Hebraico Bíblico foca em leitura orientada e compreensão linguística de textos bíblicos. São percursos diferentes, nenhum superior ao outro.",
    },
    {
      question: "Existe curso para quem está começando do zero?",
      answer: "Sim. O curso Hebraico A0 Alfabetização foi desenhado para quem nunca leu hebraico, começando pelo alef-bet.",
    },
    {
      question: "Quais são os níveis de Hebraico Moderno?",
      answer: "A progressão do Hebraico Moderno vai de A0 (Alfabetização) a A1 e depois A2/B1, em ordem sequencial.",
    },
    {
      question: "Como funciona o Hebraico Bíblico – Leitura Guiada?",
      answer: "Trabalha vocabulário, estrutura, leitura guiada e contexto linguístico de textos bíblicos, com acompanhamento do professor.",
    },
    {
      question: "Posso fazer aulas particulares?",
      answer: "Sim. O Hebraico Particular oferece aulas 1:1 com acompanhamento individual, conforme seu objetivo e ritmo.",
    },
  ],

  finalCta: {
    headline: "Encontre o percurso de Hebraico adequado ao seu objetivo.",
    support: "Conheça as opções de estudo ou fale com a Vedium para entender por onde começar.",
    primaryCta: { text: "Conheça os percursos", href: "#percursos" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
  },
};
