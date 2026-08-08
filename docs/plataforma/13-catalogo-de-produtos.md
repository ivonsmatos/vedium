# 13 — Matriz Comercial Oficial (Catálogo de Produtos)

**Fonte única de verdade** do que a Vedium vende. Se site, LMS ou Stripe
divergirem daqui, **eles** é que estão errados. Preço vem sempre ao vivo do
banco (`curso.py` / catálogo Stripe), nunca hardcoded na página.

**Dados do sistema verificados em produção:** 2026-08-08.

## Legenda de confiança de cada campo

- ✅ **Firme** — dado vivo no Frappe/Stripe (preço, nível, frequência, plano,
  professor). Não inventar; extrair.
- 🟡 **Proposto (a validar)** — sugestão pedagógica minha (padrão CEFR). Precisa
  de aval da coordenação antes de virar promessa pública.
- 🔴 **Lacuna / inconsistência** — falta definir ou as camadas divergem.

## Modelo comercial (decidido 2026-08-08)

- **Modalidade:** assinatura recorrente **individual flexível** — o aluno
  escolhe de **1 a 5 aulas/semana**. (Turmas fixas em grupo existem só como
  piloto PLE em rascunho — não é venda pública ainda.)
- **Plano:** mensal ou anual (anual ~-22%/mês; permanência mínima registrada).
- **Frequência:** 1x a 5x/semana. O catálogo Stripe tem **190 preços** (19
  cursos × 5 frequências × 2 planos) — ver [[project_catalog_price_rollout]].
- **Duração da aula:** 🟡 60 min (a validar/confirmar como padrão oficial).
- **Avaliação:** 🟡 diagnóstico na entrada + atividades ao longo + avaliação
  final para certificar (a validar o formato exato por idioma).
- **Certificado:** incluído no preço (não cobrado à parte). ⚠️ Ver
  [inconsistências](#inconsistências-a-resolver) — a *feature* está desligada
  hoje no LMS.
- **CTA:** `Matrícula` (checkout Stripe, funcionando) + `Aula experimental /
  diagnóstica` (páginas `aula-diagnostica.html` existem no site).

O **preço de destaque** abaixo é o **mensal a 1x/semana** (piso). Frequências
maiores custam mais, com desconto por frequência — grade completa no Stripe.

---

## Inglês — 6 níveis · Prof. Kayode · R$ 240/mês (flat)

| Nível | Slug (`LMS Course.name`) | CEFR | Preço/mês 1x | Objetivo 🟡 | Carga aula ao vivo 🟡 |
|---|---|---|---|---|---|
| Beginner | `ingl-s-beginner` | A1 | R$ 240 | Comunicação básica do dia a dia; chegar ao A1 | ~48–64h |
| Elementary | `ingl-s-elementary` | A2 | R$ 240 | Situações rotineiras; chegar ao A2 | ~48–64h |
| Pré-Intermediário | `ingl-s-pr-intermedi-rio` | A2→B1 | R$ 240 | Transição p/ autonomia; entrar no B1 | ~48–64h |
| Intermediário | `ingl-s-intermedi-rio` | B1 | R$ 240 | Lidar com viagem/trabalho; consolidar B1 | ~48–64h |
| Upper-Intermediário | `ingl-s-upper-intermedi-rio` | B2 | R$ 240 | Fluência e espontaneidade; chegar ao B2 | ~48–64h |
| Avançado | `ingl-s-avan-ado` | C1 | R$ 240 | Uso flexível/eficaz; chegar ao C1 | ~48–64h |

**Público 🟡:** do zero absoluto (Beginner) ao profissional que quer refinar (Avançado).
**Professor ✅:** Kayode (`kayode@vediums.com`) — instrutor **e** evaluator.

## Iorubá — 3 níveis · Profa. Busayo · R$ 320/mês (flat)

| Nível | Slug | Faixa | Preço/mês 1x | Objetivo 🟡 | Carga 🟡 |
|---|---|---|---|---|---|
| Básico | `iorub-b-sico` | Iniciante | R$ 320 | Alfabeto, saudações, frases essenciais | ~48–64h |
| Intermediário | `iorub-intermedi-rio` | Intermediário | R$ 320 | Conversação cotidiana, tempos verbais | ~48–64h |
| Avançado | `iorub-avan-ado` | Avançado | R$ 320 | Fluência cultural, textos e nuance | ~48–64h |

**Público 🟡:** diáspora e interessados em cultura iorubá/religiões de matriz africana.
**Professor ✅:** Busayo (`busayo@vediums.com`) — instrutor **e** evaluator.
*(Iorubá não segue CEFR — níveis funcionais.)*

## Português para Estrangeiros (PLE) — 3 níveis · Prof. Almir · USD

| Nível | Slug | CEFR | Preço/mês 1x | Objetivo 🟡 | Carga 🟡 |
|---|---|---|---|---|---|
| Básico | `portugues-para-estrangeiros-basico` | A1→A2 | **US$ 90** | Sobreviver no Brasil no dia a dia | ~48–64h |
| Intermediário | `portugues-para-estrangeiros-intermediario` | B1→B2 | US$ 120 | Autonomia social e profissional | ~48–64h |
| Avançado | `portugues-para-estrangeiros-avancado` | B2→C1 | US$ 120 | Fluência acadêmica/profissional | ~48–64h |

**⚠️ Único cluster em USD** (público internacional/diáspora). Básico é mais barato (US$ 90).
**Professor ✅:** Almir (`almirseller@yahoo.com`) — instrutor **e** evaluator.

## Espanhol — 3 níveis · Profa. Lupita Samayoa · preço escala por nível

| Nível | Slug | CEFR | Preço/mês 1x | Objetivo 🟡 | Carga 🟡 |
|---|---|---|---|---|---|
| Básico | `espanhol-basico` | A1→A2 | R$ 297 | Base comunicativa; chegar ao A2 | ~48–64h |
| Intermediário | `espanhol-intermediario` | B1→B2 | R$ 397 | Autonomia; consolidar B1/B2 | ~48–64h |
| Avançado | `espanhol-avancado` | B2→C1 | R$ 497 | Fluência refinada; chegar ao C1 | ~48–64h |

**Público 🟡:** brasileiros que querem espanhol para carreira/viagem na América Latina/Espanha.
**Professor ✅:** Lupita Samayoa (`lupitasamayoa3@gmail.com`) — instrutora.
🔴 **evaluator NÃO setado** (corrigir: usar a instrutora).

## Hebraico — 5 ofertas · preço escala por nível

| Oferta | Slug | Nível | Preço/mês 1x | Objetivo 🟡 |
|---|---|---|---|---|
| A0 — Alfabetização | `hebraico-a0-alfabetizacao` | Pré-A1 | R$ 197 | Ler/escrever o alfabeto hebraico |
| Moderno A1 | `hebraico-moderno-a1` | A1 | R$ 397 | Comunicação básica em hebraico moderno |
| Moderno A2/B1 | `hebraico-moderno-a2-b1` | A2→B1 | R$ 447 | Autonomia no hebraico moderno |
| Bíblico — Leitura Guiada | `hebraico-biblico-leitura-guiada` | Nicho | R$ 497 | Ler textos bíblicos no original |
| Particular 1:1 | `hebraico-particular` | Sob medida | ⚠️ ver abaixo | Aula individual personalizada |

**Público 🟡:** estudo religioso/bíblico, aliá, herança judaica.
🔴 **Professor NÃO definido** — instrutor atual = `Administrator` (placeholder).
Sem professor real, avaliação/certificado do Hebraico **não roda**.
🔴 **`hebraico-particular`:** `course_price` = R$ 140 no LMS, mas a memória/checkout
indicam plano recorrente legado **~R$ 1.120/mês** (`custom_stripe_*`, fora do
catálogo por frequência). Preço divergente — **precisa ser reconciliado**.

---

## Inconsistências a resolver (site ↔ Frappe ↔ LMS ↔ Stripe)

Levantadas em 2026-08-08 ao extrair a matriz. São o backlog de "fazer as
camadas falarem a mesma coisa":

1. 🔴 **Certificado desligado em 100% dos cursos** (`enable_certification=0`),
   mas a oferta promete certificado. **Decisão 2026-08-08: ligar em todos.**
   Requer evaluator em cada curso (ver #2). *A codificar em `pedagogical_setup`
   p/ não regredir de novo.*
2. 🔴 **Sem evaluator:** Espanhol (→ usar Lupita) e Hebraico (→ **falta
   professor real**). Sem evaluator, o fluxo de avaliação/Google Meet não gera.
3. 🟡 **`paid_certificate` inconsistente:** =1 em Inglês/Iorubá/PLE, =0 em
   Espanhol/Hebraico. Definir o modelo único (certificado incluído via
   `purchased_certificate` auto-marcado, ou cobrado à parte).
4. 🔴 **`hebraico-particular`** com preço divergente (R$ 140 no LMS vs
   ~R$ 1.120/mês no checkout legado).
5. 🟡 **Filosofia de preço mista:** Inglês/Iorubá são flat; Espanhol/Hebraico
   escalam por nível; PLE tem básico mais barato. Não é erro — mas precisa ser
   **escolha consciente e comunicada**, não acidente histórico.

## Campos 🟡 que dependem da coordenação (não inventar)

Duração oficial da aula, carga horária por nível, formato exato da avaliação,
**material didático por curso** e critérios de contratação de professor ainda
não estão no sistema. As propostas CEFR acima são ponto de partida para validar.

## O que NÃO está no catálogo hoje

- Turma em grupo PLE (`PLE Básico - Turma Agosto/2026`) — rascunho/privada
  (`published=0`, `allow_self_enrollment=0`). Não é venda pública.
- Nenhum idioma além de Inglês/Espanhol/Iorubá/PLE/Hebraico tem curso publicado
  (mesmo havendo landings de SEO para outros idiomas).
