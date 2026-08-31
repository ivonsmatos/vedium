import type { BreadcrumbItem, CtaLink, EditorialRow, FaqItem, HeroMedia } from "@/types/language";
import { WHATSAPP_HREF, HEADER_COURSES } from "@/content/site/header";

const MEDIA_BASE = "/media/";

/**
 * Conteúdo real e auditado para `/como-funciona` (Fase F.1).
 *
 * ROTA -- achado importante (ver docs/frontend-v2/16-how-it-works-seo-parity.md):
 * a produção Frappe hoje tem DUAS páginas distintas cobrindo terreno
 * parecido -- `/como-funciona` ("Da dúvida ao plano de estudo": teste de
 * nível, aula diagnóstica, plano de estudo) e `/metodologia` ("Aula ao
 * vivo, conversação real e evolução por nível": o método de ensino em si).
 * A missão F.1 pede uma única página que responde "como eu estudo na
 * Vedium?" cobrindo as duas frentes (onboarding + metodologia) -- por
 * isso o Next consolida as duas em UMA página só, na URL `/como-funciona`
 * (já é a que Header/Footer/Home apontam nesta base de código local, veja
 * `Header.tsx` e `content/site/footer.ts` e `content/home/liveClass.ts`).
 * Não criamos rota para `/metodologia` -- isso evitaria exatamente o "dois
 * caminhos concorrentes para a mesma intenção" que a missão proíbe.
 *
 * TESTE DE NÍVEL -- achado crítico: `/teste-de-nivel` (sem sufixo) NÃO é
 * um teste genérico/universal -- é o teste de PORTUGUÊS PARA
 * ESTRANGEIROS (confirmado por HTTP: título "Teste de Nível de Português
 * para Estrangeiros", H1 "Descubra seu nível de português..."). Só existe
 * mais um teste real: `/teste-de-nivel-ingles` (Inglês). Testado por HTTP
 * nesta sessão: `/teste-de-nivel-espanhol`, `/teste-de-nivel-hebraico`,
 * `/teste-de-nivel-ioruba`, `/teste-de-nivel-portugues` -- todos 404. Por
 * isso o CTA secundário do Hero NÃO promete um teste universal -- usa o
 * padrão já usado em toda página de idioma (Fale com a Vedium via
 * WhatsApp), e a seção 1 (Ponto de Partida) menciona teste só como
 * possibilidade "quando disponível", nunca como regra para os 5 idiomas.
 *
 * FREQUÊNCIA -- `vedium_core/frequency_pricing_rules.py` confirma
 * MIN_CLASSES_PER_WEEK=1 / MAX_CLASSES_PER_WEEK=5, configurável no
 * checkout (não uma frequência fixa de "2x por semana").
 *
 * FORMATOS -- "Particular" só está confirmado para Hebraico
 * (`course_urls.py`: só `hebraico-particular`). "Corporativo" está
 * confirmado via `/empresas` (aprovada, Fase E.1), hoje para 3 dos 5
 * idiomas (Inglês, Iorubá, PLE -- ver `content/b2b.ts`). "Turmas" é o
 * formato padrão, real para todos os 5 idiomas (cada página de curso já
 * confirma "turma pequena"/"professor em tempo real").
 *
 * ACOMPANHAMENTO -- mesma disciplina já aplicada em `content/b2b.ts`
 * (seção "Gestão"): NENHUM dashboard, IA avaliadora, percentual de
 * progresso ou analytics individual -- só o que é real hoje (matrícula,
 * turma, nível, presença e progressão acompanhados pela equipe Vedium).
 *
 * SEM em-dash (—) em nenhum campo -- correção pedida pelo usuário
 * (2026-08-29) para o SITE INTEIRO, não só para uma página.
 */

export const HOW_IT_WORKS_SEO = {
  title: "Como Funciona a Vedium | Aulas de Idiomas Online ao Vivo",
  description:
    "Entenda como funciona a Vedium: aulas ao vivo com professor, ponto de partida por idioma, progressão por nível e acompanhamento ao longo do percurso.",
  canonical: "https://vediums.com/como-funciona",
  robots: "index, follow, max-image-preview:large",
  ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
  // Contrato mínimo (mesma regra já usada em Espanhol/Hebraico): só os
  // locais que realmente existem nesta base de código Next local.
  hreflang: {
    "pt-br": "https://vediums.com/como-funciona",
    "x-default": "https://vediums.com/como-funciona",
  },
};

export const HOW_IT_WORKS_BREADCRUMB: BreadcrumbItem[] = [
  { label: "Início", href: "/" },
  { label: "Como Funciona", href: null },
];

export const HOW_IT_WORKS_HERO: {
  eyebrow: string;
  headline: string;
  support: string;
  primaryCta: CtaLink;
  secondaryCta: CtaLink;
  media: HeroMedia;
} = {
  eyebrow: "COMO FUNCIONA",
  headline: "Um percurso claro para aprender, praticar e avançar.",
  support:
    "Na Vedium, você estuda em aulas ao vivo, com professores nativos e especialistas, progressão por nível e acompanhamento ao longo do percurso.",
  primaryCta: { text: "Conheça os cursos", href: "/cursos-de-idiomas-online" },
  // Sem teste universal (ver nota grande no topo do arquivo) -- mesmo
  // padrão de CTA secundário já usado no Hero de toda página de idioma.
  secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF },
  media: {
    src: MEDIA_BASE + "e16-liveclass-teacher-poster.jpg",
    alt: "Pessoa adulta participa de uma videochamada em grupo, com colegas visíveis na tela, em um ambiente doméstico.",
    width: 1672,
    height: 941,
  },
};

export const OVERVIEW = {
  eyebrow: "SEU PERCURSO",
  title: "Você sabe onde começa, o que está desenvolvendo e qual é o próximo passo.",
  text: "Da entrada até a evolução para o próximo nível, cada etapa tem um lugar definido no percurso.",
  steps: [
    { label: "01 PONTO DE PARTIDA", note: "Você começa no lugar certo, conforme o idioma e o seu momento.", href: "#ponto-de-partida" },
    { label: "02 PERCURSO", note: "O curso é organizado por níveis e competências, conforme a estrutura de cada idioma.", href: "#percurso" },
    { label: "03 AULAS AO VIVO", note: "A aula acontece com professor, interação e prática em tempo real.", href: "#aulas-ao-vivo" },
    { label: "04 PROFESSOR E PRÁTICA", note: "O professor conduz a prática, corrige e orienta o desenvolvimento.", href: "#professor" },
    { label: "05 IDIOMA E CONTEXTO", note: "A língua é ensinada com o contexto necessário para usá-la de verdade.", href: "#idioma-e-contexto" },
    { label: "06 ACOMPANHAMENTO", note: "A equipe Vedium acompanha presença, progresso e nível ao longo do percurso.", href: "#acompanhamento" },
  ],
};

export const POINT_OF_START = {
  eyebrow: "01 PONTO DE PARTIDA",
  title: "Começar no lugar certo faz diferença.",
  intro:
    "O ponto de partida depende do idioma e do seu momento com ele. Nenhum dos caminhos abaixo se aplica igualmente aos 5 idiomas.",
  items: [
    {
      title: "TESTE DE NÍVEL",
      text: "Para Português para Estrangeiros e Inglês, existe um teste de nível gratuito que estima uma faixa de proficiência antes da matrícula.",
    },
    {
      title: "ENTRADA DIRETA",
      text: "Para quem está começando do zero em um idioma, existe entrada direta pelo primeiro nível ou pela alfabetização, sem depender de teste.",
    },
    {
      title: "ORIENTAÇÃO POR OBJETIVO",
      text: "Para percursos específicos, como Hebraico Bíblico ou aulas particulares, a orientação depende do objetivo do aluno, conversado com a equipe Vedium.",
    },
    {
      title: "FALE COM A EQUIPE",
      text: "Em caso de dúvida sobre qual idioma ou nível faz mais sentido, a equipe Vedium orienta antes da matrícula.",
      href: WHATSAPP_HREF,
      ctaLabel: "Fale com a Vedium",
    },
  ] satisfies EditorialRow[],
};

export const LEVEL_STRUCTURE = {
  eyebrow: "02 PERCURSO",
  title: "O curso é organizado para que o avanço faça sentido.",
  text: "Cada idioma tem uma estrutura própria de níveis e competências, confirmada na página de cada curso. Não existe uma escala única aplicada a todos.",
  rows: [
    { title: "INGLÊS", text: "Escala CEFR completa: A1, A2, A2+, B1, B2 e C1.", href: "/curso-de-ingles-online#niveis", ctaLabel: "Ver níveis de Inglês" },
    { title: "ESPANHOL", text: "Básico, Intermediário e Avançado, com equivalência CEFR de A1 a C1.", href: "/curso-de-espanhol-online#niveis", ctaLabel: "Ver níveis de Espanhol" },
    { title: "PORTUGUÊS PARA ESTRANGEIROS", text: "Básico, Intermediário e Avançado, com foco na vida no Brasil.", href: "/portugues-para-estrangeiros#niveis", ctaLabel: "Ver níveis de PLE" },
    { title: "IORUBÁ", text: "Básico, Intermediário e Avançado, do primeiro contato à autonomia.", href: "/curso-de-ioruba-online#niveis", ctaLabel: "Ver níveis de Iorubá" },
  ] satisfies EditorialRow[],
  // Hebraico não é sequencial (5 percursos distintos), por isso fica fora
  // do grid de 4 itens acima e é descrito à parte, sem forçar no mesmo
  // formato "nível único" dos demais idiomas.
  hebrewNote:
    "Hebraico é diferente dos outros 4: em vez de uma escala única, são percursos distintos (alfabetização, Hebraico Moderno A1 e A2/B1, Hebraico Bíblico e aulas particulares), cada um com seu próprio ponto de entrada.",
  hebrewCta: { text: "Conheça os percursos de Hebraico", href: "/curso-de-hebraico-online#percursos" },
};

export const LIVE_CLASS = {
  eyebrow: "03 AULAS AO VIVO",
  title: "A aula acontece com professor, interação e prática em tempo real.",
  lead: "Não são videoaulas gravadas. Cada encontro é conduzido por um professor, com participação ativa de quem está estudando.",
  points: [
    { label: "INTERAÇÃO", text: "O aluno participa durante a aula." },
    { label: "PRÁTICA", text: "O idioma é utilizado durante o encontro." },
    { label: "CORREÇÃO", text: "O professor pode orientar pronúncia, estrutura e uso." },
    { label: "DÚVIDAS", text: "Questões podem ser trabalhadas durante a própria aula." },
  ],
  media: {
    src: MEDIA_BASE + "e16-liveclass-teacher-poster.jpg",
    alt: "Pessoa adulta participa de uma videochamada em grupo, com colegas visíveis na tela, em um ambiente doméstico.",
    width: 1672,
    height: 941,
  },
};

export const TEACHER_AND_PRACTICE = {
  eyebrow: "04 CONDUÇÃO PEDAGÓGICA",
  title: "Professor não é apenas alguém que apresenta conteúdo.",
  intro:
    "O professor conduz a prática, observa dificuldades, faz correções, orienta o desenvolvimento e acompanha o percurso, com professores nativos e especialistas, de acordo com o percurso.",
  items: [
    { title: "CONVERSAÇÃO", text: "Prática de fala e escuta em situações reais de uso do idioma." },
    { title: "LEITURA E COMPREENSÃO", text: "Contato com textos e situações de compreensão, no ritmo de cada curso." },
    { title: "PRONÚNCIA", text: "Orientação sobre sons, ritmo e produção oral." },
    { title: "ESTRUTURA E VOCABULÁRIO", text: "Construções do idioma e repertório, com correção ao longo da aula." },
  ] satisfies EditorialRow[],
};

export const LANGUAGE_CONTEXT = {
  eyebrow: "05 IDIOMA E CONTEXTO",
  title: "A língua é ensinada com o contexto necessário para compreendê-la e usá-la.",
  text: "Contexto significa situações reais de uso, formas de expressão, registros, produção cultural e diferenças regionais quando relevantes, conforme o idioma. Não é curiosidade, folclore ou decoração: é o que permite usar o idioma com propriedade.",
  media: {
    src: MEDIA_BASE + "e02-study-laptop.jpg",
    alt: "Pessoa adulta participa de uma videochamada, com um mapa-múndi ao fundo, em um escritório em casa.",
    width: 1672,
    height: 941,
  },
};

export const EVOLUTION = {
  eyebrow: "06 ACOMPANHAMENTO",
  title: "Aprender também envolve perceber o que já avançou e o que ainda precisa ser desenvolvido.",
  text: "Matrícula, turma, nível, presença e progressão são acompanhados ao longo do percurso, com retorno do professor sobre o desenvolvimento do aluno.",
  media: {
    src: MEDIA_BASE + "e06-listening-online-course.jpg",
    alt: "Grupo de profissionais adultos conversa em uma sala, um deles segurando um tablet.",
    width: 1672,
    height: 941,
  },
};

export const NEXT_LEVEL = {
  eyebrow: "07 CONTINUIDADE",
  title: "O próximo passo fica mais claro quando existe um percurso.",
  text: "Ao desenvolver as competências previstas para uma etapa, o aluno avança dentro da estrutura definida para o idioma, com orientação da equipe Vedium sobre o momento adequado para seguir.",
};

export const STUDY_FORMATS = {
  eyebrow: "FORMATOS DE ESTUDO",
  title: "Formatos confirmados para estudar na Vedium.",
  intro: "O formato de estudo varia conforme o objetivo, com frequência de aulas ajustável no checkout.",
  items: [
    {
      title: "TURMAS",
      text: "O formato padrão em todos os 5 idiomas: aulas ao vivo, com professor e turma pequena.",
    },
    {
      title: "AULAS PARTICULARES",
      text: "Hoje confirmadas para Hebraico: acompanhamento individual, ajustado a objetivo e ritmo.",
      href: "/curso/hebraico-particular",
      ctaLabel: "Conheça o Hebraico Particular",
    },
    {
      title: "CORPORATIVO",
      text: "Para empresas, a Vedium estrutura programas de idiomas voltados ao desenvolvimento de equipes.",
      href: "/empresas",
      ctaLabel: "Conheça a Vedium para Empresas",
    },
    {
      title: "FREQUÊNCIA",
      text: "De 1 a 5 aulas por semana, ajustável no checkout conforme o plano escolhido.",
    },
  ] satisfies EditorialRow[],
};

export const COURSES_SECTION = {
  eyebrow: "NOSSOS CURSOS",
  title: "Cinco idiomas. Cada um com sua própria estrutura de níveis.",
  lead: "Escolha o idioma para conhecer os níveis, formatos e o ponto de partida adequado.",
  courses: HEADER_COURSES.map((course) => ({ name: course.label, href: course.href })),
};

export const HOW_IT_WORKS_FAQ: FaqItem[] = [
  {
    question: "As aulas da Vedium são ao vivo?",
    answer: "Sim. Todas as aulas são ao vivo, com professor em tempo real; não são videoaulas gravadas.",
  },
  {
    question: "Como sei em qual nível começar?",
    answer:
      "Depende do idioma. Português para Estrangeiros e Inglês têm um teste de nível gratuito. Para quem está começando do zero em qualquer idioma, existe entrada direta pelo primeiro nível. Para percursos específicos, como Hebraico Bíblico ou aulas particulares, a orientação é conversada com a equipe Vedium.",
  },
  {
    question: "Todos os idiomas usam a mesma estrutura de níveis?",
    answer:
      "Não. Inglês segue a escala CEFR completa (A1 a C1). Espanhol, Português para Estrangeiros e Iorubá usam Básico, Intermediário e Avançado. Hebraico tem percursos distintos (alfabetização, Hebraico Moderno, Hebraico Bíblico e aulas particulares), sem uma progressão sequencial única.",
  },
  {
    question: "Quem são os professores?",
    answer: "Professores nativos e especialistas, de acordo com o percurso, conduzindo a prática, a correção e a progressão de cada turma.",
  },
  {
    question: "Como funciona a progressão?",
    answer:
      "Ao desenvolver as competências previstas para uma etapa, o aluno avança dentro da estrutura definida para o idioma, com orientação da equipe sobre o momento adequado para seguir.",
  },
  {
    question: "Existem aulas particulares?",
    answer: "Hoje, aulas particulares estão confirmadas para Hebraico, com acompanhamento individual ajustado a objetivo e ritmo.",
  },
  {
    question: "A Vedium oferece cursos para empresas?",
    answer: "Sim. Para empresas, a Vedium estrutura programas de idiomas voltados ao desenvolvimento de equipes, hoje em Inglês, Iorubá e Português para Estrangeiros.",
  },
  {
    question: "Como faço para começar?",
    answer: "Conheça os cursos disponíveis, identifique o idioma e o nível adequado, e fale com a equipe Vedium para tirar dúvidas antes de começar.",
  },
];

export const FINAL_CTA = {
  headline: "Encontre o percurso adequado para você.",
  support: "Conheça os cursos da Vedium e veja como começar de acordo com o idioma e o seu momento de aprendizagem.",
  primaryCta: { text: "Conheça os cursos", href: "/cursos-de-idiomas-online" } satisfies CtaLink,
  secondaryCta: { text: "Fale com a Vedium", href: WHATSAPP_HREF } satisfies CtaLink,
};
