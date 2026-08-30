const MEDIA_BASE = "/assets/vedium_core/v2/media/home/";

/**
 * Conteúdo real e validado para `/empresas` (Vedium para Empresas / B2B).
 *
 * Fontes:
 * - SEO (title/description/canonical/hreflang/OG/Service+BreadcrumbList
 *   JSON-LD): página pública atual `https://vediums.com/empresas`
 *   (snapshot verificado nesta sessão — ver
 *   docs/frontend-v2/13-b2b-seo-parity.md).
 * - Hero/Desafio/Diagnóstico/Solução/Implementação: copy dada literalmente
 *   pela missão da Fase E.1.
 * - "Como funciona": os 4 passos REAIS já publicados na página atual
 *   (Diagnóstico da equipe → Montagem das turmas → Aulas ao vivo →
 *   Evolução do programa), não os 6 passos conceituais sugeridos pela
 *   missão — só afirmamos etapas operacionalmente confirmadas.
 * - Idiomas confirmados para B2B: SÓ 3, não os 5 do catálogo geral —
 *   confirmado no meta description E no JSON-LD Service, ambos dizendo
 *   literalmente "inglês, iorubá e português para estrangeiros". Um
 *   WebFetch inicial sugeriu erroneamente os 5 idiomas, mas essa lista
 *   vinha do RODAPÉ (site-wide, todo curso), não do conteúdo B2B real —
 *   corrigido usando o HTML bruto. Ver doc de parity para o achado
 *   completo.
 * - "Gestão e Acompanhamento": claim deliberadamente contido. A página
 *   atual já diz "relatório para o gestor" / "dados reais de progresso" —
 *   mas não existe nenhum dashboard, relatório automatizado ou portal
 *   digital para gestor implementado no backend (grep em vedium_core não
 *   encontrou nenhum doctype/report B2B, só a própria página de
 *   marketing usando essas palavras). Mantido como "a equipe Vedium
 *   acompanha e informa" (real, mediado por humano), não como "dashboard"
 *   (não real). Ver docs/frontend-v2/14-b2b-content-contract.md para a
 *   tabela completa AVAILABLE NOW / PLANNED FUTURE.
 * - "Sem amarras" (por que Vedium): confirmado — a página atual já
 *   publica "Planos mensais. A equipe continua porque está evoluindo,
 *   não porque está presa a um contrato longo." Preservado com a mesma
 *   moderação.
 * - SEM formulário funcional novo: nenhum endpoint/CRM/LGPD foi
 *   auditado nesta tarefa (fora do escopo, ver missão seção 19-20). O
 *   único mecanismo de conversão usado é o MESMO WhatsApp real já usado
 *   em toda a Vedium, mais o link para `/contato` (pipeline já existente
 *   e testado, ver project_audit_remediation_2026_08 na memória do
 *   projeto) — nenhum backend novo, nenhum acoplamento direto a um
 *   DocType Lead.
 * - SEM seção de clientes/logos/cases/depoimentos/números — nenhuma prova
 *   social real e publicável foi encontrada; a missão proíbe inventar.
 * - SEM nome de professor (mesma decisão de todas as páginas de idioma).
 */

const B2B_WHATSAPP_HREF = "https://wa.me/5511911293075?text=Ol%C3%A1%2C%20quero%20falar%20sobre%20treinamento%20de%20idiomas%20para%20minha%20empresa";

export const b2b = {
  seo: {
    title: "Vedium para Empresas: treinamento de idiomas em equipe",
    description:
      "Aulas ao vivo de inglês, iorubá e português para estrangeiros para equipes: diagnóstico por colaborador, turmas por nível e objetivo, e relatório de progresso para o gestor.",
    canonical: "https://vediums.com/empresas",
    robots: "index, follow, max-image-preview:large",
    ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    hreflang: {
      "pt-br": "https://vediums.com/empresas",
      en: "https://vediums.com/en/empresas",
      es: "https://vediums.com/es/empresas",
      fr: "https://vediums.com/fr/empresas",
      de: "https://vediums.com/de/empresas",
      "x-default": "https://vediums.com/empresas",
    },
  },

  breadcrumb: [
    { label: "Início", href: "/" },
    { label: "Empresas", href: null as string | null },
  ],

  hero: {
    eyebrow: "VEDIUM PARA EMPRESAS",
    headline: "Desenvolva um time mais preparado para atuar em contextos globais.",
    support: "Programas de idiomas com aulas ao vivo, acompanhamento e percursos organizados para as necessidades de profissionais e equipes.",
    primaryCta: { text: "Fale com a Vedium", href: B2B_WHATSAPP_HREF },
    secondaryCta: { text: "Conheça a solução", href: "#solucao" },
    media: {
      src: MEDIA_BASE + "e15-b2b-videocall.jpg",
      alt: "Pessoa adulta acompanha uma videochamada em grupo em um notebook, em um ambiente doméstico aconchegante.",
      width: 2000,
      height: 1126,
    },
  },

  challenge: {
    eyebrow: "DESENVOLVIMENTO DE EQUIPES",
    headline: "Conhecer o idioma não basta quando ele precisa ser usado no trabalho.",
    rows: [
      { title: "REUNIÕES E INTERAÇÃO", text: "Participar de conversas profissionais com mais clareza." },
      { title: "COMUNICAÇÃO INTERNACIONAL", text: "Atuar com colegas, parceiros ou clientes em outros mercados." },
      { title: "DIFERENTES NÍVEIS", text: "Organizar pessoas com necessidades e competências distintas." },
      { title: "CONTINUIDADE", text: "Transformar treinamento pontual em desenvolvimento acompanhado." },
    ],
  },

  diagnosis: {
    title: "O ponto de partida é entender quem precisa aprender, para quê e em qual nível.",
    text: "Antes do programa: alinhamos objetivo, público, nível e desenho do percurso.",
    steps: [
      { label: "01 OBJETIVO", note: "Qual necessidade de negócio ou desenvolvimento está por trás do programa?" },
      { label: "02 PÚBLICO", note: "Quais profissionais ou equipes participarão?" },
      { label: "03 NÍVEL", note: "Qual é o ponto de partida de cada participante ou grupo?" },
      { label: "04 DESENHO", note: "Qual formato de percurso faz sentido para a necessidade identificada?" },
    ],
  },

  solution: {
    eyebrow: "A SOLUÇÃO",
    subEyebrow: "PROGRAMAS DE IDIOMAS PARA EQUIPES",
    title: "Idioma, prática e progressão organizados para o contexto profissional.",
    text: "Aulas ao vivo, professores qualificados e progressão organizada por nível, com prática conectada às situações reais do trabalho.",
    text2: "Hoje, a solução está confirmada para Inglês, Iorubá e Português para Estrangeiros.",
    proofItems: [
      { label: "AULAS AO VIVO", text: "Interação real com professor." },
      { label: "PROFESSORES", text: "Nativos e especialistas conforme o percurso." },
      { label: "PROGRESSÃO", text: "Organização por nível e competências." },
      { label: "APLICAÇÃO", text: "Prática conectada às situações em que o idioma será utilizado." },
    ],
    primaryCta: { text: "Fale com a Vedium", href: B2B_WHATSAPP_HREF },
    secondaryCta: { text: "Solicite uma conversa diagnóstica", href: "/contato" },
    media: {
      src: MEDIA_BASE + "e20-b2b-aula-videochamada.jpg",
      alt: "Profissional adulto de terno participa de uma videochamada com colegas de equipe visíveis na tela, em um escritório.",
      width: 2000,
      height: 1333,
    },
  },

  // 4 passos REAIS já publicados na página atual (não os 6 conceituais da
  // missão) -- ver nota grande no topo do arquivo.
  howItWorks: {
    title: "Do primeiro contato à turma rodando.",
    text: "Um processo simples, do diagnóstico à evolução do programa.",
    steps: [
      { label: "01 DIAGNÓSTICO DA EQUIPE", note: "Cada colaborador faz o teste de nível, para saber exatamente de onde parte." },
      { label: "02 MONTAGEM DAS TURMAS", note: "A Vedium organiza turmas por nível e objetivo, evitando misturar quem está em estágios muito diferentes." },
      { label: "03 AULAS AO VIVO", note: "Professor qualificado corrigindo em tempo real, semana após semana." },
      { label: "04 EVOLUÇÃO DO PROGRAMA", note: "A equipe Vedium acompanha participação e avanço de nível, e ajusta o percurso quando necessário." },
    ],
  },

  management: {
    eyebrow: "VISIBILIDADE PARA RH E LIDERANÇAS",
    title: "Um programa corporativo precisa ser acompanhado, não apenas contratado.",
    description:
      "Matrícula, turma, nível, presença e progressão são acompanhados ao longo do programa. A equipe Vedium mantém o RH e a liderança informados sobre a evolução dos participantes.",
    media: {
      src: MEDIA_BASE + "e21-b2b-acompanhamento-notas.jpg",
      alt: "Profissional adulto sentado em um sofá faz anotações em um caderno, com um notebook ao lado.",
      width: 2000,
      height: 1514,
    },
  },

  formats: {
    eyebrow: "FORMATOS CORPORATIVOS",
    headline: "Formatos organizados conforme a necessidade da equipe.",
    rows: [
      { title: "TURMAS FECHADAS", text: "Grupos organizados por nível e objetivo, exclusivos para a equipe." },
      { title: "AULA PARTICULAR", text: "Acompanhamento individual para necessidades específicas." },
      { title: "PROGRAMAS POR NÍVEL", text: "Percursos organizados conforme a competência de cada participante." },
      { title: "NECESSIDADES ESPECÍFICAS", text: "Conteúdo adaptado a áreas como atendimento, tecnologia, negócios e mobilidade internacional." },
    ],
  },

  implementation: {
    eyebrow: "DA NECESSIDADE AO PROGRAMA",
    title: "Uma implementação clara para empresa e participantes.",
    text: "Cinco etapas, do alinhamento inicial à revisão do percurso.",
    steps: [
      { label: "01 ALINHAMENTO", note: "Definição de necessidades e público." },
      { label: "02 ORGANIZAÇÃO", note: "Níveis, grupos e percurso." },
      { label: "03 INÍCIO", note: "Entrada dos participantes e aulas." },
      { label: "04 ACOMPANHAMENTO", note: "Observação da evolução do programa." },
      { label: "05 REVISÃO", note: "Ajustes quando necessários." },
    ],
  },

  // "Sem amarras" confirmado -- já publicado na página atual (ver nota no
  // topo). "Idioma + Contexto" (5º pilar sugerido pela missão) omitido
  // por redundância com "Aplicação" já coberto em `solution.proofItems`.
  whyVedium: {
    eyebrow: "POR QUE VEDIUM",
    headline: "Provas estruturais, não superlativos.",
    rows: [
      { title: "AO VIVO DE VERDADE", text: "Aulas com interação, prática e correção." },
      { title: "PROFESSORES NATIVOS E ESPECIALISTAS", text: "Condução humana e qualificada." },
      { title: "PROGRESSÃO", text: "Desenvolvimento organizado por nível." },
      { title: "SEM AMARRAS", text: "Planos mensais, sem fidelidade de contrato longo." },
    ],
  },

  diagnosisCta: {
    eyebrow: "PRÓXIMO PASSO",
    title: "Vamos entender o que sua equipe precisa desenvolver.",
    text: "Converse com a Vedium sobre público, objetivos e contexto para estruturarmos o próximo passo.",
    primaryCta: { text: "Fale com a Vedium", href: B2B_WHATSAPP_HREF },
    secondaryCta: { text: "Solicite uma conversa diagnóstica", href: "/contato" },
  },

  // Nenhuma pergunta/resposta real existe na página atual (sem FAQPage lá)
  // -- construídas inteiramente com fatos já confirmados nas seções
  // acima desta mesma página.
  faq: [
    {
      question: "Como funciona um programa de idiomas para empresas?",
      answer: "Começa com diagnóstico por colaborador (teste de nível), montagem de turmas por nível e objetivo, aulas ao vivo com professor e acompanhamento contínuo da evolução do programa.",
    },
    {
      question: "A Vedium trabalha com turmas corporativas?",
      answer: "Sim. As turmas são organizadas por nível e objetivo, sem misturar participantes em estágios muito diferentes.",
    },
    {
      question: "É possível organizar participantes por nível?",
      answer: "Sim. Cada colaborador faz o teste de nível antes de começar, e as turmas são formadas conforme o resultado.",
    },
    {
      question: "As aulas são ao vivo?",
      answer: "Sim, sempre com professor em tempo real, corrigindo pronúncia e construção de frase durante a aula.",
    },
    {
      question: "Quais idiomas podem ser oferecidos para empresas?",
      answer: "Hoje a solução está confirmada para Inglês, Iorubá e Português para Estrangeiros.",
    },
    {
      question: "Como o RH acompanha o programa?",
      answer: "A equipe Vedium acompanha matrícula, turma, nível, presença e progressão, e mantém o RH e a liderança informados sobre a evolução dos participantes.",
    },
    {
      question: "É possível estruturar um programa para uma necessidade específica?",
      answer: "Sim. O conteúdo pode ser adaptado a áreas como atendimento, tecnologia, negócios e mobilidade internacional.",
    },
    {
      question: "Como solicitar uma proposta?",
      answer: "Fale com a Vedium pelo WhatsApp ou solicite uma conversa diagnóstica pelo formulário de contato.",
    },
  ],

};

export type B2BContent = typeof b2b;
