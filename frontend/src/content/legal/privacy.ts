import type { LegalDocument } from "./types";

export const PRIVACY_DOCUMENT: LegalDocument = {
  slug: "privacidade",
  title: "Política de Privacidade",
  lastUpdated: "Última atualização: 5 de julho de 2026. Em conformidade com a LGPD - Lei nº 13.709/2018.",
  seo: {
    title: "Política de Privacidade - Vedium",
    description: "Como a Vedium coleta, usa e protege dados pessoais em conformidade com a LGPD. Direitos dos titulares, DPO e canais de contato.",
    canonical: "https://vediums.com/privacidade",
    robots: "index, follow",
  },
  introduction: [
    {
      type: "notice",
      tone: "neutral",
      lines: [
        [{ text: "🇬🇧 This legal document is available only in Portuguese, to preserve legal accuracy under Brazilian law (LGPD). Please use your browser's translation tool if needed." }],
        [{ text: "🇪🇸 Este documento legal está disponible solo en portugués, para preservar la precisión jurídica según la ley brasileña (LGPD). Use la herramienta de traducción de su navegador si lo necesita." }],
        [{ text: "🇫🇷 Ce document juridique n'est disponible qu'en portugais, afin de préserver son exactitude juridique selon la loi brésilienne (LGPD). Utilisez l'outil de traduction de votre navigateur si nécessaire." }],
        [{ text: "🇩🇪 Dieses Rechtsdokument ist aus Gründen der rechtlichen Genauigkeit nach brasilianischem Recht (LGPD) nur auf Portugiesisch verfügbar. Nutzen Sie bei Bedarf die Übersetzungsfunktion Ihres Browsers." }],
      ],
    },
    {
      type: "notice",
      tone: "info",
      lines: [
        [{ text: "Controladora:", strong: true }, { text: " VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA CNPJ 58.434.869/0001-24" }],
        [{ text: "Encarregado de Proteção de Dados (DPO):", strong: true }, { text: " dpo@vediums.com", href: "mailto:dpo@vediums.com" }],
        [{ text: "Exercer seus direitos:", strong: true }, { text: " Área do Titular Meus Dados", href: "/privacidade/meus-dados" }],
      ],
    },
  ],
  sections: [
    {
      id: "quem-somos",
      heading: "1. Quem somos e o que esta política cobre",
      blocks: [{ type: "paragraph", content: [{ text: "Esta Política descreve como a Vedium coleta, usa, compartilha e protege dados pessoais de alunos, visitantes, professores e contatos, no Brasil e no exterior, em conformidade com a LGPD e demais normas aplicáveis." }] }],
    },
    {
      id: "dados-coletados",
      heading: "2. Dados coletados",
      blocks: [
        {
          type: "list",
          items: [
            [{ text: "Cadastro:", strong: true }, { text: " nome, e-mail, telefone, data de nascimento (quando solicitada), idioma de interesse, nível e dados necessários para prestação do serviço." }],
            [{ text: "Pagamento:", strong: true }, { text: " dados de cobrança e transação processados pela Stripea Vedium não armazena número completo de cartão." }],
            [{ text: "Uso da plataforma:", strong: true }, { text: " presença em aulas, progresso, avaliações, certificados e interações pedagógicas." }],
            [{ text: "Comunicações:", strong: true }, { text: " e-mails, mensagens e histórico de suporte." }],
            [{ text: "Técnicos:", strong: true }, { text: " endereço IP, tipo de navegador, dispositivo, logs de acesso e cookies (ver " }, { text: "Política de Cookies", href: "/cookies" }, { text: ")." }],
            [{ text: "Gravações:", strong: true }, { text: " imagem, voz, chat e participação em aulas quando aplicável." }],
          ],
        },
      ],
    },
    {
      id: "dados-sensiveis",
      heading: "3. Dados sensíveis regra especial para Iorubá",
      blocks: [
        {
          type: "notice",
          tone: "info",
          lines: [[
            { text: "O interesse em Iorubá é tratado como interesse " },
            { text: "educacional e cultural", strong: true },
            { text: ". A Vedium " },
            { text: "não", strong: true },
            { text: " infere, registra, classifica, segmenta ou usa para publicidade dados sobre religião, terreiro, convicção espiritual ou qualquer outro dado sensível." },
          ]],
        },
      ],
    },
    {
      id: "finalidades-bases-legais",
      heading: "4. Finalidades e bases legais",
      blocks: [{
        type: "table",
        label: "Finalidades e bases legais do tratamento de dados",
        headers: ["Finalidade", "Base legal (LGPD)", "Observação"],
        rows: [
          ["Criar conta e prestar aulas", "Execução de contrato", "Acesso por perfil e logs"],
          ["Processar pagamento", "Execução de contrato / obrigação legal", "Via Stripe; retenção fiscal"],
          ["Acompanhar evolução e emitir certificado", "Execução de contrato", "Acesso restrito"],
          ["Enviar comunicações do curso", "Execução de contrato / legítimo interesse", "Relacionadas ao serviço"],
          ["Marketing e relacionamento", "Consentimento / legítimo interesse com opt-out", "Descadastro fácil"],
          ["Gravar aulas", "Execução de contrato / consentimento", "Aviso prévio, retenção definida"],
          ["Publicar imagem ou depoimento", "Consentimento específico", "Termo próprio e revogação"],
          ["IA de apoio pedagógico", "Execução de contrato / legítimo interesse", "Minimização de dados"],
          ["Segurança e prevenção a fraude", "Legítimo interesse / obrigação legal", "Monitoramento proporcional"],
          ["Relatórios B2B", "Execução de contrato / legítimo interesse", "Limitados ao necessário"],
          ["Atender direitos LGPD", "Obrigação legal", "Protocolo e evidência"],
        ],
      }],
    },
    {
      id: "criancas-adolescentes",
      heading: "5. Crianças e adolescentes",
      blocks: [{ type: "paragraph", content: [{ text: "A Vedium aceita menores somente com fluxo específico de responsável legal, consentimento adequado, limitação de coleta e proteção reforçada. Dados de menores não são usados para publicidade comportamental ou treinamento de IA sem avaliação específica." }] }],
    },
    {
      id: "gravacao-aulas",
      heading: "6. Gravação de aulas",
      blocks: [{ type: "list", ordered: true, items: [
        [{ text: "Aulas podem ser gravadas para fins pedagógicos, reposição, qualidade, segurança e comprovação do serviço." }],
        [{ text: "Acesso restrito à turma, professor, coordenação e DPO quando necessário." }],
        [{ text: "Uso para marketing, redes sociais ou publicidade exige " }, { text: "termo específico", href: "/gravacao-imagem-voz" }, { text: "." }],
        [{ text: "Gravações de menores exigem autorização do responsável legal e proteção reforçada." }],
        [{ text: "Retenção: até 180 dias, salvo exceção justificada." }],
      ] }],
    },
    {
      id: "compartilhamento",
      heading: "7. Compartilhamento de dados",
      blocks: [{
        type: "table",
        label: "Destinatários e finalidades do compartilhamento de dados",
        headers: ["Destinatário", "Finalidade", "Controle"],
        rows: [
          ["Stripe", "Pagamento, recorrência, antifraude", "Contrato/DPA e transferência internacional"],
          ["Hospedagem e infraestrutura", "Operar plataforma e banco de dados", "Controle de acesso e backups"],
          ["Videoconferência", "Aulas ao vivo e gravações", "Configuração privada"],
          ["E-mail, CRM e suporte", "Comunicações e atendimento", "Acesso restrito e DPA"],
          ["Fornecedores de IA", "Apoio pedagógico", "Minimização e não-treinamento"],
          ["Professores", "Ministrar aulas e acompanhar alunos", "Contrato e confidencialidade"],
          ["Empresas B2B", "Relatórios corporativos", "Anexo B2B e transparência ao colaborador"],
          ["Autoridades", "Cumprimento legal", "Registro e minimização"],
        ],
      }],
    },
    {
      id: "transferencia-internacional",
      heading: "8. Transferência internacional",
      blocks: [{ type: "paragraph", content: [{ text: "Dados podem ser transferidos para outros países ao usar Stripe, infraestrutura global, videoconferência, e-mail, CRM, IA ou analytics. A transferência observa mecanismo legal adequado (cláusulas-padrão contratuais, decisão de adequação ou outra hipótese da LGPD e ANPD)." }] }],
    },
    {
      id: "retencao",
      heading: "9. Retenção de dados",
      blocks: [{
        type: "table",
        label: "Prazos de retenção por categoria de dado",
        headers: ["Dado", "Prazo"],
        rows: [
          ["Leads sem matrícula", "Até 24 meses da última interação ou opt-out"],
          ["Conta e histórico pedagógico", "Durante relação + até 5 anos"],
          ["Dados financeiros/fiscais", "Prazo legal, referência mínima de 5 anos"],
          ["Logs de aplicação", "Conforme obrigação legal; referência de 6 meses"],
          ["Gravações pedagógicas", "Até 180 dias, salvo exceção justificada"],
          ["Depoimentos e marketing", "Até revogação ou prazo definido no termo"],
          ["Solicitações LGPD", "Até 5 anos após encerramento do protocolo"],
          ["Incidentes", "Mínimo de 5 anos"],
        ],
      }],
    },
    {
      id: "direitos",
      heading: "10. Seus direitos como titular",
      blocks: [
        { type: "list", items: [
          [{ text: "Confirmar existência de tratamento" }],
          [{ text: "Acessar seus dados pessoais" }],
          [{ text: "Corrigir dados incompletos, inexatos ou desatualizados" }],
          [{ text: "Solicitar anonimização, bloqueio ou eliminação de dados desnecessários ou irregulares" }],
          [{ text: "Portabilidade (quando regulamentada)" }],
          [{ text: "Receber informação sobre compartilhamento" }],
          [{ text: "Revogar consentimento" }],
          [{ text: "Opor-se a tratamento irregular" }],
          [{ text: "Solicitar revisão de decisões automatizadas" }],
        ] },
        { type: "notice", tone: "neutral", lines: [
          [{ text: "Exercer meus direitos", href: "/privacidade/meus-dados" }],
          [{ text: "Falar com o DPO", href: "mailto:dpo@vediums.com" }],
        ] },
      ],
    },
    {
      id: "seguranca",
      heading: "11. Segurança",
      blocks: [{ type: "list", items: [
        [{ text: "Controle de acesso por perfil e necessidade" }],
        [{ text: "Senhas fortes e autenticação reforçada" }],
        [{ text: "Criptografia em trânsito" }],
        [{ text: "Backups, logs e monitoramento" }],
        [{ text: "Contratos de confidencialidade com operadores" }],
        [{ text: "Procedimento de resposta a incidentes" }],
      ] }],
    },
    {
      id: "incidentes",
      heading: "12. Incidentes de segurança",
      blocks: [{ type: "paragraph", content: [{ text: "Se houver incidente com risco relevante, a Vedium avaliará, conterá, registrará evidências e realizará as comunicações cabíveis à ANPD e aos titulares conforme a LGPD." }] }],
    },
    {
      id: "atualizacoes",
      heading: "13. Atualizações",
      blocks: [{ type: "paragraph", content: [{ text: "Esta Política pode ser atualizada para refletir mudanças legais, de fornecedores ou tecnológicas. A versão vigente fica sempre publicada nesta página." }] }],
    },
  ],
  actions: [{ label: "Versão PDF oficial", href: "/assets/vedium_core/legal/politica-de-privacidade.pdf", newTab: true }],
  relatedLinks: [
    { label: "Termos de Uso", href: "/termos" },
    { label: "Política de Cookies", href: "/cookies" },
    { label: "Cancelamento e Reembolso", href: "/cancelamento-reembolso" },
    { label: "Propriedade Intelectual", href: "/propriedade-intelectual" },
    { label: "Gravação, Imagem e Voz", href: "/gravacao-imagem-voz" },
    { label: "Meus Dados (LGPD)", href: "/privacidade/meus-dados" },
  ],
  stamp: "Base legal: LGPD (Lei 13.709/2018) · CDC (Lei 8.078/1990) · Código Civil (Lei 10.406/2002) · Marco Civil da Internet (Lei 12.965/2014) · Estatuto Digital da Criança e Adolescente (Lei 15.211/2025)",
};
