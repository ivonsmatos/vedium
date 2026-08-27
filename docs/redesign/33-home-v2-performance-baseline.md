# 33 — Performance baseline da Home V2 (Fase C.1)

## 1. Mídia Envato usada — inventário de produção (seção 12 da missão)

Fonte cruzada: seleção documentada em `21-course-media-selection.md` (B.6C) + `ls -la` real do diretório servido nesta fase.

| Seção | Derivado | Item Envato (master) | Licença | Data de download | Dimensões finais | Formato | Tamanho real | `object-position` (crop) desktop | Crop mobile |
|---|---|---|---|---|---|---|---|---|---|
| Hero slide 1 | `e06-listening-online-course.jpg` | `vedium-references/envato-assets/...` (ver doc 21) | Envato Elements (licença de conta da agência — não redistribuível fora do projeto) | Fase B.3-B.6A (não reconfirmada nesta fase) | 2000×1333 | JPEG | 243.459 bytes | `center` (padrão) | mesmo (sem override mobile específico) |
| Hero slide 2 | `e02-study-laptop.jpg` | idem | idem | idem | 2000×1263 | JPEG | 305.191 bytes | `center` | idem |
| Hero slide 3 | `e10-notes-at-home.jpg` | idem | idem | idem | 2000×1333 | JPEG | 227.096 bytes | `center` | idem |
| Hero slide 4 / B2B home (reused conceptually, different files) | `e07-hero-videoconference.jpg` | idem | idem | idem | 2000×1333 | JPEG | 262.728 bytes | `center` | idem |
| Curso Inglês | `e02-study-laptop.jpg` | (mesmo do Hero slide 2 — reuso documentado desde B.6C) | idem | idem | 2000×1263 | JPEG | 305.191 bytes | `center` | idem |
| Curso Iorubá | `e11-ioruba-learning.jpg` | idem | idem | B.6C (2026-08-25) | 1055×2000 | JPEG | 131.974 bytes | `center 15%` | idem |
| Curso PLE | `e14-ple-headphones-home.jpg` | idem | idem | B.6C | 1125×2000 | JPEG | 213.342 bytes | `center 20%` | idem |
| Curso Espanhol | `e12-espanhol-professora.jpg` | idem | idem | B.6C | 1125×2000 | JPEG | 253.569 bytes | `center 20%` | idem |
| Curso Hebraico | `e13-hebraico-headphones.jpg` | idem | idem | B.6C | 1080×1920 | JPEG | 157.940 bytes | `center` (padrão) | idem |
| B2B (Home) | `e15-b2b-videocall.jpg` | idem | idem | B.6C | 2000×1126 | JPEG | 182.986 bytes | `right center` | idem |
| B2B (página preview) | `e07-hero-videoconference.jpg` | (mesmo do Hero slide 4 — reuso deliberado, ver `24-b2b-v2-page-plan.md`) | idem | idem | 2000×1333 | JPEG | 262.728 bytes | `center` | idem |
| Live Class | `e16-liveclass-teacher.mp4` + poster `e16-liveclass-teacher-poster.jpg` | idem | idem | B.6C | 1280×720 (vídeo) / 1600×900 (poster) | MP4 (H.264) / JPEG | 2.281.136 bytes (vídeo) / 151.364 bytes (poster) | `center` | idem |

**Total de mídia servida pela Home V2**: ~2,4MB de imagens (10 arquivos JPEG) + ~2,28MB de vídeo = **~4,7MB de mídia**, nenhuma copiada pra produção nesta fase (`public/v2-preview-media/` gitignored, confirmado).

### Plano de formato (WebP/AVIF/JPEG fallback) — proposto, não implementado

Nenhuma imagem desta lista tem hoje um `<picture>` com fallback WebP/AVIF — todas são `<img src=".jpg">` direto. **Gate registrado**: antes de copiar qualquer asset final pra produção, gerar variantes WebP (suporte amplo) com fallback JPEG via `<picture><source type="image/webp">...<img></picture>`, e avaliar AVIF caso o ganho de compressão justifique a complexidade extra de build. Não implementado nesta fase — mudaria o pipeline de asset (masters → derivados), que a missão explicitamente pediu para não fazer ainda ("não copiar master desnecessariamente para produção... criar plano", não implementar o pipeline).

## 2. Fontes — pesos reais extraídos do CSS (seção 15 da missão)

**Não assumido** — extraído via grep de todo `font-weight:` literal em `public/css/v2/*.css`:

| Fonte | Pesos usados (confirmados no CSS) | Onde |
|---|---|---|
| Poppins (`--v2-font-heading`) | **600, 700** — nenhum 500 encontrado | Headings, labels, botões, eyebrows em todo o sistema |
| Inter (`--v2-font-body`) | **400 (implícito)** — nenhum `font-weight` explícito encontrado pra texto de corpo; nenhum `<strong>`/`<b>` no HTML da Home V2 (confirmado por grep em `home_body.html`), então 700 não é necessário pro corpo | Parágrafos, listas, texto de apoio |
| Playfair Display (`--v2-font-display`) | 700 (já auto-hospedada localmente desde a Fase B.1 — única fonte com arquivo real no repo) | Não usada na Home V2 atual (era de uma variante de Hero anterior à B.6A) |

**Lista mínima de arquivos necessários antes do rollout** (gate `V2_FONT_ASSETS_REQUIRED_BEFORE_ROLLOUT`, já registrado em `28-home-v2-seo-contract.md`):
- `Poppins-SemiBold.woff2` (600)
- `Poppins-Bold.woff2` (700)
- `Inter-Regular.woff2` (400)

3 arquivos — não 6 como o exemplo ilustrativo da missão sugeria (500/600/700 + 400/500/600). **Não baixado automaticamente nesta fase** (instrução explícita). Fallback atual: Arial/Helvetica Neue via `system` stack — funcional, confirmado visualmente em todas as fases anteriores, mas não é a identidade tipográfica final.

## 3. Hero — performance (seção 13 da missão)

| Item | Estado |
|---|---|
| Imagem inicial (slide 1) | `e06-listening-online-course.jpg`, `loading="eager" fetchpriority="high"` — confirmado no macro `v2_hero_editorial_carousel` (herdado, não alterado) |
| Slides 2-4 | `loading="lazy"` — não competem pelo LCP inicial |
| Preload | Não há `<link rel="preload">` explícito para a imagem do Hero — o `fetchpriority="high"` no próprio `<img>` já sinaliza prioridade ao navegador sem precisar de um preload duplicado (prática atual válida; um `<link rel="preload" as="image">` adicional é redundante quando o elemento já está no HTML inicial com `fetchpriority="high"`) |
| JS de inicialização do carousel | `initHeroCarousel` roda em `DOMContentLoaded` (script `defer`) — não bloqueia o parse do HTML nem o LCP da imagem (que já está no HTML, não depende de JS pra aparecer) |
| CSS | `tokens.css`+`foundations.css`+`components-base.css`+`components-editorial.css`+`header-footer.css` carregados via `<link>` síncrono no `<head>` (bloqueante, padrão) — nenhuma mudança nesta fase |
| CLS do Hero | `width`/`height` explícitos em cada `<img>` do carousel (2000×1333 etc.) — proporção reservada antes da imagem carregar, sem salto de layout |

## 4. Vídeo Live Class (seção 14 da missão)

| Item | Estado |
|---|---|
| Poster | `e16-liveclass-teacher-poster.jpg`, 1600×900, 151.364 bytes — definido via atributo `poster` |
| Preload | `preload="metadata"` (não `auto`, não `none`) — carrega só metadados até o clique de play |
| Controls | `<video controls>` — sem autoplay, comportamento aprovado desde B.6C (vídeo didático, precisa ser assistido de propósito) |
| Filesize | 2.281.136 bytes (~2,3MB) — não otimizado pra streaming adaptativo (sem HLS/DASH), aceitável pra um preview interno, **candidato a revisão antes de produção** (2,3MB num único arquivo MP4 pode ser pesado em mobile com rede ruim) |
| Mobile | Mesmo elemento `<video>`, sem variante mobile-específica de menor bitrate — gate a considerar antes do rollout |
| Reduced motion | Não aplicável diretamente ao vídeo (não faz autoplay, então não há "movimento indesejado" a suprimir) — `prefers-reduced-motion` já é respeitado pelo Hero carousel (Ken Burns/crossfade desligados), não pelo vídeo, que já não se move sozinho |
| Loading | Nenhum `loading="lazy"` no `<video>` (atributo não padronizado/suportado universalmente para `<video>` como é para `<img>`) — mitigado por `preload="metadata"`, que já evita baixar o arquivo inteiro antecipadamente |
| Viewport behavior | `initLiveClassVideo` (JS, herdado de B.6C) pausa o vídeo via `IntersectionObserver` quando sai significativamente da viewport — confirmado presente, não alterado |

## 5. Performance baseline (seção 16 da missão) — medido o que o ambiente permite

**Limitação documentada, não inventado score**: este ambiente é Docker local + Chrome headless via CDP, sem rede real (localhost) — não reproduz condições de usuário real (latência, throttling de CPU/rede real, cache de CDN). **Lighthouse não foi executado** — um score aqui seria artificialmente perfeito (localhost, sem rede) e enganoso. Os números abaixo são medições estruturais reais (tamanho de arquivo, contagem), não métricas de Web Vitals simuladas.

| Métrica | Desktop 1440 | Mobile 390 |
|---|---|---|
| HTML transferido (`/_home_v2`) | ~confirmar via `Content-Length` do response (não capturado em bytes exatos nesta fase — a resposta é gerada dinamicamente, tamanho varia por seleção de blog) | idem |
| CSS (5 arquivos v2) | Mesmo para as duas larguras (arquivos únicos, sem versão mobile separada) | idem |
| JS (2 arquivos: `vedium-language.min.js` + `design-system-v2.js`) | Mesmo para as duas larguras | idem |
| Imagens carregadas na carga inicial (sem scroll) | Hero slide 1 (eager) + o que estiver acima da dobra | Hero slide 1 (eager) — resto lazy |
| Imagens totais na página (lazy incluído) | 10 imagens + 1 vídeo (ver seção 1) | idem |
| Número de requests (estimado) | ~5 CSS + 2 JS + 10 img + 1 vídeo + 1 HTML = ~19 requests de primeira parte (sem contar GTM/GA4, que fazem requests adicionais de terceiros) | idem |
| DOM nodes | Não contado nesta fase (ferramenta de contagem de nós não disponível sem DevTools completo) — **gate aberto**, registrar em fase de staging real |
| CLS observável (manual) | Nenhum salto de layout percebido nos screenshots capturados (`width`/`height` reservados) | idem |
| LCP observável (manual) | Hero slide 1 é o maior elemento above-the-fold; `fetchpriority="high"` + `loading="eager"` já aplicados — sem medição de tempo real (ambiente local não é representativo) | idem |

**Gate aberto explícito**: medição real de LCP/CLS/INP via Lighthouse/CrUX requer ambiente de staging com rede real — fora do escopo desta fase (registrado em `30-home-v2-rollout-gates.md`).
