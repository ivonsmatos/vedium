# 29 — Contrato de analytics da Home V2 (Fase C, seções 9, 21, 25-26 da missão)

## 1. GTM — achado real e correção

**Achado**: `templates/includes/v2/footer.html` (e por extensão toda página V2 — `design_system_v2`, `design_system_v2_b2b`, `_home_v2`) **nunca carregou o container GTM**. Confirmado grepando o arquivo antes desta fase — zero menções a `googletagmanager.com`. Isso significa que toda a fundação V2 construída nas fases anteriores nunca teve GA4/GTM rodando de verdade.

**Correção**: replicado (não reescrito) o snippet real de produção — mesmo container `GTM-P6Q2FXLK` (único em todo o site, confirmado em `analytics-contracts.md`), mesmo guard de dedupe, mesmo local (fim do `<body>`, via `footer.html`). Verificado no HTML renderizado de `/_home_v2`: script + `<noscript><iframe>` presentes, container ID correto.

GA4 continua rodando 100% via GTM (client-side, tag "GA4 - Base Config", trigger `All Pages`) — nenhuma mudança necessária além de garantir que o container carregue.

## 2. Meta Pixel — não portado nesta fase

`public/js/meta-pixel.js` (ID `1539456614495904`) não foi incluído nas páginas V2. Diferente do GTM, o Meta Pixel real é **gated por consentimento LGPD** (`localStorage.vedium_cookie_consent`) na produção — portar o pixel sem portar também o gate de consentimento seria pior que não portar nada (rodaria incondicionalmente, ao contrário do comportamento real). Ver seção 4 abaixo (consentimento) — registrado como pendência conjunta, não implementado isoladamente.

## 3. Eventos preservados (sem renomear, sem reimplementar)

Nenhum evento existente foi renomeado. A Home V2 dispara os mesmos eventos que a Home real dispararia nos mesmos cliques, usando o mesmo mecanismo:

| Evento | Onde dispara na Home V2 | Mecanismo |
|---|---|---|
| `public_cta_click` | Qualquer link `wa.me/`/`api.whatsapp.com/` (header, footer ×2) | Listener global capture-phase de `vedium-language.js` (reutilizado, incluído via `<script>` desde a Fase B.6E) — **nenhum `onclick` local adicionado nos links WhatsApp do header/footer V2**, confirmado por grep. Isso significa que a Home V2 **não introduz a duplicação sistemática já documentada** (item de drift em `analytics-contracts.md`) — só 1 push por clique, não 2 |
| GA4 pageview automático | Toda navegação | Tag base do GTM, incondicional |

## 4. Eventos NOVOS nesta fase — `pathfinder_*`

**Auditoria feita antes de criar** (regra explícita da missão, seção 9): grep completo em `analytics-contracts.md` e no dataLayer real documentado — **nenhum evento `pathfinder_*` existia antes**. O único evento relacionado a idioma no GTM (`language_selected`) está confirmado como trigger morto desde 2026-07-02 (código que o disparava foi desligado) — não é o mesmo mecanismo e não foi reaproveitado (o Pathfinder é sobre escolha de curso/objetivo, não sobre idioma de interface do site).

Nomes escolhidos seguem a convenção já usada no resto do site (snake_case, sufixo `_select`/`_submit`/`_click`, mesmo padrão de `plan_select_click`, `level_test_completed`, `seo_landing_course_grid_click`):

| Evento | Disparado quando | Parâmetros |
|---|---|---|
| `pathfinder_language_select` | Usuário seleciona um rádio de idioma | `language` (valor exato do rádio, ex. "Inglês") |
| `pathfinder_goal_select` | Usuário seleciona um rádio de objetivo | `goal` (valor exato do rádio) |
| `pathfinder_submit` | Clique em "Encontrar meu caminho" | `language`, `goal`, `destination` (URL real resolvida pela matriz, ou `null` se caiu no fallback nativo) |

**Estes 3 nomes NÃO foram publicados/configurados no GTM nesta fase** — são só `dataLayer.push()` no código (client-side), aguardando configuração de tag/trigger no GTM por quem administra o container (fora do escopo de código deste repositório). Documentados aqui exatamente como a missão pediu ("não publicar automaticamente... documentar antes").

Testado de ponta a ponta via CDP (seleção real de rádio + submit real): os 3 eventos disparam na ordem certa, com os parâmetros certos, e a navegação real acontece pra URL correta (`Iorubá` + `Estudos e cultura` → `/ioruba-cultura-e-ancestralidade`, confirmado).

## 5. Consentimento LGPD — risco pré-existente, não resolvido aqui

Baseline (`analytics-contracts.md`) confirma: **GTM carrega incondicionalmente hoje, sem gate de consentimento** — só o Meta Pixel tem gate. Isso é um risco de compliance **pré-existente na produção real**, não introduzido por esta fase.

Por instrução explícita da missão (seção 26): **não resolvido silenciosamente aqui**. A Home V2 replica o MESMO comportamento da produção real (GTM incondicional) — não piora, mas também não corrige. Registrado como candidato a **P0/P1 separado**, numa fase própria dedicada a analytics/privacy, cobrindo o site inteiro (não só a Home V2 isoladamente, já que o gate precisaria ser consistente em todas as páginas).

## 6. UTMs, CRM, WhatsApp — sem mudança de mecanismo

Nenhum parâmetro UTM é gerado ou consumido de forma diferente na Home V2 (mesma passagem transparente de querystring que o resto do site). Nenhum touchpoint de CRM novo foi criado — os CTAs de B2B/contato levam pra páginas reais (`/empresas`, `/contato`) que já têm seus próprios formulários/eventos reais (`public_intent_submit` etc.), não duplicados aqui. Número de WhatsApp preservado: `+55 11 91129-3075`, mesmo texto pré-preenchido.
