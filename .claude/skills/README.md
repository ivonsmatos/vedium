# Skills recomendadas (Claude Code) — Vedium

Skills selecionadas do repositório público
[`hcb2019/claude-code-skills`](https://github.com/hcb2019/claude-code-skills)
(20 skills no total) para o contexto deste projeto: app Frappe/ERPNext em
**MariaDB**, conteúdo **PT-BR**, sensível a segurança, com sessões longas de
agente. Ver o QA em `docs/plataforma/18-qa-seguranca-arquitetura.md`.

## Adotar (encaixe direto)

| Skill | Por quê aqui |
|---|---|
| `protetor-git` | Bloqueia comandos git perigosos (empurramos direto pra `main`). |
| `humanizador-pt-br` | Todo o site/blog é PT-BR — tira a "cara de IA" do conteúdo. |
| `melhorar-arquitetura` | Relatórios de arquitetura (casa com o doc 18). |
| `diagnostico` | Debugging sistemático (bugs silenciosos, ex.: funil de leads). |
| `tdd` | Já há `test_pure_*`; formaliza a disciplina. |
| `passar-bastao` | Handoff entre sessões longas (estouram contexto). |
| `modo-caverna` | Economia de token (complementa o RTK). |
| `contexto-em-arquivos` | Engenharia de contexto via filesystem (casa com a memória). |

## Adotar com adaptação
- `setup-pre-commit` — é husky/Prettier (JS). Adaptar para **pre-commit Python**
  (ruff/black + `test_pure_*` + check de CRLF).
- `criar-skill` — para empacotar skills próprias (ex.: uma skill "deploy-vedium").

## Pular
- `postgresql-boas-praticas` — aqui o Frappe roda **MariaDB**, não Postgres.
- `para-prd`, `para-issues`, `triagem`, `fluxo-gsd` — só se adotarem o fluxo GSD.

## Como instalar

Skills vivem em `~/.claude/skills/` (globais, todos os projetos) ou
`.claude/skills/<nome>/SKILL.md` (só este repo). Instale as recomendadas:

```bash
# clona o repo num temp e copia só as skills escolhidas
git clone --depth 1 https://github.com/hcb2019/claude-code-skills /tmp/ccskills
for s in protetor-git humanizador-pt-br melhorar-arquitetura diagnostico \
         tdd passar-bastao modo-caverna contexto-em-arquivos criar-skill; do
  # ajuste o caminho de origem conforme a estrutura do repo (skills/<s> ou <s>)
  cp -r "/tmp/ccskills/$s" ".claude/skills/$s" 2>/dev/null \
    || cp -r "/tmp/ccskills/skills/$s" ".claude/skills/$s"
done
```

Depois reinicie o Claude Code (ou rode `/skills`) para carregá-las. Verifique que
cada pasta tem um `SKILL.md` com frontmatter `name`/`description`.

> ⚠️ Revise o conteúdo de cada skill antes de usar (são de terceiro). Este
> `README.md` é o nosso registro do que foi escolhido e por quê — as skills em si
> não são versionadas aqui até serem copiadas.
