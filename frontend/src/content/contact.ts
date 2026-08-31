import type { BreadcrumbItem, CtaLink, FaqItem } from "@/types/language";
import { HEADER_COURSES } from "@/content/site/header";

const WHATSAPP_NUMBER = "5511911293075";

function buildWhatsappHref(message: string): string {
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

/**
 * Conteúdo real para `/contato` (Fase F.3).
 *
 * ROTA -- `/contato` já é real em produção (HTTP 200, título "Contato -
 * Vedium") e já é para onde `content/site/footer.ts` aponta nesta base
 * de código local. Ver `docs/frontend-v2/21-contact-seo-parity.md`.
 *
 * CANAIS OFICIAIS -- WhatsApp (`WHATSAPP_NUMBER`, mesmo número usado em
 * toda a base), e-mail `contato@vediums.com` (confirmado por HTTP na
 * produção de `/contato` E como destinatário hardcoded em
 * `vedium_core/public_funnel.py`). Nenhum endereço físico, horário,
 * telefone fixo ou SLA -- nenhuma fonte confirma isso.
 *
 * ESCOLHA DO ASSUNTO -- cada item já é seu próprio CTA de WhatsApp com
 * mensagem pré-preenchida específica (satisfaz ao mesmo tempo a seção 7
 * -- navegação editorial -- e a seção 8 -- "se o usuário escolheu um
 * assunto, a mensagem pode refletir esse assunto" -- da missão, sem
 * precisar de estado client-side/JS para isso).
 *
 * FORMULÁRIO -- backend real auditado em
 * `docs/frontend-v2/23-contact-form-integration-audit.md`. `intent` usa
 * o vocabulário real de `vedium_core.public_funnel.ALLOWED_INTENTS`
 * (lead/diagnostic/community/referral/b2b/review) -- não existe intent
 * "contact" ou "particular" no backend, por isso os assuntos que não são
 * "Empresas" usam intent "lead" e carregam o assunto real no campo
 * `goal` (vai para o ticket humano e para o comentário do CRM Lead).
 */

export const CONTACT_SEO = {
  title: "Contato | Vedium",
  // Descrição atualizada -- a de produção ainda cita só "Inglês e
  // Iorubá" (desatualizada frente ao catálogo real de 5 idiomas + B2B,
  // mesmo achado já documentado nas fases anteriores). Texto sugerido
  // literalmente pela missão F.3 (seção 22).
  description: "Fale com a Vedium sobre cursos de idiomas, nível, aulas particulares ou soluções para empresas.",
  canonical: "https://vediums.com/contato",
  robots: "index, follow, max-image-preview:large",
  ogImage: "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
  hreflang: {
    "pt-br": "https://vediums.com/contato",
    "x-default": "https://vediums.com/contato",
  },
};

export const CONTACT_BREADCRUMB: BreadcrumbItem[] = [
  { label: "Início", href: "/" },
  { label: "Contato", href: null },
];

export const CONTACT_INTRO = {
  eyebrow: "FALE COM A VEDIUM",
  headline: "Vamos entender o que você quer desenvolver.",
  support: "Fale com a Vedium sobre idioma, nível, formato de estudo ou necessidades da sua equipe.",
  primaryCta: { text: "Falar pelo WhatsApp", href: buildWhatsappHref("Olá, gostaria de saber mais sobre os cursos da Vedium.") } satisfies CtaLink,
  secondaryCta: { text: "Ver cursos", href: "/cursos-de-idiomas-online" } satisfies CtaLink,
};

export const SUBJECTS_INTRO = {
  eyebrow: "ESCOLHA O ASSUNTO",
  title: "Sobre o que você quer falar com a Vedium?",
};

export const SUBJECTS = [
  {
    title: "CURSOS",
    text: "Quero entender qual curso ou nível faz sentido.",
    whatsappText: "Falar sobre isso",
    href: buildWhatsappHref("Olá, quero entender qual curso ou nível da Vedium faz sentido para mim."),
  },
  {
    title: "AULAS PARTICULARES",
    text: "Quero conversar sobre um percurso individual.",
    whatsappText: "Falar sobre isso",
    href: buildWhatsappHref("Olá, quero conversar sobre aulas particulares na Vedium."),
  },
  {
    title: "PORTUGUÊS PARA ESTRANGEIROS",
    text: "Quero informações sobre Português para viver, trabalhar ou estudar no Brasil.",
    whatsappText: "Falar sobre isso",
    href: buildWhatsappHref("Olá, quero informações sobre o curso de Português para Estrangeiros da Vedium."),
  },
  {
    title: "EMPRESAS",
    text: "Quero conversar sobre desenvolvimento linguístico para uma equipe.",
    whatsappText: "Falar sobre isso",
    href: buildWhatsappHref("Olá, quero conversar sobre a Vedium para Empresas."),
  },
  {
    title: "OUTRO ASSUNTO",
    text: "Quero falar diretamente com a Vedium.",
    whatsappText: "Falar sobre isso",
    href: buildWhatsappHref("Olá, gostaria de falar com a Vedium."),
  },
];

export const DIRECT_CONTACT = {
  eyebrow: "CONTATO DIRETO",
  title: "O jeito mais rápido de conversar com a Vedium.",
  text: "Fale pelo WhatsApp com o número oficial da Vedium, ou escreva para o e-mail institucional.",
  whatsappLabel: "+55 11 91129-3075",
  whatsappHref: buildWhatsappHref("Olá, gostaria de falar com a Vedium."),
  emailLabel: "contato@vediums.com",
  emailHref: "mailto:contato@vediums.com",
};

// Vocabulário real de `ALLOWED_INTENTS` (vedium_core/public_funnel.py).
// Cada opção do form mapeia pra um intent + goal (o assunto real vai no
// goal, que aparece no ticket humano e no comentário do CRM Lead).
export const FORM_SUBJECT_OPTIONS: { label: string; intent: "lead" | "b2b"; goal: string }[] = [
  { label: "Cursos e níveis", intent: "lead", goal: "Cursos e níveis" },
  { label: "Aulas particulares", intent: "lead", goal: "Aulas particulares" },
  { label: "Português para Estrangeiros", intent: "lead", goal: "Português para Estrangeiros" },
  { label: "Empresas", intent: "b2b", goal: "Empresas" },
  { label: "Outro assunto", intent: "lead", goal: "Outro assunto" },
];

export const FORM_LANGUAGE_OPTIONS = ["Não sei ainda", ...HEADER_COURSES.map((course) => course.label)];

export const CONTACT_FORM_COPY = {
  eyebrow: "OU ESCREVA PARA A VEDIUM",
  title: "Prefere descrever com calma? Envie uma mensagem.",
  text: "A equipe Vedium responde por e-mail ou WhatsApp, conforme o contato que você deixar.",
  fields: {
    name: "Nome",
    email: "E-mail",
    phone: "WhatsApp (opcional)",
    subject: "Assunto",
    language: "Idioma de interesse",
    message: "Mensagem",
  },
  submitLabel: "Enviar mensagem",
  submitLabelLoading: "Enviando...",
  successTitle: "Mensagem recebida.",
  successText: "A equipe Vedium vai acompanhar seu contato. Se preferir uma resposta mais rápida, fale pelo WhatsApp.",
  validationErrorText: "Confira os campos destacados e tente novamente.",
  serverErrorText: "Não foi possível enviar agora. Você também pode chamar no WhatsApp.",
  privacyNoticeText: "Seus dados são usados só para responder este contato, conforme a",
  privacyNoticeLinkText: "Política de Privacidade",
  privacyNoticeHref: "/privacidade",
};

export const B2B_BLOCK = {
  eyebrow: "PARA EMPRESAS",
  title: "Desenvolvimento linguístico para profissionais e equipes.",
  text: "Se a necessidade envolve uma empresa, fale com a Vedium sobre objetivos, público e contexto do programa.",
  cta: { text: "Conheça a solução para empresas", href: "/empresas" } satisfies CtaLink,
};

export const NEXT_STEPS = {
  eyebrow: "PRÓXIMOS PASSOS",
  title: "O que acontece depois do seu contato.",
  text: "Do primeiro contato até o próximo passo, o caminho é simples e conduzido pela equipe Vedium.",
  steps: [
    { label: "01 VOCÊ FALA COM A VEDIUM", note: "Pelo WhatsApp ou pelo formulário, com o assunto que fizer sentido para você." },
    { label: "02 A EQUIPE VEDIUM RESPONDE", note: "Com orientação sobre curso, nível ou formato adequado ao seu objetivo." },
    { label: "03 VOCÊ CONHECE O PRÓXIMO PASSO", note: "Cursos, teste de nível quando disponível, ou o percurso mais adequado." },
  ],
};

export const CONTACT_FAQ: FaqItem[] = [
  {
    question: "Como saber por onde começar?",
    answer: "Fale com a Vedium pelo WhatsApp contando seu objetivo e idioma de interesse, ou veja como funciona o percurso de cada curso.",
  },
  {
    question: "Posso falar com a Vedium antes de escolher um curso?",
    answer: "Sim. Você pode conversar pelo WhatsApp ou pelo formulário desta página antes de se matricular, para entender qual curso e nível fazem sentido.",
  },
  {
    question: "Existe atendimento para empresas?",
    answer: "Sim. Para empresas, a Vedium estrutura programas de idiomas voltados ao desenvolvimento de equipes. Fale pelo WhatsApp ou conheça a solução para empresas.",
  },
  {
    question: "Onde vejo os cursos disponíveis?",
    answer: "A Vedium oferece Inglês, Iorubá, Português para Estrangeiros, Espanhol e Hebraico, além de soluções para empresas.",
  },
  {
    question: "Como falar com a Vedium pelo WhatsApp?",
    answer: "Use o número oficial +55 11 91129-3075, disponível nos botões de WhatsApp desta página.",
  },
];
