# 10 — Implementação do VEDIUM DESIGN SYSTEM V2 (Fase B + B.1 + B.2 + B.3)

> **Escopo da Fase B (2026-08-24):** fundação isolada do design system, na stack real (Frappe SSR + Jinja + CSS/JS próprios). Nenhuma página pública existente foi alterada, substituída ou teve sua rota/redirect/controller/DocType/checkout/teste de nível/GTM/CRM/Stripe/Nginx modificados. Nenhum deploy foi feito.
>
> **Atualizado na Fase B.1 (mesmo dia):** QA visual/marca/responsividade (validação estrutural, sem browser real). Ver `docs/redesign/12-design-system-visual-qa.md`.
>
> **Atualizado na Fase B.2 (mesmo dia):** ambiente local disponibilizado (`http://localhost:8005/design_system_v2`) para revisão humana real em navegador. Ver `docs/redesign/13-human-visual-review-checklist.md`.
>
> **Atualizado na Fase B.3 (2026-08-24): redesign visual e direção de arte.** A revisão humana da B.2 **reprovou** a direção visual da Fase B (parecia biblioteca técnica de componentes/LMS/marketplace, não uma escola de idiomas premium). Este documento reflete o estado FINAL depois do redesign — ver `docs/redesign/14-art-direction-v2.md` para os princípios visuais completos e `docs/redesign/12-design-system-visual-qa.md` para o relatório de QA com screenshots reais.

## 1. Arquivos criados/alterados nesta fase (todos dentro de `v2/`)

```
vedium_core/vedium_core/public/css/v2/
  tokens.css               -- variáveis CSS (cor, tipografia, espaço, raio, sombra, container, motion)
  foundations.css          -- reset escopado (.v2-scope), tipografia utilitária, container/section/grid, sr-only
  components-base.css      -- Button, LinkButton, Badge, Breadcrumb, Form (Field/Input/Select), Alert, Modal, Icon
  components-editorial.css -- Hero(3), ProofBar, FeatureCard, LanguageCard, LanguageMosaic, CourseCard,
                               LevelCard/Timeline, LevelJourney, TeacherCard/Summary/Feature, ProcessSteps,
                               FeatureMedia, LiveClassExperience, VideoSection, TestimonialCard, StudyRhythmCard,
                               FAQAccordion, BlogCard, CTASection
  header-footer.css        -- Header v2 e Footer v2 (componentes isolados)

vedium_core/vedium_core/public/js/v2/
  design-system-v2.js      -- JS vanilla progressivo: menu mobile, accordion do FAQ, modal base, tablist do LevelJourney

vedium_core/vedium_core/public/v2-preview-media/   -- Fase B.3, NOVO. Derivados locais (resize, sem crop pré-definido)
  de 4 assets Envato já aprovados por docs/redesign/06-photography-system.md/08-page-media-map.md, gerados com
  Pillow (já presente no ambiente bench, nenhuma ferramenta nova instalada). Ignorado via `.git/info/exclude`
  (mesmo padrão de `vedium-references/`) -- NUNCA commitado. Ver seção 11.

vedium_core/vedium_core/templates/includes/v2/
  macros_base.html         -- macros Jinja dos 12 componentes base
  macros_editorial.html    -- macros Jinja dos componentes editoriais (24 nomeados + TextLink, ver seção 4)
  header.html              -- Header v2 (include, não macro -- é uma região inteira de página)
  footer.html               -- Footer v2 (idem)

vedium_core/vedium_core/www/
  design_system_v2.py      -- controller do preview (guarda de acesso, noindex, Fase B.3: query ?debug=1)
  design_system_v2.html    -- página de preview -- Fase B.3: dois modos (Presentation/Debug), ver seção 4

docs/redesign/
  10-design-system-v2-implementation.md  -- este arquivo
  11-component-migration-matrix.md       -- matriz de migração
  12-design-system-visual-qa.md          -- relatório de QA (B.1 estrutural + B.3 com screenshots reais)
  13-human-visual-review-checklist.md    -- checklist de revisão humana (Fase B.2)
  14-art-direction-v2.md                 -- NOVO (Fase B.3): princípios visuais, escala, fotografia, usos proibidos
```

Nenhum arquivo de produção fora de `v2/` foi modificado em nenhuma das quatro fases.

## 2. Arquitetura

- **Renderização**: 100% server-side via Jinja, sem runtime paralelo (sem Next.js/React/jQuery/Select2/Slick). `design_system_v2.html` é um documento HTML completo e autônomo (mesmo padrão de `curso.html`/`index.html` -- não estende `templates/base.html`), então **não herda `app_include_css`/`web_include_css` do site legado automaticamente**: isolamento real, não apenas por convenção de nome de classe.
- **Componentes = macros Jinja**. Frappe/Jinja não tem componentes com props como React; o equivalente idiomático é `{% macro %}` com parâmetros (e `{% call %}` para os que envolvem conteúdo, como `Container`/`Section`/`Alert`/`FormField`/`Modal`). Isso preserva 100% SSR, zero dependência nova, e é compatível com o restante do app.
- **CSS namespaced**: toda regra vive sob `.v2-scope` ou usa prefixo `.v2-*`, nunca seletor de elemento cru (`h1{}`, `button{}`, `img{}`, `a{}`) — não pode vazar pro CSS legado nem ser atropelado por ele.
- **JS vanilla, opt-in**: `design-system-v2.js` não é registrado em `web_include_js` (isso aplicaria a TODO o site) -- é carregado só pela própria página de preview.
- **Fase B.3, NOVO — dois modos na mesma rota, gated no Jinja (não só via CSS)**:
  - `/design_system_v2` (**Presentation mode**, padrão): só a experiência visual — Header v2 + 13 seções editoriais com fotografia e copy real da Vedium + Footer v2. Nenhum nome técnico de componente, nenhuma nota de implementação.
  - `/design_system_v2?debug=1` (**Debug mode**): tudo do Presentation mode **mais** uma "Component Library" no fim da página (depois do Footer, como apêndice) — biblioteca atômica completa, teste multilíngue/RTL, teste de conteúdo extremo.
  - O modo é decidido em `design_system_v2.py` (`context.debug_mode = frappe.form_dict.get("debug") in (...)`) e a Component Library inteira fica dentro de `{% if debug_mode %}...{% endif %}` no `.html` — em Presentation mode, esse HTML **nem é enviado ao navegador** (confirmado: 47,8 KB vs 92 KB renderizados), não é só escondido via CSS.

## 3. Tokens

Fonte original: `docs/redesign/04-design-system-plan.md` (seção 2-5). Cor e contraste validados na Fase B (ver `color-border-strong`, `#8C260F`/`#2E6DA4` conferidos contra o logo/tema atual).

### Tipografia -- decisão aprovada na Fase B.1, ESCALA aprovada na Fase B.3

A Fase B.1 aprovou a família: **Poppins (títulos/interface) + Inter (corpo/UI) + Arial (fallback) + Playfair Display (editorial seletivo, nunca estrutural)**. A Fase B.3 aprovou a **escala** (a Fase B usava uma escala pequena — a revisão humana classificou o resultado como "parecendo documentação de código"):

| Token novo | Faixa fluida (`clamp`) | Substitui |
|---|---|---|
| `--v2-text-h1` | ~38px → 72px | `.v2-h1` (antes `--v2-text-3xl`, 32-48px) |
| `--v2-text-h2` | ~30px → 48px | `.v2-h2` (antes `--v2-text-2xl`, 28px fixo) |
| `--v2-text-h3` | 24px → 32px | `.v2-h3` (antes `--v2-text-xl`, 22px fixo) |
| `--v2-text-base` | 16px → 17px | corpo (antes 16px fixo) |
| `--v2-text-lg` | 17px → 19px | lead/intro (antes 19px fixo) |

Container principal (`--v2-container-content`) foi de 1120px para **1180px** (faixa pedida: 1180–1280px). `--v2-space-section` (padding vertical de seção) foi de `clamp(48px,...,96px)` para `clamp(56px,...,128px)`. `--v2-control-height` (nova, 48px) para botões/inputs — o alvo mínimo de toque (`--v2-tap-min`, 44px) continua existindo só para os botões `compact`.

**Playfair Display** continua auto-hospedada localmente (3 subsets, `@font-face` em `tokens.css`), sem link remoto. **Poppins/Inter ainda não existem localmente** — o fallback Arial permanece ativo (ver seção 12).

### Paleta -- disciplina de uso corrigida na Fase B.3

A Fase B usava terracota (`--v2-color-accent`) como cor padrão de **todo** `.v2-eyebrow` (label pequeno acima de título) em `foundations.css`. A missão B.3 (seção 6) apontou isso como excesso: "terracota não deve aparecer em todos os labels/badges/títulos pequenos". `.v2-eyebrow` agora usa **azul institucional** (`--v2-color-brand-700`) por padrão; existe uma classe `.v2-eyebrow--accent` para os pontos raros que realmente merecem destaque terracota. Terracota ficou reservada a: 1 CTA primário por seção, badge "mais escolhido" do StudyRhythm, e o hover dos links textuais.

## 4. Componentes

**12 base** (inalterados desde a Fase B): Container, Section, Button/LinkButton, Badge, Breadcrumb, FormField, Input, Select, Alert, Modal, Icon.

**Editoriais (Fase B.3 — 5 novos, os demais redesenhados)**:

| Componente | Situação na B.3 |
|---|---|
| `LanguageMosaic` | **NOVO** — grid de ritmo editorial (cards `lg`/`md`/`sm`), substitui o uso solto de `LanguageCard` em grid uniforme na home/hub. |
| `LevelJourney` | **NOVO** — seção inteira (timeline grande + painel do nível selecionado), padrão ARIA tablist com teclado (setas/Home/End), progressive enhancement (sem JS, todos os painéis ficam visíveis). |
| `TeacherFeature` | **NOVO** — composição 50/50 grande, professor como protagonista de seção (não card de grade). |
| `LiveClassExperience` | **NOVO** — uma das "assinaturas visuais" pedidas pela missão; lista editorial (não cards), mídia grande opcional. |
| `StudyRhythmCard` | **NOVO**, substitui `PricingCard` — sem parâmetro de preço (removido, não só condicional); frequência (1-5 aulas/semana) é dado real (`frequency_pricing_rules.py`), nunca número inventado. |
| `HeroSplit`/`HeroCentered`/`HeroFullBleed` | Redesenhados: escala maior, `min-height` institucional no desktop, mídia ocupa a altura real (não `aspect-ratio` fixo pequeno). |
| `ProofBar` | Redesenhado: beneficios com título+texto (nunca mais números soltos tipo "5"/"100%"), sem caixa, divisor vertical discreto. |
| `LanguageCard` | Redesenhado: imagem 4:5 maior, nome grande, CTA textual. |
| `CourseCard` | Redesenhado: **preço removido do macro** (não só condicional — o parâmetro não existe mais), nível vira texto discreto, CTA textual. |
| `TeacherCard`/`TeacherProfileSummary` | Fallback sem foto trocado de "avatar com letra" (proibido pela missão) para o mesmo estado elegante "sem mídia" dos demais componentes. |
| `ProcessSteps` | Números grandes com baixa opacidade (antes: círculo preenchido pequeno). |
| `FeatureMedia` | 55/45 (antes 50/50), CTA vira link textual. |
| `TestimonialCard` | Avatar removido do macro (nunca teve estrelas); editorial, aspas grandes em Playfair. |
| `FAQAccordion` | Texto maior (17-18px), mais espaço, ícone mais discreto (rotação em vez de "+"). |
| `BlogCard` | Variante `featured` (imagem 16:10, título maior) para 1 destaque + N menores. |
| `CTASection` | Nova variante `--brand` (fundo azul institucional); secundário vira link textual. |
| `v2_text_link` | **NOVO helper**, usado por quase todos os CTAs secundários acima ("Conheça a trilha →"). |

**Header v2 e Footer v2**: ver seção 8 (atualizada na B.3).

Todos recebem dado por parâmetro -- nenhum tem professor, preço, depoimento, data ou nível fixo no macro.

## 5. Como usar

```jinja
{% import "templates/includes/v2/macros_base.html" as v2 %}
{% import "templates/includes/v2/macros_editorial.html" as v2e %}

{{ v2.v2_button("Matricular", href="/matricula", variant="primary") }}

{{ v2e.v2_course_card(
  title="Inglês A1", outcome="...", href="/curso/ingles-basico-a1",
  image_src="...", image_alt="...", level_label="A1"
) }}
```

Ver `www/design_system_v2.html` para um exemplo completo. Em Presentation mode ele mostra a composição de página real; em `?debug=1`, também a biblioteca atômica de cada componente isolado.

## 6. Dependências

**Nenhuma nova instalada, nenhuma remota.** CSS/JS 100% próprios (vanilla). Zero requisição a domínio externo de fonte (Playfair auto-hospedada, Poppins/Inter em fallback Arial até serem licenciadas). Para a QA visual desta fase (ver seção 9 e `12-design-system-visual-qa.md`), foi usado o **Google Chrome já instalado no ambiente** em modo headless (`--headless --disable-gpu`) mais o **Chrome DevTools Protocol** (WebSocket, via um script Node curto usando o `WebSocket`/`fetch` nativos do Node 22 já instalado) — nenhum pacote novo (`npm install`, `pip install`) foi adicionado ao projeto; é uso de uma capacidade já embutida em software já presente na máquina, não uma nova dependência do design system.

## 7. Acessibilidade

- Foco visível (`:focus-visible`, anel de 3px em `color-focus`, nunca removido sem substituto).
- `prefers-reduced-motion: reduce` zera todas as durações de transição/animação (tokens + regra global).
- Landmarks semânticos: `<header>`, `<nav>`, `<footer>` nos componentes de Header/Footer v2.
- FAQAccordion: botão real (`<button>`), `aria-expanded`, `aria-controls`, painel com `role="region"` e `aria-labelledby`; funciona sem JS.
- Modal: `role="dialog"`, `aria-modal`, `aria-labelledby`, foco preso (`Tab`/`Shift+Tab`), `Escape` fecha, foco retorna ao elemento que abriu.
- **LevelJourney (Fase B.3, novo)**: padrão `role="tablist"`/`role="tab"`/`role="tabpanel"`, `aria-selected`, setas esquerda/direita/Home/End trocam o painel e movem o foco (ver `design-system-v2.js`, `initLevelJourney`). Sem JS, todos os painéis de nível ficam visíveis empilhados (fallback seguro, nenhum conteúdo depende de JS para existir).
- Hierarquia de heading corrigida na B.3: `TeacherFeature`/`TeacherCard` tinham o nome do professor num `<p>` estilizado (não uma heading real) — agora usam `<h2>`/`<h3>` conforme o nível da seção, mantendo landmarks coerentes (regra de `04-design-system-plan.md` seção 11).
- **Achado corrigido na Fase B (mantido)**: os 3 macros de Hero renderizavam `<h1>` fixo; corrigido com parâmetro `heading_level`. Em Presentation mode (B.3), o Hero real da página usa `heading_level="h1"` (é o único H1 real da página agora — antes, na galeria da Fase B, nenhum Hero era o H1 de verdade).
- **Meta inicial**: WCAG 2.2 AA, sem alegar conformidade auditada — validação até a B.2 foi só por código; a **B.3 adicionou verificação visual real** (screenshots via Chrome headless) que pegou e corrigiu 1 bug de contraste real (ver seção 9) — ainda não é auditoria com leitor de tela nem ferramenta tipo axe-core/WAVE.

## 8. Header v2 e Footer v2 -- contrato preservado, lógica de locale NÃO reimplementada

Conforme instrução explícita da missão ("Não implementar uma lógica nova de locale nesta fase"):
- O Header v2 aceita as **mesmas duas variáveis de contexto** que o header atual usa pro CTA de teste de nível dinâmico (`vd_level_test_url_override`/`vd_level_test_contact_override`) -- mesmo fallback por idioma, mesma troca de rótulo pra "Fale conosco" quando aplicável.
- O botão de idioma do Header v2 já carrega os atributos de dado real que `vedium-language.js` sabe ler (`data-vd-nav-current`, `data-vd-nav-urls`) -- a lógica de troca de idioma em si **não foi portada nem reimplementada**.
- **Fase B.3**: o botão de idioma trocou a bandeira remota (`flagcdn.com`) por um rótulo textual — bandeira ≠ idioma (vários países falam o mesmo idioma) e era a única dependência de asset externo que restava no sistema; removida por consistência com a regra "nenhum asset remoto" já aplicada às fontes.
- **Fase B.3**: altura do header (76-88px), logo maior, mega menu reorganizado em 2 colunas (idiomas + atalhos institucionais "Para empresas"/"Fazer teste de nível") com uma pequena imagem editorial — ver seção 24 da missão. "Para empresas" continua também como item de topo da navegação (pedido explícito da missão em duas seções diferentes, não uma duplicação acidental).
- WhatsApp: mesmo número (+55 11 91129-3075) e mesmo texto pré-codificado já usado hoje.
- Footer: legal (Termos/Privacidade/Cookies/Cancelamento) continua hardcoded em português. **Fase B.3**: adicionada mensagem institucional curta acima da grade de colunas, mais espaço no topo (`padding-block-start` de 80px/96px para 160px/192px conforme breakpoint).

## 9. Responsivo (mobile first) -- Fase B.3: teste visual real feito, com correção de metodologia registrada

A Fase B.1/B.2 não tinham acesso a nenhuma ferramenta de automação de navegador. A Fase B.3 usou o **Google Chrome já instalado na máquina em modo headless** via Chrome DevTools Protocol para capturar screenshots reais em 390px, 768px e 1440px.

**Achado importante sobre metodologia**: a primeira tentativa usou `chrome --headless --window-size=390,20000 --screenshot`, que produziu screenshots com **conteúdo cortado na borda direita** (parecia um bug real de overflow horizontal). Investigação via CDP (`Emulation.setDeviceMetricsOverride` + medição de `document.body.scrollWidth`) mostrou que **não havia overflow real** — o `--window-size` sozinho, sem `mobile: true` explícito no device metrics, faz o Chrome herdar um viewport de layout largo (assunção "desktop", ~980px) mesmo com uma janela estreita, então o PNG capturado só recorta visualmente os primeiros 390px de um layout desenhado para uma tela mais larga. O método correto (`Emulation.setDeviceMetricsOverride({width:390, mobile:true})` antes de `Page.captureScreenshot`) confirmou **nenhum overflow real** em 390/768/1440px — hero empilha e os dois CTAs viram botões full-width, ProofBar vira 2×2, LanguageMosaic empilha em coluna única, o menu mobile (hambúrguer) aparece corretamente abaixo de 992px, e a timeline do LevelJourney vira uma faixa `overflow-x: auto` (rolagem horizontal **intencional**, não um bug — única "ultrapassagem de viewport" real encontrada, e é por design).

**Bug real encontrado e corrigido nesta fase**: o título do `CTASection` variante `--brand` renderizava em tinta escura (`.v2-heading` fixa `color: var(--v2-color-text)`) sobre o fundo azul institucional escuro — quase ilegível. Confirmado por screenshot real, corrigido com `.v2-cta-section--brand .v2-cta-section__title { color: var(--v2-color-surface-0); }`.

Ver `12-design-system-visual-qa.md` para as capturas e a lista completa do que foi verificado.

## 10. Locale / RTL

- Propriedades lógicas usadas consistentemente (`margin-inline`, `padding-inline`, `inset-inline-start/end`) -- os componentes funcionam em `dir="rtl"` sem CSS separado.
- `FeatureMedia--reverse` usa `order` do grid (não `direction: rtl`) desde a Fase B.
- Exemplo real de hebraico (`lang="he" dir="rtl"`) renderizado no Component Library (debug mode), incluindo a troca de fonte via `:lang(he)` e um componente real (`FeatureCard`) em RTL — confirmado visualmente por screenshot na B.3 (checkmarks e alinhamento no lado correto).
- **Não foi lançada nenhuma página RTL nova** (fora do escopo desta fase).

## 11. Mídia -- Fase B.3: fotografia real integrada, seguindo a governança de 06/07/08

A Fase B/B.1 tratavam mídia como "componente + opcional" com um SVG abstrato como referência de proporção. A missão B.3 (princípio central, seção 2) exigiu o oposto: fotografia como parte da composição desde o início. Implementado assim:

- **4 derivados locais** gerados a partir de assets Envato já classificados em `07-envato-asset-inventory.csv`, usando o **Python + Pillow já presentes no ambiente `bench`** (nenhuma instalação nova) via `docker exec` no container de desenvolvimento: `e07-hero-videoconference.jpg`, `e02-study-laptop.jpg`, `e06-listening-online-course.jpg`, `e10-notes-at-home.jpg` — redimensionados (máx. 2000px no lado maior, JPEG qualidade 82, ~220-300 KB cada) a partir dos masters de 12-29 MB. **Nenhum master Envato foi commitado** — os derivados vivem em `vedium_core/vedium_core/public/v2-preview-media/`, ignorado via `.git/info/exclude` (mesmo padrão já usado para `vedium-references/`).
- **Alocação por página segue `08-page-media-map.md` linha a linha**: E07 (Home hero + bloco institucional B2B — doc recomenda os dois), E02 (Inglês), E06 (PLE, "ponte neutra" conforme o doc), E10 (LiveClassExperience + BlogCard, categoria D/SUPPORT).
- **Gate cultural respeitado**: Iorubá, Espanhol e Hebraico **não** receberam nenhuma foto no LanguageMosaic — `06-photography-system.md` bloqueia explicitamente qualquer asset atual como hero/prova de Iorubá ("nenhuma pessoa stock pode representar Iorubá por aparência"), e não há asset estático (não-vídeo) aprovado para Espanhol; por consistência e para não repetir a mesma pessoa como se representasse vários cursos, Hebraico também ficou sem foto nesta fase. Os três usam o estado elegante "sem mídia" — uma nota visível no Presentation mode explica isso ao revisor.
- **`LiveClassExperience` não usa stock para simular "aula ao vivo real"**: `08-page-media-map.md` marca a promessa "ao vivo de verdade" como **P0 — REAL VEDIUM REQUIRED** (não deve ser publicada com stock no papel principal). A imagem usada ali (E10) é rotulada como apoio ambiental genérico, não como prova; o texto do componente descreve o processo pedagógico (verdadeiro em geral), não afirma "isto é uma aula Vedium".
- **Alt text**: literal e descritivo, sem atribuir identidade/nacionalidade/vínculo não comprovado (padrão de `06-photography-system.md` seção 10, ex.: "Pessoa adulta participa de uma videochamada profissional..."), nunca "nosso professor"/"nossa aula".
- **`object-position` por imagem**: `HeroSplit`/`LanguageCard` ganharam parâmetro `object_position` (usado no hero: `right center` para E07, seguindo a recomendação de crop do próprio `06-photography-system.md` para esse asset).
- **Prof. Almir Soares da Silva** continua o único "REAL VEDIUM" do sistema (`TeacherFeature`, `TeacherCard`) — mesma foto autorizada de uma sessão anterior desta branch.
- **Ainda não validado**: crop de rosto/mãos pixel-a-pixel contra os *envelopes* exatos da tabela da seção 7 de `06-photography-system.md` (os derivados usam resize simples + `object-fit: cover` no CSS, não um crop pré-calculado por breakpoint) — aceitável para uma fase de preview, mas é trabalho pendente antes de qualquer publicação real (ver `09-real-vedium-shoot-list.md`, que já está R0x/P0 para todo REAL VEDIUM que falta).

## 12. Limitações desta fase

1. Poppins/Inter ainda não auto-hospedadas (não existem localmente) -- fallback Arial em uso; Playfair Display já resolvida.
2. Lógica de locale switching **não portada** -- Header v2 só carrega o contrato de dado, não troca idioma de fato.
3. `Testimonials`/`VideoSection` não têm conteúdo real disponível ainda -- o preview demonstra o formato com dado fictício claramente rotulado como exemplo.
4. Nenhum componente foi testado dentro de uma página Frappe real com dado de produção (só o preview isolado, embora rodando dentro do bench real desde a B.2 — não mais só `jinja2.Environment` fora do bench).
5. Sem auditoria de acessibilidade com ferramenta real (axe/WAVE) nem leitor de tela — só teclado/ARIA por inspeção de código e teste manual do padrão tablist.
6. Crop de rosto/mãos pixel-a-pixel não validado (ver seção 11) -- os derivados de preview usam resize simples, não um crop por breakpoint calculado manualmente.
7. `LevelJourney` usa conteúdo pedagógico genérico (descrições padrão de CEFR por nível) como dado de exemplo -- a taxonomia pública A1-C1 já é a aprovada por `04-design-system-plan.md`, mas as descrições de cada nível ainda não foram revisadas por um pedagogo Vedium.
8. `LanguageMosaic`: Iorubá, Espanhol e Hebraico sem fotografia própria autorizada nesta fase (ver seção 11) -- bloqueio de governança, não uma omissão técnica.

## 13. Próximos passos sugeridos

1. Providenciar Poppins/Inter (licença + arquivos `.woff2`) e auto-hospedar, seguindo o padrão já usado para Playfair Display.
2. Auditoria de acessibilidade real (teclado, leitor de tela, zoom 200%, reflow 320px) nos fluxos de FAQ/Modal/Form/LevelJourney.
3. Aprovar a taxonomia CEFR pública (A1/A2/B1/B1+/B2/C1) e revisar pedagogicamente as descrições de nível usadas no `LevelJourney`.
4. Produzir/aprovar fotografia real (R01-R09 de `09-real-vedium-shoot-list.md`) para substituir o stock temporário -- prioridade: Iorubá (gate cultural, zero asset hoje), Inglês (R05, professor real), aula ao vivo (R01/R02).
5. Crop manual por breakpoint dos assets aprovados, seguindo a tabela de `06-photography-system.md` seção 7 (hoje só resize + `object-fit: cover`).
6. Ver `11-component-migration-matrix.md` para o plano de migração página por página, `12-design-system-visual-qa.md` para o relatório de QA completo (B.1 + B.3) e `14-art-direction-v2.md` para os princípios visuais que qualquer novo componente deve seguir.
