# 13 — Catálogo de Produtos & Preços

**Verificado em produção:** 2026-07-03. Fonte única de verdade do que a
Vedium vende hoje — se este doc divergir do site, o site é que está
desatualizado (preço vem sempre ao vivo do banco em `curso.py`, nunca
hardcoded na página).

## Inglês — 6 níveis, professor Kayode, R$ 240/mês (todos os níveis)

| Slug (`LMS Course.name`) | Nível |
|---|---|
| `ingl-s-beginner` | Beginner |
| `ingl-s-elementary` | Elementary |
| `ingl-s-pr-intermedi-rio` | Pré-Intermediário |
| `ingl-s-intermedi-rio` | Intermediário |
| `ingl-s-upper-intermedi-rio` | Upper Intermediário |
| `ingl-s-avan-ado` | Avançado |

## Iorubá — 3 níveis, professora Busayo, R$ 320/mês (todos os níveis)

| Slug | Nível |
|---|---|
| `iorub-b-sico` | Básico |
| `iorub-intermedi-rio` | Intermediário |
| `iorub-avan-ado` | Avançado |

## Português para Estrangeiros (PLE) — 3 níveis, professor Almir, US$ 120/mês (todos os níveis)

| Slug | Nível |
|---|---|
| `portugues-para-estrangeiros-basico` | Básico |
| `portugues-para-estrangeiros-intermediario` | Intermediário |
| `portugues-para-estrangeiros-avancado` | Avançado |

**⚠️ Único cluster com preço em USD** (não BRL) — moeda escolhida pro
público internacional/diáspora que não fala português. Não confundir com
os outros dois clusters ao fazer conta de receita consolidada.

## Regras de preço observadas

- Preço é **por curso/nível**, não varia dentro do mesmo idioma+nível —
  hoje não há desconto por pacote de níveis nativo (cupom cobre isso,
  ver [doc 02](02-dicionario-doctypes.md) pro doctype `Coupon`).
- Certificado/avaliação **já incluso** no preço — não é cobrado à parte
  (ver [doc 05](05-fluxo-jornada-do-aluno.md), é exatamente essa premissa
  que motivou o fix de `purchased_certificate` nesta sessão).
- 12 cursos publicados no total, todos com `evaluator` + `enable_certification`
  + `paid_certificate` ligados — agendamento de aula disponível em 100%
  do catálogo ativo.

## O que NÃO está no catálogo hoje

- Nenhuma turma em grupo (`LMS Batch`) — só aula 1-a-1 disponível pra
  compra atualmente. Ver [doc 06](06-fluxo-jornada-do-professor.md#4-aula-em-grupo-turma--nativo-configurado-nesta-sessão)
  pro que falta pra abrir uma.
- Nenhum outro idioma além de Inglês/Iorubá/PLE tem curso publicado
  (mesmo havendo cluster de marketing/SEO pra outros idiomas em
  desenvolvimento — ver [[project_i18n_n_language_rollout]]).
