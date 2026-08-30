# 32 — Achados consolidados do QA Global (Fase G.1)

Consolida os resultados dos scripts (`crawl-global.mjs`,
`check-overflow-global.mjs`) e as auditorias manuais de segurança,
analytics/consent e acessibilidade feitas nesta fase.

## 1. Overflow horizontal (bug do Footer 768px e correlatos)

**Status: RESOLVIDO, verificado.** Sweep de 15 rotas x 6 larguras
(320/375/390/768/1024/1440) = 90 checagens via Playwright, comparando
`scrollWidth` vs `clientWidth`. Resultado final:
`{ totalChecks: 90, overflowsFound: 0 }`.

3 causas-raiz distintas corrigidas (ver detalhe em cada arquivo):

| Arquivo | Fix | Página(s) afetada(s) |
|---|---|---|
| `header-footer.css` | `.v2-footer__grid` de `1.3fr repeat(4,1fr)` para `minmax(0,1.3fr) repeat(4,minmax(0,1fr))`; `min-width:0` em `.v2-footer__links`/`.v2-footer__whatsapp`; `overflow-wrap:anywhere` nos links e no número de telefone | Footer (site inteiro), 768px |
| `components-base.css` | `.v2-btn` ganhou `max-width:100%` e `@media (max-width:359px){ white-space:normal; text-align:center }` | Home (B2BHomeFeature), 320px |
| `components-editorial.css` | `.v2-vedium-method__list` grid com `minmax(0,1fr)`; `.v2-vedium-method__item > div{min-width:0}`; `.v2-vedium-method__item-label{overflow-wrap:anywhere}`; `.v2-cta-section--brand-full .v2-cta-section__title{overflow-wrap:anywhere}` | Sobre, 1024px; Contato, 320px |

Padrão recorrente identificado: grid/flex tracks sem `minmax(0, ...)`
ou sem `min-width:0` recusam encolher abaixo do tamanho do conteúdo, e
`overflow-wrap:break-word` sozinho NÃO resolve (não reduz o
min-content) -- só `overflow-wrap:anywhere` resolve de verdade. Vale a
pena revisar esse padrão em qualquer CSS novo do design system daqui
pra frente.

## 2. Crawler global (links, imagens, canonical, schema, referências)

- **Imagens quebradas: 0**
- **Referências antigas de WhatsApp: 0**
- **Referências antigas de Instagram: 0**
- **Referências de domínio errado: 0**
- **Título longo demais: 1** -- o artigo de blog migrado tem um título
  real de produção com 77 caracteres. Não é um bug -- é o título já
  publicado no Frappe (regra: não reescrever título de artigo já
  publicado sem motivo editorial real).
- **"Links internos quebrados"**: nenhum link realmente quebrado.
  Todos os itens que o crawler sinalizou são URLs legítimas fora do
  escopo desta migração (páginas de nível de curso, `/teste-de-nivel`,
  locale roots, `/professores`, ~19 páginas de marketing/legal) -- ver
  `31-global-route-inventory.csv` para a lista completa reclassificada.
- **JSON-LD**: parseável em todas as páginas verificadas, sem host
  incorreto.

## 3. Sitemap, robots, 404

- `sitemap.xml`: PASS -- gera URLs absolutas corretas
  (`https://vediums.com/...`), `lastModified` só quando existe dado
  editorial real (nunca a data do build).
- `robots.txt`: PASS -- detecção por host (`headers()`, não
  `NODE_ENV`), confirmado `Disallow: /` em localhost.
- `/rota-inexistente`: PASS -- devolve HTTP 404 real (confirmado via
  `fetch()`), reaproveita Header/Footer/design system.

## 4. Segurança

- **Segredos no bundle cliente**: nenhum encontrado. Busca por
  `process.env.`, `API_KEY`, `SECRET`, `TOKEN`, `PASSWORD` em todo
  `frontend/src` não retornou nenhuma ocorrência.
- **Endpoint de contato** (`app/api/contact/route.ts`): roda 100% no
  servidor (Route Handler), nunca expõe o endpoint Frappe real como uma
  chamada direta do cliente. `intent` é restrito a um `Set` fixo
  (`lead`/`b2b`) -- não repassa valor arbitrário do usuário.
- **Mensagens de erro do Frappe**: `extractFrappeMessage()` extrai só o
  texto e remove tags HTML (`replace(/<[^>]+>/g, "")`) antes de
  devolver ao cliente -- não há injeção de HTML nem
  `dangerouslySetInnerHTML` no `ContactForm.tsx` para exibir esse
  texto.
- **Honeypot**: campo `companyWebsite` preenchido causa retorno de
  sucesso silencioso sem repassar nada ao Frappe (nem gasta cota de
  rate-limit real) -- funciona como esperado.

**Veredito: PASS.**

## 5. Analytics / Consent

- **Contrato `public_cta_click`**: reaproveitado literalmente do Jinja
  de produção (`templates/includes/public_intent_page.html`) via
  `TrackedWhatsappLink` -- mesmo nome de evento, mesmos campos (`cta`,
  `location`). Escopo apenas nos CTAs de WhatsApp do Contato e no botão
  de WhatsApp da página 404 (não retrofitado no site inteiro).
- **GTM (`GTM-P6Q2FXLK`)**: **não está referenciado em nenhum lugar do
  código Next** (busca por `dataLayer`/`gtm`/`GTM`/`Consent` retornou
  só o próprio `TrackedWhatsappLink`). Isso significa que hoje, se o
  Next fosse pro ar, NENHUM evento de analytics seria coletado exceto
  o `public_cta_click` manual -- nem pageview, nem Consent Mode, nem
  Meta Pixel.
- **Isso é esperado nesta fase?** Sim, no sentido de que a missão G.1
  pediu para "auditar contrato de analytics/consent sem implementar
  nenhum novo" -- não fabriquei um GTM novo. Mas é um **bloqueador real
  de cutover**: nenhuma página pode ir para produção sem o container
  GTM real carregado, porque isso apagaria a coleta de dados de
  marketing/growth inteira para qualquer rota migrada.
- **Recomendação**: antes do cutover (fase DEPLOY PREVIEW do
  `29-cutover-plan.md`), adicionar o snippet real do GTM
  (`GTM-P6Q2FXLK`) + Consent Mode ao `app/layout.tsx`, replicando
  exatamente o que o Frappe já injeta hoje (não inventar uma
  configuração nova de consent) -- e então re-testar
  `public_cta_click` para confirmar que não duplica (o próprio Jinja já
  teve histórico de duplicidade desse evento, por isso a Fase F.3 exigiu
  reaproveitar o contrato ao pé da letra).

**Veredito: NOT READY** -- é o achado mais importante desta fase de QA.

## 6. Acessibilidade (spot-check manual)

- **Hierarquia de heading**: PASS nas páginas verificadas -- H1 vem do
  componente de Hero (`HeroEditorial.tsx:32`), seções usam H2 em
  sequência, sem pular nível.
- **Landmarks**: PASS -- `<header>`, `<nav aria-label="Principal">`,
  `<main>` (uma por página), `<footer>` presentes.
- **Formulários**: PASS -- `ContactForm.tsx` e `PathfinderForm.tsx` usam
  `<label htmlFor>` real para cada campo, não só placeholder.
- **Imagens decorativas vs informativas**: PASS no Header -- o logo
  colorido tem `alt="Vedium"`, a versão duplicada (troca de cor no
  overlay) tem `alt=""` + `aria-hidden="true"` corretamente.
- **Foco visível / `prefers-reduced-motion`**: PASS -- ambos definidos
  em `foundations.css` e usados pelos componentes de acordeão/carrossel.
- **Skip link -- ACHADO REAL**: a classe `.v2-skip-link` existe em
  `foundations.css:233` (com estado `:focus` correto, `top:-3rem` ->
  `top:var(--v2-space-4)`), mas **não é usada em nenhum componente**
  (`Header.tsx`, `layout.tsx`) -- é CSS morto, não uma funcionalidade
  real. Usuário de teclado/leitor de tela não tem como pular a
  navegação e ir direto pro conteúdo em nenhuma página.
  - **Severidade**: baixa-média (não bloqueia uso, mas é uma regressão
    de acessibilidade real vs. ter a intenção documentada em CSS).
  - **Não corrigido nesta sessão**: consertar direito exige adicionar o
    link em `Header.tsx` E um alvo `id="main-content"` em cada `page.tsx`
    (são ~13 arquivos) -- maior que um fix pontual de CSS, então documento
    como item PRÉ-CUTOVER em vez de arriscar uma implementação parcial
    (ex.: só em algumas páginas) nesta rodada.
  - **Fix recomendado**: em `Header.tsx`, antes de `{utilityBar}`,
    adicionar `<a href="#main-content" className="v2-skip-link">Pular
    para o conteúdo</a>`; em cada `page.tsx`, dar `id="main-content"`
    ao primeiro elemento depois de `<Header />` (ou envolver com uma
    div). Regressão global obrigatória depois (mesma regra que qualquer
    mudança de componente compartilhado).

**Veredito: PASS COM RESSALVA** (1 achado real, não bloqueador, com fix
documentado).

## 7. Não verificável localmente (itens PRÉ-CUTOVER, não bloqueadores desta fase)

Este ambiente é local, sem deploy -- os itens abaixo exigem um host
real e ficam registrados como checklist pré-produção, não como
"passou"/"falhou":

- **Lighthouse / Core Web Vitals reais**: métricas de campo (LCP/INP/
  CLS) exigem tráfego real ou pelo menos um host público -- não
  simuláveis com precisão em `localhost`.
- **GTM / Meta Pixel / Consent Mode ao vivo**: mesmo depois de
  implementado (ver seção 5), o comportamento real de disparo/carga
  precisa ser validado contra o container de produção
  `GTM-P6Q2FXLK`, não só a presença do snippet.
- **Cloudflare / DNS**: a arquitetura de proxy reverso parcial descrita
  em `29-cutover-plan.md` depende da configuração real de Cloudflare/
  Nginx em produção -- não tenho acesso a essa camada nesta sessão, e
  o plano não pede para eu mexer nela agora.
- **Search Console**: qualquer novo sitemap só deve ser submetido
  manualmente por quem tem acesso à propriedade verificada -- não é
  algo para automatizar nem para eu fazer.

## Resumo por área

| Área | Veredito |
|---|---|
| Overflow horizontal | PASS (0/90, corrigido) |
| Links/imagens/schema/robots/sitemap/404 | PASS |
| Segurança | PASS |
| Analytics/Consent | **NOT READY** (GTM real ausente do Next) |
| Acessibilidade | PASS com ressalva (skip link morto, fix documentado) |
| Itens pré-produção (Lighthouse/Cloudflare/Search Console) | Não aplicável nesta fase, checklist registrado |
