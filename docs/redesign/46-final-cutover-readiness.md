# 46 — Prontidão final de cutover (Fase C.1.3, atualizado pós-decisão do responsável pelo projeto)

> **Atualização**: o responsável pelo projeto autorizou expressamente o uso de toda a biblioteca `vedium-references/envato-assets/`, assumindo a responsabilidade pelo licenciamento. `MEDIA = PASS — USER AUTHORIZED`. Media usage authorized by project owner. Individual license evidence was not independently verified during the redesign workflow. Isso é aceitação de risco documental do responsável, não uma auditoria técnica de cada certificado — ver `37-production-media-readiness.md` seção "Decisão do responsável pelo projeto". Todas as regras editoriais/culturais (Iorubá, Hebraico, PLE, Espanhol, não-simular-professor/aluno-real, não-inferir-identidade) continuam em vigor sem exceção.

## Matriz de gates

| Gate | Status | Evidência |
|---|---|---|
| MEDIA | **PASS — USER AUTHORIZED** | Uso de toda a biblioteca `vedium-references/envato-assets/` (não só os 11 assets já selecionados) autorizado explicitamente pelo dono do projeto, que assume a responsabilidade pelo licenciamento. Certificado individual por item deixou de ser pré-condição de gate. Regras editoriais/culturais continuam valendo integralmente. Ver `37-production-media-readiness.md`. |
| COURSE DATA | **PASS** | Inalterado desde C.1.1. |
| CONSENT | **PASS** | Contrato site-side completo e testado (doc 45): ordem `default`→GTM corrigida e verificada empiricamente em 8 pontos reais, zero/duplo-default impossível (guard testado), banner Aceitar/Recusar/Gerenciar preferências com paridade de acesso, 6 locales com os textos aprovados, categorias granulares reais (Analytics/Marketing, sem inventar), persistência testada em 6 cenários (A–F). Único item não implementado — link de revogação no Footer — foi explicitamente autorizado a ficar como proposta parada aguardando aprovação (Footer congelado), não uma falha de gate. |
| FONTS | **PASS** | Inalterado. |
| SEO | **PASS** | Inalterado. |
| ANALYTICS | **PASS** | Inalterado; a duplicação de GTM (head+footer) é pré-existente, não piorada. |
| LOCALE | **PASS** | Inalterado, não modificado nesta fase. |
| A11Y | **PASS** | Inalterado; banner novo usa `role="dialog"`/`aria-label` nos 2 diálogos (barra e painel de preferências), inputs de checkbox com `aria-label`. |
| ROLLBACK | **PASS** | Todos os arquivos desta fase são reversíveis (ver seção "Arquivos alterados" abaixo); nenhum dado de produção foi criado/alterado. |

**Placar: 9 PASS / 0 FAIL.**

## Testes

**362 passed / 0 failed / 11 skipped** (piso anterior 353, +9 líquidos: consent mode reescrito com 18 testes reais, 1 teste pré-existente corrigido pro novo cache-bust). Nenhuma regressão.

## Regressão

`/`, `/_home_v2`, `/contato`, `/en/`, `/curso-de-ingles-online` — todos 200, sem mudança visual fora da própria barra de cookies (que é literalmente o objeto desta correção). Nenhuma seção congelada (Hero/Header visual/Cursos/Live/B2B/Conhecimento/CTA/Footer) foi tocada.

## Arquivos alterados nesta fase (Fase C.1.3)

**Novos:**
- `vedium_core/vedium_core/templates/includes/consent_default.html`
- `docs/redesign/45-consent-remediation-result.md`
- `docs/redesign/46-final-cutover-readiness.md` (este arquivo)

**Modificados:**
- `vedium_core/vedium_core/public/js/cookie-consent.js` (Aceitar/Recusar/Gerenciar preferências, 6 locales)
- `vedium_core/vedium_core/public/js/cookie-consent.min.js` (regenerado via terser)
- `vedium_core/vedium_core/public/js/v2/consent-mode-v2.js` (guard de duplicação, preferências granulares, cableado em produção)
- `vedium_core/vedium_core/hooks.py` (comentário corrigido sobre `web_include_js` não se aplicar às páginas reais; versão de cache-bust atualizada)
- `vedium_core/vedium_core/www/index.html`, `en/index.html`, `es/index.html`, `de/index.html`, `fr/index.html`, `ru/index.html`, `curso.html` — include do `consent_default.html` antes do GTM
- `templates/includes/site_footer.html` — idem
- **120 arquivos `www/*.html`/`templates/includes/*.html`** — inserção do `<script>` de `consent-mode-v2.js` logo após `cookie-consent.min.js`, e bump do cache-bust deste último (lista completa reproduzível via `git status`/`git diff --stat`, não replicada aqui por serem 120 entradas mecânicas idênticas)
- `vedium_core/vedium_core/tests/test_pure_consent_mode_v2.py` (reescrito, 18 testes)
- `vedium_core/vedium_core/tests/test_pure_marketing_pages.py` (1 assert corrigido pro novo cache-bust)

**Nenhum arquivo fora deste escopo foi tocado.** `/` e as demais rotas de produção continuam servindo o mesmo conteúdo visual, com a única mudança funcional sendo a própria barra de consentimento (autorizada explicitamente pela missão desta fase).

## Achado colateral registrado, não corrigido

`meta-pixel.min.js` nunca foi de fato incluído em nenhuma página real (mesmo gap estrutural que afetava `consent-mode-v2.js` antes desta fase) — a lógica de consentimento do arquivo está correta, mas ele nunca carrega. Não corrigido por instrução explícita ("não reescrever/republicar Meta"). Registrado em `45-consent-remediation-result.md` seção 11 para decisão humana separada.

## GO / NO-GO FINAL

# **GO — READY FOR CONTROLLED CUTOVER**

Aplicando a regra explícita desta missão: com CONSENT em PASS (site-side contract completo e verificado) e MEDIA em PASS (autorizado pelo responsável do projeto), não resta nenhum gate FAIL na matriz — placar 9/9. **Nenhuma nova regressão surgiu** (362 passed / 0 failed / 11 skipped, `/` e demais rotas intactas visualmente). Esta é a primeira fase da série C.1.x a fechar sem nenhum bloqueador técnico ou administrativo em aberto.

**"GO" aqui significa "tecnicamente pronto para um cutover controlado quando o dono do produto decidir"** — não uma instrução para executar o cutover agora. Nenhum deploy, substituição de `/`, redirect ou cutover foi feito ou será feito automaticamente; a decisão de quando promover `/_home_v2` a `/` continua sendo humana, seguindo `34-home-v2-rollout-runbook.md` (PRE-FLIGHT já reflete o Consent Mode validado; o item de licenciamento de mídia nesse runbook deve ser atualizado para refletir a autorização do responsável em vez do checklist de certificados).

## Decisões humanas remanescentes — não bloqueantes para o cutover técnico

1. Link de revogação de preferências de cookies no Footer (proposta em `45-` seção 7, aguardando aprovação por envolver mudança visual — Footer continua congelado até essa aprovação).
2. Decidir se/quando corrigir o gap do Meta Pixel nunca carregado (achado da Fase C.1.3, decisão de negócio sobre ligar tracking de Ads que hoje nunca rodou).
3. Confirmar com quem administra o GTM se as tags estão em Basic ou Advanced Consent Mode (checklist em `45-` seção 9) — recomendado antes do lançamento público amplo, não bloqueante para um cutover controlado/interno.
4. Ao expandir a seleção de mídia usando a biblioteca completa agora autorizada, seguir as regras editoriais/culturais de `37-production-media-readiness.md` (Iorubá, Hebraico, PLE, Espanhol, etc.) — decisão de curadoria de conteúdo, não de código.
