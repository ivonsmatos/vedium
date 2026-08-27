# 28 — Contrato de SEO da Home V2 (Fase C, seções 22-24 da missão)

## 1. SEO da rota paralela `/_home_v2` (implementado, obrigatório)

| Item | Valor implementado | Mecanismo |
|---|---|---|
| `robots` (meta) | `noindex, nofollow` | `<meta name="robots" content="noindex, nofollow" />` hardcoded em `_home_v2.html` |
| Sitemap | Não incluída | `context.no_sitemap = 1` (mesmo padrão de `design_system_v2.py`) — `www/sitemap.py` não referencia esta rota |
| Canonical | Aponta pra `/` (Home real) | Ver achado real abaixo |
| hreflang | Nenhum | Nenhuma tag `hreflang` adicionada apontando pra `/_home_v2` |
| Navegação pública | Não linkada | Nenhum link real do site (header/footer/sitemap) aponta pra `/_home_v2` — só o link cruzado no banner interno de `/design_system_v2` |
| robots.txt | Não alterado | Arquivo de produção compartilhado (`www/robots.txt`/`robots.py`) — fora do escopo desta fase; a meta tag `noindex` já é suficiente e não exige tocar num arquivo compartilhado |

### Achado real: `context.canonical` é sobrescrito pelo core do Frappe

`frappe/website/page_renderers/base_template_page.py:58` faz `self.context.canonical = frappe.utils.get_url(self.path)` **incondicionalmente**, depois que `get_context()` roda — qualquer valor setado em `context.canonical` dentro do controller é substituído pela URL da própria página antes do template renderizar. Confirmado lendo o código-fonte do Frappe (não é bug do vedium_core).

**Solução**: `_home_v2.py` seta `context.v2_canonical_override` (chave própria, não reservada pelo core) = `frappe.utils.get_url("/")`; o template referencia `{{ v2_canonical_override }}` no `<link rel="canonical">`, contornando o comportamento padrão em vez de tentar vencer a corrida contra ele. Verificado no HTML renderizado: `<link rel="canonical" href="http://vedium.local:8000/" />`.

## 2. SEO da futura Home real (`/`) — CONTRATO DOCUMENTADO, NÃO IMPLEMENTADO

Por instrução explícita da missão (seção 23): preparar os valores esperados sem alterar a Home pública agora. Valores abaixo refletem o que a Home V2, quando promovida a `/` de verdade, deveria usar — cross-referenciados com o que a Home atual já tem hoje (`content-contracts.md`, `baseline-summary.md`).

| Item | Estado atual da Home real (`/`) | Estado proposto pra Home V2 quando promovida |
|---|---|---|
| `<title>` | Confirmado em produção (PT) | Manter o mesmo título real já usado — não fabricar um novo antes de decisão do time |
| `<h1>` | CONFIRMADO só em pt-BR; **`/en`,`/es`,`/fr`,`/de`,`/ru` respondem SEM `<h1>` hoje** (achado da Fase A, `content-contracts.md`) | Home V2 tem exatamente 1 `<h1>` (slide 1 do Hero) — **oportunidade de corrigir o gap das 5 variantes de idioma quando a migração de fato acontecer**, não regressão |
| `description` | Existe hoje (não relido linha a linha nesta fase) | Preservar o mesmo texto real até revisão editorial explícita |
| `canonical` | `/` (auto) | `/` (auto) — sem mudança de estrutura |
| OG (`og:title`, `og:type`, etc.) | `EducationalOrganization` + `ContactPoint` + `PostalAddress` confirmados em produção (`content-contracts.md`) | Preservar os mesmos tipos de schema — nenhum JSON-LD novo nem duplicado (ver seção 24 da missão, tratado no doc `26-home-v2-integration.md` seção "áreas congeladas") |
| Twitter Card | Não relido linha a linha nesta fase | Preservar padrão existente |
| `hreflang` | Confirmado presente na Home real (PT/en/es/fr/de) | Preservar reciprocidade real já existente — nenhuma alteração de estrutura de hreflang nesta fase |
| Breadcrumbs | Não aplicável na Home (é a raiz) | Não aplicável |
| Structured Data (`EducationalOrganization`) | Presente e confirmado em produção | **Não duplicar** — se/quando a Home V2 substituir `/`, deve reaproveitar o MESMO bloco JSON-LD já existente, não recriar um novo em paralelo |

**Regra explícita respeitada**: nenhum valor de SEO da Home pública (`/`) foi alterado nesta fase. A tabela acima é só o contrato documentado para quando (e se) a decisão de promover `/_home_v2` a `/` for tomada — decisão humana, fora do escopo desta fase.

## 3. Structured Data — auditoria (seção 24 da missão)

Não implementado JSON-LD novo em `/_home_v2` nesta fase — a rota é `noindex`, então não há benefício de SEO em publicar `Organization`/`EducationalOrganization`/`Course` ali, e fazer isso criaria risco de manutenção duplicada (dois blocos JSON-LD "quase iguais" em dois lugares diferentes do código, um deles nunca indexado). **Proposta registrada, não implementada**: quando a Home V2 for promovida a `/`, ela deve reaproveitar a MESMA função/lógica que gera o JSON-LD da Home atual (não recriar), evitando duplicidade de manutenção — este é o "risco de indexação/interferência" que a missão pede pra evitar antes de implementar (seção 24: "Implementar na rota V2 somente quando não houver risco de indexação/interferência" — hoje HÁ risco de duplicidade de manutenção sem ganho real, já que a rota nem é indexada).

## 4. Fontes (seção 28 da missão)

Poppins e Inter são as fontes oficiais, mas **não existem arquivos locais auto-hospedados no repo ainda** (confirmado — `tokens.css` usa fallback Arial/system, sem `@font-face` de Poppins/Inter; só Playfair Display tem arquivo local, herdado de fase anterior). Nenhum download automático foi feito nesta fase (instrução explícita: "NÃO baixar automaticamente"). Fallback funcional confirmado — a Home V2 renderiza legível com a stack de fallback do próprio `tokens.css`.

**Gate registrado**: `V2_FONT_ASSETS_REQUIRED_BEFORE_ROLLOUT` — Poppins/Inter precisam ser licenciadas e auto-hospedadas (arquivo local, nunca Google Fonts remoto — regra já vigente desde a Fase B.1) antes do rollout de produção. Não bloqueia esta fase de integração técnica.
