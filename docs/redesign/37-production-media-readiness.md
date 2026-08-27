# 37 — Prontidão de mídia de produção (Fase C.1.1, Parte A)

> Nenhum asset foi copiado para produção nesta fase. O pipeline abaixo foi executado de verdade (números reais), mas os arquivos gerados ficam em `public/v2-preview-media/{webp,avif,webm}/` — a mesma pasta já gitignorada da fase anterior, nunca deployada.
>
> **ATUALIZAÇÃO — decisão do responsável pelo projeto (pós Fase C.1.3)**: o uso de toda a biblioteca em `vedium-references/envato-assets/` (imagens e vídeos, não só os 11 assets já selecionados) foi **autorizado explicitamente pelo dono do projeto**, que assume a responsabilidade pelo licenciamento. **Media usage authorized by project owner. Individual license evidence was not independently verified during the redesign workflow.** Isso é uma aceitação de risco documental do responsável, não uma afirmação técnica de que cada certificado foi auditado — a classificação `NEEDS_LICENSE_EVIDENCE` das seções 1-2 abaixo permanece como registro histórico do que foi (e não foi) encontrado nesta fase, mas **deixou de ser um blocker de gate**. `MEDIA = PASS — USER AUTHORIZED`. Ver `46-final-cutover-readiness.md` para o gate atualizado.

## 1. Inventário final — assets efetivamente usados na Home V2

| Arquivo servido hoje | Seção | Item Envato (master) | Dimensões | JPEG/MP4 atual (bytes) | Status de licença |
|---|---|---|---|---|---|
| `e02-study-laptop.jpg` | Hero (slide 2) + Cursos → Inglês | E02 — `arab-student-guy-learning-online-at-laptop-sitting-...utc.jpg` | 2000×1263 | 305.191 | **USER_AUTHORIZED** |
| `e06-listening-online-course.jpg` | Hero (slide 1) | E06 — `listening-to-online-university-course-...utc.jpg` | 2000×1333 | 243.459 | **USER_AUTHORIZED** |
| `e07-hero-videoconference.jpg` | Hero (slide 4, Empresas) | E07 — `man-in-video-conference-with-coworkers-in-office-...utc.JPG` | 2000×1333 | 262.728 | **USER_AUTHORIZED** |
| `e10-notes-at-home.jpg` | Hero (slide 3, Português) | E10 — `woman-listening-to-music-taking-notes-at-home-...utc.jpg` | 2000×1333 | 227.096 | **USER_AUTHORIZED** |
| `e11-ioruba-learning.jpg` | Cursos → Iorubá | E03 (frame extraído em t=4s) — `black-woman-laptop-and-typing-with-report-at-offi-...utc.mov` | 1055×2000 | 131.974 | **USER_AUTHORIZED** |
| `e12-espanhol-professora.jpg` | Cursos → Espanhol | E05 (frame em t=6.5s) — `indian-latina-hispanic-woman-professor-teacher-tal-...utc.mov` | 1125×2000 | 253.569 | **USER_AUTHORIZED** |
| `e13-hebraico-headphones.jpg` | Cursos → Hebraico | E13 (frame em t=6s) — `woman-with-headphones-studies-at-computer-at-home-...utc.mov` | 1080×1920 | 157.940 | **USER_AUTHORIZED** |
| `e14-ple-headphones-home.jpg` | Cursos → Português para Estrangeiros | E12 (frame em t=6s) — `man-with-headphones-attends-online-meeting-taking-...utc.mov` | 1125×2000 | 213.342 | **USER_AUTHORIZED** |
| `e15-b2b-videocall.jpg` | B2B (Home) | E14 — `41df3f96-bdbd-4131-93ba-e90eef6a1c77.png` | 2000×1126 | 182.986 | **USER_AUTHORIZED** |
| `e16-liveclass-teacher-poster.jpg` | Live Class (poster) | E08 (frame em t=8s) — `smiling-female-teacher-in-glasses-giving-video-cal-...utc.mp4` | 1600×900 | 151.364 | **USER_AUTHORIZED** |
| `e16-liveclass-teacher.mp4` | Live Class (vídeo) | E08 (recodificado, master de 582MB) — idem acima | 1280×720, h264+aac, 25fps, 23,77s | 2.281.136 | **USER_AUTHORIZED** |

11 arquivos ativos na Home V2 (10 imagens + 1 vídeo). O item Envato/master de cada um já estava mapeado em `docs/redesign/07-envato-asset-inventory.csv` (colunas `envato_item_id`/`envato_item_url`/`arquivo_licenca`/etc.) — nenhuma linha nova precisou ser inventada aqui, só referenciada.

## 2. Classificação de licença — sem inventar comprovação

**Busca real realizada nesta fase** (não assumida): varredura de `vedium-references/envato-assets/` e de `Cliente/Vedium/` por qualquer arquivo de licença/recibo (`*license*`, `*licenca*`, `*receipt*`, `*.pdf`, `*.txt` correlato) — **nenhum arquivo de comprovação encontrado em nenhum dos dois locais**.

Confirmado também em `07-envato-asset-inventory.csv`: as colunas `envato_item_id`, `envato_item_url`, `data_download`, `projeto_licenciado`, `arquivo_licenca`, `master_original` e `responsavel_download` estão marcadas **"a confirmar" em 100% das linhas** — ou seja, esse campo nunca foi de fato preenchido em nenhuma fase anterior, apesar da estrutura da planilha já prever isso desde a Fase B.

**Classificação resultante**: todos os 11 assets = **USER_AUTHORIZED**.

Nenhum foi classificado como `REJECTED` — não há evidência de uso indevido, só ausência de comprovação documentada no repositório. O padrão de nomenclatura dos arquivos (`nome-descritivo-AAAA-MM-DD-HH-mm-ss-utc.ext`) é consistente com exportações do Envato Elements (licença por assinatura contínua, não por item individual comprado — nesse modelo não existe "certificado por arquivo", só a assinatura ativa da conta), mas **isso é uma inferência a partir do padrão de nome, não uma comprovação** — por isso a classificação permanece NEEDS_LICENSE_EVIDENCE, não VERIFIED_LICENSE.

**Ação necessária, fora do escopo desta fase** *(histórico — superado pela autorização do responsável abaixo)*: confirmar com quem administra a conta Envato Elements da Vedium (a) que a assinatura está ativa, (b) se os arquivos foram baixados sob essa assinatura, e (c) guardar a confirmação em `docs/redesign/07-envato-asset-inventory.csv` preenchendo as colunas já existentes. Isso seria uma verificação administrativa, não técnica — não podia ser feita a partir do código ou dos arquivos de mídia em si.

### Decisão do responsável pelo projeto — substitui a exigência de certificado individual

O dono do projeto autorizou expressamente o uso de **toda** a biblioteca em `vedium-references/envato-assets/` (não só os 11 assets listados na seção 1), assumindo a responsabilidade pelo licenciamento. Isso vale para Home, páginas de idioma, níveis, B2B, professores, blog e demais páginas V2 — a biblioteca completa (imagens e vídeos) fica disponível para seleção de mídia no redesign, sem exigir certificado individual por arquivo como pré-condição de uso.

**Regras que continuam valendo, sem exceção** (decisão do responsável é sobre licenciamento, não sobre direção editorial/cultural):
- nunca apresentar stock como professor, aluno ou aula real da Vedium;
- não inferir nacionalidade, etnia ou identidade cultural pela aparência;
- Iorubá: evitar África genérica, exotização e símbolos religiosos/decorativos (gate cultural já em vigor desde B.3/B.4, ver seção 4 abaixo);
- Hebraico: evitar iconografia religiosa sem relação direta com o conteúdo (mesmo critério que levou à escolha de `e13-hebraico-headphones.jpg`);
- PLE: evitar turismo/clichês de Brasil;
- Espanhol: evitar clichês nacionais;
- pessoas reais, adultas, aparência profissional;
- priorizar cenas de aprendizagem, aula, comunicação e ambiente profissional;
- usar derivados otimizados para produção (ver pipeline WebP/AVIF da seção 3), nunca publicar masters pesados diretamente;
- preservar os masters originais sem edição destrutiva (masters em `vedium-references/envato-assets/` continuam intocados, só derivados são gerados/usados).

Ao selecionar novos assets da biblioteca completa: escolher pela qualidade e pertinência editorial/cultural, não simplesmente porque o arquivo existe.

## 3. Pipeline de produção — executado com números reais (não estimado)

Gerado com Pillow 12.0 (WebP/AVIF) e ffmpeg (WebM), a partir dos MESMOS 10 JPEGs/1 MP4 já em uso — nenhum master gigante foi copiado, nenhum arquivo foi movido para fora de `public/v2-preview-media/` (pasta gitignorada, confirmada fora do controle de versão).

| Arquivo | JPEG (bytes) | WebP q82 (bytes) | Redução WebP | AVIF q55 (bytes) | Redução AVIF |
|---|---|---|---|---|---|
| e02-study-laptop | 305.191 | 188.068 | 38,4% | 108.076 | 64,6% |
| e06-listening-online-course | 243.459 | 135.750 | 44,2% | 70.321 | 71,1% |
| e07-hero-videoconference | 262.728 | 134.490 | 48,8% | 69.604 | 73,5% |
| e10-notes-at-home | 227.096 | 117.544 | 48,2% | 56.570 | 75,1% |
| e11-ioruba-learning | 131.974 | 59.886 | 54,6% | 28.991 | 78,0% |
| e12-espanhol-professora | 253.569 | 143.910 | 43,2% | 71.313 | 71,9% |
| e13-hebraico-headphones | 157.940 | 80.114 | 49,3% | 40.165 | 74,6% |
| e14-ple-headphones-home | 213.342 | 113.820 | 46,6% | 58.814 | 72,4% |
| e15-b2b-videocall | 182.986 | 91.936 | 49,8% | 51.293 | 72,0% |
| e16-liveclass-teacher-poster | 151.364 | 77.364 | 48,9% | 42.352 | 72,0% |

**AVIF vence em todos os 10 arquivos** (64–78% de redução vs. 38–55% do WebP) — mas exige fallback JPEG para navegadores sem suporte (cobertura ampla em 2026, mas não universal). Recomendação técnica: `<picture><source type="image/avif">...<source type="image/webp">...<img src=".jpg"></picture>`, 3 níveis de fallback, nenhum nível novo de complexidade de build além do já necessário (gerar os 2 derivados por imagem uma vez, versionar como asset final).

**Não implementado nesta fase**: trocar os `<img>`/macros para `<picture>` — isso é uma mudança de marcação que só faz sentido aplicar quando os assets finais (pós-decisão de licença) forem definidos; aplicar agora arriscaria ter que refazer com os arquivos certos depois.

### Vídeo Live Class — comparação real (não estimado)

| Formato | Codec | Bytes | Redução |
|---|---|---|---|
| MP4 atual (produção) | h264 + aac | 2.281.136 | baseline |
| WebM/VP9 (gerado nesta fase, CRF 34) | vp9 + opus | 1.811.169 | 20,6% |

Ganho mais modesto que nas imagens — H.264 já é razoavelmente eficiente para este tipo de conteúdo (fala, pouco movimento). Padrão recomendado se o vídeo for promovido a produção: `<video><source type="video/webm">...<source type="video/mp4">...</video>`, MP4 como fallback universal (H.264 é decodificável em qualquer browser moderno, WebM/VP9 não é 100% universal ainda em alguns dispositivos legados). **Vídeo em si não foi alterado nem re-selecionado** — só gerada uma variante de comparação, conforme pedido explícito da missão ("não mudar vídeo sem aprovação").

## 4. Hero — preservado, sem mudança visual

Confirmado idêntico à Fase C.1: slide 1 com `loading="eager" fetchpriority="high"`; slides 2–4 com `loading="lazy"`. Nenhuma alteração nesta fase — já estava correto.

## 5. Vídeo Live Class — specs confirmadas via ffprobe (não assumidas)

`codec_name=h264` (vídeo) + `aac` (áudio), `1280x720`, `25fps`, `duration=23.766s`, `2.281.136 bytes`. `poster="e16-liveclass-teacher-poster.jpg"` (1600×900), `preload="metadata"`, `controls`, sem autoplay — inalterado desde B.6C/Fase C.1.

## 6. Gate de rollout

`MEDIA = PASS — USER AUTHORIZED`. O pipeline técnico de derivados está pronto e testado com números reais (seção 3); a pendência administrativa/jurídica que bloqueava o gate (confirmação de licença Envato item a item) foi resolvida por aceitação de risco explícita do responsável pelo projeto — **Media usage authorized by project owner. Individual license evidence was not independently verified during the redesign workflow.** Não é mais um blocker de cutover. Checklist `42-envato-license-evidence-checklist.md` permanece como referência (não descartado), mas deixou de ser pré-condição de gate.
