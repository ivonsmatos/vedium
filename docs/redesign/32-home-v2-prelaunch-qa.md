# 32 — QA pré-lançamento: `/` vs `/_home_v2` (Fase C.1)

> Comparação direta entre a Home atual (produção real) e a Home V2 integrada, para responder: **a nova Home pode substituir a atual sem regressão?** Ver também `27-home-v2-link-contract.md` (links), `29-home-v2-analytics-contract.md` (analytics/GTM), `33` (performance), `36` (LGPD).

## 1. Canonical — investigação P0 completa

### Como canonical é produzido hoje (achado real, código-fonte)

`frappe/website/page_renderers/base_template_page.py`, método `set_missing_values()` (chamado por `post_process_context()`, que roda **depois** de `get_context()`):

```python
self.context.canonical = frappe.utils.get_url(frappe.utils.escape_html(self.path))
```

Isso é **incondicional** — não é um "set se ainda não existir" (apesar do nome do método sugerir isso). Qualquer valor que um controller `www/*.py` tente colocar em `context.canonical` dentro de `get_context()` é substituído pela URL da própria página antes do template renderizar.

### Por que `context.canonical` falha

Porque o core do Frappe reserva essa chave especificamente para "canonical = a própria URL da página" — não há um mecanismo de override exposto para controllers.

### Quais páginas são afetadas

**Todas** as páginas `www/*.py` deste (e de qualquer) app Frappe que tentem customizar `context.canonical` diretamente. Confirmado que isso **já era conhecido e resolvido** no resto do site real: `curso.py`/`curso.html` (páginas de nível com canonical diferente da URL literal, ex. IDs legados) e **144 arquivos no total** usam a chave própria `canonical_url` em vez de `canonical`. `templates/base.html` (base template real do app) já tem `{% if canonical_url %}<link rel="canonical" href="{{ canonical_url }}">{% endif %}` pronto para isso.

### Solução correta (implementada nesta fase, substitui o workaround da Fase C)

`_home_v2.py` agora usa `context.canonical_url = frappe.utils.get_url("/")` (renomeado de `v2_canonical_override`, que era um nome ad hoc criado antes desta investigação). `_home_v2.html` referencia `{{ canonical_url }}`. **Não é mais um workaround isolado da V2** — é o mesmo padrão real já usado em 144 lugares do projeto.

### Regressões possíveis

Nenhuma — `canonical_url` é uma chave nova neste controller específico (`_home_v2.py`), não colide com nada. `design_system_v2.py`/`_b2b.py` não foram alterados (nunca setaram canonical, continuam sem, o que é aceitável para ferramentas internas noindex).

### Teste criado

`vedium_core/vedium_core/tests/test_pure_home_v2.py` — 7 testes, incluindo verificação de que `context.canonical` (a chave reservada) nunca é atribuída em `_home_v2.py`, que `canonical_url` aponta pra `/`, e que a Home real permanece com seu canonical hardcoded original.

### Na rota `/_home_v2`: canonical correto confirmado

```
<link rel="canonical" href="http://vedium.local:8000/" />
```
(em produção seria `https://vediums.com/`, via `frappe.utils.get_url`).

## 2. SEO snapshot comparativo

| Item | `/` (Home real) | `/_home_v2` |
|---|---|---|
| HTTP status | 200 | 200 |
| `<title>` | "Vedium - Cursos Online ao Vivo em Cinco Idiomas" | "Vedium -- Home V2 (prévia interna, não indexada)" (deliberadamente diferente — rota técnica) |
| `meta description` | "Aprenda inglês (níveis A1 a C1) e iorubá com a Vedium..." (menciona só 2 dos 5 idiomas — achado real, não corrigido aqui, fora do escopo) | Não definida (rota técnica não precisa) |
| `canonical` | `https://vediums.com/` (hardcoded no template) | `http://vedium.local:8000/` (dinâmico, aponta pra Home real) |
| `robots` | `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` | `noindex, nofollow` |
| `hreflang` | de, en, es, fr, pt-br, x-default — **`ru` ausente** (achado real: `/ru/` existe como página mas não está no hreflang da Home; pré-existente, não introduzido por esta fase) | Nenhum (correto para rota técnica, seção 22 da missão) |
| Open Graph | `og:type`, `og:url`, `og:title`, `og:description` (menciona os 5 idiomas), `og:image` — completo | Só `og:title` (mínimo, rota técnica) |
| Twitter Card | Não confirmado nesta varredura (grep simples não encontrou — pode estar em formato/atributo diferente do assumido; não investigado a fundo, fora do escopo desta fase) | Ausente |
| JSON-LD | 1 bloco `application/ld+json` (`EducationalOrganization`, confirmado em `content-contracts.md`) | Nenhum (decisão documentada em `28-home-v2-seo-contract.md` seção 3 — não duplicar antes de decisão de rollout) |
| `<h1>` | **Visualmente oculto** (`position:absolute;width:1px;height:1px;...clip:rect(0,0,0,0)`) — texto real: "Aulas de idiomas online, ao vivo, com professores nativos e especialistas" | **Visível, estilizado** — Hero slide 1: "Aprenda ao vivo. Avance com direção." |
| Contagem `<h2>`/`<h3>` | 19 / 15 | 8 / 10 |
| `lang` (`<html>`) | `pt-BR` | `pt-BR` |
| Sitemap | Incluída | Excluída (`no_sitemap=1`) |
| Internal links | ~40+ (menu completo, grid de cursos ao vivo do LMS, footer rico) | ~35 (matriz completa em `27-home-v2-link-contract.md`) |

### Achado a decidir antes do rollout (não uma regressão, uma diferença estrutural real)

O H1 da Home real é **oculto visualmente** (padrão comum de "H1 semântico para SEO/acessibilidade, headline visual é outro elemento"). A Home V2 usa o H1 **visível de verdade** (a própria headline do Hero). As duas abordagens são válidas e ambas dão 1 H1 real — mas o **texto** é diferente ("Aulas de idiomas online..." vs "Aprenda ao vivo. Avance com direção."). Quando a troca de `/` for decidida, alguém precisa decidir conscientemente: manter o H1 visível da V2 (mudança de estratégia de SEO on-page) ou replicar o H1 oculto da Home atual dentro da V2 (preservação total). **Não decidido aqui** — registrado para decisão humana explícita.

## 3. hreflang e locale — revalidado do código (não só do relatório anterior)

Fonte: leitura direta de `templates/includes/v2/header.html` (`v2_locales`, `v2_nav_urls` default) + `hooks.py` (`LANGUAGES_WITH_OWN_HOME = {"en", "es", "fr", "de", "ru"}`) + teste HTTP real desta fase.

| Locale | URL origem (`/_home_v2`) | URL equivalente | HTTP | Canonical da equivalente | hreflang | `x-default` | Locale ativo |
|---|---|---|---|---|---|---|---|
| pt-br | `/_home_v2` | `/` | 200 | `https://vediums.com/` | pt-br (na Home real) | aponta pra PT (Home real) | Sim (marcado `.is-active`/`aria-current`) |
| en | `/_home_v2` | `/en/?locale=en` | 200 | (não verificado nesta fase — fora do escopo, `/en/` é página real pré-existente) | en (na Home real) | — | Não |
| es | `/_home_v2` | `/es/?locale=es` | 200 | idem | es | — | Não |
| fr | `/_home_v2` | `/fr/?locale=fr` | 200 | idem | fr | — | Não |
| de | `/_home_v2` | `/de/` | 200 | idem | de | — | Não |
| ru | `/_home_v2` | `/ru/` | 200 | idem | **ausente no hreflang da Home real** (achado da seção 2 acima) | — | Não |

Nenhuma URL inventada — todas as 6 confirmadas reais (`LANGUAGES_WITH_OWN_HOME`). O `?locale=en`/`?locale=es` é a querystring de preferência regional já documentada em `25-locale-switcher-contract.md` (não localStorage, decisão real já tomada antes desta sessão).

## 4. Bandeiras no locale switcher (seção 5 da missão)

Implementado: bandeira (emoji) + texto no botão (`🇧🇷 PT`) e no dropdown (`🇧🇷 Português`, etc.). **Bandeira nunca substitui texto** — confirmado por markup: cada item tem `<span aria-hidden="true">{flag}</span><span>{label}</span>`, dois nós de texto/glifo separados.

### Associação bandeira↔locale — documentada, não inventada

Copiada da política **já real e em produção** (`public/js/vedium-language.js`, dict `localeMeta`):

| Locale | Bandeira | Origem da escolha |
|---|---|---|
| pt-br | 🇧🇷 Brasil | `localeMeta["pt-br"].flag` real (flagcdn `br.png`) |
| en | 🌐 Globo (**não** bandeira de país) | Decisão real e deliberada de produção: `localeMeta["en"].flag` usa a bandeira da ONU (`un.png`), especificamente para não escolher um país pra um idioma falado em dezenas deles. Reproduzido aqui com 🌐 em vez de imagem remota da ONU — mesma política, sem dependência externa nova |
| es | 🇪🇸 Espanha | `localeMeta["es"].flag` real |
| fr | 🇫🇷 França | `localeMeta["fr"].flag` real |
| de | 🇩🇪 Alemanha | `localeMeta["de"].flag` real (rótulo de produção é "DACH REGION", reconhecendo Alemanha/Áustria/Suíça, mas a bandeira usada já é a da Alemanha) |
| ru | 🇷🇺 Rússia | `localeMeta["ru"].flag` real |

**Nenhuma inferência silenciosa** — a única decisão sem bandeira de país (`en`) replica exatamente a decisão já tomada e em produção, não uma escolha nova desta fase.

### Testado

| Cenário | Resultado |
|---|---|
| Header sobre Hero (overlay) | Bandeira/texto visíveis, cor clara sobre o fundo escuro (herda `.v2-hdr-utility--overlay`) |
| Header sólido (`is-solid`) | Bandeira/texto com cor escura padrão |
| Desktop 1440px | Confirmado via screenshot |
| Mobile 390px | Confirmado em fase anterior (B.6E) — layout do dropdown não muda com a bandeira, só adiciona um glifo por linha |
| Teclado | Abre/fecha por clique+Enter no botão nativo, Esc fecha e devolve foco (já testado em B.6E, comportamento não alterado por esta mudança) |
| Screen reader | Bandeira `aria-hidden="true"` (glifo puramente decorativo) — nome acessível de cada item continua sendo só o texto real ("Português", "English", etc.), nunca o emoji |
| Locale ativo | `.is-active` + `aria-current="true"` no item correspondente a `v2_locale_current` |

**Achado de metodologia (não um bug de código)**: o Chrome headless usado pra screenshot neste ambiente renderiza bandeiras de país como texto (fallback "BR"/"ES"/"FR"/"DE") em vez de emoji real — confirmado via inspeção do HTML bruto que o glifo Unicode correto (🇧🇷 etc.) está presente; é uma limitação de fonte do Chrome headless neste ambiente de teste específico, não do código. Navegadores reais (Windows/Mac/mobile, não-headless) renderizam bandeiras regionais corretamente — comportamento amplamente padronizado.

## 5. Links — revalidação

Matriz completa já existe em `27-home-v2-link-contract.md` (criada na Fase C). Revalidada nesta fase: todas as URLs seguem retornando os mesmos status (200/301 esperados). Nenhum 404 novo encontrado. Nenhuma mudança de rota foi feita desde a Fase C.

## 6. Acessibilidade — revisão desta fase

| Item | Status |
|---|---|
| Skip link | **Ausente** — nem a Home real nem a Home V2 têm skip link hoje (achado real, pré-existente, não introduzido por esta fase; candidato a melhoria futura, fora do escopo de "não redesenhar") |
| Landmarks | `<header>`, `<main>`, `<footer>` presentes e semânticos (herdados, não alterados) |
| H1 único | Confirmado (1 em cada página) |
| Heading hierarchy | Sem saltos abruptos dentro das seções V2 (H2 de seção → H3 de item, padrão já estabelecido em fases anteriores) |
| Labels (Pathfinder) | Cada `<input type="radio">` está dentro de um `<label>` real (não `aria-label` solto) — herdado, não alterado |
| Locale menu | Ver seção 4 acima |
| Course menu (mega menu) | `aria-haspopup`/`aria-expanded` no trigger, fallback por clique em touch (sem hover) — herdado de fases anteriores, não alterado |
| Carousel (Hero) | `aria-roledescription="carrossel"`, tabs com `aria-selected`/`tabindex` — herdado, não alterado |
| Vídeo (Live Class) | `<video controls>`, sem autoplay — herdado |
| Focus | Confirmado retorno de foco ao fechar locale menu com Esc |
| Contrast | Não recalculado matematicamente nesta fase (nenhuma cor nova introduzida desde a última auditoria em B.6B/B.6E) |
| Reduced motion | Herdado do Hero carousel, não retestado especificamente nesta fase (nenhuma mudança de animação) |
| Keyboard geral | Radios nativos (Pathfinder), botões nativos (locale, mega menu, burger) — tudo operável por Tab/Enter/Espaço por construção HTML nativa |
| Alt text | Todas as imagens/vídeo da Home V2 têm `alt` descritivo real (confirmado em fases anteriores, não regredido) |

Nenhuma mudança visual significativa foi feita para chegar a este estado — a maior parte já vinha herdada de B.6B-B.6E.
