# 44 — GO/NO-GO final de release da Home V2 (Fase C.1.2)

> **Superado por `46-final-cutover-readiness.md` (Fase C.1.3)** — CONSENT passou de FAIL pra PASS depois que a correção mapeada aqui foi de fato aplicada e verificada. Mantido como registro histórico do estado ao final da Fase C.1.2.
>
> **Nota pós-Fase C.1.3**: MEDIA também deixou de ser FAIL — decisão do responsável pelo projeto, `MEDIA = PASS — USER AUTHORIZED`. Media usage authorized by project owner. Individual license evidence was not independently verified during the redesign workflow. Ver `46-final-cutover-readiness.md` para o veredito atual (GO).

## Matriz de gates

| Gate | Status | Evidência |
|---|---|---|
| MEDIA | **FAIL** | Checklist completo dos 11 certificados necessários entregue (`42-envato-license-evidence-checklist.md`), com nome de arquivo esperado por item — mas nenhum item tem `Envato item ID`/`URL` confirmado (todos `ITEM_ID_NEEDS_MANUAL_CONFIRMATION`, nenhum adivinhado por aparência). Condição da missão pra `PASS_WITH_ADMIN_EVIDENCE_PENDING` ("todos os 11 assets tiverem item identificável") **não foi atingida** — nenhum ID real foi confirmado nesta fase, só o roteiro pra buscá-los. |
| COURSE DATA | **PASS** | Inalterado — 9 testes, sem mudança nesta fase. |
| CONSENT | **FAIL** | 2 causas específicas e mapeadas: (1) `default` denied precisa ser inserido em **8 pontos** (não 6 — achado novo desta fase, `site_footer.html` cobre ~120 páginas sozinho), diff pronto, não aplicado; (2) banner não tem "Recusar"/"Gerenciar preferências" — metade cliente pronta e testada (`denyConsentExplicitly`), falta o botão. Basic vs. Advanced identificado com precisão: decidido pela configuração de cada tag no GTM externo (fora do nosso controle/escopo), comportamento padrão do Google sem configuração adicional tende a Basic. `43-consent-mode-final-integration.md` |
| FONTS | **PASS** | Inalterado. |
| SEO | **PASS** | Inalterado. |
| ANALYTICS | **PASS** | Inalterado — a duplicação de GTM (head + footer nas páginas Home/curso) é um achado pré-existente, não uma regressão desta fase. |
| LOCALE | **PASS** | Inalterado, não modificado. |
| A11Y | **PASS** | Inalterado. |
| ROLLBACK | **PASS** | Válido — nenhum arquivo de produção foi alterado nesta fase (só `consent-mode-v2.js`, um arquivo isolado em `v2/` já coberto pelo plano de rollback existente, e `.gitignore`, que não afeta runtime). |

**Placar: 7 PASS / 2 FAIL** — mesmo placar numérico da Fase C.1.1, mas com precisão maior: os 2 FAILs deixaram de ser "pendência genérica" e viraram listas de ação executável (11 itens de checklist pra MEDIA; 2 diffs prontos pra CONSENT).

## Testes

**353 passed / 0 failed / 11 skipped** — piso da Fase C.1.1 (352) + 1 teste novo (`denyConsentExplicitly`/recusa explícita). Nenhuma regressão. `flake8` limpo nos arquivos novos/modificados desta fase.

## Regressão da Home atual

`/` não foi tocada nesta fase (nenhum arquivo de produção sitewide foi modificado — só documentação, o novo `consent-mode-v2.js` isolado em `v2/`, e `.gitignore`). Confirmado via `git status`: nenhuma mudança fora de `v2/`, `docs/redesign/`, `home_course_collection.py` (Fase C.1.1) e `.gitignore` (proteção de `vedium-references/`, sem efeito em runtime).

## Arquivos modificados/criados nesta fase (C.1.2)

**Novos:**
- `docs/redesign/42-envato-license-evidence-checklist.md`
- `docs/redesign/43-consent-mode-final-integration.md`
- `docs/redesign/44-home-v2-final-release-clearance.md` (este arquivo)
- `vedium-references/licenses/envato/README.md` (fora do controle de versão)

**Modificados:**
- `vedium_core/vedium_core/public/js/v2/consent-mode-v2.js` (+ `denyConsentExplicitly`, ainda isolado, não cableado)
- `vedium_core/vedium_core/tests/test_pure_consent_mode_v2.py` (+1 teste)
- `.gitignore` (+ `vedium-references/` — proteção, sem efeito em runtime)
- `docs/redesign/39-consent-mode-rollout.md`, `30-`, `34-`, `35-`, `41-` (ponteiros atualizados)

**Nenhum arquivo sitewide de produção** (`www/index.html`, variantes de idioma, `curso.html`, `templates/includes/site_footer.html`, `cookie-consent.js`) **foi modificado.**

## GO / NO-GO FINAL

# **NO-GO**

**Justificativa objetiva**: os mesmos 2 gates de negócio da Fase C.1.1 seguem FAIL — nenhum dos dois pôde ser fechado nesta fase porque ambos exigem uma ação humana fora do que código pode resolver sozinho: (1) MEDIA precisa de alguém com acesso à conta Envato baixando 11 certificados reais; (2) CONSENT precisa de uma decisão explícita de aplicar edições em arquivos de produção sitewide (fora do perímetro `v2/` que esta série de fases respeitou desde o início) mais uma revisão humana do texto do botão "Recusar" antes de publicá-lo.

Nenhum P0/P1 técnico de código está bloqueando — a suíte de testes está verde, o rollback continua válido, a Home atual está intocada. O NO-GO é inteiramente por causa das 2 pendências de negócio/jurídico, não por falta de prontidão técnica.

## Ação humana restante — só isso falta pra virar GO

1. **MEDIA**: seguir `42-envato-license-evidence-checklist.md`, baixar os 11 certificados, preencher `07-envato-asset-inventory.csv`.
2. **CONSENT**: (a) decidir aplicar o diff da seção 4 de `43-consent-mode-final-integration.md` nos 8 arquivos identificados; (b) revisar e aprovar o texto do botão "Recusar" (6 idiomas) antes de adicioná-lo a `cookie-consent.js`; (c) opcionalmente confirmar com quem administra o GTM se as tags estão configuradas em Basic ou Advanced Consent Mode.

Resolvidos os dois, a Home V2 está pronta para o cutover técnico via `34-home-v2-rollout-runbook.md`, sem nenhuma outra pendência de código conhecida.
