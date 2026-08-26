# 21 — Seleção de mídia para os 5 cursos + Aula ao vivo (Fase B.6C)

> **Origem**: a missão exigiu que os 5 idiomas de Cursos deixassem de ter blocos só de cor — "TODOS OS CINCO IDIOMAS DEVEM TER MÍDIA VISUAL" — e que "Aulas ao vivo, na prática" ganhasse vídeo real da biblioteca. Auditoria recursiva de `vedium-references/envato-assets/` (52 arquivos: 23 imagens/PNGs + 29 vídeos), com inspeção visual real de cada candidato considerado — nunca decisão só pelo nome do arquivo. Inventário completo em `07-envato-asset-inventory.csv` (18 linhas: E01-E18); mapa de página em `08-page-media-map.md`.
>
> **Atualização B.6D** (`22-density-and-transition-refinement.md`): as 5 seleções de mídia desta fase (imagens/crop/`object-position`) foram **mantidas sem troca**, conforme pedido explícito da missão B.6D — a única mudança nos blocos de curso foi tipografia (índice/nível/headline/texto aumentados) e espaçamento entre blocos (reduzido). Nenhuma linha da tabela abaixo mudou.

## 1. Tabela final — o que foi escolhido e por quê

| Idioma | Asset selecionado (CSV) | Por que foi escolhido | O que comunica | O que NÃO deve ser inferido | Crop | Substituição futura |
|---|---|---|---|---|---|---|
| **Inglês** | E02 — `arab-student-guy-learning-online-at-laptop-sitting...jpg` (já era o master de `e02-study-laptop.jpg`) | Mantido — mission autorizou explicitamente ("pode permanecer se continuar sendo a melhor opção"); já usado como Inglês desde fases anteriores. | Adulto concentrado, fones, notebook, caderno — estudo online. | Que a pessoa é professor ou aluno Vedium; nacionalidade a partir do nome do arquivo. | `object-position: center` (padrão), imagem esquerda. | R05 (shoot list real), quando aprovado. |
| **Iorubá** | E03 — `black-woman-laptop-and-typing-with-report-at-offi...mov`, frame em t=4s | Único candidato com adulto negro em contexto **neutro** (escritório, digitando) sem nenhum marcador cultural/religioso/étnico decorativo — nem roupa "tradicional", nem tecido estampado, nem objeto ritual. Rejeitados antes dela: E01 (contexto de sala de aula presencial sobre "internet skills", tema errado), E15/"black-female-teacher" (turbante estampado + cartaz sobre Austrália, tema errado e risco de "tecido exotizante"). | **Aprendizagem** — adulto negro focado, digitando em notebook, ambiente profissional. | Que a pessoa É Iorubá, fala Iorubá, ou representa a cultura Iorubá. | `object-position: center 15%` (mostra rosto completo, corta menos a testa). Imagem à direita (reverse). | **IORUBA_REAL_MEDIA_PREFERRED** — professor real, aula real ou material real, assim que existir. |
| **PLE (Português)** | E12 — `man-with-headphones-attends-online-meeting-taking...mov`, frame em t=6s | Precisava ser diferente do Hero (que já usa E10 no slide "Português") — ver bug corrigido na seção 3. Homem careca, fones azuis, escrevendo em caderno em frente a notebook, ambiente doméstico claro com planta. | Adulto participando de aula/reunião online, escrevendo. | Nacionalidade, ou que a pessoa é estrangeira vivendo no Brasil. | `object-position: center 20%`, imagem à esquerda. | Captação real de aluno de PLE (P0 conforme `08-page-media-map.md`). |
| **Espanhol** | E05 — `indian-latina-hispanic-woman-professor-teacher-tal...mov`, frame em **t=6.5s** (testados 0.5s/2s/4s antes — descartados por boca em posição de fala a meio; 6.5s tem expressão calma) | Único candidato claramente "professora/estudo" entre os nomeados pela missão (`indian-latina-hispanic-woman-professor`) que não colidia com nenhum asset já em uso. Cabelo cacheado, óculos, cardigã mostarda, estante ao fundo. | Adulta concentrada, olhando para baixo (lendo/escrevendo). | Nacionalidade específica (indiana/latina/hispânica) — o próprio nome do arquivo é um rótulo do banco de imagens, não um fato sobre a pessoa; alt-text não menciona nenhuma. | `object-position: center 20%`, imagem à direita (reverse). | Captação real. |
| **Hebraico** | E13 — `woman-with-headphones-studies-at-computer-at-home...mov`, frame em t=6s | Escolhida **especificamente por não ter nenhuma iconografia religiosa** (sem Estrela de Davi, Torá, kipá, sinagoga) nem marcador étnico — sorriso natural, fones, notebook, estante doméstica com uma pequena estátua decorativa (não religiosa). | Adulto estudando online, neutro. | Que a pessoa é judia, fala hebraico, ou pratica qualquer religião. | `object-position: center` (padrão — o enquadramento original já centraliza bem o rosto). Imagem à esquerda. | Professor real de Hebraico (Bíblico ou Moderno), conforme a trilha. |
| **B2B** | E14 — `41df3f96-bdbd-4131-93ba-e90eef6a1c77.png` (PNG, não um master de câmera nativo — ver nota técnica §4) | Precisava ser diferente do Hero (que já usa E07 no slide "Empresas") — ver bug corrigido na seção 3. Visão por cima do ombro de uma pessoa acompanhando uma videochamada em grupo (6 pessoas na tela), xícara de chá, ambiente de home office aconchegante. | Equipe em reunião remota — conecta com a copy "Idiomas para equipes que precisam se comunicar". | Que a reunião, a empresa ou os participantes são clientes reais da Vedium. | `object-position: right center` (preserva a tela do laptop inteira). | Case B2B real e autorizado (P0 conforme `08-page-media-map.md`). |
| **Aula ao vivo (vídeo)** | E08 — `smiling-female-teacher-in-glasses-giving-video-cal...mp4`, clipe completo (23.76s) + poster em t=8s | Único candidato landscape 4K claramente "professora explicando ao vivo, de frente pra câmera" (segurando quadro branco "Present Simple", biblioteca ao fundo) — o outro forte candidato landscape (E04, "friendly-man-teaching-english-lesson") tinha conteúdo de gramática ainda mais explicitamente em tela cheia (tabelas grandes de verbos), preterido por ser um pouco mais "textbook" que "aula". | Professora conduzindo uma explicação ao vivo, gesticulando, quadro branco, laptop. | Que é uma aula real da Vedium ou que a pessoa é professora Vedium. | N/A (vídeo landscape nativo). | R01/R02/R05 (captação real de aula ao vivo, gate P0 já registrado desde a Fase B.5). |

## 2. Assets rejeitados (auditados, não usados)

| Asset | Motivo da rejeição |
|---|---|
| E01 — `adults-learning-internet-skills-with-instructor...mov` | Inspecionado (frame em t=5s): sala de aula **presencial** com quadro-negro sobre "internet skills" para idosos — tema errado (não é aula de idioma), e reforça exatamente o risco já registrado no inventário original ("não associar a Iorubá pela cor da pele da instrutora"). |
| E15 — `black-female-teacher-answering-questions...mov` | Inspecionado (frame em t=8s): mulher com turbante estampado, ao ar livre, segurando um cartaz com o mapa da Austrália — turbante estampado é exatamente "tecido exotizante" (proibido pela missão) e o conteúdo (mapa da Austrália) não tem relação com aula de idioma. |
| E16 — `man-in-traditional-african-attire-studying...mp4` | **Rejeitado só pelo nome do arquivo, sem abrir o vídeo** — o próprio nome ("traditional african attire") descreve exatamente o padrão que a missão proíbe explicitamente para Iorubá (seção 4: "não usar roupa tradicional genérica"). Não inventamos conteúdo a partir do nome (regra da própria missão), mas também não há necessidade de abrir um asset cujo nome já aciona a regra de exclusão. |
| E11 — `woman-teaching-math-using-tablet-at-home...jpg` | Já rejeitado no inventário original (Fase 0.5): conteúdo de matemática infantil (banana com contas "1+8="), câmera de "criador de conteúdo" — nada a ver com idiomas para adultos. Reconfirmado nesta fase. |
| E17 — `close-up-girl-girl-learning-online.jpg` | Inspecionado: mostra o que aparenta ser uma criança/adolescente em aula online (contexto escolar, material colorido) — a Vedium se posiciona para público adulto em toda a documentação do projeto; usar essa imagem contradiria esse posicionamento. |
| E18 — `470bd106-...png` | Inspecionado: **não é uma fotografia de stock crua** — é uma peça de anúncio/social já finalizada de uma campanha anterior (logo Vedium, bandeiras dos 5 idiomas, ícones, CTA "Agende sua aula experimental"). Não há como extrair só a foto sem o resto da composição. |
| `49828a44-...png`, `6d5be17c-...png`, `97e21dcd-...png` | Inspecionados (aperto de mão corporativo; reunião em lounge; videochamada em sala de reunião grande) — fotografia corporativa genérica sem relação direta com idiomas; nenhum foi necessário dado que E14 já cobriu bem o B2B. Não usados, não descartados — permanecem como candidatos de reserva para B2B. |
| `9aaf3352-...png`, `9beb278b-...png`, `d4df977e-...png` | **Não inspecionados** — a auditoria priorizou os candidatos com maior probabilidade de uso (nomes descritivos, ou already-cataloged assets); estes 3 PNGs sem nome descritivo ficaram fora do escopo desta rodada. Registrar como pendência para uma futura auditoria, não como "aprovados" nem "rejeitados". |

## 3. Bugs reais encontrados e corrigidos (duplicação de mídia)

A missão pediu explicitamente para evitar reusar a mesma fotografia entre Hero/Inglês/PLE/B2B/Blog/Pathfinder. Dois erros reais de seleção foram cometidos e corrigidos **antes** do primeiro screenshot, via comparação de hash MD5 (não só inspeção visual):

1. **PLE quase duplicou o Inglês**: a primeira escolha para PLE foi `arab-student-guy-learning-online-at-laptop-sitting...jpg` — exatamente o mesmo arquivo-fonte que **já é** o master de `e02-study-laptop.jpg` (Inglês, em uso desde fases anteriores). A imagem foi revisada visualmente ("adulto, fones, notebook, estante") e pareceu uma nova descoberta, mas era o mesmo arquivo. Corrigido comparando hash MD5 do arquivo-fonte contra o derivado existente antes de prosseguir — substituído por E12 (`man-with-headphones-attends-online-meeting-taking`).
2. **B2B quase duplicou o Hero**: a primeira escolha para B2B foi `man-in-video-conference-with-coworkers-in-office...JPG` — o **mesmo arquivo-fonte** já usado para gerar `e07-hero-videoconference.jpg` (Hero, slide "Empresas", **congelado** desde a Fase B.6A). Confirmado por hash MD5 idêntico entre o derivado recém-gerado e o `e07` existente. Corrigido substituindo por E14 (a foto `41df3f96-...png`).

Depois da correção, uma verificação final de hash MD5 confirmou que os 11 arquivos em `v2-preview-media/` (9 imagens + vídeo + poster) são todos byte-distintos entre si — nenhuma duplicação restante.

## 4. Nota técnica — PNGs de dimensão atípica

Os arquivos `NNNNNNNN-....png` em `vedium-references/envato-assets/` (8 no total) têm dimensões incomuns para masters de câmera (a maioria 1672×941px, um 1729×910px) — não são resoluções nativas típicas de câmera/celular. Inspeção visual confirmou que pelo menos um deles (`470bd106`) é uma peça de design já finalizada (banner de anúncio), não uma fotografia crua — provavelmente exports/previews de uma sessão anterior de curadoria de assets, não masters originais do Envato. Usar esses arquivos (como E14, para B2B) é aceitável para o preview local (qualidade suficiente pra web), mas eles não devem ser tratados como "masters de alta resolução para toda finalidade" — se o mesmo asset for necessário em resolução maior no futuro, buscar o master original no Envato pelo item ID (ainda não registrado — todos os campos `envato_item_id`/`envato_item_url` do inventário permanecem "a confirmar").

## 5. Vídeo da "Aula ao vivo" — decisões técnicas

- **Master**: `smiling-female-teacher-in-glasses-giving-video-cal-2025-12-17-14-50-51-utc.mp4`, h264, 3840×2160, 23.76s, com áudio AAC, 582MB.
- **Derivado web**: `e16-liveclass-teacher.mp4` — 1280×720, h264 CRF 24, AAC 96kbps, ~2.3MB (758kbps). Clipe completo mantido (não cortado) para não interromper a explicação a meio.
- **Poster**: `e16-liveclass-teacher-poster.jpg`, frame em t=8s, 1600×900.
- **Áudio**: mantido como veio no master (não verificado o conteúdo da fala/idioma da narração além do que aparece escrito no quadro branco) — para rollout real, revisar o áudio antes de publicar.
- **Player**: `<video controls preload="metadata" poster="..." playsinline>` — **sem autoplay/loop/mute**. Decisão da seção 16 da missão: o conteúdo é didático (fala explicando gramática), então usa controles reais em vez de loop ambiente. Isso também satisfaz `prefers-reduced-motion` estruturalmente (nunca autoplaya, mostra sempre o poster até o clique).
- **Performance**: pausa automática via `IntersectionObserver` se o vídeo estiver tocando e a seção sair significativamente da viewport (`design-system-v2.js`, `initLiveClassVideo`).

## 6. VediumPathfinder — decisão de não usar mídia

A missão (seção 13) autorizou usar uma foto no painel esquerdo do Pathfinder **somente se houvesse UMA imagem excelente**, e pediu explicitamente para não usar imagem só pra preencher espaço. Avaliação: o painel já tem presença visual forte (gradiente navy + tipografia grande + a lista numerada "01 IDIOMA / 02 OBJETIVO", ver `20-bain-editorial-rhythm.md` §2) — adicionar uma foto de fundo arriscaria reduzir a legibilidade desse dispositivo numerado sem ganho editorial claro. **Decisão: manter o painel sólido, sem foto.** Nenhuma mudança feita nesta seção.

## 7. Testes executados

- 326 testes puros passando, 5 skipped; flake8 limpo
- Render Jinja real (Docker), 0 `Traceback`, único `<h1>`, 0 `.v2-media-empty`
- **Hero verificado intacto**: hash MD5 do HTML renderizado do `<section class="v2-editorial-hero">` idêntico antes/depois (`1acd805606a5cd559f92969de0437315`) — confirmado em 3 pontos de checagem ao longo da fase
- 0 overflow horizontal em 1440px e 390px
- 0 ocorrências de "aluno Vedium"/"professor Vedium"/"aula Vedium" no HTML renderizado (nenhuma mídia stock descrita como prova real)
- Contraste: seções de curso não sobrepõem texto em foto (conteúdo sempre na coluna separada, sem overlay) — sem necessidade de nova auditoria WCAG nesta fase
- Vídeo testado sob `prefers-reduced-motion: reduce`: `autoplay:false, paused:true, controls:true, poster` correto
- Screenshots reais em 1440px (5 idiomas + Live Class + B2B) e 390px (Iorubá, Hebraico, Live Class) confirmando imagem-primeiro no mobile, sem placeholder, sem overflow
- Todas as imagens novas verificadas carregando de verdade (não só presentes no DOM) via `naturalWidth > 0` após scroll real — achado real de metodologia: `Emulation.setDeviceMetricsOverride` do CDP não dispara o `loading="lazy"` nativo do Chrome headless da mesma forma que um scroll de verdade; corrigido usando scroll progressivo real antes de cada captura
- CRLF: nenhum arquivo modificado contém `\r` (incluindo o CSV, onde um bug real de escaping — `\"` em vez de `""` — quebrava o parsing e foi corrigido)
- `git status --porcelain`: mudanças isoladas a `vedium_core/vedium_core/{public/css/v2,public/js/v2,templates/includes/v2,www/design_system_v2.*}` e `docs/redesign/*`; `vedium_core/vedium_core/public/v2-preview-media/` e `vedium-references/` continuam ignorados pelo git (`.git/info/exclude`)

## 8. Tamanho dos arquivos finais em `v2-preview-media/`

| Arquivo | Tamanho |
|---|---|
| e11-ioruba-learning.jpg | 129 KB |
| e12-espanhol-professora.jpg | ~200 KB |
| e13-hebraico-headphones.jpg | 154 KB |
| e14-ple-headphones-home.jpg | ~300 KB |
| e15-b2b-videocall.jpg | ~260 KB |
| e16-liveclass-teacher-poster.jpg | 151 KB |
| e16-liveclass-teacher.mp4 | 2.3 MB |

Nenhum master foi commitado ou movido para dentro do controle de versão — todos os derivados vivem em `vedium_core/vedium_core/public/v2-preview-media/`, ignorado pelo git desde a Fase B (`.git/info/exclude`).
