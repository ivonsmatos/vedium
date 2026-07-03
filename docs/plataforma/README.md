# Documentação de Plataforma — Vedium

Esta pasta é a **camada operacional/técnica** da documentação da Vedium: descreve
como as regras de negócio rodam de fato sobre a plataforma Frappe/ERPNext/LMS +
o app custom `vedium_core`.

É diferente — e complementar — da documentação **estratégica/de marca** (identidade,
personas, modelo de negócio, GTM, financeiro, legal), que vive na pasta do cliente
(`Cliente/Vedium/Documentação`). Aquela responde "o que a Vedium é e para onde vai".
**Esta responde "como o sistema faz, hoje, o que a Vedium promete".**

## Por que esta camada existe

Sem ela, cada tarefa vira tentativa e erro: constrói-se do zero algo que a
plataforma já faz nativo, ou mexe-se num doctype legado achando que é o certo.
O caso concreto que motivou esta pasta: o agendamento de aulas foi implementado
como páginas custom no site antes de descobrir que o **Frappe LMS já traz
agendamento 1-a-1 nativo** (Course Evaluator + Google Meet). O documento
[01 — Mapa Nativo vs. Custom](01-mapa-nativo-vs-custom.md) existe para que isso
não se repita.

## Regra de ouro

> **Antes de construir qualquer coisa, consulte o [Mapa Nativo vs. Custom](01-mapa-nativo-vs-custom.md).**
> Se a plataforma já faz nativo, use o nativo. Só se escreve código custom quando
> o mapa mostra que não existe nada nativo que atenda. Se a necessidade for maior
> que o que `vedium_core`+LMS já cobrem (RH, CRM, suporte, BI, aula em grupo),
> veja também o [Ecossistema Frappe Oficial](04-ecossistema-frappe-oficial.md)
> antes de propor um app de terceiro ou construir do zero.

## Índice

| # | Documento | O que responde | Status |
|---|-----------|----------------|--------|
| 01 | [Mapa Nativo vs. Custom](01-mapa-nativo-vs-custom.md) | Cada necessidade já é nativa ou é custom? Onde? | ✅ |
| 02 | [Dicionário de Doctypes & Modelo de Domínio](02-dicionario-doctypes.md) | O que cada doctype representa e como se relacionam | ✅ |
| — | [Arquitetura i18n](03-arquitetura-i18n.md) | Como funciona a tradução do site por idioma | ✅ |
| 04 | [Ecossistema Frappe Oficial](04-ecossistema-frappe-oficial.md) | Quais apps oficiais Frappe (instalados ou não) resolvem lacunas de operar a escola | ✅ |
| 05 | [Fluxo — Jornada do Aluno](05-fluxo-jornada-do-aluno.md) | Checkout → matrícula → aula → certificado | ✅ |
| 06 | [Fluxo — Jornada do Professor](06-fluxo-jornada-do-professor.md) | Instrutor → evaluator → slots → aula → certifica | ✅ |
| 07 | Fluxo — Agendamento de aulas | 1-a-1 (Evaluator/Meet) vs. grupo (Live Class/Meet) | ⏳ |
| 08 | Fluxo — Pagamento, Cupom e Indicação | Checkout custom → webhook → matrícula → recompensa | ⏳ |
| 09 | Fluxo — Certificação | enable_certification → avaliação → certificado | ⏳ |
| 10 | Matriz de Integrações | Google, Stripe, e-mail, Zoom, WhatsApp, GTM, IA | ⏳ |
| 11 | [Estado do Ambiente (checklist vivo)](11-estado-do-ambiente.md) | O que está ligado/desligado em produção hoje | ✅ |
| 12 | Runbook de Operação & Deploy | Como deploya, footguns, logs, rollback | ⏳ |
| 13 | Catálogo de Produtos & Preços | Cursos publicados, slugs, níveis, preços, professor | ⏳ |

Legenda: ✅ escrito · ⏳ a escrever

## Como manter

- Estes documentos **acompanham o código**. Mudou a plataforma? Atualize o doc na
  mesma PR.
- Fatos de produção (o que está ligado, quais cursos existem) têm data de
  verificação. Se estiver velho, reconfirme no servidor antes de confiar.
