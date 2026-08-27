# 34 — Runbook de troca de `/` pela Home V2 (Fase C.1, atualizado nas Fases C.1.1/C.1.2/C.1.3)

> **NÃO EXECUTAR.** Este é o roteiro para quando (e se) a decisão humana de promover `/_home_v2` a `/` for tomada. Nenhum passo abaixo foi rodado nesta fase.

## PRE-FLIGHT

1. Confirmar todos os gates P0 de `30-home-v2-rollout-gates.md` resolvidos (nenhum `[ ]` crítico aberto).
2. ~~Confirmar licenciamento final da mídia via certificados individuais~~ — **resolvido pós-Fase C.1.3**: uso da biblioteca `vedium-references/envato-assets/` autorizado explicitamente pelo responsável pelo projeto, que assume a responsabilidade pelo licenciamento (`37-production-media-readiness.md`). `42-envato-license-evidence-checklist.md` permanece como referência, não como pré-condição.
3. ~~Confirmar fontes Poppins/Inter auto-hospedadas localmente~~ — reclassificado NON-BLOCKER na Fase C.1.1 (`40-font-production-readiness.md`); recomendado mas não impede o cutover.
4. Decidir conscientemente a questão do H1 (visível na V2 vs. oculto na Home atual — `32-home-v2-prelaunch-qa.md` seção 2).
5. Configurar no GTM as 3 tags/triggers para `pathfinder_language_select`/`pathfinder_goal_select`/`pathfinder_submit` (contrato em `29-home-v2-analytics-contract.md`); aproveitar pra confirmar Basic vs. Advanced Consent Mode nas tags do GA4/Ads (checklist em `45-consent-remediation-result.md` seção 9).
6. ~~Aplicar o Google Consent Mode v2~~ — **feito e verificado na Fase C.1.3** (`45-consent-remediation-result.md`): ordem `default`→GTM corrigida nos 8 pontos reais, banner com Aceitar/Recusar/Gerenciar preferências nos 6 locales, persistência testada. Decisão pendente, não bloqueante: link de revogação no Footer (proposta parada aguardando aprovação, doc 45 seção 7).
7. Congelar o conteúdo dinâmico da Home V2 no momento da troca (capturar snapshot da seleção de blog vigente, para conferência pós-troca).

## BACKUP

1. Snapshot do banco de dados (backup padrão do site, `bench backup --with-files`) — mesmo sem esta fase alterar schema, qualquer operação de produção deveria ter backup prévio por disciplina padrão.
2. Cópia do `index.py`/`index.html` atuais (e das 5 variantes de idioma) para um local versionado fora do caminho ativo (ex. branch/tag `pre-home-v2-cutover`), para rollback rápido de arquivo sem depender só do histórico Git.
3. Registro do hash MD5 do Hero renderizado da Home V2 no momento da promoção (mesma técnica já usada nesta sessão) — referência de "estado aprovado no momento do cutover".

## DEPLOY

1. **Opção A (recomendada, menor risco)**: renomear os arquivos — `www/index.py`/`.html` viram `www/_index_legacy.py`/`.html` (ou movidos para uma pasta de arquivo morto fora de `www/`, já que Frappe rotearia qualquer arquivo em `www/` automaticamente); `www/_home_v2.py`/`.html` viram `www/index.py`/`.html`. Isso preserva a URL `/` apontando para o conteúdo novo sem precisar de `website_route_rules`.
2. **Opção B (mais reversível, mais complexa)**: manter os dois arquivos, adicionar uma `website_route_rule` em `hooks.py` redirecionando `/` para o controller novo condicionalmente (ex. por feature flag em `site_config.json`) — permite rollback instantâneo trocando a flag, sem mexer em arquivo. Mais complexo de implementar corretamente; avaliar se vale a pena versus a Opção A + rollback por reversão de commit.
3. Atualizar `robots`/`no_sitemap` do controller promovido para os valores REAIS da Home (remover `noindex`, remover `no_sitemap=1`, aplicar os valores documentados em `28-home-v2-seo-contract.md` seção 2).
4. Aplicar `canonical_url` real (auto-referencial a `/`, como a Home atual já faz).
5. Remover o banner de dev-tool (`.dstool-banner`) do template promovido — não faz sentido em produção.
6. Adicionar hreflang recíproco real (mesmo padrão de `de/en/es/fr/pt-br/x-default` já usado — decidir separadamente se `ru` entra ou não, dado o achado da seção 2 do doc 32).

## CACHE CLEAR

1. `bench --site <site> clear-cache` (cache de página/contexto do Frappe).
2. `bench --site <site> clear-website-cache` se disponível separadamente.
3. Reiniciar o processo web (`bench restart` ou equivalente de produção — **achado real desta sessão**: mudanças em arquivo `.py` de controller exigem reinício do processo Python, `clear-cache` sozinho não recarrega o módulo já importado).
4. Invalidar cache de CDN/proxy reverso se houver um na frente de produção (Nginx com cache de página, Cloudflare, etc. — verificar antes; memória do projeto indica que Cloudflare **não** faz edge-cache do HTML deste site hoje, mas confirmar não custa).

## SMOKE TEST

1. `curl -I https://vediums.com/` → 200.
2. Verificar visualmente Hero, Pathfinder, Cursos, Live Class, B2B, Insights, CTA, Footer em 1440 e 390px.
3. Testar Pathfinder de ponta a ponta (submissão real, confirmar redirecionamento).
4. Testar o locale switcher pros 6 idiomas reais.
5. Clicar em pelo menos 1 CTA de cada seção e confirmar destino real.

## SEO CHECK

1. Confirmar `<title>`/`description`/`canonical`/`robots`/`hreflang`/JSON-LD com os valores do contrato (`28-home-v2-seo-contract.md`).
2. Submeter a URL pro Google Search Console pra recrawl manual (não esperar o crawl orgânico).
3. Monitorar Search Console por 48-72h por quedas de impressão/clique anormais.

## ANALYTICS CHECK

1. Confirmar GTM carregando (1 container, sem duplicação de `<noscript>` — a V2 já corrige o bug de duplicação da Home atual, ver `29-home-v2-analytics-contract.md`).
2. Confirmar GA4 recebendo pageview real (GTM Preview mode ou GA4 DebugView).
3. Confirmar WhatsApp disparando `public_cta_click` uma única vez por clique (não duas).
4. Confirmar as 3 tags novas do Pathfinder disparando (se já configuradas no GTM).

## LOCALE CHECK

1. Testar cada um dos 6 locales reais a partir da Home recém-promovida.
2. Confirmar que o locale ativo é detectado corretamente.
3. Confirmar hreflang recíproco nas páginas de destino.

## ROLLBACK DECISION

Critério objetivo pra decidir rollback nas primeiras 24-72h:
- Erro 500 recorrente na Home.
- Queda abrupta (>30%) de tráfego orgânico não explicada por sazonalidade.
- Quebra confirmada de conversão (CTA de teste de nível, matrícula, ou B2B parando de funcionar).
- Duplicação de evento de analytics inflando métricas de forma enganosa pra decisões de negócio.

Se qualquer critério acima for atingido: seguir `35-home-v2-rollback-plan.md` imediatamente, sem esperar diagnóstico completo da causa raiz primeiro (reverter, depois investigar com calma).
