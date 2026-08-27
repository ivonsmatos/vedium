# 41 — GO/NO-GO final da Home V2 (Fase C.1.1)

> **Superado por `44-home-v2-final-release-clearance.md` (Fase C.1.2)** — mantido aqui como registro histórico do estado ao final da Fase C.1.1. Para o veredito e a matriz de gates mais atuais, ver o documento 44.
>
> **Nota pós-Fase C.1.3**: o gate MEDIA descrito abaixo como FAIL foi resolvido por decisão do responsável pelo projeto — `MEDIA = PASS — USER AUTHORIZED`. Media usage authorized by project owner. Individual license evidence was not independently verified during the redesign workflow. Ver `46-final-cutover-readiness.md` para o veredito atual.

## Matriz de gates

| Gate | Status | Evidência |
|---|---|---|
| MEDIA | **FAIL** | 11 assets ativos = `NEEDS_LICENSE_EVIDENCE` (nenhum comprovante de licença Envato encontrado no repositório/referências). Pipeline de derivados WebP/AVIF pronto com números reais. Ação pendente: administrativa (confirmar assinatura Envato Elements), não técnica. `37-production-media-readiness.md` |
| COURSE DATA | **PASS** | `HomeCourseCollection` implementado, testado (9 testes), curadoria explicitamente declarada como tal, regressão confirmada byte-a-byte. `38-home-course-collection-contract.md` |
| LGPD | **FAIL** (pré-existente, não agravado por este rollout) | Consent Mode v2 implementado e testado (5 testes), diff de integração sitewide pronto — mas ainda não aplicado a `www/index.html`+variantes de idioma. GTM real de produção continua carregando sem gate de consentimento hoje, com ou sem este cutover. `39-consent-mode-rollout.md` |
| FONTS | **PASS** (non-blocking) | Poppins/Inter = SIL OFL 1.1, sem ambiguidade jurídica; fallback funcional sem CLS perceptível; 3 arquivos pendentes de download manual, não bloqueante. `40-font-production-readiness.md` |
| SEO | **PASS** | Canonical corrigido na raiz (`context.canonical_url`), noindex/no_sitemap corretos em `/_home_v2`, contrato completo da futura Home real documentado. `32-`, `28-` |
| ANALYTICS | **PASS** | GTM presente (gap da Fase C corrigido), sem duplicação nova de `public_cta_click`, dataLayer/Pathfinder documentado e testado. Configuração de tags/triggers do Pathfinder no GTM externo é tarefa administrativa remanescente, não bloqueia o código. |
| LOCALE | **PASS** | 6 locales reais, bandeiras implementadas e testadas, política de bandeira replicada da produção real. |
| ACCESSIBILITY | **PASS** | Teclado, foco, headings, reduced motion confirmados; contraste não recalculado matematicamente nesta fase (risco baixo, nenhuma cor nova). |
| ROLLBACK | **PASS** | Plano de 2 cenários documentado com comandos/tempo estimado/necessidade de restart. `35-` |

**Placar: 7 PASS / 2 FAIL** (eram 4 gates de negócio em aberto na Fase C.1; hoje restam 2, ambos com causa e próximo passo exatos, não vagos).

## Testes

**352 passed / 0 failed / 11 skipped** — piso da Fase C.1 (338) + 9 testes de `HomeCourseCollection` + 5 testes de `consent-mode-v2.js` = 352. Nenhuma regressão. `flake8` limpo em todos os arquivos novos/modificados. CRLF normalizado em 100% dos arquivos tocados nesta fase.

## Arquivos modificados/criados nesta fase (C.1.1)

**Novos:**
- `vedium_core/vedium_core/home_course_collection.py`
- `vedium_core/vedium_core/public/js/v2/consent-mode-v2.js`
- `vedium_core/vedium_core/tests/test_pure_home_course_collection.py`
- `vedium_core/vedium_core/tests/test_pure_consent_mode_v2.py`
- `docs/redesign/37-production-media-readiness.md`
- `docs/redesign/38-home-course-collection-contract.md`
- `docs/redesign/39-consent-mode-rollout.md`
- `docs/redesign/40-font-production-readiness.md`
- `docs/redesign/41-final-home-go-no-go.md` (este arquivo)
- `vedium_core/vedium_core/public/v2-preview-media/{webp,avif,webm}/*` (derivados gerados, gitignorados, não versionados)

**Modificados:**
- `vedium_core/vedium_core/www/_home_v2.py` (consome `HomeCourseCollection`)
- `vedium_core/vedium_core/www/design_system_v2.py` (idem)
- `vedium_core/vedium_core/templates/includes/v2/home_body.html` (loop sobre `home_courses`, substitui 5 blocos hardcoded)
- `docs/redesign/30-home-v2-rollout-gates.md` (gates atualizados)
- `docs/redesign/34-home-v2-rollout-runbook.md` (pré-flight atualizado)
- `docs/redesign/35-home-v2-rollback-plan.md` (arquivos afetados atualizados)

**Nenhum arquivo de produção fora de `v2/`/`docs/redesign/` foi alterado.** `consent-mode-v2.js` existe mas não está incluído em nenhuma página — zero efeito em produção até uma decisão explícita de aplicar o diff documentado em `39-`.

## GO / NO-GO

# **NO-GO**

**Justificativa objetiva**: 2 gates seguem FAIL — MEDIA (licenciamento não comprovado, ação administrativa) e LGPD (consentimento sitewide ainda não aplicado, ação que expande escopo pra fora de `v2/`). Nenhum dos dois é um problema de código sem solução — os dois têm solução pronta ou próximo passo exato documentado. A diferença real desta fase para a C.1: os gates deixaram de ser "pendências vagas" e viraram "2 decisões humanas específicas, com todo o trabalho técnico já feito à espera delas."

## Ações exatas necessárias para virar GO

1. **MEDIA**: confirmar com o responsável pela conta Envato Elements da Vedium que a assinatura está ativa e que os 11 arquivos foram baixados sob ela; preencher `07-envato-asset-inventory.csv` com a confirmação. Sem isso, promover a mídia atual a produção é risco de direito autoral não verificado.
2. **LGPD**: decidir aplicar o diff de `39-consent-mode-rollout.md` seção 4 em `www/index.html` + 5 variantes de idioma — decisão explícita de expandir o escopo desta iniciativa a arquivos fora de `v2/`, já que consentimento é inerentemente sitewide.

Resolvidos esses 2 pontos (ou aceitos conscientemente como risco de negócio pelo dono do produto), a Home V2 está tecnicamente pronta para o cutover, seguindo o runbook em `34-home-v2-rollout-runbook.md`.
