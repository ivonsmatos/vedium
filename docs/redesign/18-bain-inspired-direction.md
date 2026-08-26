# 18 — Reset visual Bain-inspired (Fase B.6, segunda passada)

> **Origem**: no meio da execução da missão "AUTORIDADE VISUAL E PROVA INSTITUCIONAL" (`17-home-v2-proof-system.md`), a missão foi substituída por "RESET VISUAL BAIN-INSPIRED" — uma mudança de referência visual (Bain.com como inspiração de **princípios**, nunca de código/texto/assets) e de arquitetura da Home (nova ordem de seção, Hero sem foto, novo componente VediumPathfinder, "grandes blocos alternados" para Cursos). As melhorias de componente de baixo nível da primeira passada (raio, rail de progressão, card tipográfico) foram mantidas — ver `17-home-v2-proof-system.md` §1 para o que sobreviveu.
>
> **⚠️ Hero substituído na Fase B.6A**: a seção 3 abaixo ("Hero — de HeroSplit com foto para HeroEditorial + Pathfinder") descreve o Hero SEM foto desta fase, que por sua vez foi substituído por um Hero full-bleed em carousel editorial (nova referência: o hero atual do Bain.com). O VediumPathfinder (seção 4 abaixo) continua existindo e funcionando exatamente como descrito, só mudou de lugar (saiu de dentro do Hero, virou a seção logo abaixo dele). **Para o Hero atual, ver `19-editorial-hero-carousel.md`.**

## 1. O que foi observado no Bain.com (princípios, não implementação)

A missão foi explícita: **nunca copiar código/CSS/textos/imagens/logos/identidade proprietária do Bain** — só reproduzir princípios de composição, largamente já documentados na indústria de design editorial/institucional:

- Escala editorial (tipografia grande, poucos elementos por tela)
- Grandes áreas de respiro (padding de seção generoso, não densidade de "página de produto")
- Forte contraste tipográfico (H1 muito maior que o corpo, hierarquia clara)
- Navegação institucional (não menu de e-commerce/marketplace)
- Poucos elementos por seção (1 ideia por bloco, não 5 cards competindo por atenção)
- Blocos grandes em vez de grades pequenas
- Conteúdo como autoridade (texto/copy carregando a credibilidade, não badges/selos/ícones decorativos)
- Interações discretas e úteis (não bounce/parallax/carrossel automático)
- Fotografia com presença quando existe (não fotografia decorativa genérica)
- Disciplina cromática (poucas cores, uso deliberado)
- CTAs simples (1 ação clara por seção, não uma caixa cheia de botões)
- Ausência de aparência de marketplace/LMS/ThemeForest

## 2. Nova ordem de seção do Presentation Mode (`www/design_system_v2.html`)

Ordem única, conforme missão (substitui as 13 seções da B.5/B.6-v1 documentadas em `15-home-v2-art-direction.md` §2):

1. Header utility bar (Área do aluno / WhatsApp / idioma)
2. Header principal (Logo / Cursos / Como funciona / Para empresas / Conteúdo / Sobre / CTA)
3. Hero editorial + VediumPathfinder
4. O que define a Vedium (4 colunas editoriais, sem cards)
5. Cursos (5 blocos grandes alternados)
6. Aula ao vivo
7. Progressão
8. B2B
9. Conhecimento Vedium
10. CTA institucional
11. Footer

**Removido da sequência**: "Como começar"/`ProcessSteps` (a interação de orientação inicial passou a ser o Pathfinder, no Hero) — o componente continua demonstrado em `?debug=1#lib-process`. **Fundido em uma seção só**: Trust Strip + "Como a Vedium ensina" + parte do Institucional Vedium viraram "O que define a Vedium".

## 3. Hero — de HeroSplit com foto para HeroEditorial + Pathfinder

**Antes (B.5)**: `v2_hero_split` — conteúdo 48% + foto 52% (E06), 2 CTAs de botão.

**Depois (B.6-v2)**: `v2_hero_editorial` — sem foto, largura editorial ampla (44rem), left-aligned:
- Eyebrow: "Escola de idiomas online"
- H1: "Aprenda ao vivo. Avance com direção." (5 palavras — bem mais curto que o H1 da B.5, de propósito: a missão pediu headline dominante, não apoiado em foto)
- Apoio: "A Vedium é uma escola de idiomas online com aulas ao vivo, professores nativos e especialistas e progressão organizada por nível."
- Sem par de botões CTA — a interação principal é o Pathfinder logo abaixo (2 CTAs concorrentes no mesmo momento violaria "poucos elementos por seção")

O teto de `--v2-text-h1` foi reaberto de 52px (calibrado na B.5 para um H1 de 9 palavras numa coluna de 47%) para ~76px (`clamp(2.375rem, 1.5rem + 4.2vw, 4.75rem)`), já que o H1 atual é curto e a coluna é editorial larga, não dividida. Confirmado por screenshot real em 1440px: o H1 renderiza em exatamente 3 linhas, sem quebra artificial.

## 4. VediumPathfinder — protótipo funcional isolado

Componente novo (`v2_pathfinder` em `macros_editorial.html`, CSS em `components-editorial.css` `.v2-pathfinder*`): 2 perguntas —"Qual idioma você quer aprender?" (Inglês/Iorubá/Português para Estrangeiros/Espanhol/Hebraico) e "Qual é o seu principal objetivo?" (Trabalho e carreira/Comunicação cotidiana/Viagens/Estudos e cultura/Viver e trabalhar no Brasil) — com CTA "Encontrar meu caminho".

**Implementação deliberadamente mínima, conforme a missão ("protótipo funcional isolado")**:
- `<fieldset>`/`<legend>`/`<input type="radio">` nativos — funciona sem JS, teclado e leitor de tela já cobertos pela semântica HTML padrão
- Seleção visual em "chip" via `:has(input:checked)` — puro CSS, sem JS de estado
- `<form action="/teste-de-nivel" method="get">` — o CTA aponta pra URL fixa do teste de nível real, igual a qualquer outro CTA estático do design system
- **Não conecta a CRM, não altera o teste de nível real, não cria regra de negócio nova** — exatamente como a missão pediu

### Bug real encontrado e corrigido: botão submit sem estilo

Ao revisar o primeiro screenshot do Hero, o CTA "Encontrar meu caminho" renderizava como texto puro, sem cor/fundo/borda — não parecia botão. Causa raiz: `foundations.css` tem um reset global `.v2-scope button { background: none; border: 0; color: inherit }` (especificidade 0,1,1) que **vencia** `.v2-btn--primary { background: ...; border-color: ... }` (especificidade 0,1,0, uma classe só) na cascata CSS. Todo botão do design system até agora era renderizado como `<a>` (LinkButton), que o reset não afeta — o Pathfinder é o primeiro `<button type="submit">` real do sistema, por isso o bug nunca tinha aparecido antes. Corrigido em `components-base.css`: as regras de cor/borda dos variantes (`--primary`/`--secondary`/`--tertiary`/`--danger`) e a borda base do `.v2-btn` passaram a ser escritas como `.v2-scope .v2-btn...` (2 classes = especificidade 0,2,0), que vence o reset sem precisar de `!important`. Confirmado por screenshot antes/depois.

## 5. Cursos — de LanguageMosaic (grade de 5 posições) para CourseFeature (blocos grandes alternados)

Componente novo (`v2_course_feature`): um bloco de **escala de seção** por curso, não um card numa grade.

- **Com foto** (Inglês, Português para Estrangeiros): grid 55/45 (`1.1fr 1fr` desktop), mesmo princípio do `FeatureMedia` — `reverse` alterna o lado da imagem entre os dois blocos com foto, pra não repetir o mesmo layout duas vezes seguidas.
- **Sem foto** (Iorubá, Espanhol, Hebraico): bloco de texto largo em fundo tonal sólido (`tone="brand"` azul ou `tone="warm"` surface-warm), nunca `.v2-media-empty` — mesma lógica do card tipográfico da B.6-v1 (`17-home-v2-proof-system.md` §4), em escala maior.

**Ordem dos cursos — decisão documentada**: a missão pediu prioridade estratégica Iorubá → Inglês → PLE → Espanhol → Hebraico, mas explicitamente permitiu "avaliar Home: Inglês pode ser a primeira entrada comercial se necessário", com a condição de documentar qualquer desvio. Optei por manter **Inglês primeiro** — é o curso mais estabelecido como carro-chefe comercial em toda a documentação de produto do projeto até aqui (matriz comercial, ver memória do projeto) e a entrada mais familiar para um visitante novo navegando a Home institucional. Ordem final: **Inglês, Iorubá, Português para Estrangeiros, Espanhol, Hebraico** — mantendo Iorubá em segundo (não no fim) para preservar boa parte da prioridade estratégica pedida, e alternando foto/tonal (foto, tonal, foto, tonal, tonal) para variação rítmica ao longo da rolagem.

## 6. Aula ao vivo — copy e pontos atualizados

Título trocado de "Veja como uma aula ao vivo funciona." para **"Aulas ao vivo, na prática."** (mais próximo do registro "resultados" do Bain, sem inventar resultado nenhum — a seção continua sendo sobre o que acontece na aula, não uma métrica). Pontos trocados de "Prática em tempo real/Correção e orientação/Participação ativa/Aplicação do idioma" para os 4 rótulos exatos da missão: **Participação / Correção / Prática / Acompanhamento**. Gate de mídia mantido (`HOME_MEDIA_GATE_02`, ver `17-home-v2-proof-system.md` §6) — continua sem foto/vídeo real de aula.

## 7. Progressão, B2B, Conhecimento Vedium, CTA — ajustes de copy

- **Progressão**: rail mantido (ver `17-home-v2-proof-system.md` §5); rótulos trocados de "Nível atual/Objetivos/Prática/Avaliação/Próximo nível" para **Nível atual/Competências/Prática/Avaliação/Próximo nível** (Objetivos → Competências).
- **B2B**: eyebrow "Para empresas" adicionado acima do bloco (a missão pediu eyebrow explícito, referência ao padrão "results"/case do Bain — sem inventar case/depoimento). Gate `VEDIUM_B2B_REAL_MEDIA_PREFERRED` mantido (E07 continua provisório).
- **Conhecimento Vedium**: renomeado de "Conteúdo Vedium" (referência ao "Our Latest Insights" do Bain, só no nome da seção — layout 50%+25%+25% já existia da B.6-v1). Prioridade de conteúdo pedida pela missão era Inglês/Iorubá/PLE/B2B; **não existe post real de PLE nem de B2B em `blog_content.py` hoje** (busquei por tag/categoria, sem resultado) — mantido Hebraico como 3º artigo real disponível, decisão documentada aqui em vez de fabricar conteúdo inexistente.
- **CTA institucional**: H2 trocado de "Encontre o curso certo para o seu objetivo." para **"Como a Vedium pode ajudar você?"**; variante trocada de `brand` (fundo navy) para `section` (fundo warm) — parte da redução geral de navy na página, ver seção 9 abaixo.

## 8. VediumResults — componente futuro, preparado mas NÃO renderizado

A missão pediu que um componente futuro similar ao "Client Results" do Bain fosse **preparado, mas não implementado nem renderizado** no Presentation Mode nesta fase — reservado para quando houver depoimento real, indicador acadêmico documentado, case B2B real ou progresso de aluno documentado (nunca número inventado, seguindo a mesma regra do `StudyRhythmCard`/`TestimonialCard` já em vigor no resto do design system). Não há código para este componente ainda — este parágrafo é o registro da intenção, para retomar quando houver conteúdo real disponível.

## 9. Cor — proporção 70/20/10

A missão pediu 70% branco/off-white, 20% azul institucional, 10% terracota (CTA/detalhes), nunca copiar o vermelho do Bain. Antes desta fase, 3 seções usavam fundo navy (Trust Strip, Live Class, CTA final). Depois: **2 seções navy** (Aula ao vivo, mais os 2 blocos tonais `tone="brand"` de Cursos — Iorubá e Hebraico) + Footer; Trust Strip virou "O que define a Vedium" em fundo claro; CTA final virou fundo warm. Terracota (`--v2-color-accent`) só aparece nos CTAs primários (botões) e nos eyebrows — nunca como decoração recorrente.

## 10. Footer — sem repetir slogan

A missão pediu "não repetir slogans — abaixo do logo usar apenas uma frase curta com os 5 idiomas". A `brand-signature` anterior ("Aulas de idiomas ao vivo, com professores nativos e especialistas e progressão acompanhada.") repetia quase o mesmo conteúdo da `v2-footer__message` logo acima. Trocada por: **"Inglês, Iorubá, Português para Estrangeiros, Espanhol e Hebraico."**

## 11. Mobile

Confirmado por screenshot real (CDP + emulação `mobile:true`) em 390px: Hero = eyebrow + H1 + apoio + Pathfinder empilhado (chips quebram em várias linhas, CTA vira botão full-width); "O que define a Vedium" = grid 2 colunas (não empilha em coluna única — decisão de manter 2 colunas por item ser curto o suficiente para não precisar de rolagem extra); Cursos = blocos verticais únicos, cada um ocupando a largura toda; Aula ao vivo/B2B/Progressão empilham em coluna única mantendo hierarquia; Conhecimento Vedium = destaque + lista vertical; CTA final = bloco único centralizado. Nenhum mosaico complexo recriado em mobile, conforme pedido.

### Bug real encontrado e corrigido: divisor do ProofBar na 2ª linha do grid mobile

"O que define a Vedium" usa `ProofBar` com 4 itens num grid de 2 colunas em mobile. A regra que remove o divisor vertical do primeiro item (`:first-child`) só zerava a borda do item 1 — o item 3 (início da 2ª linha, visualmente a coluna esquerda de novo) mantinha o divisor e o padding-inline-start, criando um recuo/traço à esquerda que não correspondia a nenhum vizinho real. Corrigido em `components-editorial.css`: `:nth-child(odd)` remove o divisor em mobile (2 colunas — ímpares são sempre a coluna esquerda), revertendo para a lógica `:first-child` só dentro do breakpoint desktop (4 colunas, 1 linha). Confirmado por screenshot antes/depois nos dois breakpoints.

## 12. Testes e QA executados

- 326 testes puros passando, 5 skipped (`pytest vedium_core/tests/test_pure_*.py vedium_core/tests/test_course_urls.py`)
- `flake8` limpo em `design_system_v2.py`
- Render Jinja real via container Docker (`vedium-frappe`), ambos os modos: Presentation ~30KB/200, Debug ~103KB/200, 0 `Traceback`
- Único `<h1>` em Presentation e em Debug mode
- 0 ocorrências de `.v2-media-empty` em Presentation mode
- 0 ocorrências de "contexto", travessão (`—`), "professor real", "Título de exemplo" no HTML renderizado
- CRLF: nenhum arquivo modificado contém `\r`
- `git status --porcelain`: mudanças isoladas a `vedium_core/vedium_core/public/css/v2/*`, `public/js/v2/*` (inalterado nesta fase), `templates/includes/v2/*`, `www/design_system_v2.{py,html}` e `docs/redesign/*` — nenhum arquivo de produção tocado
- Screenshots reais via CDP (Chrome headless + `Emulation.setDeviceMetricsOverride` + `Page.reload({ignoreCache:true})`) em 1440px e 390px, seção por seção: Hero+Pathfinder, "O que define a Vedium", Cursos (5 blocos), Aula ao vivo, Progressão, B2B, Conhecimento Vedium, CTA+Footer, Header (utility+principal) — 2 bugs visuais reais encontrados e corrigidos nesta rodada (botão do Pathfinder sem estilo, seção 4; divisor do ProofBar em mobile, seção 11)

## 13. O que NÃO foi feito nesta fase (fora de escopo, por instrução explícita da missão)

- Nenhuma migração da Home real de produção (`site_navbar.html`/`site_footer.html`/página inicial real) — tudo isolado em `v2/`
- Nenhum deploy
- Nenhum commit automático
- VediumPathfinder não conecta a CRM nem altera o teste de nível real
- VediumResults não foi implementado, só documentado como intenção (seção 8)
