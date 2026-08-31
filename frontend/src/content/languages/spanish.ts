import type { LanguagePillarContent } from "@/types/language";
import { WHATSAPP_HREF } from "@/content/site/header";

const MEDIA_BASE = "/media/";

/**
 * Conteúdo real e validado para `/curso-de-espanhol-online`.
 *
 * Fontes:
 * - SEO (title/description/canonical/OG) e JSON-LD: página pública atual
 *   (snapshot verificado nesta sessão -- ver
 *   docs/frontend-v2/11-spanish-seo-parity.md). Achado: hreflang real hoje
 *   é só pt-br(self) + x-default(self) -- SEM outros locales (diferente
 *   de Iorubá/Inglês/PLE) -- nenhum locale foi inventado aqui.
 * - Níveis (3, Básico/Intermediário/Avançado -- com faixa CEFR real por
 *   nível: A1-A2 / B1-B2.1 / B2.2-C1): `catalog_registry.py` +
 *   `course_urls.py`, confirmado contra o HTML real das 3 páginas de
 *   nível (title/H1/description recuperados literalmente).
 * - FAQs: 4 das 5 reais e indexadas na página atual (excluída a que cita
 *   preço, mesma regra já aplicada a Inglês/PLE) + 4 construídas só com
 *   fatos já confirmados em outras partes desta mesma página.
 * - Insights: SÓ 2 artigos reais existem no blog para Espanhol (não 3) --
 *   mostra 2, não inventa um terceiro (`InsightsEditorial.secondaryB`
 *   ficou opcional por causa deste caso real).
 *
 * SEM seção de professor nomeado (mesma decisão de Iorubá/Inglês/PLE) --
 * mensagem institucional genérica entra como apoio de "Aulas ao vivo".
 *
 * SEM seção "Espanhol em diferentes contextos" (mission seção 16,
 * explicitamente opcional -- "só inserir se o ritmo da página
 * justificar"): a página já tem duas seções dedicadas à relação
 * português-espanhol (seções 8 e 13 da missão); uma terceira lista de
 * "onde o idioma entra na rotina" seria redundante, não editorial.
 */
export const spanish: LanguagePillarContent = {
  languageKey: "spanish",
  displayName: "Espanhol",

  seo: {
    // title/description recuperados literalmente (inclui preço no
    // description/OG -- é metadado de crawler, não conteúdo visível da
    // página; a regra "sem preço em componente editorial" vale pro que é
    // renderizado, não pra meta tag). Ver nota na SEO parity doc.
    title: "Curso de Espanhol Online ao Vivo (Básico ao Avançado) | Vedium",
    description:
      "Curso de espanhol online ao vivo da Vedium: aulas com professor em tempo real, do Básico ao Avançado, foco em conversação e correção de portunhol. A partir de R$ 297/mês.",
    canonical: "https://vediums.com/curso-de-espanhol-online",
    robots: "index, follow, max-image-preview:large",
    ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    hreflang: {
      "pt-br": "https://vediums.com/curso-de-espanhol-online",
      "x-default": "https://vediums.com/curso-de-espanhol-online",
    },
  },

  breadcrumb: [
    { label: "Início", href: "/" },
    { label: "Cursos de Idiomas", href: "/cursos-de-idiomas-online" },
    { label: "Curso de Espanhol Online", href: null },
  ],

  hero: {
    eyebrow: "CURSO DE ESPANHOL ONLINE",
    headline: "Espanhol para comunicar com mais precisão.",
    support:
      "Aulas ao vivo com professores nativos e especialistas para desenvolver compreensão, pronúncia, vocabulário e uso do idioma de forma estruturada.",
    primaryCta: { text: "Conheça os níveis", href: "#niveis" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
    media: {
      src: MEDIA_BASE + "e12-espanhol-professora.jpg",
      alt: "Pessoa adulta assiste a uma aula online em um monitor, ouvindo com atenção e fazendo anotações em um caderno.",
      width: 2000,
      height: 1333,
    },
  },

  studyPillars: {
    eyebrow: "ALÉM DO PORTUNHOL",
    headline: "Proximidade com o português ajuda. Precisão exige estudo.",
    rows: [
      { title: "PRONÚNCIA", text: "Perceber e produzir sons do espanhol com mais clareza." },
      { title: "VOCABULÁRIO", text: "Ampliar repertório sem depender de adaptações do português." },
      { title: "ESTRUTURA", text: "Compreender diferenças gramaticais e formas reais de uso." },
      { title: "COMUNICAÇÃO", text: "Construir respostas com mais autonomia e precisão." },
    ],
  },

  liveClass: {
    title: "Espanhol ao vivo, com prática e correção durante a aula.",
    lead: "As aulas são conduzidas por professores preparados para orientar prática, correção e desenvolvimento do idioma ao longo do percurso.",
    points: [
      { label: "CONVERSAÇÃO", text: "Prática do idioma em interação." },
      { label: "PRONÚNCIA", text: "Orientação sobre sons, ritmo e produção oral." },
      { label: "COMPREENSÃO", text: "Contato com diferentes situações de comunicação." },
      { label: "CORREÇÃO", text: "Identificação de interferências do português e desenvolvimento de maior precisão." },
    ],
    media: {
      src: MEDIA_BASE + "e12-espanhol-professora.jpg",
      alt: "Pessoa adulta de cabelo cacheado usa óculos, concentrada, olhando para baixo.",
      width: 1125,
      height: 2000,
    },
  },

  levels: {
    title: "Seu percurso em espanhol.",
    lead: "Do primeiro contato à comunicação avançada, em três níveis confirmados contra a página real de cada curso.",
    sequential: true,
    items: [
      {
        code: "basico",
        publicLabel: "Básico",
        title: "Espanhol Nível Básico (A1-A2)",
        competencySummary: "Para quem quer começar espanhol do jeito certo. Aprenda saudações, frases essenciais, pronúncia, vocabulário e conversas básicas sem cair no portunhol.",
        focuses: [],
        href: "/curso/espanhol-basico",
      },
      {
        code: "intermediario",
        publicLabel: "Intermediário",
        title: "Espanhol Nível Intermediário (B1-B2.1)",
        competencySummary: "Para quem já entende espanhol, mas precisa falar melhor. Desenvolva conversação, narrativa, opinião, passado, subjuntivo e vocabulário mais natural.",
        focuses: [],
        href: "/curso/espanhol-intermediario",
      },
      {
        code: "avancado",
        publicLabel: "Avançado",
        title: "Espanhol Nível Avançado (B2.2-C1)",
        competencySummary: "Para quem já fala espanhol e quer refinar fluência. Trabalhe precisão, argumentação, apresentações, cultura e comunicação profissional avançada.",
        focuses: [],
        href: "/curso/espanhol-avancado",
      },
    ],
  },

  // "Para quem fala português" (mission seção 13) -- mesmo formato
  // EditorialRows de studyPillars, renderizado com o mesmo VediumMethod.
  applications: {
    eyebrow: "PORTUGUÊS E ESPANHOL",
    headline: "Idiomas próximos também têm diferenças que mudam a comunicação.",
    rows: [
      { title: "FALSOS COGNATOS", text: "Palavras parecidas podem ter sentidos diferentes." },
      { title: "PRONÚNCIA", text: "Sons semelhantes nem sempre são produzidos da mesma forma." },
      { title: "ESTRUTURA", text: "Construções naturais em português podem não funcionar em espanhol." },
      { title: "REGISTRO", text: "Escolhas de palavras variam conforme situação e contexto." },
    ],
  },

  culture: {
    eyebrow: "IDIOMA E CULTURA",
    title: "O espanhol muda conforme as pessoas, os lugares e as situações em que é usado.",
    description:
      "O espanhol tem diversidade linguística e cultural real: pronúncia, vocabulário, formas de tratamento e registros variam entre países e regiões. Não existe um único \"espanhol latino\", e a Espanha não é um padrão superior; são variedades diferentes, cada uma válida no seu contexto.",
    media: {
      src: MEDIA_BASE + "e02-study-laptop.jpg",
      alt: "Pessoa adulta usando fones de ouvido estuda em um notebook, sentada em um sofá, em um ambiente doméstico aconchegante.",
      width: 2000,
      height: 1333,
    },
  },

  insights: {
    headline: "Aprenda também fora da aula.",
    featured: {
      title: "Falsos cognatos em espanhol que mais confundem brasileiros",
      summary: "Conheça falsos cognatos em espanhol que confundem brasileiros e aprenda a evitar erros com prática ao vivo.",
      href: "/blog/espanhol/falsos-cognatos-em-espanhol-que-mais-confundem-brasileiros",
      category: "Espanhol",
      date: "2 de abril de 2025",
    },
    // Só 2 artigos reais existem -- sem terceiro (secondaryB fica ausente,
    // InsightsEditorial já suporta isso).
    secondary: [
      {
        title: "Por que brasileiro entende espanhol, mas trava para falar",
        summary: "Entenda por que brasileiros entendem espanhol, mas travam para falar, e como destravar com pronúncia, ritmo e aula ao vivo.",
        href: "/blog/espanhol/por-que-brasileiro-entende-espanhol-mas-trava-para-falar",
        category: "Espanhol",
        date: "24 de fevereiro de 2025",
      },
    ],
  },

  // 4 primeiras: reais e indexadas na página atual (exclui a que cita
  // preço). 4 últimas: construídas só com fatos já confirmados em outras
  // seções desta mesma página.
  faq: [
    {
      question: "As aulas são ao vivo ou gravadas?",
      answer: "Ao vivo, com professor em tempo real e turmas pequenas. Você pratica a fala e é corrigido na hora; não é videoaula gravada.",
    },
    {
      question: "Preciso já saber espanhol?",
      answer: "Não. O curso Básico (A1-A2) começa do zero; se você já tem alguma base, pode entrar direto no Intermediário ou Avançado.",
    },
    {
      question: "O curso ajuda a corrigir o portunhol?",
      answer: "Sim; a correção do professor em tempo real é focada exatamente nas interferências mais comuns do português: falsos cognatos, pronúncia e tempos verbais.",
    },
    {
      question: "Tem certificado?",
      answer: "Sim, ao concluir cada nível com presença mínima, projeto final e avaliação.",
    },
    {
      question: "As aulas são conduzidas por professor?",
      answer: "Sim, sempre com professor em tempo real, nunca videoaula gravada.",
    },
    {
      question: "Quais são os níveis do curso?",
      answer: "Básico (A1-A2), Intermediário (B1-B2.1) e Avançado (B2.2-C1), em ordem sequencial.",
    },
    {
      question: "O curso trabalha conversação?",
      answer: "Sim. A conversação é um dos focos centrais das aulas ao vivo, junto com pronúncia, compreensão e correção.",
    },
    {
      question: "Como saber por onde começar?",
      answer: "Fale com a equipe da Vedium para entender qual nível é mais adequado ao seu ponto de partida.",
    },
  ],

  finalCta: {
    headline: "Avance do entendimento à comunicação em espanhol.",
    support: "Conheça os níveis ou fale com a Vedium para entender qual percurso é adequado para você.",
    primaryCta: { text: "Conheça os níveis", href: "#niveis" },
    secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
  },
};
