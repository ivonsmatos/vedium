# Arquitetura de i18n (multi-idioma)

> Leia isto ANTES de traduzir qualquer página. Decisão do usuário (2026-07-02):
> páginas reais pré-renderizadas por idioma, **não** tradução via JS no
> navegador. A tentativa anterior (vedium-language.js reescrevendo o DOM)
> travava o navegador em produção e foi desligada — ver histórico em
> `vedium_core/vedium_core/public/js/vedium-language.js` (função `localizePage`,
> hoje um no-op comentado).

## Por que páginas reais, não JS

- Google indexa o HTML que o servidor manda — JS trocando texto depois do
  carregamento não é visto pelo crawler, então SEO em outro idioma exigia
  conteúdo genuinamente traduzido no HTML.
- JS-translate travava o navegador em páginas com carrossel/grid (isotope.js,
  swiper, owl-carousel competindo pela main thread com a troca de texto).
- Páginas reais = controle editorial de verdade (copy adaptado, não tradução
  palavra-por-palavra) e permite prosa mais rica pra SEO/GEO.

## As 3 famílias de página traduzível

| Família | Template | Onde mora o conteúdo | Como funciona o roteamento |
|---|---|---|---|
| Landing/pilar | `templates/includes/marketing_landing.html` | dict `LANDINGS` em `marketing_landing_content.py` | `www/<lang>/<slug>.html` de 2 linhas: `{% set landing = get_marketing_landing("slug") %}` + include. **NÃO precisa de `.py` funcional** — o `.html` chama `get_marketing_landing()` direto como global do Jinja (registrado em `hooks.py` → `jinja.methods`), ignorando `context.landing` do `.py`. Isso é intencional, mas significa que qualquer dado novo (ex.: grid de cursos) tem que ser calculado DENTRO de `get_marketing_landing()`, nunca em `apply_landing_context()`. |
| Post de blog | `templates/includes/blog_post.html` | dict `BLOG_POSTS` em `blog_content.py` | Rota dinâmica única `/blog/<slug>` (`hooks.py` → `website_route_rules`) — SEM prefixo de idioma na URL. O slug em si já é o idioma (ex.: `yoruba-greetings` vs `saudacoes-em-ioruba`). `www/blog_post.py` lê `frappe.form_dict.get("slug")` e busca em `BLOG_POSTS` — este .py FUNCIONA de verdade (ao contrário do padrão acima), porque o `.html` (`www/blog_post.html`) só faz `{% include "templates/includes/blog_post.html" %}`, sem chamar nenhuma função direto. |
| Curso individual | `www/curso.py` + `www/curso.html` | dict `COURSE_TRANSLATIONS` em `course_translations.py` | Mesmo controller `curso.py` atende `/curso/<slug>` E `/<lang>/curso/<slug>` (rota extra em `hooks.py`). Dentro do `.py`, `frappe.local.path` (SEM barra inicial — `PathResolver.strip("/ ")`) é comparado com `"<lang>/curso/"` pra decidir se sobrepõe `title`/`short_introduction`/`description` com a tradução. Cursos sem entrada em `COURSE_TRANSLATIONS` fazem 301 de volta pro `/curso/<slug>` em vez de 404 ou página fina. |

## Fonte de verdade de cada campo (não adivinhar)

**Nunca invente preço, nível, nome de professor ou contagem de aulas.**
Esses vêm do banco (`LMS Course`) e já aparecem certos na versão em
português — a tradução só troca `title`, `short_introduction`, `description`
(ficha de curso) ou o conteúdo do dict `LANDINGS`/`BLOG_POSTS` (que é
100% texto editorial, sem dado de banco misturado).

## Slugs: não traduza URL literalmente

- Pesquise a palavra-chave real no idioma alvo antes de definir o slug
  (ex.: em inglês não usamos `/en/curso-de-ioruba-online`, usamos
  `/en/learn-yoruba-online` — como um falante nativo buscaria).
- Todo par PT↔idioma precisa de `"alt"` recíproco nos dois dicts
  (`LANDINGS[pt_slug]["alt"]` e `LANDINGS[lang_slug]["alt"]` apontando um pro
  outro) — isso gera as tags `<link rel="alternate" hreflang="...">`
  automaticamente via `get_marketing_landing()`.

## Seletor de idioma (bandeiras no cabeçalho)

`templates/includes/site_navbar.html` calcula, para a página atual, a URL
real em cada idioma (quando existe) e expõe via `data-vd-nav-<lang>-url` no
`<header>`. `public/js/vedium-language.js` lê esses atributos e usa a URL
real em vez de adivinhar por troca de prefixo (bug real corrigido em
2026-07-03 — ver commits `fix(i18n): seletor de idioma...`).

**⚠️ Hoje esse mecanismo só sabe de 2 idiomas (`en_url`/`pt_url`), hardcoded.**
Antes de qualquer agente traduzir pra espanhol/francês/alemão/russo/chinês,
`site_navbar.html` e `vedium-language.js` precisam generalizar pra um mapa
`{lang_code: url}` genérico — sem isso, a bandeira de um idioma novo não vai
saber que aquela URL existe (vai cair no fallback antigo de troca de prefixo,
que 404). **Isso é trabalho de infraestrutura, não de tradução — não faça
isso dentro de um agente de tradução de conteúdo; é uma mudança cross-cutting
que precisa ser feita uma vez só, coordenada.**

## Checklist por página traduzida

1. Conteúdo real (não Google Translate literal — adapte pro público: ex.
   "Study from anywhere in Brazil" virou "Study from anywhere in the world"
   pro público de fora do Brasil).
2. `"alt"` recíproco nos dois idiomas (dict PT + dict do idioma novo).
3. `test_url`/CTA de teste de nível: só existe teste formal para Inglês e
   Português-para-estrangeiros. Outros clusters (ex. Iorubá) usam
   `"test_url": None` — vira botão "falar com a equipe" em vez de link
   pra teste que não existe (não invente teste falso).
4. Rodar a suíte pura antes de comitar:
   `python -m pytest vedium_core/vedium_core/tests/test_pure_marketing_pages.py -q`
5. Adicionar um teste travando o par novo (ver exemplos:
   `test_yoruba_cluster_has_english_pages_with_reciprocal_hreflang`,
   `test_yoruba_blog_cluster_has_english_translations`).
6. Nunca faça `git push` sem confirmação explícita do usuário — cada deploy
   vai pra produção automaticamente via GitHub Actions.

## Onde olhar exemplos já funcionando (inglês)

- Landing: `vedium_core/vedium_core/www/en/learn-yoruba-online.html` +
  entrada `"learn-yoruba-online"` em `LANDINGS`.
- Blog: entrada `"yoruba-greetings"` em `BLOG_POSTS`
  (`vedium_core/vedium_core/blog_content.py`).
- Curso: `course_translations.py` + lógica em `www/curso.py`.
