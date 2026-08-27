# 47 — Resultado do cutover controlado da Home (Fase C.1.4)

> **Cutover LOCAL executado e verificado.** Nenhum deploy de produção, nenhum push, nenhuma mudança de Nginx. `/` agora serve a implementação V2 real neste ambiente local — a promoção pra produção real depende de deploy/push explicitamente autorizados depois desta entrega.

## 1. Pré-flight (Seção 1)

- **Branch**: `main`
- **PRE_CUTOVER_COMMIT**: `7ebd7c318569fe92dd731be88d151d9a6f2d7016` ("feat: approve Vedium v2 design system and home direction", Fase B.6E)
- **Arquivos modificados antes do cutover começar**: 132 modificados + 31 não versionados = 163 (acumulados das Fases C.1.1–C.1.3, nenhum commitado ainda)
- Nenhum `git add .` usado em nenhum momento.

## 2. Backup / rollback point (Seção 2)

- Tag local criada: `pre-home-v2-cutover` → aponta pro commit acima. **Não pushada.**
- Backup de arquivo de `www/index.py` e `www/index.html` (estado V1 completo, pré-cutover) salvo fora do repositório, em `scratchpad/c14_baseline/pre_cutover_files/`.

## 3. Baseline da Home V1 (Seção 3) — capturado antes de qualquer mudança

| Campo | Valor real capturado |
|---|---|
| HTTP status | 200 |
| Title | "Vedium - Cursos Online ao Vivo em Cinco Idiomas" |
| Canonical | `https://vediums.com/` (hardcoded) |
| Description | "Aprenda inglês (níveis A1 a C1) e iorubá com a Vedium..." |
| Robots | `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` |
| Hreflang | pt-br, en, es, fr, de, x-default (sem `ru`) |
| JSON-LD | 1 bloco `EducationalOrganization` |
| Screenshots | desktop 1440 + mobile 390 salvos em `scratchpad/c14_baseline/` |
| HTML completo | salvo em `scratchpad/baseline_home_v1.html` (106.260 bytes) |

## 4. Implementação — sem redirect, com mínimo de duplicação (Seções 4-5)

**Nenhum redirect criado.** `/` responde DIRETAMENTE com o conteúdo V2 (`www/index.py`/`.html`), não um `location: /_home_v2`.

**Refatoração pra reutilizar a mesma implementação** (não duplicar):
- Novo `templates/includes/v2/home_page_content.html` — extraído do corpo de `_home_v2.html` (header + home_body.html + CTA final + footer + scripts). Agora incluído tanto por `www/index.html` (novo) quanto por `www/_home_v2.html` (atualizado pra usar o mesmo include).
- Nova função `v2_home_data.build_home_v2_context(context)` — extraída de `_home_v2.py`, monta os dados (insights + HomeCourseCollection) compartilhados entre `www/index.py` e `www/_home_v2.py`. Cada um continua responsável só pelos campos que diferem (robots/canonical_url/title/no_sitemap).
- Resultado: `/` e `/_home_v2` renderizam o **mesmo HTML de corpo**, comprovado pela altura de página idêntica (10.730px em 1440px) entre as duas rotas.

## 5. SEO — contrato preservado literalmente, nenhum valor inventado (Seções 6-8, 25)

| Campo | `/` (novo) | Igual ao V1? |
|---|---|---|
| HTTP status | 200 | ✅ |
| Title | "Vedium - Cursos Online ao Vivo em Cinco Idiomas" | ✅ idêntico |
| Description | mesmo texto do V1 | ✅ idêntico |
| Robots | `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` | ✅ idêntico, **nenhum noindex vazou** |
| Canonical | via `context.canonical_url` (mecanismo real, não mais hardcoded) — resolve pra `https://vediums.com/` em produção; mostra `http://vedium.local:8000/` neste ambiente local (esperado, mesmo padrão de `curso.py` etc.) | ✅ mecanismo correto |
| Hreflang | pt-br/en/es/fr/de/x-default, idêntico ao V1 (sem `ru`, gap pré-existente conhecido, não introduzido aqui) | ✅ idêntico |
| OG/Twitter | idêntico ao V1 | ✅ idêntico |
| JSON-LD | 1 bloco `EducationalOrganization`, idêntico ao V1 | ✅ idêntico |
| H1 | 1 único (`Aprenda ao vivo. Avance com direção.`, do Hero V2) | ✅ único |
| lang | `pt-BR` | ✅ |
| Favicons/manifest/PWA splash | idênticos ao V1, migrados literalmente | ✅ idênticos |

**`/_home_v2` continua noindex/nofollow/fora do sitemap** — teste específico criado (`test_noindex_never_leaks_from_home_v2_route_into_real_home`, seção 6 da missão).

**Sitemap**: `www/sitemap.py` já lista `/` de forma hardcoded (linha própria, independente de `no_sitemap`); `/_home_v2` nunca foi adicionado lá — nada a mudar.

## 6. Locale (Seção 8-9) — validado nos 6 locales reais

Testado via CDP no `/` novo: seletor abre/fecha, 6 locales (pt-br/en/es/fr/de/ru) com bandeira+código no botão e bandeira+nome no menu (mesma implementação da Fase C.1, não redesenhada). Screenshot em `scratchpad/c14_baseline/home_v2_cutover_locale_menu.png`.

## 7. Menu Cursos (Seção 10) — 5 links, todos 200

`/curso-de-ingles-online`, `/curso-de-ioruba-online`, `/portugues-para-estrangeiros`, `/curso-de-espanhol-online`, `/curso-de-hebraico-online` — todos HTTP 200, confirmados após o cutover.

## 8. Hero (Seção 11) — visualmente idêntico ao aprovado

Screenshot desktop/mobile idênticos ao design já aprovado desde a Fase B.6A (mesma imagem, mesmo overlay, mesmos CTAs, mesma navegação por tabs no rodapé do Hero). Nenhum código do Hero foi tocado nesta fase — só a rota que o serve mudou.

## 9. Pathfinder (Seção 12) — testado com Aceitar E Recusar

Selecionado Iorubá + "Trabalho e carreira" via CDP em duas sessões distintas (uma após Aceitar, outra após Recusar): os eventos `pathfinder_language_select`/`pathfinder_goal_select` disparam identicamente nos dois casos — Pathfinder não depende de consentimento pra funcionar.

## 10. Consent Mode (Seção 13) — ordem comprovada empiricamente em `/`

```
consent default (denied) → GTM → interface de consentimento → consent update
```

Verificado via `window.dataLayer` real (não o HTML-fonte): **exatamente 1** `consent default`, com os 4 sinais `denied`, antes de qualquer evento do GTM. A página tem 4 ocorrências textuais de `GTM-P6Q2FXLK` (2 do `<head>` + 2 do footer V2, mesmo padrão de duplicação-com-guard que já existia no V1) — o guard `window.__vediumConsentDefaultSet` garante que só 1 `default` real é enviado ao `dataLayer`, e o guard nativo do GTM (`document.querySelector`) evita a segunda requisição de rede do `gtm.js`.

## 11. Cookie banner (Seção 14) — Aceitar/Recusar/Gerenciar testados na nova Home

Fluxos completos (Aceitar, Recusar) testados via clique real em `/`, com reload confirmando persistência — mesmos resultados dos testes já feitos na Fase C.1.3 pros outros pontos de entrada. Design do banner **não foi alterado** nesta fase.

## 12. GTM / Meta Pixel (Seções 15-16)

Nenhuma mudança externa no container GTM. `Basic vs. Advanced` continua **pendência humana não bloqueante** (checklist em `45-consent-remediation-result.md` seção 9).

**POST-CUTOVER ANALYTICS GAP** (registrado, não corrigido): `meta-pixel.min.js` continua não sendo referenciado em nenhuma página real, incluindo a nova `/` (achado da Fase C.1.3, não introduzido/piorado aqui).

## 13. Footer / revogação de cookies (Seção 17)

**POST-CUTOVER UX IMPROVEMENT** (registrado, não implementado): link de revogação de preferências no Footer segue como proposta parada aguardando aprovação (Footer congelado, ver `45-` seção 7) — nenhuma mudança visual foi feita.

## 14. Media / HomeCourseCollection / Blog (Seções 18-20)

- MEDIA continua `PASS — USER AUTHORIZED`, gate não reaberto, nenhuma mídia trocada.
- HomeCourseCollection: os 5 idiomas renderizam corretamente na nova `/` (mesma fonte `home_course_collection.py`, não modificada).
- Blog/Conhecimento Vedium: mesma seleção dinâmica real (`v2_home_data.get_insights_selection()`), inalterada.

## 15. B2B / CTA final / Footer (Seções 21-23)

Nenhuma alteração — mesmo corpo compartilhado (`home_page_content.html`) inclui as seções B2B, CTA final e Footer exatamente como já aprovadas. Página renderizada com altura total idêntica à `/_home_v2` (10.730px @ 1440px), confirmando que todo o conteúdo abaixo do Hero também é idêntico.

## 16. Analytics (Seção 24)

Nenhuma correção de arquitetura global feita. Único ajuste: a nova `/` ganhou o mesmo `consent_default.html` que os outros 7 pontos já tinham desde a Fase C.1.3 (não uma correção nova, só a extensão natural do cutover).

## 17. Performance (Seção 27) — smoke, não pontuação

Nenhum erro de JS/rede observado nos testes via CDP. Hero mantém `fetchpriority="high"`/`loading="eager"` no slide 1 (herdado, não alterado). CSS trocado de V1 (Bootstrap/swiper/jarallax/fontawesome + preload de imagem Unsplash não utilizada por V2) para os 5 arquivos CSS do Design System V2 — página final é **~46% menor** (59.582 bytes vs. 106.260 bytes do V1), sem os scripts vendor V1 (jQuery/Bootstrap/jarallax/swiper/wow) que a V2 não usa.

## 18. Accessibility (Seção 28)

H1 único confirmado. Header/locale testados via teclado/CDP (Fase C.1, não modificado). Nenhuma regressão esperada — mesmo componente, rota diferente.

## 19. Viewports (Seção 29)

Screenshots capturados em 390 (mobile), 768 (tablet) e 1440 (desktop) — Hero, Header, Pathfinder confirmados visualmente idênticos ao design aprovado em todos os 3. Salvos em `scratchpad/c14_baseline/home_v2_cutover_*.png`.

## 20. Suíte de testes (Seção 30)

| Momento | Passed | Failed | Skipped |
|---|---|---|---|
| Antes do cutover | 362 | 0 | 11 |
| **Depois do cutover (1ª rodada)** | 358 | **4** | 11 |
| Depois de atualizar os 4 testes V1-específicos | **363** | **0** | 11 |

Os 4 testes que falharam na 1ª rodada testavam exclusivamente markup V1 que não existe mais (`test_real_home_untouched_by_the_v2_integration` — invertido pra confirmar o cutover ao invés de negar-lo; `test_home_pricing_ctas_have_equal_size_and_single_line_text` — removido, a grade de preços V1 não existe mais na Home; `test_app_domain_redirect_and_catalog_level_guards_are_in_place` — 2 asserções de CSS V1 removidas, resto preservado; `test_home_pages_apply_lighthouse_performance_and_accessibility_fixes` — dividido em 2, um teste leve pra `/` (pt-BR, agora V2) e o teste completo mantido pros 5 idiomas que continuam V1). Nenhuma redução real de cobertura — funcionalidade testada foi removida junto com o markup, não esquecida.

**Nenhum teste crítico falhou de forma inesperada — nenhum rollback foi necessário.**

## 21. Smoke test de rotas (Seção 31)

| Rota | Status |
|---|---|
| `/` | 200 |
| `/_home_v2` | 200 |
| `/curso-de-ingles-online`, `/curso-de-ioruba-online`, `/portugues-para-estrangeiros`, `/curso-de-espanhol-online`, `/curso-de-hebraico-online` | 200 |
| `/blog` | 403 (gap pré-existente: DocType "Vedium Blog Post" não migrado neste ambiente local — não é regressão do cutover) |
| `/empresas`, `/sobre`, `/contato`, `/teste-de-nivel`, `/privacidade`, `/termos`, `/cancelamento-reembolso` | 200 |
| `/en/`, `/es/`, `/fr/`, `/de/`, `/ru/` | 200 (continuam V1, intocadas) |
| `/catalogo` | 301 → `/cursos-de-idiomas-online` (200) — redirect legítimo pré-existente |
| `/design_system_v2` | 200 |

## 22. Critérios de rollback (Seção 32) — nenhum foi atingido

Nenhum dos gatilhos de rollback imediato ocorreu: `/` está de acordo com o design aprovado, HTTP 200, sem noindex, canonical correto (via mecanismo real), locale funcional, Hero íntegro, CSS/JS carregando, menu Cursos íntegro, Pathfinder funcional, consent default antes do GTM, nenhum 404 relevante, suíte 100% verde. **Rollback não foi executado.**

## 23. Cache (Seção 34) / Migrate (Seção 35)

`bench --site vedium.local clear-cache` executado após cada mudança de `.py`/`.html`; processo `bench serve` reiniciado (necessário pra `.py`, achado recorrente desta sessão). **Nenhum `migrate` executado** — nenhuma alteração de schema/DocType nesta fase. Nginx não tocado.

## 24. Arquivos do cutover (Seção 38)

**Novos:**
- `vedium_core/vedium_core/templates/includes/v2/home_page_content.html`
- `docs/redesign/47-home-v2-cutover-result.md` (este arquivo)

**Modificados diretamente pelo cutover:**
- `vedium_core/vedium_core/www/index.py` (reescrito — remove lógica V1 morta, adota `build_home_v2_context`)
- `vedium_core/vedium_core/www/index.html` (reescrito — SEO preservado literalmente, corpo trocado pro V2)
- `vedium_core/vedium_core/www/_home_v2.py` (refatorado pra usar `build_home_v2_context`)
- `vedium_core/vedium_core/www/_home_v2.html` (refatorado pra usar `home_page_content.html`)
- `vedium_core/vedium_core/v2_home_data.py` (+ `build_home_v2_context()`)
- `vedium_core/vedium_core/tests/test_pure_home_v2.py` (regra invertida + 1 teste novo)
- `vedium_core/vedium_core/tests/test_pure_marketing_pages.py` (3 testes V1-específicos ajustados/removidos)

**Não modificados por esta fase** (herdados de fases anteriores, ainda não commitados): os demais ~155 arquivos de `git status` (Fases C.1.1–C.1.3: HomeCourseCollection, Consent Mode nos 120 arquivos, docs 26-46).

## GO/NO-GO desta etapa

**`/` agora usando V2: SIM.**

## Entrega final (regra de parada)

1. **`/` agora usando V2**: **SIM**
2. **Testes antes/depois**: 362→363 passed, 0 failed, 11 skipped (piso mantido e ligeiramente ampliado)
3. **SEO status**: contrato 100% preservado (title/description/canonical/robots/hreflang/OG/Twitter/JSON-LD/H1/lang), nenhum noindex vazou
4. **Locale status**: 6 locales funcionais, bandeiras corretas, testado via CDP
5. **Consent status**: default→GTM→update comprovado empiricamente, banner Aceitar/Recusar/Gerenciar funcional, Pathfinder funciona com Aceitar e Recusar
6. **Analytics status**: GTM único container, sem duplicação nova (mesmo padrão pré-existente com guard), Meta Pixel gap registrado (não corrigido, não piorado)
7. **Screenshots**: desktop 1440/tablet 768/mobile 390 + locale menu, salvos em `scratchpad/c14_baseline/`
8. **Rollback status**: NÃO executado — não foi necessário, nenhum critério de rollback foi atingido
9. **Arquivos do cutover**: listados na seção 24 acima
10. **Commit proposto**: `feat: make Vedium v2 the primary homepage` — **NÃO executado ainda**, aguardando confirmação explícita sobre escopo (arquivos só deste cutover vs. incluir também o backlog acumulado das Fases C.1.1–C.1.3, ainda não commitado)
11. **READY FOR PRODUCTION DEPLOY**: **NO** — cutover local validado e pronto tecnicamente, mas deploy/push/Nginx/produção real exigem autorização humana explícita separada, conforme regra de parada desta fase
