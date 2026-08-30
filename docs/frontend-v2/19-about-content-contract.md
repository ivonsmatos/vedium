# 19 — Content Contract: `/sobre`

Separação exigida pela missão F.2 (seção 37): o que é público e
verificado contra a fonte oficial, o que é informação interna que não
deve ser publicada, e o que não está verificado e por isso não foi
usado.

Fonte oficial: `01_Vedium_Identidade_Organizacional_Completa_v4.docx`
(extraído e lido nesta sessão em texto puro a partir do XML interno do
.docx).

## PUBLIC / VERIFIED

| Conteúdo em `/sobre` | Origem no documento oficial |
|---|---|
| H2 "Uma escola construída sobre interação, método e repertório." | Título da seção "01 · Fundamentos da marca" |
| Texto de Quem Somos ("O valor não está apenas no acesso ao conteúdo...") | Parágrafo de abertura da seção 01, citado quase literalmente (já era a mensagem central pedida pela própria missão, seção 7) |
| 2ª frase de Quem Somos (papel da Missão oficial) | Seção "03 · Razão de ser" → Missão: "Oferecer educação linguística online ao vivo, conduzida por professores nativos e especialistas, com trilhas claras, acompanhamento próximo e aplicação na vida pessoal, acadêmica e profissional." — incorporada sem criar caixa "Missão" (missão F.2 seção 9) |
| H2 de Propósito ("Ampliar a capacidade de compreender, comunicar e participar.") | Seção 03 → Propósito oficial, resumido no H2, com o parágrafo completo no corpo do texto |
| Fechamento de "Por Que Existimos" (Visão) | Seção 03 → Visão: "Ser reconhecida como uma referência premium e acessível em ensino de idiomas ao vivo, valorizando tanto idiomas de alta demanda internacional quanto línguas de relevância histórica e cultural." — equilíbrio exato preservado, sem "ser líder de mercado" |
| 4 itens de "No Que Acreditamos" (Interação/Contexto/Constância/Tecnologia) | Seção "04 · Manifesto", paráfrase editorial dos mesmos 4 conceitos sugeridos literalmente pela missão F.2 (seção 11) |
| Texto de "Professores e Tecnologia" | Seção 04 (Manifesto): "A tecnologia amplia o acesso, organiza a jornada e torna o progresso visível. Ela não substitui o professor. O centro da experiência continua sendo o encontro entre pessoas..." |
| "professores nativos e especialistas, de acordo com a natureza de cada percurso" | Seção "06 · Arquitetura acadêmica" → "Padrões comuns a todas as trilhas" (mesma formulação, adaptada de "conforme a natureza da trilha") |
| 4 itens de "A Experiência" (Clareza de entrada/Interação real/Progressão/Acompanhamento) | Seção "07 · Princípios da experiência" — 4 dos 7 princípios oficiais da tabela (os outros 3 estão cobertos em Condução Pedagógica e Rigor Cultural) |
| Texto de "Rigor Cultural" | Valor oficial "Rigor cultural" (seção 05) + as 5 restrições por idioma já aprovadas e publicadas nas próprias páginas de curso (Iorubá sem exotismo, Hebraico sem reduzir à religião, PLE sem reduzir a turismo, Espanhol sem tratar o mundo hispânico como bloco único) |
| 4 itens de "Princípios" (Profissionalismo/Rigor cultural/Evolução visível/Transparência) | Seção "05 · Valores e comportamentos", coluna "Na prática" de cada valor, resumida |
| "ausência de fidelidade nos planos aplicáveis" | Citação quase literal do valor "Transparência" (seção 05): "Condições claras, expectativas realistas e ausência de fidelidade nos planos aplicáveis." — escopo "nos planos aplicáveis" preservado, sem generalizar (missão F.2 seção 19) |
| Portfólio (5 idiomas + referência a B2B) | Seção "06 · Arquitetura acadêmica", só a coluna pública (idioma existe, direção formativa geral) — URLs reais via `HEADER_COURSES`, mesma fonte da Home |
| Boilerplate/assinatura (inspiração do tom da página, não copiado literalmente) | Seção "10 · Tom e assinatura institucional" |

## INTERNAL / DO NOT PUBLISH

Informação real, presente no documento oficial, mas que não deve
aparecer numa página pública — nada disso foi usado:

- Coluna "Papel de marca" da tabela de Arquitetura Acadêmica (volume,
  autoridade, receita, ticket por idioma) — função estratégica interna,
  proibida explicitamente pela missão (seção 17).
- Seção "08 · Cultura interna" (rituais: revisão mensal de experiência,
  encontro pedagógico mensal, revisão de marca quinzenal, painel
  executivo semanal, escuta de alunos trimestral) — operação interna,
  não conteúdo institucional público.
- Seção "09 · Governança de marca" (filtros de aprovação, hierarquia de
  fontes oficiais) — processo interno de decisão.
- Seção "11 · Plano de adoção" (matriz de responsabilidades, plano de
  90 dias) — planejamento operacional interno.
- Razão social completa (VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA) —
  reservada para footer/legal/schema institucional quando fizer
  sentido (missão F.2 seção 24); não usada em headline nenhuma desta
  página.

## UNVERIFIED / DO NOT PUBLISH

Não confirmado por nenhuma fonte (nem o documento oficial, nem HTTP, nem
código do backend) — nada disso foi publicado:

- Ano de fundação, fundadores, história/origem da empresa — ausentes do
  documento oficial; sem timeline na página (missão F.2 seção 20).
- Número de alunos, professores, países atendidos — nenhuma fonte
  confirma um número; nenhum número publicado.
- Prêmios, certificações institucionais, rankings — não mencionados em
  nenhuma fonte.
- `foundingDate`, `founder`, `award`, `numberOfEmployees` no JSON-LD —
  omitidos do schema por não terem fonte (missão F.2 seção 25).
- Fotos reais de equipe/professores/operação Vedium — não fornecidas
  nesta sessão; a página usa mídia licenciada de forma genérica/
  institucional (interação, estudo, presença humana), sem apresentar
  ninguém como "nossa equipe" ou "nossos professores" (missão F.2
  seção 21).
- Página ou CTA "Conheça nossos professores" — removida por instrução
  explícita do usuário durante esta fase; a Vedium não terá catálogo
  de professores como página institucional.
