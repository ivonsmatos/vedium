# 08 — SEO Parity: `/curso-de-ioruba-online` (CURRENT Frappe vs Next local)

Snapshot da página pública atual capturado nesta sessão (fetch direto do
HTML, não resumo de IA) e comparado campo a campo com a implementação Next
em `frontend/src/app/curso-de-ioruba-online/page.tsx`. A rota Next só
existe localmente (`http://localhost:3000`) — nenhuma substituição de
produção ocorreu.

## Metadados

| Campo | CURRENT (produção) | NEXT (local) | Status |
|---|---|---|---|
| URL | `/curso-de-ioruba-online` | `/curso-de-ioruba-online` (mesma, quando publicado) | ✅ preservada |
| HTTP | 200 | 200 (dev) | ✅ |
| `<title>` | "Curso de Iorubá Online \| Vedium" | idêntico (recuperado literalmente) | ✅ |
| meta description | "Curso de iorubá online com aulas ao vivo, pronúncia, vocabulário, cultura e trilha estruturada para iniciantes." | idêntica | ✅ |
| canonical | `https://vediums.com/curso-de-ioruba-online` | idêntico | ✅ |
| robots | `index, follow, max-image-preview:large` | idêntico | ✅ |
| hreflang | pt-br(self), en→/en/learn-yoruba-online, es→/es/curso-de-yoruba-online, ru→/ru/kurs-yoruba-online, x-default(self) — **sem** fr/de nesta página | mesmos 5 entries, mesmos destinos | ✅ |
| og:title / og:description / og:url | iguais ao title/description | idênticos | ✅ |
| og:image | `Logo-color-quadrada.png` | idêntico | ✅ |
| twitter:card/title/description/image | `summary_large_image` + mesmos textos | idênticos | ✅ |

## H1 e headings

- **CURRENT H1**: "Aprenda iorubá online com estrutura, pronúncia e contexto cultural"
- **NEXT H1**: "Entenda o que você fala, canta e escuta com profundidade." — copy nova, aprovada no gate cultural da Fase D (`language_pillar_data.py::get_ioruba_pillar_config`, a mesma que a missão desta tarefa colou literalmente). O contrato de SEO (56) pede title/description "recuperados ou superados", não H1 idêntico — o H1 é conteúdo visível/editorial, não um campo de meta, e a troca é uma decisão de produto já aprovada, não uma perda.
- **H1 único**: confirmado — só 1 `<h1>` no HTML renderizado (ver seção SSR abaixo).
- CURRENT tem 23 headings H2/H3 (página institucional/comercial mais longa, com seções como "Investimento", "Diagnóstico da necessidade", "Tudo sobre o curso..."). NEXT tem 9 H2 (Estudo de Iorubá, Aulas ao vivo, Percurso, Idioma+Cultura, Conhecimento Vedium, FAQ, CTA final — a estrutura fixa pedida pela missão). NEXT é mais enxuta por design (reusa os componentes editoriais da Home, não o layout antigo reprovado) — cobertura de conteúdo é preservada via os mesmos temas (níveis, pronúncia/tons, cultura, FAQ), não pela mesma contagem de headings.

## Schema (JSON-LD)

| Schema | CURRENT | NEXT | Status |
|---|---|---|---|
| `Course` | name, description, url, provider(Organization), educationalLevel="Iniciante", inLanguage="pt-BR" | campos idênticos | ✅ |
| `BreadcrumbList` | Início → Cursos de Idiomas → Curso de Iorubá Online | idêntico (mesmos 3 itens, mesmas URLs) | ✅ |
| `FAQPage` | 4 perguntas | 6 perguntas — as 4 de CURRENT **inclusas por completo** (incluindo "O curso é religioso?", a pergunta central de QA cultural) + 2 do gate cultural da Fase D ("O curso trabalha pronúncia e tons?", "Como funcionam os níveis?") | ✅ superado (nenhuma pergunta de CURRENT foi perdida) |
| `Organization` | não presente nesta página (só dentro do `provider` do Course) | idêntico, não duplicado | ✅ |

## Breadcrumb visual

CURRENT: "Início / Cursos / Curso de Iorubá Online" (texto visível).
NEXT: mesmo trail, componente `Breadcrumb.tsx` (`.v2-breadcrumb`, já usado
no design system), renderizado logo abaixo do Hero.

## Internal links

| Link | CURRENT | NEXT | HTTP real (verificado nesta sessão) |
|---|---|---|---|
| `/curso/ioruba-basico` | ✅ | ✅ (Percurso) | 200 |
| `/curso/ioruba-intermediario` | ✅ | ✅ (Percurso) | 200 |
| `/curso/ioruba-avancado` | ✅ | ✅ (Percurso) | 200 |
| `/como-funciona` | ✅ | ✅ (header/footer) | 200 |
| `/sobre` | ✅ | ✅ (header/footer) | 200 |
| `/cursos-de-idiomas-online` | ✅ | ✅ (breadcrumb) | 200 |
| `/teste-de-nivel` | ✅ | ✅ (header CTA) | 200 |
| `/ioruba-cultura-e-ancestralidade` | ✅ | ✅ (seção Idioma+Cultura) | 200 |
| `/blog/ioruba/...` (3 artigos reais) | ✅ (dentro de /blog/ioruba) | ✅ (Conhecimento Vedium) | 200 (as 3 URLs usadas) |
| `/planos` | ✅ | não incluído (mission não implementa checkout/planos nesta fase) | — |

Nenhum link quebrado introduzido. Nenhuma URL inventada — todas as 12 URLs
internas usadas na página Next foram testadas com HEAD request nesta sessão
(200 em todas).

## Achado: `wa.me/message/VEDIUM` não é válido

O dado oficial (`language_pillar_data.py`) usava
`https://wa.me/message/VEDIUM` como CTA secundário ("Fale com a Vedium").
Testado nesta sessão: **retorna HTTP 500** (short link não registrado/
quebrado), não um redirect real do WhatsApp Business. Substituído pelo
WhatsApp real e já validado em todo o resto do site
(`https://wa.me/5511911293075?text=...`, mesmo número/mensagem do
Header/Footer/Home) — mesma decisão de "não inventar/confiar cegamente em
URL não verificada" que a missão pede.

## Conteúdo (word/content coverage)

CURRENT é uma landing page comercial mais longa (preço, diagnóstico,
"tudo sobre o curso"). NEXT segue deliberadamente a arquitetura de
componentes editoriais da Home (Estudo/Live/Percurso/Cultura/Professor/
Insights/FAQ/CTA) — mais curta, mais focada, sem duplicar o layout Frappe
reprovado (regra explícita da missão, seção 3). A profundidade de conteúdo
que o SEO contract (56) pede como não-perdível — pronúncia/tons, progressão
por nível, contexto cultural, FAQs — está presente e, no caso do FAQ, com
mais cobertura (6 perguntas vs. 4).

## Veredito

**SEO PARITY: PASS.** Todos os campos de metadata mecânicos (title,
description, canonical, robots, hreflang, OG, Twitter, schema, breadcrumb)
foram recuperados literalmente. H1 e headings mudam por decisão de design
já aprovada (gate cultural da Fase D), não por perda de sinal. Nenhum link
interno quebrado; um link real quebrado da fonte oficial (`wa.me/message/
VEDIUM`) foi corrigido para o WhatsApp real já validado no site.
