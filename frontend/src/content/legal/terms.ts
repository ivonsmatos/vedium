import type { LegalDocument } from "./types";

export const TERMS_DOCUMENT: LegalDocument = {
  slug: "termos",
  title: "Termos de Uso e Contratação",
  lastUpdated: "Última atualização: 5 de julho de 2026.",
  seo: {
    title: "Termos de Uso e Contratação - Vedium",
    description: "Termos de Uso e Contratação da Vedium: cadastro, planos, pagamento, aulas ao vivo, cancelamento e propriedade intelectual.",
    canonical: "https://vediums.com/termos",
    robots: "index, follow",
  },
  introduction: [
    {
      type: "notice",
      tone: "neutral",
      lines: [
        [{ text: "🇬🇧 This legal document is available only in Portuguese, to preserve legal accuracy under Brazilian law. Please use your browser's translation tool if needed." }],
        [{ text: "🇪🇸 Este documento legal está disponible solo en portugués, para preservar la precisión jurídica según la ley brasileña. Use la herramienta de traducción de su navegador si lo necesita." }],
        [{ text: "🇫🇷 Ce document juridique n'est disponible qu'en portugais, afin de préserver son exactitude juridique selon la loi brésilienne. Utilisez l'outil de traduction de votre navigateur si nécessaire." }],
        [{ text: "🇩🇪 Dieses Rechtsdokument ist aus Gründen der rechtlichen Genauigkeit nach brasilianischem Recht nur auf Portugiesisch verfügbar. Nutzen Sie bei Bedarf die Übersetzungsfunktion Ihres Browsers." }],
      ],
    },
    {
      type: "notice",
      tone: "info",
      lines: [
        [{ text: "Controladora:", strong: true }, { text: " VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA CNPJ 58.434.869/0001-24" }],
        [{ text: "Endereço:", strong: true }, { text: " Av. Eng. Luiz Carlos Berrini, 1681, Conj. Salas 111 e 112, Cidade Monções, São Paulo/SP, CEP 04571-011" }],
        [{ text: "Contato:", strong: true }, { text: " contato@vediums.com", href: "mailto:contato@vediums.com" }],
      ],
    },
    {
      type: "notice",
      tone: "warning",
      lines: [[
        { text: "⏱ Direito de arrependimento:", strong: true },
        { text: " contratações online podem ser canceladas com reembolso integral em até " },
        { text: "7 (sete) dias corridos", strong: true },
        { text: " da contratação, conforme o Código de Defesa do Consumidor. Ver " },
        { text: "Política de Cancelamento e Reembolso", href: "/cancelamento-reembolso" },
        { text: "." },
      ]],
    },
  ],
  sections: [
    { id: "aceitacao", heading: "1. Aceitação", blocks: [{ type: "paragraph", content: [{ text: "Ao criar conta, contratar um plano ou acessar as aulas, você concorda com estes Termos e com todos os documentos legais da Vedium referenciados aqui. Leia antes de contratar." }] }] },
    { id: "elegibilidade", heading: "2. Elegibilidade", blocks: [{ type: "list", ordered: true, items: [
      [{ text: "A Vedium é voltada a maiores de 18 anos ou emancipados legalmente." }],
      [{ text: "Menores poderão ser aceitos em momento futuro mediante fluxo específico de responsável legal." }],
      [{ text: "Até a implementação desse fluxo, não é permitido cadastro autônomo de menor sem responsável legal." }],
      [{ text: "O responsável legal responde pela veracidade das informações, pagamento e uso adequado da plataforma." }],
    ] }] },
    { id: "conta-senha", heading: "3. Conta, senha e uso pessoal", blocks: [{ type: "list", ordered: true, items: [
      [{ text: "A conta é pessoal, individual e intransferível." }],
      [{ text: "É proibido compartilhar login, senha, links, gravações ou materiais com terceiros." }],
      [{ text: "Forneça dados verdadeiros, completos e atualizados." }],
      [{ text: "A Vedium pode bloquear contas com uso fraudulento, compartilhamento indevido, violação de direitos autorais, assédio ou descumprimento destes Termos." }],
    ] }] },
    { id: "planos-pagamento", heading: "4. Planos, assinatura, preço e pagamento", blocks: [{ type: "list", ordered: true, items: [
      [{ text: "Valores, periodicidade, moeda e benefícios são exibidos no checkout ou proposta comercial." }],
      [{ text: "Pagamentos online são processados pela " }, { text: "Stripe", strong: true }, { text: " ou provedor informado pela Vedium. A Vedium não armazena número completo de cartão." }],
      [{ text: "Planos recorrentes são cobrados conforme periodicidade contratada, até cancelamento." }],
      [{ text: "Tributos, IOF, variação cambial e tarifas bancárias podem incidir conforme meio de pagamento e país." }],
      [{ text: "A Vedium pode reajustar preços mediante aviso prévio razoável, sem afetar valores já pagos no ciclo vigente." }],
    ] }] },
    { id: "cancelamento-reembolso", heading: "5. Cancelamento e reembolso", blocks: [{ type: "paragraph", content: [
      { text: "Planos mensais B2C não têm fidelidade nem multa. O cancelamento impede cobranças futuras, mas não gera reembolso automático do ciclo vigente após os 7 dias. Detalhamento completo: " },
      { text: "Política de Cancelamento e Reembolso", href: "/cancelamento-reembolso" },
      { text: "." },
    ] }] },
    { id: "aulas-gravacao", heading: "6. Aulas ao vivo, presença e gravação", blocks: [{ type: "list", ordered: true, items: [
      [{ text: "Aulas são online e ao vivo, com interação em tempo real." }],
      [{ text: "Aulas podem ser gravadas pela Vedium para reposição, qualidade, segurança e cumprimento de contrato. O aluno é informado previamente." }],
      [{ text: "Uso público de imagem, voz ou depoimento para marketing exige autorização específica ver " }, { text: "Termo de Gravação, Imagem, Voz e Depoimento", href: "/gravacao-imagem-voz" }, { text: "." }],
      [{ text: "É proibido ao aluno gravar, transmitir ou compartilhar aulas ou materiais sem autorização prévia." }],
      [{ text: "Regras de falta, reposição e remarcação são informadas no plano ou regulamento da turma." }],
    ] }] },
    { id: "conduta", heading: "7. Conduta nas aulas e na comunidade", blocks: [{ type: "list", items: [
      [{ text: "Tratar professores, alunos, equipe e parceiros com respeito." }],
      [{ text: "Não praticar assédio, discriminação, intolerância religiosa, racismo, xenofobia ou discurso de ódio." }],
      [{ text: "Não usar aula ou comunidade para spam, venda, propaganda política ou captação de alunos." }],
      [{ text: "Respeitar conteúdos culturais e tradicionais (especialmente Iorubá) sem apropriação ou exotização indevida." }],
    ] }] },
    { id: "inteligencia-artificial", heading: "8. Inteligência Artificial", blocks: [{ type: "list", items: [
      [{ text: "A Vedium pode oferecer IA como apoio pedagógico não substitui professor nem avaliação humana." }],
      [{ text: "Não insira senhas, documentos sensíveis, dados de terceiros ou segredos em ferramentas de IA." }],
      [{ text: "Saídas de IA podem conter erros; revise decisões relevantes com professor ou equipe." }],
    ] }] },
    { id: "propriedade-intelectual", heading: "9. Propriedade intelectual", blocks: [{ type: "paragraph", content: [
      { text: "Marca, plataforma, método, aulas, materiais, exercícios, vídeos e certificados são protegidos por direitos autorais. A contratação concede licença limitada, pessoal, revogável e intransferível. É proibido copiar, vender, licenciar, distribuir ou treinar IA com materiais da Vedium sem autorização. Ver " },
      { text: "Política de Propriedade Intelectual", href: "/propriedade-intelectual" },
      { text: "." },
    ] }] },
    { id: "privacidade", heading: "10. Privacidade", blocks: [{ type: "paragraph", content: [
      { text: "Tratamento de dados conforme a " }, { text: "Política de Privacidade", href: "/privacidade" }, { text: ". Canal do DPO: " }, { text: "dpo@vediums.com", href: "mailto:dpo@vediums.com" }, { text: "." },
    ] }] },
    { id: "disponibilidade", heading: "11. Disponibilidade e limitações técnicas", blocks: [{ type: "paragraph", content: [{ text: "A Vedium envidará esforços para manter a plataforma disponível e segura. Interrupções podem ocorrer por manutenção, falhas de terceiros ou força maior. O aluno é responsável por equipamento, câmera, microfone e conexão." }] }] },
    { id: "suspensao", heading: "12. Suspensão e encerramento", blocks: [{ type: "paragraph", content: [{ text: "A Vedium pode suspender acesso por inadimplência, fraude, risco de segurança, violação de direitos autorais, comportamento abusivo ou ordem legal. Quando possível, o aluno será notificado com oportunidade de regularização." }] }] },
    { id: "lei-foro", heading: "13. Lei aplicável e foro", blocks: [{ type: "paragraph", content: [{ text: "Aplica-se a lei brasileira. Para relações de consumo, o aluno pode exercer os direitos do Código de Defesa do Consumidor. Fica eleito o foro da Comarca de São Paulo/SP, sem prejuízo de foro legal obrigatório em favor do consumidor." }] }] },
    { id: "alteracoes", heading: "14. Alterações", blocks: [{ type: "paragraph", content: [{ text: "Estes Termos podem ser atualizados para refletir mudanças legais, operacionais ou tecnológicas. Alterações relevantes serão comunicadas e não prejudicarão direitos adquiridos no ciclo já pago." }] }] },
  ],
  actions: [{ label: "Versão PDF oficial", href: "/assets/vedium_core/legal/termos-de-uso-e-contratacao.pdf", newTab: true }],
  relatedLinks: [
    { label: "Política de Privacidade", href: "/privacidade" },
    { label: "Política de Cookies", href: "/cookies" },
    { label: "Cancelamento e Reembolso", href: "/cancelamento-reembolso" },
    { label: "Propriedade Intelectual", href: "/propriedade-intelectual" },
    { label: "Gravação, Imagem e Voz", href: "/gravacao-imagem-voz" },
    { label: "Meus Dados (LGPD)", href: "/privacidade/meus-dados" },
  ],
  stamp: "Base legal: LGPD (Lei 13.709/2018) · CDC (Lei 8.078/1990) · Código Civil (Lei 10.406/2002) · Marco Civil da Internet (Lei 12.965/2014)",
};
