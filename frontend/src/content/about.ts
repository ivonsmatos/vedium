import type { BreadcrumbItem, CtaLink, EditorialRow, HeroMedia } from "@/types/language";
import { HEADER_COURSES } from "@/content/site/header";

const MEDIA_BASE = "/assets/vedium_core/v2/media/home/";

/**
 * Conteúdo real para `/sobre` (Fase F.2), baseado na fonte oficial
 * `01_Vedium_Identidade_Organizacional_Completa_v4.docx` (extraído e lido
 * nesta sessão -- Propósito, Missão, Visão, Manifesto, Valores,
 * Arquitetura Acadêmica e Princípios da Experiência).
 *
 * ROTA -- `/sobre` já é real em produção (HTTP 200, título "Sobre a
 * Vedium - Escola de Idiomas Online ao Vivo") e já é para onde
 * `Header.tsx` (nav desktop/mobile) e `content/site/footer.ts` apontam
 * nesta base de código local. `/sobre-a-vedium` e `/quem-somos`
 * retornam 404 -- nenhuma rota concorrente criada.
 *
 * NÃO INVENTADO (missão seção 1 e 20) -- o documento oficial não cita
 * ano de fundação, fundadores, número de alunos/professores/países,
 * prêmios ou certificações institucionais. Nada disso aparece aqui.
 * Sem timeline, sem "nascemos de...".
 *
 * ESTRATÉGIA INTERNA NÃO PUBLICADA (missão seção 17) -- a tabela
 * "Arquitetura Acadêmica" do documento oficial tem uma coluna "Papel de
 * marca" com função estratégica de cada idioma (volume, autoridade,
 * receita, ticket). Essa coluna NÃO é usada aqui -- só a direção
 * formativa (o que cada trilha desenvolve), que é informação pública e
 * já usada nas próprias páginas de curso.
 *
 * CONDUÇÃO PEDAGÓGICA -- por instrução explícita do usuário (correção
 * enviada durante esta mesma fase, 2026-08-29): a Vedium NÃO terá uma
 * página institucional de catálogo de professores. Esta seção NÃO tem
 * CTA nem link para nenhuma rota "/professores" -- só explica o papel
 * institucional da condução pedagógica.
 *
 * MISSÃO/VISÃO -- por instrução da missão (seções 9-10), não viram
 * caixas "Missão"/"Visão" -- a missão oficial foi incorporada em
 * `whoWeAre.text` (segunda frase) e a visão oficial em
 * `whyWeExist.closing`, preservando o equilíbrio exato do documento
 * ("idiomas de alta demanda internacional" + "línguas de relevância
 * histórica e cultural") -- sem "ser líder de mercado".
 *
 * TRANSPARÊNCIA -- o documento oficial fala em "ausência de fidelidade
 * NOS PLANOS APLICÁVEIS", não como regra universal. `principles`
 * preserva esse escopo, sem generalizar para B2B ou contratos
 * específicos (missão seção 19).
 */

export const ABOUT_SEO = {
  // title/description recuperados literalmente da página pública atual
  // (mesma regra já aplicada em todas as páginas anteriores).
  title: "Sobre a Vedium - Escola de Idiomas Online ao Vivo",
  description:
    "Conheça a Vedium: escola online com aulas ao vivo de inglês, espanhol, hebraico, iorubá e português para estrangeiros, professores e certificado.",
  canonical: "https://vediums.com/sobre",
  robots: "index, follow, max-image-preview:large",
  ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
  // Contrato mínimo (mesma regra já usada em Como Funciona/Espanhol/Hebraico):
  // só os locais que existem nesta base de código Next local.
  hreflang: {
    "pt-br": "https://vediums.com/sobre",
    "x-default": "https://vediums.com/sobre",
  },
};

export const ABOUT_BREADCRUMB: BreadcrumbItem[] = [
  { label: "Início", href: "/" },
  { label: "Sobre", href: null },
];

export const ABOUT_HERO: {
  eyebrow: string;
  headline: string;
  support: string;
  primaryCta: CtaLink;
  secondaryCta: CtaLink;
  media: HeroMedia;
} = {
  eyebrow: "SOBRE A VEDIUM",
  headline: "Educação linguística ao vivo para participar de novos contextos.",
  support:
    "A Vedium é uma escola de idiomas 100% online que une aulas ao vivo, professores nativos e especialistas, progressão estruturada e profundidade cultural.",
  primaryCta: { text: "Conheça os cursos", href: "/cursos-de-idiomas-online" },
  secondaryCta: { text: "Como funciona", href: "/como-funciona" },
  media: {
    src: MEDIA_BASE + "e19-espanhol-estudo-online.jpg",
    alt: "Pessoa adulta assiste a uma aula online em um monitor, ouvindo com atenção e fazendo anotações em um caderno.",
    width: 2000,
    height: 1333,
  },
};

// "Quem Somos" -- Fundamentos + Missão oficial incorporada editorialmente
// (2a frase de `text`, sem caixa "Missão").
export const WHO_WE_ARE = {
  eyebrow: "A VEDIUM",
  title: "Uma escola construída sobre interação, método e repertório.",
  text: "O valor não está apenas no acesso ao conteúdo, mas na forma como o aluno é conduzido para compreender, comunicar e agir em situações reais. A Vedium oferece educação linguística online ao vivo, conduzida por professores nativos e especialistas, com trilhas claras, acompanhamento próximo e aplicação na vida pessoal, acadêmica e profissional.",
  items: [
    { title: "AULAS AO VIVO", text: "Interação real, com professor presente, prática e correção em tempo real." },
    { title: "PROFESSORES", text: "Nativos e especialistas, de acordo com a natureza de cada percurso." },
    { title: "PROGRESSÃO", text: "Trilhas organizadas por nível, com objetivos claros a cada etapa." },
    { title: "CONTEXTO", text: "Cada idioma é ensinado com as situações e referências em que ganha sentido." },
  ] satisfies EditorialRow[],
};

// "Por Que Existimos" -- Propósito oficial + Visão oficial incorporada
// como fechamento curto (sem caixa "Visão").
export const WHY_WE_EXIST = {
  eyebrow: "NOSSO PROPÓSITO",
  title: "Ampliar a capacidade de compreender, comunicar e participar.",
  text: "Aprender um idioma amplia a capacidade de participar de diferentes contextos: no trabalho, nos estudos, na cultura e no dia a dia. É essa ampliação de repertório, não uma promessa de transformação abstrata, que orienta o que a Vedium constrói.",
  closing:
    "A Vedium busca ser reconhecida como uma referência premium e acessível em ensino de idiomas ao vivo, valorizando tanto os idiomas de maior demanda internacional quanto línguas de relevância histórica e cultural.",
};

// "No Que Acreditamos" -- 4 ideias do Manifesto oficial (não o
// documento inteiro).
export const WHAT_WE_BELIEVE = {
  eyebrow: "NOSSA FORMA DE PENSAR",
  title: "Conhecimento ganha valor quando se transforma em participação.",
  items: [
    { title: "INTERAÇÃO", text: "A pergunta, a prática e a correção acontecem no encontro entre pessoas." },
    { title: "CONTEXTO", text: "Toda língua existe dentro de situações, histórias e formas de uso." },
    { title: "CONSTÂNCIA", text: "Aprendizagem é construída nível a nível, não em atalhos." },
    { title: "TECNOLOGIA", text: "Organiza e amplia o acesso, mas não substitui o professor." },
  ] satisfies EditorialRow[],
};

// "A Experiência Vedium" -- 4 dos 7 princípios oficiais da experiência
// (os outros 3 -- competência docente, contexto, transparência -- estão
// cobertos em Condução Pedagógica, Rigor Cultural e Princípios).
export const EXPERIENCE = {
  eyebrow: "A EXPERIÊNCIA",
  title: "O aluno precisa entender onde está, o que está desenvolvendo e qual é o próximo passo.",
  items: [
    { title: "CLAREZA DE ENTRADA", text: "O aluno entende qual curso, nível e modalidade atendem ao seu objetivo." },
    { title: "INTERAÇÃO REAL", text: "A aula mostra fala, correção, pergunta e participação." },
    { title: "PROGRESSÃO", text: "O próximo marco está claro em cada etapa do percurso." },
    { title: "ACOMPANHAMENTO", text: "Feedback e indicadores tornam a evolução visível." },
  ] satisfies EditorialRow[],
};

// "Condução Pedagógica" -- SEM CTA, SEM link para qualquer rota de
// professores (ver nota grande no topo do arquivo).
export const PEDAGOGICAL_GUIDANCE = {
  eyebrow: "PROFESSORES E TECNOLOGIA",
  title: "A tecnologia organiza. A condução pedagógica continua humana.",
  text: "A tecnologia amplia o acesso, organiza a jornada e torna o progresso visível, mas não substitui o professor. O centro da experiência continua sendo o encontro entre pessoas: professores nativos e especialistas, de acordo com a natureza de cada percurso, que orientam, corrigem, acompanham o desenvolvimento e respondem pela responsabilidade pedagógica e cultural de cada aula.",
  media: {
    src: MEDIA_BASE + "e28-sobre-conducao-pedagogica.jpg",
    alt: "Grupo de pessoas adultas reunidas em roda, conversando em um espaço profissional.",
    width: 1672,
    height: 941,
  },
};

// "Rigor Cultural" -- princípio institucional aplicado aos 5 idiomas,
// cada nota alinhada às restrições já aprovadas nas páginas de idioma
// (sem exotizar Iorubá, sem reduzir Hebraico à religião, sem reduzir
// PLE a turismo, sem tratar o mundo hispânico como bloco único).
export const CULTURAL_RIGOR = {
  eyebrow: "IDIOMA + CULTURA",
  title: "Cada idioma exige contexto.",
  text: "Ensinar Inglês, Iorubá, Português, Espanhol ou Hebraico significa apresentar estruturas linguísticas e também os ambientes em que elas são usadas, interpretadas e transformadas. Iorubá é ensinado com estrutura, oralidade, literatura e história, sem reduzir a cultura a curiosidade. Hebraico cobre alfabetização, uso contemporâneo e leitura textual, sem reduzir o idioma à religião. Português para Estrangeiros trata da vida real no Brasil, não do Brasil como destino turístico. Espanhol reconhece a diversidade de países e variedades do idioma, sem tratar o mundo hispânico como um bloco único.",
  media: {
    src: MEDIA_BASE + "e27-como-funciona-contexto.jpg",
    alt: "Pessoa adulta participa de uma videochamada, com um mapa-múndi ao fundo, em um escritório em casa.",
    width: 1672,
    height: 941,
  },
};

export const PORTFOLIO = {
  eyebrow: "UM PORTFÓLIO, DIFERENTES PORTAS DE ENTRADA",
  title: "Idiomas diferentes. O mesmo compromisso com clareza, presença e progressão.",
  lead: "Escolha o idioma para conhecer níveis, formatos e o ponto de partida adequado.",
  courses: HEADER_COURSES.map((course) => ({ name: course.label, href: course.href })),
  b2bText: "Para empresas, a Vedium também estrutura programas de idiomas voltados ao desenvolvimento de equipes.",
  b2bCta: { text: "Conheça a Vedium para Empresas", href: "/empresas" } satisfies CtaLink,
};

// "Princípios" -- 4 dos 7 valores oficiais (profissionalismo, presença
// ao vivo, rigor cultural, evolução visível, transparência, conexão
// humana, melhoria contínua) -- os que funcionam melhor editorialmente
// sem repetir o que já foi dito em Quem Somos/Experiência.
export const PRINCIPLES = {
  eyebrow: "NOSSOS PRINCÍPIOS",
  title: "Princípios que sustentam a experiência.",
  items: [
    { title: "PROFISSIONALISMO", text: "Planejamento, pontualidade, preparação pedagógica e comunicação cuidadosa." },
    { title: "RIGOR CULTURAL", text: "Cada idioma é ensinado com contexto histórico, social e contemporâneo." },
    { title: "EVOLUÇÃO VISÍVEL", text: "Metas, níveis, feedback e avaliação tornam o avanço compreensível." },
    // "nos planos aplicáveis" preserva o escopo oficial -- não é uma
    // regra universal para todo contrato (B2B incluso).
    { title: "TRANSPARÊNCIA", text: "Condições claras, expectativas realistas e ausência de fidelidade nos planos aplicáveis." },
  ] satisfies EditorialRow[],
};

export const ABOUT_FINAL_CTA = {
  headline: "Conheça a Vedium pela experiência de aprender ao vivo.",
  support: "Explore os cursos e encontre o percurso mais adequado para o idioma que você quer desenvolver.",
  primaryCta: { text: "Conheça os cursos", href: "/cursos-de-idiomas-online" } satisfies CtaLink,
  secondaryCta: { text: "Como funciona", href: "/como-funciona" } satisfies CtaLink,
};
