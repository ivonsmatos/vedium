# 30 — Checklist de gates para rollout da Home V2 (Fase C, seção 36 da missão; atualizado na Fase C.1)

> Este documento NÃO autoriza rollout. É o checklist do que falta confirmar/entregar antes de qualquer decisão humana de promover `/_home_v2` a `/`. Marcado `[x]` = confirmado nesta fase; `[ ]` = pendente/gate aberto, com a razão registrada.
>
> **Atualização Fase C.1**: auditoria pré-lançamento completa (SEO/analytics/locale/acessibilidade/performance/rollback) — ver `32-home-v2-prelaunch-qa.md`, `33-home-v2-performance-baseline.md`, `34-home-v2-rollout-runbook.md`, `35-home-v2-rollback-plan.md`, `36-lgpd-analytics-gap.md`, e o roadmap futuro em `31-webmcp-agentic-web-roadmap.md`. Dois itens que estavam em aberto na Fase C foram fechados nesta fase (canonical, bandeiras do locale); um novo gate P1 foi adicionado (LGPD/consentimento).
>
> **Atualização Fase C.1.1 (remediação de rollout)**: os 4 gates então abertos (mídia/licenciamento, agregação de cursos por idioma, LGPD/consentimento, fontes) foram fechados ou reclassificados com trabalho real — ver `37-production-media-readiness.md`, `38-home-course-collection-contract.md`, `39-consent-mode-rollout.md`, `40-font-production-readiness.md`, e o veredito final em `41-final-home-go-no-go.md`.
>
> **Atualização Fase C.1.2 (clearance final)**: MEDIA e CONSENT (ex-LGPD) continuam FAIL, agora com ação executável precisa em vez de pendência genérica — checklist dos 11 certificados Envato (`42-envato-license-evidence-checklist.md`) e mapeamento completo dos 8 pontos de integração do Consent Mode + gap real de "Recusar" no banner (`43-consent-mode-final-integration.md`). Veredito final consolidado em `44-home-v2-final-release-clearance.md` — **NO-GO**, só por essas 2 pendências de negócio/jurídico, nenhum bloqueador técnico.
>
> **Atualização Fase C.1.3 (remediação autorizada do Consent Mode)**: CONSENT virou **PASS** — o diff de 8 pontos foi aplicado de verdade (ordem `default`→GTM corrigida e comprovada empiricamente), o banner ganhou Aceitar/Recusar/Gerenciar preferências nos 6 locales, preferências granulares e persistência foram testadas (cenários A–F via CDP). Placar nesse momento: 8 PASS / 1 FAIL (MEDIA), veredito **NO-GO — MEDIA ADMIN ONLY**.
>
> **Atualização pós-C.1.3 (decisão do responsável pelo projeto)**: o dono do projeto autorizou expressamente o uso de toda a biblioteca `vedium-references/envato-assets/`, assumindo a responsabilidade pelo licenciamento. `MEDIA = PASS — USER AUTHORIZED`. Media usage authorized by project owner. Individual license evidence was not independently verified during the redesign workflow. **Placar final: 9 PASS / 0 FAIL — GO (cutover controlado, não automático)**. Ver `46-final-cutover-readiness.md`.

### Design

- [x] aprovado — Fases 0 a B.6E, congelado como contrato desta fase; nenhuma seção redesenhada.

### Conteúdo

- [x] real — cursos (5 pilares reais, URLs validadas), artigos de blog (seleção dinâmica real via `blog_content.py`), header/footer (links reais auditados).
- [x] sem placeholders — scan de "exemplo/placeholder/lorem/mock/fake/demo" no HTML renderizado = 0 ocorrências.
- [x] **Fase C.1.1**: agregação dinâmica por idioma continua não existindo no sistema (achado mantido) — mas a curadoria agora vive numa fonte única, testada e versionada (`home_course_collection.py`, `HomeCourseCollection`), não mais 5 blocos inline duplicados no template. Contrato explícito de que é curadoria, não agregação, em `38-home-course-collection-contract.md`. 9 testes novos garantem 5 idiomas ativos, sem duplicação, URLs reais, campos obrigatórios. Regressão confirmada: `Content-Length` de `/_home_v2` idêntico byte-a-byte antes/depois da migração.

### Mídia

- [x] **Resolvido — decisão do responsável pelo projeto (pós Fase C.1.3)**: os 11 assets ativos na Home V2 (e toda a biblioteca `vedium-references/envato-assets/`, não só esses 11) tiveram o uso autorizado explicitamente pelo dono do projeto, que assume a responsabilidade pelo licenciamento. `MEDIA = PASS — USER AUTHORIZED`. Media usage authorized by project owner. Individual license evidence was not independently verified during the redesign workflow. Regras editoriais/culturais continuam valendo integralmente. Ver `37-production-media-readiness.md`.
- [x] **Fase C.1.1**: pipeline de derivados WebP/AVIF gerado com números reais (não estimados) a partir dos mesmos JPEGs em uso — AVIF reduz 64–78%, WebP 38–55%, ambos em `v2-preview-media/{webp,avif}/` (gitignorado, não deployado). Comparação real de vídeo WebM/VP9 também gerada (-20,6% vs. o MP4 atual). Pronto pra aplicar quando os assets finais forem definidos.
- [x] alt — todo `<img>`/`<video>` da Home V2 tem `alt`/contexto real, nenhum genérico vazio.
- [x] crops — `object-position` de cada imagem já validado visualmente em fases anteriores (B.6C/B.6D), preservado sem mudança.

### SEO

- [x] title/description — contrato da rota técnica implementado (noindex); contrato da futura Home real DOCUMENTADO em `28-home-v2-seo-contract.md`, não aplicado à Home pública ainda.
- [x] canonical — **corrigido na raiz na Fase C.1** (não é mais workaround). Investigação completa do core do Frappe (`base_template_page.py`, `set_missing_values()`) confirmou que `context.canonical` é sempre sobrescrito incondicionalmente pelo core; a correção real foi migrar de uma chave ad hoc (`v2_canonical_override`, usada na Fase C) para `context.canonical_url`, a convenção JÁ estabelecida e usada em 144 arquivos do projeto (`curso.py`, `templates/base.html`, etc.), renderizada via `{{ canonical_url }}`. Teste de regressão criado (`test_pure_home_v2.py`). Ver `32-home-v2-prelaunch-qa.md` seção 2 para a investigação completa.
- [ ] **gate aberto**: hreflang — a futura Home real precisa reciprocar com `/en`,`/es`,`/fr`,`/de`,`/ru` exatamente como a Home atual já faz; isso só é implementável no momento da migração real (não em `/_home_v2`, que explicitamente não deve ter hreflang apontando pra si). Revalidado na Fase C.1 a partir do código/dado real (não só do relatório anterior) — tabela completa por locale em `32-home-v2-prelaunch-qa.md` seção 4.
- [x] sitemap — `/_home_v2` confirmado fora do sitemap (`no_sitemap=1`).
- [ ] **gate aberto**: schema — proposta de reaproveitar o JSON-LD real da Home (`EducationalOrganization` etc.) documentada, não implementada em `/_home_v2` (rota noindex, sem ganho de SEO em publicar agora; ver `28-home-v2-seo-contract.md` seção 3).

### Analytics

- [x] GTM — container real `GTM-P6Q2FXLK` adicionado ao footer V2 (gap real encontrado e corrigido nesta fase — não existia antes).
- [x] GA4 — roda via GTM, sem mudança de mecanismo.
- [x] dataLayer — eventos existentes preservados sem renomear; 3 eventos novos (`pathfinder_*`) documentados e testados, não publicados no GTM ainda (gate abaixo).
- [ ] **gate aberto**: configurar tags/triggers pros 3 eventos `pathfinder_*` no container GTM (fora do escopo de código deste repositório — depende de quem administra o GTM).
- [x] WhatsApp — mesmo número/texto/mecanismo; confirmado que a Home V2 NÃO introduz nova duplicação de `public_cta_click`.
- [x] level test — CTA "Faça o teste de nível"/"Descubra seu nível" aponta pra `/teste-de-nivel` real, mesmo contrato dinâmico de override preservado (não usado nesta página, mas a variável continua sendo aceita).
- [ ] **gate aberto**: UTMs — nenhum teste específico de preservação de UTM através da navegação foi feito nesta fase (fora do escopo — nenhuma lógica de UTM existe hoje pra V2 alterar ou quebrar).

### Locale

- [x] desktop — seletor testado (abre/fecha, Esc, clique fora, hrefs corretos).
- [x] mobile — testado em 390px, funcional.
- [x] todas as línguas — 6 locales reais confirmados (pt-br/en/es/fr/de/ru), URLs resolvidas e validadas.
- [x] bandeiras — **requisito aprovado, implementado e testado na Fase C.1**. Botão mostra bandeira+código (ex. 🇧🇷 PT), menu mostra bandeira+nome completo; política de bandeira copiada da real (`vedium-language.js` `localeMeta`), incluindo a decisão deliberada de `en` usar 🌐 (globo) em vez de bandeira de país, para não inferir silenciosamente uma nacionalidade para um idioma falado em múltiplos países. Testado via CDP em estados do header/dropdown; observação de tooling: emoji de bandeira regional não renderiza como glifo colorido em Chrome headless (limitação de fonte do ambiente de teste, não bug de código — o Unicode correto foi confirmado direto no HTML renderizado).

### Performance

- [x] LCP (qualitativo) — Hero slide 1 usa `loading="eager" fetchpriority="high"`; slides 2-4 usam `loading="lazy"` (herdado do macro `v2_hero_editorial_carousel`, não alterado).
- [x] CLS (estrutural) — `width`/`height` explícitos em todas as imagens/vídeo (padrão já estabelecido, preservado).
- [x] JS — nenhum novo script bloqueante adicionado; `vedium-language.min.js` e `design-system-v2.js` continuam `defer`.
- [x] imagens — cards de curso abaixo da dobra usam `loading="lazy"` (padrão já existente nos macros, preservado).
- [x] vídeo — `preload="metadata"`, poster definido, sem autoplay (Live Class, inalterado desde B.6C).
- [ ] **gate aberto**: medição real de LCP/CLS/INP (Lighthouse/CrUX) não foi feita nesta fase — o ambiente de teste (CDP headless local) não reproduz condições de rede/dispositivo reais; medição real exige ambiente de staging com rede real, fora do escopo desta fase de integração funcional.
- [x] **Fase C.1.1**: `V2_FONT_ASSETS_REQUIRED_BEFORE_ROLLOUT` reclassificado como **NON-BLOCKER** — Poppins/Inter são Google Fonts sob SIL OFL 1.1 (licença pública conhecida, sem ambiguidade jurídica), fallback de sistema já confirmado sem CLS perceptível. 3 arquivos (`Poppins-SemiBold/Bold.woff2`, `Inter-Regular.woff2`) seguem pendentes de download manual (não automatizado, por instrução), recomendado antes do lançamento público por consistência de marca, mas não bloqueia o cutover técnico. Ver `40-font-production-readiness.md`.

### Accessibility

- [x] keyboard — locale menu (Esc, foco, clique fora) e Pathfinder (radios nativos) testados via CDP.
- [x] focus — foco retorna ao botão do locale menu ao fechar com Esc.
- [x] headings — único `<h1>` confirmado; hierarquia de headings preservada das fases anteriores (não alterada).
- [ ] **gate aberto**: contraste — reconfirmado nas fases B.6B-B.6E para as áreas então tocadas; não foi re-auditado matematicamente nesta fase (nenhuma cor nova foi introduzida, então o risco é baixo, mas não há novo cálculo formal registrado aqui).
- [x] reduced motion — Hero carousel já respeita `prefers-reduced-motion` (herdado, não alterado; comportamento não re-testado nesta fase especificamente, mas nenhuma mudança de animação foi feita).

### LGPD / Consentimento

- [x] **Fase C.1.3 — resolvido**: as 2 causas identificadas na Fase C.1.2 foram corrigidas e verificadas empiricamente (não só aplicadas): (1) `consent default` agora roda antes do GTM nos 8 pontos reais, sem duplicação (guard testado); (2) banner ganhou "Recusar"/"Gerenciar preferências" com paridade de acesso a "Aceitar", nos 6 locales aprovados. Persistência testada em 6 cenários via CDP (Aceitar/Recusar/Gerenciar/reload/navegação/troca de locale). Basic vs. Advanced permanece uma decisão de configuração do GTM externo (fora do código, ver checklist de ações do GTM em `45-consent-remediation-result.md` seção 9) — não declarado unilateralmente. Link de revogação no Footer fica como proposta documentada, não implementada (mudança visual, aguardando aprovação). Ver `45-consent-remediation-result.md`.

### Rollback

- [x] plano documentado — `/_home_v2` é uma rota adicional, isolada; `/` nunca foi tocada. Rollback = simplesmente não promover a rota (não há redirect criado, não há mudança em `hooks.py`, não há alteração de `website_route_rules`). Reverter esta fase = deletar `www/_home_v2.py`/`.html`, `templates/includes/v2/home_body.html` (revertendo `design_system_v2.html`/`.py` pro estado anterior), `v2_home_data.py`, e as linhas do GTM em `templates/includes/v2/footer.html` — nenhum dado de produção, nenhuma migração de banco, nenhum arquivo compartilhado fora de `v2/`/`docs/redesign/` foi tocado.
- [x] **Fase C.1**: plano de rollback detalhado (2 cenários — antes e depois de um eventual cutover, com arquivos/comandos/tempo estimado/necessidade de migrate-build-restart) documentado em `35-home-v2-rollback-plan.md`. Runbook de troca (para quando o cutover for decidido) documentado em `34-home-v2-rollout-runbook.md` — nenhum dos dois foi executado.
- [x] **Fase C.1.3**: rollback do Consent Mode adicionado a `35-home-v2-rollback-plan.md` — reverter é remover as inclusões de `consent_default.html`/`consent-mode-v2.js` (mecânico, mesmo padrão nos 120 arquivos) e restaurar `cookie-consent.min.js` antigo; nenhum dado de produção foi criado.

## Resumo

**Fase C**: 10 gates abertos. **Fase C.1**: 2 fechados (canonical, bandeiras), 1 novo (LGPD, P1) → 9 abertos. **Fase C.1.1**: 3 dos 4 gates de negócio fecharam de fato (curadoria de curso, fontes, LGPD ready-to-apply), 1 permaneceu aberto por razão administrativa (mídia). **Fase C.1.2**: os 2 gates ainda abertos (MEDIA, CONSENT) chegaram ao máximo de precisão possível sem decisão humana externa. **Fase C.1.3**: CONSENT foi de fato corrigido e verificado empiricamente (autorização explícita desta fase para editar arquivos compartilhados) — vira **PASS**. **Pós-C.1.3**: MEDIA vira **PASS** por decisão explícita do responsável pelo projeto (aceitação de risco documental de licenciamento, biblioteca completa autorizada). **Placar final: 9 PASS / 0 FAIL, GO/NO-GO = GO (cutover controlado, não automático)** — ver veredito consolidado em `46-final-cutover-readiness.md` (substitui `44-`/`41-` como a referência mais atual).
