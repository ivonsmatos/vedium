import type { LanguagePillarContent } from "@/types/language";
import { WHATSAPP_HREF } from "@/content/site/header";

const MEDIA_BASE = "/assets/vedium_core/v2/media/home/";

/**
 * Conteúdo real e validado para `/curso-de-ioruba-online`.
 *
 * Fontes:
 * - Hero/estudo/live class/cultura/FAQ (parcial): configuração aprovada no
 *   gate cultural da Fase D
 *   (`vedium_core/vedium_core/language_pillar_data.py::get_ioruba_pillar_config`).
 * - Níveis (nomes/URLs): `catalog_registry.CATALOG` + `course_urls.py`
 *   (mesmos 3 cursos reais: iorub-b-sico/intermedi-rio/avan-ado →
 *   /curso/ioruba-{basico,intermediario,avancado}, HTTP 200 confirmado).
 * - SEO (title/description/canonical/hreflang/OG) e 2 das 6 FAQs: página
 *   pública atual `https://vediums.com/curso-de-ioruba-online` (snapshot
 *   verificado nesta sessão — ver docs/frontend-v2/08-ioruba-seo-parity.md).
 * - Insights: 3 artigos reais de `/blog/ioruba` (blog_content.py), os mais
 *   recentes, nenhum de outro idioma.
 *
 * Sem seção de professor -- decisão de escopo (2026-08-29): nenhuma página
 * de curso exibe nome de professor individual (ver memória
 * feedback_no_teacher_name_on_course_pages).
 */
export const yoruba: LanguagePillarContent = {
  languageKey: "yoruba",
  displayName: "Iorubá",

  seo: {
    // title/description recuperados literalmente da página pública atual
    // (mesma URL, já indexada) -- "recuperados ou superados" (56-language-page-seo-contract.md).
    title: "Curso de Iorubá Online | Vedium",
    description:
      "Curso de iorubá online com aulas ao vivo, pronúncia, vocabulário, cultura e trilha estruturada para iniciantes.",
    canonical: "https://vediums.com/curso-de-ioruba-online",
    robots: "index, follow, max-image-preview:large",
    ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    hreflang: {
      "pt-br": "https://vediums.com/curso-de-ioruba-online",
      en: "https://vediums.com/en/learn-yoruba-online",
      es: "https://vediums.com/es/curso-de-yoruba-online",
      ru: "https://vediums.com/ru/kurs-yoruba-online",
      "x-default": "https://vediums.com/curso-de-ioruba-online",
    },
  },

  breadcrumb: [
    { label: "Início", href: "/" },
    { label: "Cursos de Idiomas", href: "/cursos-de-idiomas-online" },
    { label: "Curso de Iorubá Online", href: null },
  ],

  hero: {
    eyebrow: "CURSO DE IORUBÁ ONLINE",
    headline: "Entenda o que você fala, canta e escuta com profundidade.",
    support:
      "Estude Iorubá em aulas ao vivo, com progressão do básico ao avançado e uma abordagem estruturada que integra língua, oralidade, leitura, história e uso.",
    primaryCta: { text: "Conheça os níveis", href: "#niveis" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
    media: {
      // e11-ioruba-learning.jpg é retrato (1055x2000) -- num hero full-bleed
      // (viewport inteiro de largura) ficava estourado/borrado (object-fit:cover
      // upscalando uma fatia estreita). e10 é paisagem nativa 2000x1333, mesma
      // resolução dos outros slides de hero da Home -- sem upscale perceptível.
      src: MEDIA_BASE + "e10-notes-at-home.jpg",
      alt: "Estudante usando fones de ouvido, sorrindo, escreve em um caderno durante uma aula online.",
      width: 2000,
      height: 1333,
    },
  },

  studyPillars: {
    eyebrow: "ESTUDO DE IORUBÁ",
    headline: "Uma língua para estudar com estrutura, oralidade e profundidade.",
    rows: [
      { title: "COMEÇAR COM ESTRUTURA", text: "Do primeiro contato aos fundamentos do idioma." },
      { title: "PRONÚNCIA E TONS", text: "Compreender sons, padrões e oralidade com orientação." },
      { title: "LEITURA E VOCABULÁRIO", text: "Avançar na compreensão e no uso do idioma." },
      { title: "LÍNGUA E PRODUÇÃO CULTURAL", text: "Estudar expressões, textos, história e formas de uso." },
    ],
  },

  liveClass: {
    title: "Iorubá ao vivo, com prática e orientação.",
    points: [
      { label: "PRONÚNCIA", text: "Correção e orientação durante a aula." },
      { label: "ORALIDADE", text: "Uso do idioma em interação." },
      { label: "LEITURA", text: "Textos e estruturas trabalhados com acompanhamento." },
      { label: "PROGRESSÃO", text: "O percurso avança por níveis e competências." },
    ],
    media: {
      src: MEDIA_BASE + "e06-listening-online-course.jpg",
      alt: "Aula online ao vivo.",
      width: 2000,
      height: 1333,
    },
  },

  levels: {
    title: "Seu percurso em Iorubá.",
    lead: "Avançando do contato inicial à autonomia.",
    sequential: true,
    items: [
      {
        code: "basico",
        publicLabel: "Básico",
        title: "Iorubá Básico: primeiro contato estruturado.",
        competencySummary:
          "Introdução ao sistema fonológico, tons, saudações, vocabulário essencial e estruturas básicas de frase.",
        focuses: [
          "Sistema de tons do Iorubá",
          "Saudações e apresentações",
          "Estruturas básicas de frase",
          "Vocabulário do cotidiano",
        ],
        href: "/curso/ioruba-basico",
      },
      {
        code: "intermediario",
        publicLabel: "Intermediário",
        title: "Iorubá Intermediário: expressão e compreensão ampliadas.",
        competencySummary:
          "Expansão de vocabulário, textos mais elaborados, oralidade com maior fluência e leitura de materiais autênticos.",
        focuses: [
          "Conversação em situações variadas",
          "Leitura de textos autênticos",
          "Produção oral e escrita",
          "Contexto cultural e histórico",
        ],
        href: "/curso/ioruba-intermediario",
      },
      {
        code: "avancado",
        publicLabel: "Avançado",
        title: "Iorubá Avançado: autonomia e profundidade.",
        competencySummary: "Literatura, história, produção cultural e uso refinado do idioma em contextos formais e informais.",
        focuses: [
          "Análise de literatura Iorubá",
          "Discussão de temas culturais complexos",
          "Produção escrita avançada",
          "Compreensão de registros formais e informais",
        ],
        href: "/curso/ioruba-avancado",
      },
    ],
  },

  culture: {
    eyebrow: "IDIOMA E CULTURA",
    title: "Língua, oralidade, literatura e história fazem parte do mesmo percurso.",
    description:
      "Nossa abordagem integra os sentidos reais das palavras, as formas de expressão, a literatura e a história do Iorubá. Você entende não apenas como falar, mas o contexto que dá vida ao idioma.",
    media: {
      src: MEDIA_BASE + "e02-study-laptop.jpg",
      alt: "Estudo profundo da língua e cultura.",
      width: 2000,
      height: 1263,
    },
    relatedLink: { text: "Iorubá, cultura e ancestralidade", href: "/ioruba-cultura-e-ancestralidade" },
  },

  insights: {
    headline: "Aprofunde o estudo do Iorubá também fora da aula.",
    featured: {
      title: "Plano de 30 dias para começar iorubá com base sólida",
      summary: "Comece iorubá em 30 dias com base sólida, respeito cultural e prática ao vivo. Veja um plano seguro para iniciar do jeito certo.",
      href: "/blog/ioruba/plano-de-30-dias-para-comecar-ioruba-com-base-solida",
      category: "Iorubá",
      date: "3 de julho de 2026",
    },
    secondary: [
      {
        title: "Como avaliar se um conteúdo de iorubá é sério e responsável",
        summary: "Aprenda a avaliar se um conteúdo de iorubá é sério, responsável e respeitoso com a língua, a cultura e a tradição.",
        href: "/blog/ioruba/como-avaliar-se-um-conteudo-de-ioruba-e-serio-e-responsavel",
        category: "Iorubá",
        date: "26 de junho de 2026",
      },
      {
        title: "O papel do professor qualificado no ensino de iorubá",
        summary: "Entenda por que um professor qualificado é essencial para aprender Iorubá com respeito, profundidade cultural e domínio da tradição.",
        href: "/blog/ioruba/o-papel-do-professor-qualificado-no-ensino-de-ioruba",
        category: "Iorubá",
        date: "5 de junho de 2026",
      },
    ],
  },

  // 4 primeiras: validadas no gate cultural (language_pillar_data.py). 2
  // últimas: já publicadas e indexadas na página atual (JSON-LD FAQPage de
  // produção) -- inclui "O curso é religioso?", pergunta central de QA
  // cultural, preservada por completo.
  faq: [
    {
      question: "Preciso ter conhecimento prévio para começar?",
      answer: "Não. A trilha pode começar do zero, com foco em pronúncia e vocabulário inicial.",
    },
    {
      question: "O curso é religioso?",
      answer: "A proposta é educacional e linguística, com contexto cultural tratado com respeito.",
    },
    {
      question: "O curso trabalha pronúncia e tons?",
      answer: "Sim. A oralidade, os tons e as estruturas são focos centrais e praticados ativamente nas aulas ao vivo.",
    },
    {
      question: "Como funcionam os níveis?",
      answer: "A progressão é sequencial: Básico, Intermediário e Avançado. Cada um focado no seu momento atual de aprendizagem.",
    },
    {
      question: "Iorubá tem certificado?",
      answer: "Sim, conforme conclusão e requisitos do curso livre.",
    },
    {
      question: "Como sei por onde começar?",
      answer: "Você pode falar com a equipe e fazer o diagnóstico inicial antes da matrícula.",
    },
  ],

  finalCta: {
    headline: "Comece seu percurso em Iorubá.",
    support: "Conheça os níveis ou fale com a Vedium para entender por onde começar.",
    primaryCta: { text: "Conheça os níveis", href: "#niveis" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
  },
};
