import type { LanguagePillarContent } from "@/types/language";
import { PROGRESSION_STEPS } from "@/content/home/progression";

const MEDIA_BASE = "/media/";
const LEVEL_TEST_HREF = "/teste-de-nivel-ingles";

/**
 * Conteúdo real e validado para `/curso-de-ingles-online`.
 *
 * Fontes:
 * - Hero/"Por onde começar"/Live/Objetivos: copy dada literalmente pela
 *   missão da Fase D.2 (já alinhada ao tom de voz aprovado).
 * - Níveis (6, A1/A2/A2+/B1/B2/C1 -- NÃO "B1+"): `course_urls.py`
 *   (`ENGLISH_COURSE_LEVELS` + `ENGLISH_COURSE_NAV_LABELS`), confirmado
 *   contra o HTML real de produção de cada uma das 6 páginas de nível
 *   (title/H1/meta description recuperados literalmente). Achado: existe
 *   um `catalog_registry.py` com o MESMO curso rotulado "Inglês B1+" —
 *   divergência real entre fontes internas, documentada e resolvida a
 *   favor do dado confirmado no HTML ao vivo. Ver
 *   docs/frontend-v2/09-english-seo-parity.md.
 * - Objetivos (Executivo/Viagens/Entrevista/Programadores): 4 páginas
 *   reais e validadas (HTTP 200), title/H1/description recuperados
 *   literalmente. "Comunicação cotidiana"/"Estudos" da sugestão da missão
 *   não têm página própria confirmada -- não incluídas (não inventar rota).
 * - SEO (title/description/canonical/hreflang/OG) e FAQs: página pública
 *   atual `https://vediums.com/curso-de-ingles-online` (snapshot
 *   verificado nesta sessão).
 * - Insights: 3 artigos reais de `/blog/ingles` (blog_content.py), os mais
 *   recentes.
 * - Progressão (conceito abstrato): mesmo conteúdo já usado na Home
 *   (`@/content/home/progression`), reaproveitado -- não é dado específico
 *   de Inglês, é o mesmo conceito institucional em toda a plataforma.
 *
 * Sem seção de professor (decisão de escopo 2026-08-29, ver memória
 * feedback_no_teacher_name_on_course_pages) -- a mensagem institucional
 * genérica sobre professores entra como apoio da seção "Aulas ao vivo".
 */
export const english: LanguagePillarContent = {
  languageKey: "english",
  displayName: "Inglês",

  seo: {
    title: "Curso de Inglês Online ao Vivo do A1 ao C1 | Vedium",
    description: "Aulas de inglês online ao vivo, turmas pequenas e progressão do A1 ao C1. Faça o teste de nível grátis.",
    canonical: "https://vediums.com/curso-de-ingles-online",
    robots: "index, follow, max-image-preview:large",
    ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    hreflang: {
      "pt-br": "https://vediums.com/curso-de-ingles-online",
      en: "https://vediums.com/en/learn-english-online",
      es: "https://vediums.com/es/curso-de-ingles-online-en-vivo",
      fr: "https://vediums.com/fr/cours-anglais-en-ligne-en-direct",
      de: "https://vediums.com/de/englischkurs-online-live",
      ru: "https://vediums.com/ru/kurs-angliyskogo-online",
      "x-default": "https://vediums.com/curso-de-ingles-online",
    },
  },

  breadcrumb: [
    { label: "Início", href: "/" },
    { label: "Cursos de Idiomas", href: "/cursos-de-idiomas-online" },
    { label: "Inglês", href: null },
  ],

  hero: {
    eyebrow: "CURSO DE INGLÊS ONLINE",
    headline: "Inglês para avançar com segurança.",
    support:
      "Aulas ao vivo, professores nativos e especialistas e uma progressão organizada por nível para você desenvolver o idioma com prática e acompanhamento.",
    primaryCta: { text: "Descubra seu nível", href: LEVEL_TEST_HREF },
    secondaryCta: { text: "Conheça o curso", href: "#niveis" },
    media: {
      src: MEDIA_BASE + "e02-study-laptop.jpg",
      alt: "Pessoa adulta concentrada, usando fones de ouvido, estuda em um notebook e faz anotações em um caderno.",
      width: 2000,
      height: 1263,
    },
  },

  studyPillars: {
    eyebrow: "SEU PONTO DE PARTIDA",
    headline: "Seu nível é definido pelo que você consegue fazer em inglês.",
    lead: "O tempo de estudo, sozinho, não determina o nível. A progressão parte das competências que você já consegue utilizar e do que precisa desenvolver a seguir.",
    rows: [
      { title: "ENTENDA SEU NÍVEL", text: "Identifique as competências que você já consegue utilizar." },
      { title: "COMECE NO PONTO CERTO", text: "Entre em um percurso adequado à sua etapa atual." },
      { title: "PRATIQUE", text: "Use o inglês durante aulas ao vivo." },
      { title: "AVANCE", text: "Acompanhe competências e próximos passos ao longo dos níveis." },
    ],
    cta: { text: "Faça o teste de nível", href: LEVEL_TEST_HREF },
  },

  liveClass: {
    title: "Inglês ao vivo, com prática e correção durante a aula.",
    lead: "Professores nativos e especialistas conduzem as aulas com prática, orientação e correção.",
    points: [
      { label: "CONVERSAÇÃO", text: "Uso do idioma em interação." },
      { label: "CORREÇÃO", text: "Ajustes de pronúncia, estrutura e uso durante a prática." },
      { label: "COMPREENSÃO", text: "Escuta e interpretação em situações reais." },
      { label: "APLICAÇÃO", text: "Uso do inglês em situações profissionais, acadêmicas e cotidianas." },
    ],
    media: {
      src: MEDIA_BASE + "e16-liveclass-teacher.mp4",
      alt: "Aula ao vivo de inglês, professora explica o tempo verbal Present Simple em um quadro branco.",
      width: 800,
      height: 600,
    },
  },

  levels: {
    title: "Seus níveis de inglês.",
    lead: "Do primeiro contato à comunicação avançada, com cada nível confirmado contra a página real do curso.",
    sequential: true,
    items: [
      {
        code: "a1",
        publicLabel: "A1",
        title: "Inglês A1: Iniciante",
        competencySummary:
          "Para quem está começando do zero. Aprenda cumprimentos, vocabulário essencial, frases simples e primeiras conversas em inglês com professor ao vivo.",
        focuses: [],
        href: "/curso/ingles-basico-a1",
      },
      {
        code: "a2",
        publicLabel: "A2",
        title: "Inglês A2: Elementar",
        competencySummary:
          "Para quem já conhece o básico e quer ganhar segurança. Consolide gramática, vocabulário cotidiano, escuta e conversação em inglês ao vivo.",
        focuses: [],
        href: "/curso/ingles-elementar-a2",
      },
      {
        code: "a2+",
        publicLabel: "A2+",
        title: "Inglês A2+: Pré-Intermediário",
        competencySummary: "Para quem já sabe o básico, mas trava ao falar. Desenvolva conversação, vocabulário, tempos verbais e comunicação funcional em inglês.",
        focuses: [],
        href: "/curso/ingles-pre-intermediario",
      },
      {
        code: "b1",
        publicLabel: "B1",
        title: "Inglês B1: Intermediário",
        competencySummary:
          "Para quem já conversa, mas precisa falar com mais estrutura. Desenvolva fluência intermediária, vocabulário e comunicação em situações diversas.",
        focuses: [],
        href: "/curso/ingles-intermediario-b1",
      },
      {
        code: "b2",
        publicLabel: "B2",
        title: "Inglês B2: Intermediário Superior",
        competencySummary: "Para quem quer falar inglês com mais precisão e presença. Desenvolva argumentação, vocabulário profissional, escuta e fluência em nível B2.",
        focuses: [],
        href: "/curso/ingles-intermediario-superior-b2",
      },
      {
        code: "c1",
        publicLabel: "C1",
        title: "Inglês C1: Avançado",
        competencySummary: "Para quem já fala inglês e quer refinamento. Aperfeiçoe fluência, precisão, discurso, vocabulário sofisticado e comunicação profissional.",
        focuses: [],
        href: "/curso/ingles-avancado-c1",
      },
    ],
  },

  objectives: {
    eyebrow: "INGLÊS PARA A VIDA REAL",
    title: "O idioma muda conforme a situação em que você precisa usá-lo.",
    items: [
      { name: "Trabalho e carreira: Inglês Executivo", href: "/ingles-executivo" },
      { name: "Entrevista de emprego", href: "/ingles-para-entrevista" },
      { name: "Viagens", href: "/ingles-para-viagens" },
      { name: "Tecnologia e times globais", href: "/ingles-para-programadores" },
    ],
  },

  progressionConcept: {
    title: "Você sabe onde está e o que precisa desenvolver a seguir.",
    text: "Cada nível organiza competências e objetivos. O acompanhamento ajuda a identificar avanços e próximos passos.",
    steps: PROGRESSION_STEPS,
  },

  insights: {
    headline: "Aprenda também fora da aula.",
    featured: {
      title: "Curso de inglês com professor ao vivo: o que muda na evolução da fala",
      summary: "Entenda como um curso de inglês com professor ao vivo acelera a fala, corrige travas e melhora a conversação.",
      href: "/blog/ingles/curso-de-ingles-com-professor-ao-vivo-o-que-muda-na-evolucao-da-fala",
      category: "Inglês",
      date: "15 de julho de 2026",
    },
    secondary: [
      {
        title: "Aula de inglês online ao vivo: como funciona e para quem vale a pena",
        summary: "Entenda como funciona a aula de inglês online ao vivo, para quem vale a pena e como avançar com professor ao vivo.",
        href: "/blog/ingles/aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-vale-a-pena",
        category: "Inglês",
        date: "13 de julho de 2026",
      },
      {
        title: "Checklist para escolher sua primeira turma de inglês online ao vivo",
        summary: "Veja um checklist prático para escolher sua primeira turma de inglês online ao vivo com conversação, nível CEFR e evolução real.",
        href: "/blog/ingles/checklist-para-escolher-sua-primeira-turma-de-ingles-online-ao-vivo",
        category: "Inglês",
        date: "6 de julho de 2026",
      },
    ],
  },

  // 8 das 13 FAQs reais e indexadas na página atual -- excluídas: a que
  // menciona preço (design system não mistura preço em componente
  // editorial, mesma regra de v2_course_card) e a de aula particular
  // (resposta condicional/incerta, fraca como FAQ).
  faq: [
    {
      question: "Como descubro meu nível de inglês?",
      answer: "Você faz o teste de nível gratuito e uma conversa diagnóstica com a equipe, que situam você no CEFR (A1 a C1) antes de definir o plano.",
    },
    {
      question: "As aulas são ao vivo ou gravadas?",
      answer: "Ao vivo, com professor em tempo real e turmas pequenas. Você pratica a fala e é corrigido na hora; não é videoaula gravada.",
    },
    {
      question: "A Vedium trabalha com quais níveis de inglês?",
      answer: "A trilha publicada reúne cursos do A1 ao C1. O teste de nível orienta em qual etapa o aluno deve começar.",
    },
    {
      question: "Preciso já saber alguma coisa de inglês?",
      answer: "Não. A trilha pode começar do zero (A1) ou continuar de onde você parou, conforme o resultado do diagnóstico.",
    },
    {
      question: "O curso tem certificado?",
      answer: "Sim, há certificado de conclusão conforme os requisitos do curso livre.",
    },
    {
      question: "O curso de inglês tem conversação?",
      answer: "Sim. A prática oral faz parte das aulas ao vivo e inclui perguntas, respostas, vocabulário em contexto e correção durante a interação.",
    },
    {
      question: "Posso estudar inglês para o trabalho?",
      answer: "Sim. A Vedium possui conteúdos voltados a entrevistas, comunicação executiva, tecnologia, atendimento e outras situações profissionais, conforme o objetivo informado.",
    },
    {
      question: "Como começar o curso de inglês?",
      answer: "Faça o teste de nível de inglês gratuito e use o resultado para conversar com a equipe sobre nível, frequência e objetivo de estudo.",
    },
  ],

  finalCta: {
    headline: "Descubra o próximo passo no seu inglês.",
    support: "Faça o teste de nível ou conheça os percursos disponíveis para começar no ponto adequado.",
    primaryCta: { text: "Faça o teste de nível", href: LEVEL_TEST_HREF },
    secondaryCta: { text: "Conheça o curso", href: "#niveis" },
  },
};
