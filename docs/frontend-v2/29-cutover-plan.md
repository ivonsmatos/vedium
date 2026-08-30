# 29 — Plano de Cutover, Rollback e Smoke Test

Nenhuma etapa abaixo foi executada. Este documento é o plano — a
missão G.1 é explícita: "DEPLOY: NOT PERFORMED" e "não executar cutover
sem autorização humana explícita".

## Achado crítico que define a arquitetura do cutover

Um swap total de DNS/host (tudo que hoje serve de `app.vediums.com`
passar a servir do Next) **quebraria imediatamente** todas as URLs que
o Next não serve e que só existem no Frappe hoje (ver
`31-global-route-inventory.csv`, linhas "OUT OF SCOPE -- SERVE VIA
FRAPPE"):

- ~18 páginas de nível de curso (`/curso/<slug>`)
- `/teste-de-nivel`, `/teste-de-nivel-ingles`
- Locale roots `/en/`, `/es/`, `/fr/`, `/de/`, `/ru/`
- 96 dos 97 artigos do blog (só 1 foi migrado nesta fase)
- ~19 páginas de marketing/institucionais (`/matricula`, `/catalogo`,
  `/faq`, `/cookies`, etc.)
- O LMS inteiro (`app.vediums.com/lms`, matrícula, aluno)

**Conclusão**: o cutover não pode ser um swap completo enquanto o
Next não cobrir essas rotas. A arquitetura correta é um **cutover
parcial por proxy reverso**: o Nginx/Cloudflare passa a rotear, rota a
rota, só as URLs que o Next já serve (as 13 páginas migradas + o hub e
o 1 artigo de blog), e delega tudo o mais para o Frappe como já
acontece hoje. Isso permite migrar incrementalmente sem perder nenhuma
URL indexada.

## Fases

### 1. PREPARE (sem risco, pode começar a qualquer momento)
- Build de produção do Next (`next build`) rodando limpo, sem erros de
  tipo/lint.
- Variáveis de ambiente de produção configuradas (destino real do
  `POST /api/contact` -- hoje aponta para
  `https://app.vediums.com/api/method/vedium_core.public_funnel.submit_public_intent`,
  já é produção real, não precisa mudar).
- `NEXT_PUBLIC_*` (se algum existir) revisado -- nesta auditoria não
  encontrei nenhuma env var client-side com segredo (ver
  `32-qa-global-findings.md`, seção Segurança).
- Confirmar com o time de infraestrutura qual container/porta o Next
  vai rodar em produção (fora do escopo desta sessão -- não tenho
  acesso à infra de produção).

### 2. DEPLOY PREVIEW (sem tráfego real)
- Subir o Next em um host de preview (subdomínio interno ou porta
  isolada), SEM apontar DNS/Cloudflare pra ele.
- Rodar o Smoke Test Plan (seção abaixo) contra esse preview.

### 3. VALIDATE (contra o preview, ainda sem tráfego real)
- Repetir `check-overflow-global.mjs` e `crawl-global.mjs` (scripts
  desta fase) contra a URL de preview, não só localhost.
- Rodar Lighthouse/PageSpeed real contra o preview (não é possível
  localmente -- ver `32-qa-global-findings.md`, seção "Não verificável
  localmente").
- Confirmar GTM (`GTM-P6Q2FXLK`) e Consent Mode carregando de verdade
  no preview -- hoje o container não está referenciado no código Next
  (ver achado abaixo); precisa ser adicionado ANTES do preview, não
  depois.

### 4. FREEZE
- Congelar mudanças de conteúdo no Frappe para as páginas que serão
  cortadas (as 13 migradas) durante a janela de cutover, para não
  perder uma edição de última hora que só existe no Frappe.

### 5. CUTOVER (parcial, por rota -- não por DNS completo)
- Regra de proxy: se a URL bater em uma das 13 rotas migradas (ou
  `/blog/ingles/aula-de-ingles-online-...`), servir do Next; qualquer
  outra URL sob `vediums.com`/`app.vediums.com`, continuar servindo do
  Frappe exatamente como hoje.
- Implementar o redirect `/metodologia -> /como-funciona` (301) nesse
  mesmo momento -- é o único redirect desta fase ainda pendente (ver
  `28-global-redirect-map.csv`, linha 2).
- Nenhuma mudança de Stripe, e-mail (Brevo) ou LMS -- esta migração é
  só o frontend público institucional, o backend inteiro continua no
  Frappe (ver contrato de separação já documentado nas Fases F.1-F.3).

### 6. SMOKE (ver Smoke Test Plan abaixo, agora contra produção real)

### 7. MONITOR
- Observar por 48-72h: taxa de erro 4xx/5xx nas 13 rotas cortadas,
  Search Console (cobertura/erros -- não submeter nada novo, só
  observar o que já está indexado), volume de `public_cta_click` no
  GTM (deve continuar estável, não duplicar -- ver contrato de
  Fase F.3), volume de submissões do formulário de contato.

### 8. ROLLBACK IF REQUIRED
Ver seção dedicada abaixo.

## Rollback Plan

**Gatilho**: qualquer um destes dispara rollback imediato --
(a) taxa de erro 5xx acima do normal em qualquer uma das 13 rotas
cortadas; (b) queda abrupta de tráfego orgânico não explicada em
qualquer rota cortada (indício de problema de indexação/canonical);
(c) formulário de contato parar de gerar Helpdesk Ticket/CRM Lead no
Frappe; (d) qualquer regressão visual/funcional reportada por um
usuário real que não foi pega no Smoke Test.

**Responsável**: quem executou o cutover (dono da mudança de
proxy/DNS) -- não delegar a decisão de rollback para alguém sem acesso
à infra.

**Passos**:
1. Reverter a regra de proxy reverso para 100% Frappe nas 13 rotas
   (reverter é mais rápido que consertar, sempre rollback primeiro,
   investigar depois).
2. Confirmar via `curl`/browser que as 13 URLs voltaram a responder do
   Frappe com o conteúdo antigo.
3. Reverter o redirect `/metodologia -> /como-funciona` se ele tiver
   sido implementado nesta janela (a página `/metodologia` do Frappe
   continua existindo e servindo até uma decisão futura).
4. Comunicar o rollback e o motivo para quem monitorou (passo MONITOR
   acima).

**Tempo estimado**: rollback de uma regra de proxy reverso é
tipicamente minutos, não horas -- não envolve migração de dados (o
Next não tem estado próprio, é 100% stateless/leitura de conteúdo
estático + 1 endpoint de formulário que só repassa pro Frappe).

**Preservação do backend Frappe**: nenhuma etapa deste plano toca o
Frappe, o Stripe, o Brevo ou o LMS -- o rollback do frontend não tem
nenhuma dependência de rollback de backend, porque nenhuma dessas
camadas foi alterada por esta migração (ver `23-contact-form-
integration-audit.md`: o form já usa `Route Handler -> Frappe`, nunca
grava direto num DocType).

## Smoke Test Plan

Checklist mínimo (missão G.1, seção 53) para rodar depois de cada
deploy (preview E produção):

| # | Item | O que verificar |
|---|---|---|
| 1 | Home | Carrega, hero renderiza, CTA principal funciona |
| 2 | 1 página de idioma (ex.: `/curso-de-ingles-online`) | Carrega, preço real aparece, CTA de matrícula aponta pro Frappe |
| 3 | PLE (`/portugues-para-estrangeiros`) | Carrega, sem imagem quebrada |
| 4 | B2B (`/empresas`) | Carrega, formulário/CTA de contato B2B funciona |
| 5 | Blog (hub, `/blog`) | Lista o artigo migrado, links de categoria funcionam |
| 6 | 1 artigo de 2025 | Confirma que `publishedAt` bate com a data original (regra da correção obrigatória) |
| 7 | 1 artigo de 2026 | idem |
| 8 | Legal (`/privacidade`, `/termos`, `/cancelamento-reembolso`) | Carrega, sem alteração de texto |
| 9 | Contato (`/contato`) | Formulário envia e recebe confirmação; WhatsApp CTA dispara `public_cta_click` |
| 10 | WhatsApp | Todos os links abrem `wa.me` com o número correto (+55 11 91129-3075) |
| 11 | Formulário | Honeypot não bloqueia envio legítimo; erro do Frappe aparece formatado, não como stack trace |
| 12 | Locale switcher | Aponta pra `/en/`, `/es/` etc. sem 404 |
| 13 | 404 | URL inexistente devolve a página 404 real (status HTTP 404, não 200) |
| 14 | Sitemap | `/sitemap.xml` responde com as URLs corretas |
| 15 | Robots | `/robots.txt` permite crawl em produção (não `Disallow: /`) |

**Nota sobre o item 7 (artigo de 2025)**: nesta fase só 1 artigo foi
migrado (`aula-de-ingles-online-ao-vivo...`, publicado 2026-07-13) --
não há ainda um artigo de 2025 migrado para testar o item 6 de verdade.
Esse item do smoke test só fica executável depois de uma fase futura de
migração em massa do blog (ver `27-blog-url-migration-map.csv`). Deixo
isso registrado explicitamente em vez de marcar o item como "passou"
sem evidência.
