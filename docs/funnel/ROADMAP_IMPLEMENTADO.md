# Melhorias de funil e produto

## Implementado no código

- Captura pública de intenções por endpoint seguro: lead, aula diagnóstica, comunidade, indicação, B2B e depoimento verificado.
- Criação de Support Ticket para cada intenção pública, com e-mail interno para contato@vediums.com.
- Página pública de verificação de certificado por código.
- Páginas públicas de interesse para comunidade, programa de indicação, B2B e prática diária.
- Funil público: teste -> diagnóstico -> planos -> matrícula -> plataforma.
- Auditoria read-only de B1/B2 em produção.
- GTM com eventos do funil público.

## Depende de operação

- Publicar depoimentos reais somente após autorização.
- Configurar agenda/slots reais de professores em Lesson Slot.
- Definir regras comerciais de plano por curso antes de criar checkout direto sem etapa de plataforma.
- Conectar automação externa de WhatsApp/e-mail quando houver provedor e credenciais aprovadas.
