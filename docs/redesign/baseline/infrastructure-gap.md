# Baseline de Infraestrutura — divergências entre documentação, deploy e produção

> **Fase A (baseline técnico) — 2026-08-24.** Documento read-only. Nenhuma configuração foi alterada. Cruza achados desta sessão (código + `.github/workflows/deploy.yml`, executado nesta mesma sessão para a missão PLE) com o audit paralelo já existente em `docs/redesign/01-current-stack-audit.md` (mesma data), que é tratado aqui como fonte primária pra tudo que envolve acesso a produção que esta Fase A não repetiu.

## Fonte de verdade confirmada

- **`vediums.com`**: CONFIRMADO NO CÓDIGO E EM PRODUÇÃO — é a mesma aplicação Frappe/ERPNext que serve `app.vediums.com`. A home respondeu `200` com cookies de sessão Frappe (`sid=Guest`) e conteúdo vindo do LMS (`docs/redesign/01-current-stack-audit.md:24`). Os controllers `www/*.py` deste repositório (`vedium_core`) só funcionam se o request chegar ao backend Frappe — o que descarta qualquer hipótese de site estático servido direto por Nginx.
- **`app.vediums.com`**: CONFIRMADO NO CÓDIGO — Frappe LMS nativo (app `lms` + `vedium_core` instalados no mesmo site Frappe). Destino de login, registro, checkout e acesso a curso.
- **Deploy pipeline (CONFIRMADO NESTA SESSÃO, executado ao vivo em 2026-08-23 pra outra tarefa)**: `.github/workflows/deploy.yml` dispara em `push` para `main`; via SSH, faz `docker cp` do código pro container `vedium-frappe`, `bench migrate`, `bench build` (não-crítico), `bench clear-cache`, **`docker restart vedium-frappe`** (obrigatório — gunicorn não recarrega `.py` sozinho) e depois reinicia os workers de fila (`vedium-worker-short/long/default`, `vedium-scheduler`) com healthcheck próprio. Mudança só em `.html` não exige restart (sync + clear-cache bastam); mudança em `.py` exige.

## Código legado (não é mais fonte de verdade)

| Item | Situação |
|---|---|
| `deploy/nginx/vediums.com.conf` | Descreve `vediums.com` como site ESTÁTICO (`root /opt/vedium/site; try_files ...`) — **incompatível** com a existência dos controllers `www/*.py` Frappe confirmados em produção. Tratar como hipótese desatualizada, não config ativa. |
| `deploy/vediums.com.nginx` | Versão alternativa/mais antiga, com blocos DIFERENTES do arquivo acima (não tem os atalhos `/app`, `/login`, `/cursos`, `/lms` que o outro tem) — os dois arquivos já divergem **entre si**, sinal de que nenhum dos dois é mantido ativamente. |
| README / fluxo de publicação estática legado | Mencionado em `docs/redesign/01-current-stack-audit.md:166` como parte do "caminho de build/publicação" documentado mas não reconciliado com o deploy real via Docker/GitHub Actions. |

## Deploy — o que a documentação diz

- `docs/ARCHITECTURE.md:85` (citado pelo agente de redirects): `vediums.com` = "marketing + páginas SEO (Frappe via host-rewrite no nginx)".
- Memória de projeto (sessões anteriores) confirma: **"o Host-rewrite (nginx força Host `app.vediums.com` p/ vediums.com) faz o navegador mandar Origin/Referer `vediums.com` mas o Frappe se ver como `app.vediums.com`"** — mecanismo já causou um incidente real em produção (LMS quebrando com POST 404, resolvido em 2026-06-02 apontando os links de plataforma para o host nativo `app.vediums.com`).
- `docs/plataforma/pendente-pwa-marketing-404.md` e `scripts/migrations/oneshot/fix_nginx_pwa.py` confirmam, por evidência indireta, que o Nginx real em produção faz `proxy_pass` pro Frappe (127.0.0.1:8005) em vez de servir arquivos estáticos — reforça que os 2 arquivos `deploy/nginx/*` versionados não são a config ativa.

## Produção — o que foi efetivamente verificado

Nesta Fase A (2026-08-24), via HTTP:
- **336/336 URLs do sitemap.xml responderam HTTP 200 direto** (`--max-redirs 0`, sem nenhum redirect intermediário) — verificado em lote.
- `robots.txt` responde 200, com `Allow: /` geral e permissões explícitas para crawlers de IA (GPTBot, ChatGPT-User, CCBot, anthropic-ai, Claude-Web, Google-Extended) além do `Sitemap:` apontando pro `sitemap.xml` real.
- Amostra de 66 URLs (todas as famílias × todos os locales, ao menos 1x) teve título/meta/canonical/H1/hreflang/schema extraídos com sucesso — ver `seo-snapshot.csv`.

Não foi feito, nesta Fase A: acesso SSH ao servidor, export da config Nginx ativa, inspeção de containers Docker, nem consulta ao Search Console/GA4 (ver `baseline-summary.md`, seção "exige acesso externo").

## Divergências

| Documentação | Código | Produção | Risco | Decisão recomendada futura |
|---|---|---|---|---|
| `docs/ARCHITECTURE.md` descreve host-rewrite Nginx pra unificar vediums.com↔app.vediums.com | `website_route_rules`/`website_redirects` (hooks.py) não têm regra equivalente — o mecanismo não está neste app | Comportamento observado (both hosts servidos pela mesma app Frappe) é consistente com a documentação | **ALTO** — mecanismo crítico para o funcionamento do site inteiro vive **fora do Git**, só no servidor (`/etc/nginx/sites-available/vediums.com`) | Exportar a config Nginx ativa do servidor pro repositório ANTES de qualquer corte de tráfego do redesign; sem isso, um novo deploy de infraestrutura pode reintroduzir o incidente de LMS quebrado já documentado em memória de projeto (2026-06-02) |
| Nenhum documento afirma normativamente a regra `www.vediums.com → vediums.com` | `website_redirects` (Frappe) não tem essa regra | CONFIRMADO EM PRODUÇÃO: `www.vediums.com/*` responde 301 pro host sem `www` (`docs/redesign/01-current-stack-audit.md:24`) | MÉDIO | Camada exata (Nginx vs Cloudflare/edge) não comprovada — descobrir antes de qualquer migração de DNS/CDN no redesign |
| `deploy/nginx/vediums.com.conf` tem `location /cursos → return 301 app.vediums.com/lms/courses` | `hooks.py:266` trata `/cursos` como alias interno pro catálogo institucional (`/cursos-de-idiomas-online`), resposta 200 | Sitemap não inclui `/cursos` (correto, é alias não-canônico); comportamento real não testado nesta Fase A especificamente pra essa URL | MÉDIO — **CONFLITO POTENCIAL**: se o bloco Nginx versionado algum dia for aplicado como está, ele intercepta `/cursos` ANTES do Frappe e manda pro LMS, quebrando o alias institucional que o código espera | Não aplicar `deploy/nginx/vediums.com.conf` como está sem reconciliar essa rota primeiro |
| `www/pratica_diaria.py:12-13` — controller redireciona por Host header pra `app.vediums.com/pratica-diaria` | Redirect condicional confirmado no código-fonte | `docs/redesign/01-current-stack-audit.md:164` registra produção observada = **200, sem redirecionar** | **ALTO** | Investigar causa raiz (provável: o Host header que chega no controller já foi reescrito pelo proxy antes de alcançar o Python, então a condição `Host == vediums.com` nunca bate) antes de decidir se a página `/pratica-diaria` fica no site institucional ou migra de vez pro LMS |
| `/manifest.json`, `/sw.js` | `website_route_rules` encaminha pro handler Frappe (criado especificamente pra contornar um alias Nginx antigo quebrado, `/opt/vedium/pwa/manifest.json`, pasta inexistente) | Ambos respondem 200 hoje | BAIXO (drift já contornado) | Não remover a route rule nem "corrigir" o Nginx nesta fase — o contorno está funcionando |
| PWA / Service Worker | `web_include_js` registra `pwa-register.min.js` em toda página | Comportamento de cache do SW restrito a `vediums.com/www`, ignorando `/api`, `/app`, `/lms`, `/login`, checkout (ver comentário em `hooks.py`) | NÃO CONFIRMADO nesta Fase A se o SW real em produção respeita esses limites | BAIXO-MÉDIO | Testar registro do SW em produção antes do redesign alterar `/sw.js` |

## Nota sobre `.claude/worktrees/` e outras branches

Esta sessão encontrou, no repositório local, worktrees e branches de outras tarefas em andamento (ex.: `agent/stripe-recurring-phase4-hardening`, branches de catálogo Stripe). Não fazem parte do escopo desta Fase A e não foram tocados. Cross-checado apenas para não confundir código de outra tarefa com o estado real de `vedium_core` na branch `redesign/vedium-v2`.
