# 17 — Content Contract: `/como-funciona`

Separação exigida pela missão F.1 (seção 38): o que está confirmado por
fonte primária (HTTP, código-fonte do backend, conteúdo já aprovado em
outras páginas Next), o que não está confirmado, e o que não deve ser
publicado nesta página.

## CONFIRMED PUBLIC CLAIMS

Tudo que a página `/como-funciona` afirma, com a fonte:

| Afirmação | Fonte |
|---|---|
| Aulas são ao vivo, com professor em tempo real, turmas pequenas | Já confirmado e publicado nas 5 páginas de idioma + Home |
| Teste de nível gratuito existe para Português para Estrangeiros e Inglês | HTTP: `/teste-de-nivel` (200, conteúdo real de teste PT) e `/teste-de-nivel-ingles` (200) |
| Nenhum teste de nível existe hoje para Espanhol, Iorubá ou Hebraico | HTTP: `/teste-de-nivel-espanhol`, `/teste-de-nivel-hebraico`, `/teste-de-nivel-ioruba` — todos 404 |
| Inglês usa escala CEFR completa (A1, A2, A2+, B1, B2, C1) | `content/languages/english.ts` (`levels.items`), já aprovado na Fase D.2 |
| Espanhol usa Básico/Intermediário/Avançado (equivalência A1-A2/B1-B2.1/B2.2-C1) | `content/languages/spanish.ts`, já aprovado na Fase D.4 |
| PLE usa Básico/Intermediário/Avançado | `content/languages/portuguese-for-foreigners.ts`, já aprovado na Fase D.3 |
| Iorubá usa Básico/Intermediário/Avançado | `content/languages/yoruba.ts`, já aprovado na Fase D |
| Hebraico não é sequencial: percursos distintos (Alfabetização, Moderno A1/A2-B1, Bíblico, Particular) | `content/languages/hebrew.ts` + `course_urls.py` (`_SEQUENTIAL_LANGUAGES` exclui hebrew), já aprovado na Fase D.5 |
| Frequência de aulas ajustável de 1 a 5 por semana no checkout | `vedium_core/frequency_pricing_rules.py`: `MIN_CLASSES_PER_WEEK=1`, `MAX_CLASSES_PER_WEEK=5` |
| Aulas particulares confirmadas hoje só para Hebraico | `course_urls.py`: único slug `*-particular` é `hebraico-particular` |
| Turmas (formato padrão) existem nos 5 idiomas | Confirmado em cada página de idioma ("turma pequena"/"professor em tempo real") |
| Vedium para Empresas existe, hoje para Inglês/Iorubá/PLE | `/empresas` (aprovada Fase E.1), `content/b2b.ts` (`solution.text2`) |
| Matrícula, turma, nível, presença e progressão são acompanhados pela equipe Vedium | Mesma formulação institucional já aprovada em `content/b2b.ts` (`management.description`), sem alteração |
| Professores nativos e especialistas, conforme o percurso | Formulação já usada e aprovada em `content/b2b.ts` e nas 5 páginas de idioma |
| WhatsApp oficial: `+55 11 91129-3075` | `content/site/header.ts` (`WHATSAPP_HREF`), mesmo número usado em toda a base |

## UNCONFIRMED (não usado nesta página)

- Existência de teste de nível para Espanhol, Iorubá ou Hebraico —
  testado e refutado (404) nesta sessão. A página é explícita: só PT e
  Inglês têm teste.
- Tamanho máximo de turma, número exato de vagas — nenhuma fonte
  confirma um número universal; a página não cita nenhum.
- "Duas vezes por semana" como frequência padrão — a fonte real
  (`frequency_pricing_rules.py`) confirma uma faixa configurável de 1 a
  5, não um valor fixo. A página usa a faixa real, não um valor fixo.
- Aulas particulares para idiomas além de Hebraico — não confirmado em
  `course_urls.py`; a página não estende essa promessa aos outros 4
  idiomas.
- Tradução da página (`/en/como-funciona` etc.) — existe em produção
  Frappe, mas não nesta base Next; por isso o hreflang usado é o
  contrato mínimo (só pt-br + x-default), não o hreflang completo da
  produção.

## DO NOT PUBLISH (descartado explicitamente)

- Dashboard de progresso, IA avaliadora, percentual de progresso,
  analytics individual sofisticado — nenhuma dessas capacidades está
  implementada hoje (mesma auditoria já feita para `content/b2b.ts` na
  Fase E.1); a seção "Acompanhamento" usa só a formulação institucional
  já validada.
- Promessa de prazo fixo para avançar de nível ("em X meses você estará
  no próximo nível") — explicitamente proibido pela missão (seção 15);
  a seção "Continuidade" fala em "competências previstas para uma
  etapa", nunca em prazo.
- "Máximo 5 alunos por turma" ou qualquer regra de tamanho de turma como
  política comercial universal — a missão (seção 18) alerta que isso
  pode vir de contrato de um professor específico, não de política
  geral; não usado.
- Metodologia proprietária/exclusiva, "método revolucionário",
  "fluência garantida", linguagem de infoproduto — evitado
  integralmente, conforme o tom pedido (seção 3 da missão).
- Teste de nível apresentado como universal para os 5 idiomas — troca
  do CTA secundário do Hero (de "Descubra seu nível" para "Fale com a
  Vedium") evita exatamente essa promessa não confirmada.
- Página `/metodologia` como rota separada — não criada, para não gerar
  dois caminhos concorrentes para a mesma intenção (ver
  `16-how-it-works-seo-parity.md`, seção 2).
