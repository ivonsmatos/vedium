# 13 — Catálogo de Produtos & Preços

**Verificado em produção:** 2026-07-10. Fonte única de verdade do que a
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

## Hebraico — 5 ofertas

| Slug | Oferta | Preço |
|---|---|---|
| `hebraico-a0-alfabetizacao` | Hebraico A0 — Alfabetização | R$ 197 |
| `hebraico-moderno-a1` | Hebraico Moderno — Nível A1 | R$ 397 |
| `hebraico-moderno-a2-b1` | Hebraico Moderno — Nível A2/B1 | R$ 447 |
| `hebraico-biblico-leitura-guiada` | Hebraico Bíblico — Leitura Guiada | R$ 497 |
| `hebraico-particular` | Hebraico Particular 1:1 | R$ 140-220/hora, consultivo |

`hebraico-particular` **não deve ir para checkout Stripe de valor fixo**:
o CTA público abre conversa com a equipe para definir pacote, horário e
valor final.

## Regras de preço observadas

- Preço é **por curso/nível**, não varia dentro do mesmo idioma+nível —
  hoje não há desconto por pacote de níveis nativo (cupom cobre isso,
  ver [doc 02](02-dicionario-doctypes.md) pro doctype `Coupon`).
- Certificado/avaliação **já incluso** no preço — não é cobrado à parte
  (ver [doc 05](05-fluxo-jornada-do-aluno.md), é exatamente essa premissa
  que motivou o fix de `purchased_certificate` nesta sessão).
- Catálogo publicado atual: 17 cursos/ofertas (6 Inglês, 3 Iorubá, 3 PLE,
  5 Hebraico). Cursos com cobrança mensal/por nível usam checkout; oferta
  consultiva 1:1 usa conversa comercial antes da cobrança.

## O que NÃO está no catálogo hoje

- A primeira turma em grupo PLE já existe como infraestrutura/piloto:
  `PLE Básico - Turma Agosto/2026`, ainda rascunho/privada. Não é venda
  pública aberta enquanto `published=0` e `allow_self_enrollment=0`.
- Nenhum outro idioma além de Inglês/Iorubá/PLE/Hebraico tem curso
  publicado (mesmo havendo cluster de marketing/SEO para outros idiomas em
  desenvolvimento).
