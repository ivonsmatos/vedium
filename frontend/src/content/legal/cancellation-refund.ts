import type { LegalDocument } from "./types";

export const CANCELLATION_REFUND_DOCUMENT: LegalDocument = {
  slug: "cancelamento-reembolso",
  title: "Política de Cancelamento e Reembolso",
  lastUpdated: "Última atualização: 5 de julho de 2026. Aplica-se a planos B2C. Contratos B2B podem ter regras específicas.",
  seo: {
    title: "Cancelamento e Reembolso - Vedium",
    description: "Regras de cancelamento de assinatura, direito de arrependimento de 7 dias corridos e reembolso na Vedium. Sem fidelidade, sem multa.",
    canonical: "https://vediums.com/cancelamento-reembolso",
    robots: "index, follow",
  },
  introduction: [
    { type: "notice", tone: "success", lines: [[
      { text: "✅ Assinatura sem fidelidade e sem multa de cancelamento.", strong: true },
      { text: " Cancele quando quiser para impedir novas cobranças. Pagamentos processados pela Stripe." },
    ]] },
    { type: "notice", tone: "info", lines: [[
      { text: "⏱ Direito de arrependimento 7 dias corridos:", strong: true },
      { text: " contratações online podem ser canceladas com " },
      { text: "reembolso integral", strong: true },
      { text: " em até 7 dias corridos da contratação, conforme o Código de Defesa do Consumidor (art. 49)." },
    ]] },
  ],
  sections: [
    { id: "assinatura-mensal", heading: "1. Assinatura mensal", blocks: [{ type: "list", ordered: true, items: [
      [{ text: "Planos mensais B2C não têm fidelidade nem multa de cancelamento." }],
      [{ text: "A cobrança recorrente é realizada pela Stripe conforme a periodicidade contratada." }],
      [{ text: "O cancelamento impede novas cobranças futuras, mas não elimina obrigações já vencidas." }],
    ] }] },
    { id: "direito-arrependimento", heading: "2. Direito de arrependimento 7 dias", blocks: [{ type: "list", ordered: true, items: [
      [{ text: "Pedido enviado pelo canal de suporte ou meio indicado no site/app, com identificação e e-mail da conta." }],
      [{ text: "Prazo contado em dias corridos a partir da contratação." }],
      [{ text: "Após aprovação, o estorno segue os prazos da Stripe, bandeira e banco emissor." }],
      [{ text: "O exercício do arrependimento pode encerrar o acesso ao plano, aulas e benefícios vinculados." }],
    ] }] },
    { id: "cancelamento-apos-sete-dias", heading: "3. Cancelamento após 7 dias", blocks: [{ type: "paragraph", content: [
      { text: "Após o prazo de arrependimento, o cancelamento encerra a renovação futura, mas " },
      { text: "não gera reembolso automático", strong: true },
      { text: " do ciclo vigente. O aluno pode manter acesso até o fim do período já pago, salvo violação de Termos, fraude ou inadimplência." },
    ] }] },
    { id: "hipoteses-reembolso", heading: "4. Hipóteses de reembolso ou crédito fora dos 7 dias", blocks: [{ type: "list", items: [
      [{ text: "Cobrança duplicada comprovada" }],
      [{ text: "Erro material de cobrança imputável à Vedium" }],
      [{ text: "Indisponibilidade relevante e prolongada do serviço por culpa da Vedium, sem alternativa razoável" }],
      [{ text: "Cancelamento de turma pela Vedium sem oferta de reposição, crédito ou alternativa equivalente" }],
      [{ text: "Direito legal obrigatório reconhecido no caso concreto" }],
      [{ text: "Exceção comercial aprovada pela Vedium por escrito" }],
    ] }] },
    { id: "sem-reembolso-automatico", heading: "5. Situações que não geram reembolso automático", blocks: [{ type: "notice", tone: "danger", lines: [
      [{ text: "Falta do aluno à aula marcada" }],
      [{ text: "Problemas de internet, câmera, microfone ou equipamento do aluno" }],
      [{ text: "Desistência após os 7 dias sem falha da Vedium" }],
      [{ text: "Baixa participação, falta de estudo ou expectativa de resultado não garantido" }],
      [{ text: "Compartilhamento indevido de conta ou violação de direitos autorais" }],
      [{ text: "Impossibilidade temporária do aluno por motivos pessoais (salvo política comercial de crédito aplicável)" }],
    ] }] },
    { id: "reposicao-aulas", heading: "6. Reposição de aulas", blocks: [{ type: "paragraph", content: [{ text: "Quando existir, a política de reposição é informada no plano ou regulamento da turma. Aulas gravadas, exercícios e mudança de turma podem ser oferecidos como alternativas, sem que isso represente reembolso automático." }] }] },
    { id: "aula-experimental", heading: "7. Aula experimental", blocks: [{ type: "paragraph", content: [{ text: "Aula experimental gratuita não gera cobrança. Caso esteja vinculada a cadastro, vaga ou promoção, as condições são informadas antes da participação." }] }] },
    { id: "inadimplencia", heading: "8. Falha no pagamento e inadimplência", blocks: [{ type: "list", ordered: true, items: [
      [{ text: "Falha de pagamento gera aviso e nova tentativa de cobrança pela Stripe." }],
      [{ text: "Inadimplência persistente pode gerar suspensão de acesso, vaga, aulas, certificados e suporte até regularização." }],
      [{ text: "A regularização não garante a mesma turma ou horário se houver perda de vaga por inadimplência prolongada." }],
    ] }] },
    { id: "chargeback", heading: "9. Chargeback e contestação", blocks: [{ type: "paragraph", content: [{ text: "Contestações indevidas podem gerar suspensão do acesso até esclarecimento. A Vedium poderá apresentar à Stripe, banco ou bandeira comprovantes de contratação, aceite, acesso, aulas realizadas e uso da plataforma." }] }] },
    { id: "como-solicitar", heading: "10. Como solicitar cancelamento ou reembolso", blocks: [
      { type: "steps", items: [
        { number: "1", text: "Acesse a área do aluno" },
        { number: "2", text: "Envie pelo canal oficial de suporte" },
        { number: "3", text: "Informe nome, e-mail, plano e data" },
        { number: "4", text: "Guarde o protocolo de solicitação" },
      ] },
      { type: "paragraph", content: [{ text: "Contato: " }, { text: "contato@vediums.com", href: "mailto:contato@vediums.com", strong: true }] },
    ] },
  ],
  actions: [{ label: "Versão PDF oficial", href: "/assets/vedium_core/legal/politica-de-cancelamento-reembolso.pdf", newTab: true }],
  relatedLinks: [
    { label: "Termos de Uso", href: "/termos" },
    { label: "Política de Privacidade", href: "/privacidade" },
    { label: "Política de Cookies", href: "/cookies" },
    { label: "Propriedade Intelectual", href: "/propriedade-intelectual" },
  ],
  stamp: "Base legal: CDC (Lei 8.078/1990 - art. 49) · LGPD (Lei 13.709/2018) · Marco Civil da Internet (Lei 12.965/2014)",
};
