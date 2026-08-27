# 49 — Home V2: hotfix de produção (mídia ausente)

## Causa raiz

`vedium_core/vedium_core/public/v2-preview-media/` (os 11 derivados de mídia
usados pela Home V2: Hero, 5 cards de Cursos, B2B, Live Class vídeo+poster)
nunca foi versionada no Git — estava listada apenas em `.git/info/exclude`
(exclusão local, não `.gitignore`) desde a Fase C. Enquanto a Home V2 vivia
só em `/_home_v2` (rota técnica, não indexada, não linkada), isso não tinha
efeito visível em produção.

A Fase C.1.4 ("Controlled Home Cutover") tornou `/` a implementação real da
Home V2, reutilizando os mesmos paths de mídia. O deploy (`deploy.yml`) usa
`rsync` a partir da árvore do Git — como a pasta nunca foi commitada, o
`rsync` nunca a sincronizou pro servidor. Resultado: pós-deploy, os 11 assets
retornavam HTTP 404 em `https://vediums.com/` (Hero sem imagem, 5 cards de
Cursos quebrados, B2B quebrado, Live Class com player preto). Achado via
smoke test próprio, pós-deploy, não reportado pelo usuário.

## Fix

Novo diretório de produção definitivo, versionado no Git:

```
vedium_core/vedium_core/public/v2/media/home/
```

servido em `/assets/vedium_core/v2/media/home/`. Os 11 arquivos foram
copiados **byte-idênticos** (mesmo tamanho, sem reencode/resize/recrop) da
pasta antiga `v2-preview-media/` (que permanece intocada, ainda
`.git/info/exclude`-only, não é mais referenciada por nenhum código). Os
masters em `vedium-references/envato-assets/` não foram tocados nem
commitados.

### Os 11 arquivos

| # | Arquivo | Bytes |
|---|---|---|
| 1 | `e02-study-laptop.jpg` | 305191 |
| 2 | `e06-listening-online-course.jpg` | 243459 |
| 3 | `e07-hero-videoconference.jpg` | 262728 |
| 4 | `e10-notes-at-home.jpg` | 227096 |
| 5 | `e11-ioruba-learning.jpg` | 131974 |
| 6 | `e12-espanhol-professora.jpg` | 253569 |
| 7 | `e13-hebraico-headphones.jpg` | 157940 |
| 8 | `e14-ple-headphones-home.jpg` | 213342 |
| 9 | `e15-b2b-videocall.jpg` | 182986 |
| 10 | `e16-liveclass-teacher.mp4` | 2281136 |
| 11 | `e16-liveclass-teacher-poster.jpg` | 151364 |

Nenhum arquivo "impróprio pra web" — o maior é o MP4 (2.28 MB), já aceito
como adequado desde a Fase C (docs/redesign/33).

### Path antigo → novo

`/assets/vedium_core/v2-preview-media/<arquivo>` →
`/assets/vedium_core/v2/media/home/<arquivo>`

### Referências de código corrigidas (6 arquivos, 25 ocorrências)

- `vedium_core/vedium_core/templates/includes/v2/home_page_content.html` (11) — partial real da Home (`/` e `/_home_v2`)
- `vedium_core/vedium_core/home_course_collection.py` (constante `V2_PREVIEW_MEDIA_BASE` renomeada para `V2_HOME_MEDIA_BASE`)
- `vedium_core/vedium_core/templates/includes/v2/header.html` (1) — mega-menu Cursos, também estava 404 em produção (achado durante o hotfix, não reportado antes)
- `vedium_core/vedium_core/www/design_system_v2.html` (11) — ferramenta interna de preview, não crítico pra produção mas corrigido por consistência
- `vedium_core/vedium_core/www/design_system_v2_b2b.html` (1) — idem
- `vedium_core/vedium_core/tests/test_pure_home_course_collection.py` — assertion de `media_src` atualizada; novo teste `test_home_media_directory_has_all_referenced_files_committed` adicionado como guarda de regressão (falha se os arquivos referenciados em `media_key` não existirem em disco ou se o diretório `public/v2/media/home` for adicionado ao `.gitignore`)

### Fora do escopo (não alterado)

Layout, copy, Hero (estrutura/slider/Ken Burns), Header, seleção de idioma,
Pathfinder, seção Cursos, Consent Mode, analytics, CTA, Footer, seção B2B,
SEO, WebMCP — nenhum desses foi tocado. Apenas os paths de mídia e a
constante que os gera.

## Verificação local (pré-push)

`flake8` limpo, suíte pytest completa: **364 passed, 11 skipped, 0 failed**
(inclui o novo teste de regressão).

### Tabela HTTP dos 11 assets (local, `http://127.0.0.1:8005`, `Host: vedium.local`)

| Asset | HTTP | Content-Type | Bytes | Resultado |
|---|---|---|---|---|
| e02-study-laptop.jpg | 200 | image/jpeg | 305191 | PASS |
| e06-listening-online-course.jpg | 200 | image/jpeg | 243459 | PASS |
| e07-hero-videoconference.jpg | 200 | image/jpeg | 262728 | PASS |
| e10-notes-at-home.jpg | 200 | image/jpeg | 227096 | PASS |
| e11-ioruba-learning.jpg | 200 | image/jpeg | 131974 | PASS |
| e12-espanhol-professora.jpg | 200 | image/jpeg | 253569 | PASS |
| e13-hebraico-headphones.jpg | 200 | image/jpeg | 157940 | PASS |
| e14-ple-headphones-home.jpg | 200 | image/jpeg | 213342 | PASS |
| e15-b2b-videocall.jpg | 200 | image/jpeg | 182986 | PASS |
| e16-liveclass-teacher.mp4 | 200 | video/mp4 | 2281136 | PASS |
| e16-liveclass-teacher-poster.jpg | 200 | image/jpeg | 151364 | PASS |

### Retest visual local da Home (`/`, via CDP/Chrome headless)

- Hero: 4 imagens de slide carregadas (`complete: true`, `naturalWidth: 2000`)
- Cursos: 5 imagens presentes e carregadas após scroll (lazy-load confirmado, sem 404)
- B2B: imagem presente e carregada
- Live Class: `<video>` com `src`/`poster` corretos, `readyState: 4` (pronto pra reproduzir)
- Sweep de rede completo (scroll até o fim da página): 48 requisições, **0 erros >=400**, `brokenImgs: []`

### Smoke SEO/Consent local (leve, não repete a auditoria completa)

- `/` → HTTP 200
- `robots`: `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` (indexável, sem regressão)
- `canonical_url` presente e resolvido
- Consent Mode default dispara antes do `gtm.js` (confirmado por posição no HTML)
- Partial `home_page_content.html` presente (`v2-scope`) — confirma que a Home real continua servida pela V2

## Produção (pós-push/deploy)

_Preenchido após o deploy via GitHub Actions e o smoke test em
`https://vediums.com/` — ver commit de acompanhamento (docs-only) que
atualiza esta seção._

- Commit do hotfix: `PENDENTE`
- Deploy (`deploy.yml`): `PENDENTE`
- Rollback usado: `PENDENTE`
