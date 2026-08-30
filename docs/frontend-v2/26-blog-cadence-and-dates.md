# 26 — Cadência Editorial e Preservação de Datas (CORREÇÃO OBRIGATÓRIA)

Este documento registra e aplica a correção enviada pelo usuário em
2026-08-30, que **substitui** qualquer afirmação anterior sobre cadência
ou início do histórico editorial do Blog. Vale como regra operacional
atual — qualquer outro documento desta fase que mencione "44 artigos, 2
por semana" ou trate 2026 como início do Blog está descrevendo o
diagnóstico da planilha SEO/GEO v3, não a regra final.

## BLOG CADENCE

**3 artigos por semana.** Não 2 (o que a própria planilha SEO/GEO v3
calculou como meta, ver `Diagnostico`, achado #5: "Cadência real medida:
1,16 artigo/semana... Novo plano em 2 artigos por semana"). O usuário
corrigiu essa meta para 3/semana como regra operacional atual — mais
alta do que a própria SEO/GEO v3 recomendava. Nenhuma planilha foi
alterada; a correção fica só documentada aqui e deve orientar qualquer
planejamento editorial futuro.

## EDITORIAL HISTORY

**Começa em 2025**, não em 2026. Confirmado por evidência primária, não
só pela instrução do usuário: a aba `Publicados_Auditoria` da SEO/GEO v3
tem 94 artigos com datas reais (convertidas de serial Excel) entre
**2025-01-01 e 2026-07-13** — 63 em 2025, 31 em 2026 (números do próprio
`Diagnostico` da planilha, achado "Resumo quantitativo"). `blog_content.py`
confirma o mesmo intervalo: o artigo mais antigo com data explícita
("Portuguese for work meetings in Brazil: first phrases to master") tem
`date: "2025-03-04"`.

## PUBLISHED DATES: imutáveis durante a migração técnica

Regra aplicada literalmente nesta fase:

- `AULA_DE_INGLES_ONLINE_AO_VIVO.publishedAt` (o único artigo migrado)
  = `"2026-07-13"`, copiado direto do campo `date` de
  `blog_content.py`, sem nenhum `new Date()`, sem data de commit, sem
  data de execução do script.
- `scripts/migrate-blog.mjs` nunca escreve uma data nova: ele só LÊ
  `date` de `blog_content.py` e, quando encontra uma correspondência em
  `Publicados_Auditoria`, COMPARA as duas. Se divergem, marca
  `date_conflict = "REVIEW REQUIRED"` na linha do CSV e **não decide
  qual das duas está certa** (comportamento testado: rodar o script de
  novo produz exatamente o mesmo CSV, prova de que não há aleatoriedade
  nem sobrescrita silenciosa).
- Nenhum artigo teve a data alterada por esta migração. O único artigo
  migrado (prova de conceito) foi escolhido justamente por ter a MESMA
  data nas duas fontes (`blog_content.py` = `Publicados_Auditoria` =
  2026-07-13), eliminando qualquer ambiguidade no exemplo entregue.

## DATE_CONFLICT encontrados nesta auditoria

Rodando `node scripts/migrate-blog.mjs` sobre os 97 artigos do dict
contra os 94 da auditoria: **0 conflitos de data** entre os 77 artigos
que casaram por título. Isso não significa que os outros 20 (97-77)
estão livres de conflito — significa que não foram cruzados (título não
bateu exatamente, incluindo os que o próprio dict corrompe via
concatenação de string Python de várias linhas — ver limitação abaixo).
Antes de migrar qualquer um desses 20 em uma fase futura, cruzar
manualmente contra a auditoria original ou re-extrair o título completo.

**Limitação conhecida do script**: a extração de título via regex não
resolve literais Python concatenados em múltiplas linhas (ex.:
`'texto ' 'continuação'`), o que trunca alguns títulos longos no CSV
(ex.: linha do artigo "How to learn Portuguese for Brazil when you
already speak another Romance..." fica cortada em "...Romance "). Isso
é um problema de EXTRAÇÃO, não de dado: o `publishedAt` desses artigos
ainda foi lido corretamente (é um campo separado, não afetado pelo
título truncado). Registrado aqui em vez de consertado silenciosamente,
seguindo a mesma regra de não esconder limitação.

## UNKNOWN PUBLICATION DATES

**0.** Todos os 97 artigos do dict têm um campo `date` preenchido
(`missingDates: 0` no output do script). Nenhuma data foi inventada para
preencher lacuna.

## 2025 CONTENT PRESERVED / 2026 CONTENT PRESERVED

Ambos preservados: `27-blog-url-migration-map.csv` lista os 97 artigos
com a data original de cada um (`published_at_original`), sem filtrar
ou esconder os de 2025. O artigo migrado como prova de conceito é de
2026 (2026-07-13) só porque foi o escolhido por segurança cultural/de
conflito (missão F.3 seção 49: preferir Inglês, ação MANTER) — isso não
representa "o Blog começou em 2026"; é só a amostra desta fase.

## MIGRATION DATE OVERRIDES

**0.** Nenhum artigo recebeu uma data diferente da que já tinha na
fonte, nesta fase.

## Gate desta correção

| Item | Resultado |
|---|---|
| PUBLISHED DATE PARITY | PASS -- publishedAt do artigo migrado = data real de produção, confirmada em 2 fontes independentes |
| 2025 CONTENT PRESERVED | PASS -- inventário completo (CSV) preserva as datas de 2025 dos 63 artigos daquele ano |
| 2026 CONTENT PRESERVED | PASS |
| MIGRATION DATE OVERRIDES | 0 |
| UNKNOWN PUBLICATION DATES | 0 |
| DATE CONFLICTS | 0 (entre os cruzados; 20 artigos não cruzados ficam como pendência explícita, não como conflito resolvido) |
| CADENCE CONTRACT | 3 artigos/semana (substitui os "2 por semana" calculados pela SEO/GEO v3) |
