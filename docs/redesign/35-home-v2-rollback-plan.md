# 35 — Plano de rollback (Fase C.1, atualizado nas Fases C.1.1/C.1.2/C.1.3)

> **NÃO EXECUTAR.** Plano documentado para três cenários: (A) rollback da fase atual (Home V2 nunca chegou a substituir `/`), (B) rollback pós-cutover (Home V2 já substituiu `/` e precisa voltar atrás), e (C) rollback específico do Consent Mode (Fase C.1.3 — toca produção real, independente de `/_home_v2`).

## Cenário A — Reverter esta fase (mais simples, mais provável de precisar antes do cutover)

`/` nunca foi tocada nesta fase — reverter significa só remover a rota paralela.

### Arquivos afetados

| Arquivo | Ação de rollback |
|---|---|
| `vedium_core/vedium_core/www/_home_v2.py` | Deletar |
| `vedium_core/vedium_core/www/_home_v2.html` | Deletar |
| `vedium_core/vedium_core/templates/includes/v2/home_body.html` | Deletar |
| `vedium_core/vedium_core/v2_home_data.py` | Deletar |
| `vedium_core/vedium_core/home_course_collection.py` | Deletar (Fase C.1.1) |
| `vedium_core/vedium_core/public/js/v2/consent-mode-v2.js` | **Atenção Fase C.1.3**: este arquivo foi cableado em produção real (ver Cenário C abaixo) — deletá-lo sem também reverter as 120 referências quebraria o carregamento de script em produção. Não faz parte do escopo de "reverter só a Home V2". |
| `.gitignore` (linha `vedium-references/`, Fase C.1.2) | Reverter só se necessário — é proteção pura, sem efeito em runtime; não há necessidade real de desfazer |
| `vedium-references/licenses/envato/` | Fora do controle de versão, nada a reverter no Git |
| `vedium_core/vedium_core/www/design_system_v2.py` | Reverter pro estado anterior à Fase C (remove import/uso de `v2_home_data`) |
| `vedium_core/vedium_core/www/design_system_v2.html` | Reverter pro estado anterior à Fase C (remove `{% include home_body.html %}`, volta às 7 seções inline) |
| `vedium_core/vedium_core/templates/includes/v2/footer.html` | Remover as ~10 linhas do snippet GTM (volta a não carregar GTM nas páginas V2) |
| `vedium_core/vedium_core/templates/includes/v2/header.html` | Reverter as bandeiras (Fase C.1) e, se necessário, o locale menu inteiro (Fase B.6E) |
| `vedium_core/vedium_core/public/js/v2/design-system-v2.js` | Remover `initPathfinderRouting`/`PATHFINDER_MATRIX` (Fase C.1/C) |
| `vedium_core/vedium_core/tests/test_pure_home_v2.py` | Deletar |
| `docs/redesign/26-*.md` até `36-*.md` | Manter (documentação histórica não atrapalha nada estando presente) ou remover, à critério |

### Comandos

```bash
git log --oneline  # identificar o(s) commit(s) desta fase, se já commitados
git revert <commit-da-fase-C> <commit-da-fase-C.1>  # ou reset se ainda local/não pusheado
```

Ou, se as mudanças ainda não foram commitadas: `git checkout -- <arquivos modificados>` + `rm <arquivos novos>` (usar `git status` pra confirmar a lista exata antes).

### Tempo estimado

< 5 minutos (é remoção/reversão de arquivo, sem dado de produção envolvido).

### Necessidade de migrate/build/restart

- **Migrate**: não — nenhuma mudança de schema/DocType foi feita.
- **Build**: não — nenhum asset compilado (JS/CSS são servidos diretos, sem bundler nesta parte do V2).
- **Restart**: **sim, do processo Python** (`bench restart` ou reiniciar `web.1` do `bench start`) — achado real desta sessão: mudanças em `.py` exigem reinício pra recarregar o módulo já importado; `clear-cache` sozinho não basta.
- **Cache**: `bench --site <site> clear-cache` depois do restart.
- **Nginx**: não aplicável (nenhuma mudança de configuração de proxy foi feita nesta fase).

### Validação pós-rollback

1. `curl -I http://<site>/` → 200, comportamento idêntico ao de antes da Fase C.
2. `curl -I http://<site>/_home_v2` → 404 (rota não existe mais).
3. `curl -I http://<site>/design_system_v2` → 200, com o conteúdo curado original (3 artigos hardcoded, não os dinâmicos).
4. Rodar a suíte de testes: `pytest apps/vedium_core` — deve voltar ao piso de 326 (Fase B.6E) já que os 7+ testes novos de `test_pure_home_v2.py` também são removidos.

## Cenário B — Reverter pós-cutover (Home V2 já é `/`)

Mais crítico — a Home V2 já está recebendo tráfego real.

### Passos

1. Reverter o passo "DEPLOY" do runbook (`34-home-v2-rollout-runbook.md`): restaurar `www/index.py`/`.html` (e as 5 variantes de idioma, se tocadas) a partir do backup de arquivo feito no PRE-FLIGHT, ou via `git revert` do commit de cutover.
2. Restaurar `robots`/`canonical`/`no_sitemap` da Home real.
3. `bench restart` (processo Python) + `clear-cache`.
4. Invalidar cache de CDN/proxy se aplicável.
5. Confirmar via smoke test (mesmo checklist do runbook, seção SMOKE TEST) que `/` voltou ao comportamento anterior.
6. Notificar Search Console se o cutover já tinha sido indexado (evitar sinal confuso de "página mudou de novo" repetidamente).

### Tempo estimado

15-30 minutos (mais checklist de validação do que trabalho técnico em si, assumindo backup de arquivo/commit limpo disponível).

### Dado gerado durante o período com Home V2 ativa

Nenhum dado de usuário é perdido no rollback — a Home V2 não introduz nenhuma tabela/DocType nova, nenhum formulário próprio (os CTAs levam pra formulários REAIS já existentes, como `/contato`/`/empresas`, que continuam intactos independente de qual Home estava ativa). Leads gerados durante o período continuam no CRM normalmente.

## Cenário C — Reverter o Consent Mode (Fase C.1.3)

Independente dos cenários A/B: o Consent Mode toca produção real hoje (`/`, `/contato`, todas as ~120 páginas), não só a rota `/_home_v2`. Reverter isso é uma operação separada.

### Arquivos afetados

| Arquivo | Ação de rollback |
|---|---|
| `vedium_core/vedium_core/templates/includes/consent_default.html` | Deletar |
| `vedium_core/vedium_core/www/index.html`, `en/es/de/fr/ru/index.html`, `curso.html` | Remover a linha `{% include "templates/includes/consent_default.html" %}` antes do bloco GTM (7 arquivos) |
| `vedium_core/vedium_core/templates/includes/site_footer.html` | Remover a mesma linha antes do bloco GTM do rodapé |
| **120 arquivos `www/*.html`/`templates/includes/*.html`** | Remover a linha `<script defer src=".../consent-mode-v2.js?v=c1-3"></script>` inserida logo após `cookie-consent.min.js` (mecânico, mesmo padrão reproduzível via busca por essa string) |
| `vedium_core/vedium_core/public/js/cookie-consent.js` | Reverter pro estado anterior à Fase C.1.3 (só botão "Aceitar", sem Recusar/Gerenciar preferências) — versão anterior recuperável via `git log`/`git show` |
| `vedium_core/vedium_core/public/js/cookie-consent.min.js` | Regenerar via `terser` a partir do `.js` revertido, ou restaurar a versão anterior do Git |
| `vedium_core/vedium_core/public/js/v2/consent-mode-v2.js` | Reverter pro estado da Fase C.1.2 (sem `applyGranularPreferences`/guard de duplicação) ou deletar, já que sem os 120 includes ele para de ser referenciado |
| `vedium_core/vedium_core/hooks.py` | Reverter o comentário/versão de cache-bust em `web_include_js` |
| Query strings de cache-bust (`?v=c1-3-consent-banner`) | Reverter para `?v=mobile-pwa-fix` nos mesmos 120 arquivos, OU manter uma versão nova ao reverter o conteúdo (evita servir conteúdo antigo com cache do novo) |

### Comandos

```bash
git diff --stat HEAD -- 'vedium_core/vedium_core/www/*.html' 'vedium_core/vedium_core/templates/includes/*.html'
# lista exata dos 120+ arquivos tocados nesta fase, pra reverter em lote:
git checkout -- <lista de arquivos>  # se ainda não commitado
```

### Tempo estimado

5-10 minutos (reversão mecânica via Git, já que são inserções de 1-2 linhas por arquivo, sem lógica condicional a desfazer manualmente).

### Necessidade de restart

**Sim** — mudanças em `.html`/`.js` servidos como assets estáticos precisam de `bench --site <site> clear-cache` (cache de página) e, se algum `.py` foi tocado no processo de reversão, restart do processo `bench serve`/`bench start`.

### Validação pós-rollback

1. `curl -I http://<site>/` → 200.
2. Verificar visualmente que a barra de cookies voltou a mostrar só "Aceitar" (sem Recusar/Gerenciar).
3. `window.dataLayer` não deve mais ter uma entrada `consent`/`default` antes do GTM (comportamento revertido pro estado da Fase C.1.2).
4. Rodar a suíte de testes — os 18 testes de `test_pure_consent_mode_v2.py` seriam removidos/revertidos junto.
