# 27 — Matriz de links da Home V2 (Fase C, seção 32 da missão)

> Todo link presente em `/_home_v2` (via `home_body.html`, `header.html`, `footer.html`), com origem da URL e status HTTP validado nesta fase (2026-08-26, ambiente de dev local, `Host: vedium.local`). Nenhuma URL inventada — toda URL vem de: (a) rota já confirmada real em `02-route-and-seo-map.md`/`baseline/ui-contracts.md`, ou (b) arquivo `www/<slug>.html` confirmado existente nesta fase.

## Header (utility bar + nav + mega menu)

| Texto | Destino | HTTP | Origem da URL |
|---|---|---|---|
| Área do aluno | `https://app.vediums.com/login` | — (externo, LMS) | `ui-contracts.md` (contrato de Login) |
| WhatsApp (utility) | `https://wa.me/5511911293075?text=...` | — (externo) | `ui-contracts.md` |
| Seletor de idioma → Português | `/` | 200 | `v2_nav_urls` default (Home real) |
| Seletor de idioma → English | `/en/?locale=en` | 200 | idem (family=en, querystring de preferência regional) |
| Seletor de idioma → Español | `/es/?locale=es` | 200 | idem |
| Seletor de idioma → Français | `/fr/?locale=fr` | 200 | idem |
| Seletor de idioma → Deutsch | `/de/` | 200 | idem |
| Seletor de idioma → Русский | `/ru/` | 200 | idem |
| Cursos ▾ → Inglês | `/curso-de-ingles-online` | 200 | mega menu já existente (B.3+) |
| Cursos ▾ → Iorubá | `/curso-de-ioruba-online` | 200 | idem |
| Cursos ▾ → Português para Estrangeiros | `/portugues-para-estrangeiros` | 200 | idem |
| Cursos ▾ → Espanhol | `/curso-de-espanhol-online` | 200 | idem |
| Cursos ▾ → Hebraico | `/curso-de-hebraico-online` | 200 | idem |
| Cursos ▾ → Professores | `/professores` | 301 → `/sobre` | route map (`02-route-and-seo-map.md`), redirect já existente, preservado |
| Cursos ▾ → Para empresas | `/empresas` | 200 | route map |
| Cursos ▾ → Fazer teste de nível | `/teste-de-nivel` | 200 | `v2_level_test_url` (contrato dinâmico, sem override nesta página) |
| Como funciona | `/como-funciona` | 200 | route map |
| Para empresas | `/empresas` | 200 | route map |
| Conteúdo | `/blog` | 200 (produção) / 403 neste dev local | ver nota no doc 26, seção 4 (doctype não migrada localmente) |
| Sobre | `/sobre` | 200 | route map |
| CTA principal (header) | `/catalogo` | 301 → `/cursos-de-idiomas-online` | `v2_hdr_primary_cta_override` (mesmo usado no Presentation Mode) |

## Corpo (home_body.html)

| Seção | Texto | Destino | HTTP | Origem |
|---|---|---|---|---|
| Hero slide 1 | Conheça os cursos | `/catalogo` | 301 → `/cursos-de-idiomas-online` | redirect canônico já usado no resto do site |
| Hero slide 2 | Conheça inglês | `/curso-de-ingles-online` | 200 | pilar real |
| Hero slide 3 | Discover Portuguese | `/portugues-para-estrangeiros` | 200 | pilar real |
| Hero slide 4 | Para empresas | `/empresas` | 200 | pilar real |
| Pathfinder | Encontrar meu caminho (sem JS) | `/teste-de-nivel` | 200 | fallback seguro (form GET nativo) |
| Pathfinder | Encontrar meu caminho (com JS, 25 combinações) | ver `26-home-v2-integration.md` seção 5 e `v2_home_data.PATHFINDER_MATRIX` | 200/301 (todas validadas) | matriz documentada, nenhuma inventada |
| Índice de cursos | Inglês/Iorubá/PLE/Espanhol/Hebraico | mesmas 5 URLs de pilar acima | 200 | idem |
| Course feature × 5 | Conheça o curso / Explore o programa / Conheça as trilhas | mesmas 5 URLs de pilar | 200 | idem |
| Live Class | Conheça como funcionam as aulas | `/como-funciona` | 200 | route map |
| B2B | Conheça as soluções corporativas | `/empresas` | 200 | route map — **nunca** aponta pro preview técnico `/design_system_v2_b2b` |
| B2B | Solicite uma conversa diagnóstica | `/contato` | 200 | route map (não existe formulário dedicado de "conversa diagnóstica" ainda) |
| Conhecimento Vedium | Leia o artigo (featured) | URL real do post mais recente (dinâmico) | 200 (produção); 301 neste dev local em alguns slugs (ver nota) | `v2_home_data.get_insights_selection()` |
| Conhecimento Vedium | Ver todos os conteúdos | `/blog` | 200 (produção) / 403 neste dev local | idem seção "Conteúdo" acima |

## CTA final e Footer

| Texto | Destino | HTTP | Origem |
|---|---|---|---|
| Conheça os cursos (CTA final) | `/catalogo` | 301 → `/cursos-de-idiomas-online` | mesmo padrão do header |
| Faça o teste de nível (CTA final) | `/teste-de-nivel` | 200 | route map |
| Footer: Inglês/Iorubá/PLE/Espanhol/Hebraico | 5 pilares reais | 200 | idem acima |
| Footer: Sobre / Professores / Como funciona / Blog / Para empresas | `/sobre`, `/professores`(301→/sobre), `/como-funciona`, `/blog`, `/empresas` | 200/301 | route map |
| Footer: FAQ / Contato / Descubra seu nível | `/faq`, `/contato`, `/teste-de-nivel` | 200 | route map |
| Footer: Privacidade / Termos / Cancelamento-reembolso | `/privacidade`, `/termos`, `/cancelamento-reembolso` | 200 | route map (hardcoded PT-only, decisão já registrada) |
| Footer: Instagram / LinkedIn / WhatsApp | URLs externas reais | — | `ui-contracts.md` |
| Footer SEO ("Vedium online para você" etc., 18 links) | ver `templates/includes/v2/footer.html` | todos 200 (validados na fase de ajuste pontual anterior) | replicados de `site_footer.html`, sem inventar |

## Notas

- Nenhum link aponta para `/design_system_v2` ou `/design_system_v2_b2b` (rotas de preview técnico) a partir da Home V2 real — só o banner de dev-tool (fora de `.v2-scope`) tem esse link, e ele mesmo se identifica como ferramenta interna.
- `/catalogo` e `/professores` são redirects **301 já existentes e documentados** em `02-route-and-seo-map.md` — preservados intencionalmente (mission: "Não mudar rotas indexadas").
- `/blog` (403 neste ambiente) é a única URL desta matriz sem confirmação de 200 neste ambiente específico — causa raiz documentada em `26-home-v2-integration.md`, não é uma URL inventada nem quebrada em produção (confirmada 200 em `content-contracts.md`/`analytics-contracts.md`).
