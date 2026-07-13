# 12 — Runbook de Operação & Deploy

**Verificado:** 2026-07-03. Como fazer deploy, footguns conhecidos, como
investigar produção, como reverter.

## Deploy normal

1. `git push origin main` → GitHub Actions roda **Test and Lint** e
   **Deploy to Production** (ver `.github/workflows/deploy.yml`).
2. Deploy faz `bench --site app.vediums.com migrate` (aplica mudança de
   doctype JSON/schema) **e reinicia o gunicorn automaticamente** — isso
   já foi corrigido (era footgun antigo, exigia restart manual toda vez
   que um `.py` mudava; não é mais o caso).
3. **Test and Lint pode falhar sem travar o Deploy** — os dois workflows
   rodam em paralelo no mesmo push, não em série. Já aconteceu nesta
   sessão: um commit quebrou o Test and Lint (teste órfão sem os dados
   correspondentes) enquanto o Deploy passou normalmente. **Sempre
   conferir os dois** (`gh run list --repo ivonsmatos/vedium --limit 3`)
   depois de um push, não só um.

## Mudanças que NÃO passam pelo deploy normal (cache)

Permissão de doctype (`Custom DocPerm`) e tradução (`Translation`) feitas
direto no banco via `bench execute`/console **não precisam de deploy**,
mas o Frappe cacheia permissão/tradução em Redis — depois de mudar,
`bench --site app.vediums.com clear-cache` (ou aguardar expirar
naturalmente) antes de testar no navegador, senão a sessão antiga
continua vendo o estado velho.

## Investigar produção sem quebrar nada (leitura)

- `bench --site app.vediums.com execute <dotted.path> --args "[...]"` —
  chama uma função Python existente, argumentos posicionais via lista
  JSON. Só serve pra chamar função já existente, não roda script livre.
- `bench --site app.vediums.com console` (via `docker exec -i`, precisa
  do `-i` pra stdin funcionar com heredoc) — REPL Python completo, único
  jeito de rodar lógica arbitrária (múltiplas linhas, `frappe.set_user`
  pra simular outro usuário, etc.) sem criar um script novo no repo.
- Traceback real de erro 500 numa página do LMS: clicar em "Show Error"
  na própria tela (só visível pra quem tem permissão elevada) — mais
  rápido que vasculhar log de container/Error Log, que nem sempre captura
  o erro de front-end.
- `docker logs vedium-frappe --tail N` — tem MUITO ruído de bot
  escaneando `/files/*.7z` etc.; filtrar por `grep -A 40 Traceback` ajuda
  mas nem sempre pega o erro certo (erros de front-end/permissão às vezes
  não aparecem no stdout do container, só no "Show Error" da própria
  página ou no `Error Log` do Frappe).

## Footguns conhecidos

- **Controller `www/<slug>.py` com hífen nunca roda** — Frappe converte
  hífen→underscore na resolução de módulo. Sempre `www/<slug>.py` com
  underscore, mesmo que o `.html`/URL tenha hífen. Falha **silenciosa**
  (página vazia ou 500, sem pista óbvia). Ver [[project_www_controller_underscore]].
- **`bench execute` só serializa o retorno da função** — chamar
  `frappe.get_doc({...})` sozinho via `execute` NÃO insere nada (só
  constrói o objeto em memória e tenta serializar pra imprimir, o que
  pode até dar erro tipo "object is not bound"). Pra inserir/mutar,
  precisa do `console` com `.insert()`/`.save()` explícito.
- **SSH/produção sempre precisa de autorização explícita por ação** — o
  classificador de modo automático deste ambiente NÃO aceita autorização
  genérica ("pode mexer no servidor") pra cobrir ações subsequentes
  distintas; cada escrita nova em produção (mesmo pequena, tipo um
  `Custom DocPerm`) pede confirmação de novo, nomeando a ação específica.
- **Patch manual em arquivo de app instalado (fora do `vedium_core`) não
  é rastreado por git** — o fix do `crm` (`crm/utils/__init__.py`) foi
  editado direto no container. Funciona, mas um futuro `bench update`
  do app `crm` pode sobrescrever sem aviso. Registrar esse tipo de patch
  no [doc 11](11-estado-do-ambiente.md) (checklist vivo) pra não
  esquecer que existe.
- **Commit com múltiplos agentes na mesma árvore (sem isolamento de
  worktree)**: usar `git add <arquivo>` + `git commit <arquivo...>`
  (pathspec explícito), nunca `git add -A`/`git commit -a`, quando há
  outro processo com mudanças não commitadas na mesma árvore — evita
  capturar/misturar trabalho incompleto de outro agente no seu commit.
- **Cloudflare NÃO faz edge-cache do HTML** deste site — `curl
  --resolve vediums.com:443:127.0.0.1` bate direto na origem, então
  `clear-cache` do Frappe já é suficiente pra refletir mudança de tema.
- **`/sw.js` e `/manifest.json` interceptados por alias quebrado do
  nginx** (pasta `/opt/vedium/pwa/` inexistente) — pendência de infra
  registrada em `pendente-pwa-marketing-404.md`, fora do repo de código.

## Rollback

Não há rollback automatizado. Em caso de deploy ruim: `git revert` do
commit problemático + push (dispara novo deploy limpo). Para mudança
feita direto em produção (Custom DocPerm/Translation/patch manual), a
reversão é manual — refazer a ação contrária (ex.: deletar o registro
`Custom DocPerm`/`Translation`, restaurar o arquivo original do app).

## Backup

O host executa `/opt/vedium/scripts/backup.sh` diariamente às 02:00. As
credenciais ficam em `/etc/vedium/backup.env` (modo `0600`), separadas do
`.env` do Docker Compose. O backup Restic inclui o banco do site, o volume
`vedium_frappe-bench-v16`, a configuração de produção e o Nginx.

O repositório local padrão é `/var/backups/vedium-restic`. Ele é criptografado
e permite validar backup/restauração, mas não protege contra perda total do
servidor. Para proteção contra desastre, configure `RESTIC_REPOSITORY` e as
credenciais S3 em `/etc/vedium/backup.env` para Wasabi ou Cloudflare R2.

Comandos operacionais:

```bash
. /etc/vedium/backup.env
/opt/vedium/scripts/restore.sh --list
/opt/vedium/scripts/restore.sh --dry-run
restic check --read-data-subset=5%
```
