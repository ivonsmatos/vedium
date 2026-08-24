# 10 — Implementação do VEDIUM DESIGN SYSTEM V2 (Fase B + B.1)

> **Escopo da Fase B (2026-08-24):** fundação isolada do design system, na stack real (Frappe SSR + Jinja + CSS/JS próprios). Nenhuma página pública existente foi alterada, substituída ou teve sua rota/redirect/controller/DocType/checkout/teste de nível/GTM/CRM/Stripe/Nginx modificados. Nenhum deploy foi feito.
>
> **Atualizado na Fase B.1 (mesmo dia):** QA visual/marca/responsividade. Ver `docs/redesign/12-design-system-visual-qa.md` para o relatório completo da B.1 -- este documento reflete só as DECISÕES FINAIS incorporadas (tipografia, mídia, cor, botões), não repete o relatório de QA inteiro.

## 1. Arquivos criados

```
vedium_core/vedium_core/public/css/v2/
  tokens.css               -- variáveis CSS (cor, tipografia, espaço, raio, sombra, container, motion)
  foundations.css          -- reset escopado (.v2-scope), tipografia utilitária, container/section/grid, sr-only
  components-base.css      -- Button, LinkButton, Badge, Breadcrumb, Form (Field/Input/Select), Alert, Modal, Icon
  components-editorial.css -- Hero(3), ProofBar, FeatureCard, LanguageCard, CourseCard, LevelCard/Timeline,
                               TeacherCard/Summary, ProcessSteps, FeatureMedia, VideoSection, TestimonialCard,
                               PricingCard, FAQAccordion, BlogCard, CTASection
  header-footer.css        -- Header v2 e Footer v2 (componentes isolados)

vedium_core/vedium_core/public/js/v2/
  design-system-v2.js      -- JS vanilla progressivo: menu mobile, accordion do FAQ, modal base

vedium_core/vedium_core/templates/includes/v2/
  macros_base.html         -- macros Jinja dos 12 componentes base
  macros_editorial.html    -- macros Jinja dos 19 componentes editoriais
  header.html              -- Header v2 (include, não macro -- é uma região inteira de página)
  footer.html               -- Footer v2 (idem)

vedium_core/vedium_core/www/
  design_system_v2.py      -- controller do preview (guarda de acesso, noindex)
  design_system_v2.html    -- página de preview (galeria de todos os componentes)

docs/redesign/
  10-design-system-v2-implementation.md  -- este arquivo
  11-component-migration-matrix.md       -- matriz de migração
```

Nenhum arquivo existente do projeto foi modificado.

## 2. Arquitetura

- **Renderização**: 100% server-side via Jinja, sem runtime paralelo (sem Next.js/React/jQuery/Select2/Slick). `design_system_v2.html` é um documento HTML completo e autônomo (mesmo padrão de `curso.html`/`index.html` -- não estende `templates/base.html`), então **não herda `app_include_css`/`web_include_css` do site legado automaticamente**: isolamento real, não apenas por convenção de nome de classe.
- **Componentes = macros Jinja**. Frappe/Jinja não tem componentes com props como React; o equivalente idiomático é `{% macro %}` com parâmetros (e `{% call %}` para os que envolvem conteúdo, como `Container`/`Section`/`Alert`/`FormField`/`Modal`). Isso preserva 100% SSR, zero dependência nova, e é compatível com o restante do app.
- **CSS namespaced**: toda regra vive sob `.v2-scope` ou usa prefixo `.v2-*`, nunca seletor de elemento cru (`h1{}`, `button{}`, `img{}`, `a{}`) — não pode vazar pro CSS legado nem ser atropelado por ele.
- **JS vanilla, opt-in**: `design-system-v2.js` não é registrado em `web_include_js` (isso aplicaria a TODO o site) -- é carregado só pela própria página de preview. Cobre menu mobile, accordion do FAQ e modal; tudo funciona sem JS (fallback `<noscript>` no FAQ; menu mobile do Header vira lista sempre visível).

## 3. Tokens

Fonte: `docs/redesign/04-design-system-plan.md` (seção 2-5), **validados nesta fase**:
- **Cor**: confrontados visualmente com o logo oficial (`Logo-color-quadrada.png`) -- confirma a paleta azul/terracota do 04 é a mesma do logo real, não uma paleta inventada. `#8C260F` (accent-700) já aparece literalmente em `vedium_assets/css/vedium.css` hoje, e `#2E6DA4` já é `app_theme_color` em `hooks.py` -- os tokens não são uma ruptura com a marca atual.
- **Contraste WCAG**: todos os pares texto/fundo usados pelos componentes (branco sobre brand-600/700, accent-600/700, success/warning/danger; ink-900/700/500 sobre branco) passam AA (≥4.5:1 texto normal, ≥3:1 texto grande/UI) -- ratios calculados nesta fase (fórmula de luminância relativa padrão WCAG). Único achado: `color-border` (#D9DEE3) tem 1.35:1 contra branco -- **não atinge nem o mínimo de 3:1 para bordas funcionais** (WCAG 1.4.11). Criado `color-border-strong` (#7C8794, 3.6:1) como token novo desta fase para bordas de input/card interativo; `color-border` fica só para divisores puramente decorativos.

Escala de tipografia, espaçamento (base 4px), raio, sombra (máx. 3 níveis), containers (reading/content/wide/full) e grid (4/8/12) implementados exatamente como especificado em 04.

### Tipografia -- DECISÃO FINAL APROVADA na Fase B.1

`docs/redesign/04-design-system-plan.md` (seção 3) havia escolhido **Kumbh Sans** para interface/corpo. A Fase B.1 trouxe a decisão aprovada oficialmente (Manual de Tom de Voz): **Poppins (títulos/interface) + Inter (corpo/UI) + Arial (fallback) + Playfair Display (editorial seletivo, nunca estrutural)**. Kumbh Sans **não é mais a fonte principal** -- conflito da Fase B está resolvido por decisão humana explícita, não por escolha do design system.

**Verificação de arquivos locais (Fase B.1, sem baixar nada)**:
- **Playfair Display 700** (latin/latin-ext/cirílico) já existia localmente (`vedium_core/public/fonts/*.woff2`, licença OFL 1.1) -- agora **auto-hospedada de verdade** via `@font-face` em `tokens.css`, sem nenhum link remoto.
- **Poppins e Inter NÃO existem localmente neste projeto.** Nenhum download foi feito (fora do escopo desta fase). Até serem licenciadas/auto-hospedadas, a pilha cai no fallback **Arial** -- comportamento correto e visível no preview (alerta explícito na seção Typography). **Requisito documentado antes de produção**: providenciar os arquivos `.woff2` (subset latin/latin-ext/cirílico no mínimo) e declarar `@font-face` local no mesmo padrão do Playfair.
- **Kumbh Sans** (arquivos já presentes: `kumbh-sans-latin.woff2`, `kumbh-sans-latin-ext.woff2`) permanece no repo sem uso nesta decisão.
- **Nenhuma fonte remota**: o `<link>` do Google Fonts que existia na Fase B foi **removido** da página de preview na B.1 (regra explícita: evitar `@import`/link remoto em produção).

Cobertura de script verificada:
- Poppins/Inter cobrem Latim (incl. estendido -- testado com exemplo de Iorubá: diacríticos e dígrafos) e Cirílico (russo) -- verificação por especificação conhecida das famílias, não glifo-a-glifo (arquivos ainda não estão no projeto pra testar ao vivo).
- **Nem Poppins nem Inter cobrem hebraico.** Resolvido com regra `:lang(he)` em `tokens.css`, que troca a pilha para `"Noto Sans Hebrew", "Arial Hebrew", "David", Arial` -- testado na seção Typography do preview com texto hebraico real, `dir="rtl"`, e também num componente real (`FeatureCard`) renderizado em RTL (Fase B.1).

## 4. Componentes

**12 base**: Container, Section, Button/LinkButton, Badge, Breadcrumb, FormField, Input, Select, Alert, Modal, Icon.
**19 editoriais**: HeroSplit, HeroCentered, HeroFullBleed, ProofBar, FeatureCard, LanguageCard, CourseCard, LevelCard, LevelTimeline, TeacherCard, TeacherProfileSummary, ProcessSteps, FeatureMedia, VideoSection, TestimonialCard, PricingCard, FAQAccordion, BlogCard, CTASection.
**Header v2 e Footer v2**: componentes isolados (ver seção 8).

Todos recebem dado por parâmetro -- nenhum tem professor, preço, depoimento, data ou nível fixo no macro. Regras de negócio herdadas de `04-design-system-plan.md`:
- `CourseCard` só mostra preço quando `price` **e** `price_period` vêm preenchidos juntos (nunca um número solto sem periodicidade).
- `ProofBar` aceita no máximo 4 itens (`items[:4]`); a responsabilidade de só passar fatos com fonte auditável é de quem chama o macro, não do macro.
- `TeacherCard`/`TeacherProfileSummary` sem `image_src` caem num fallback com a inicial do nome -- nunca renderizam foto de banco de imagens como se fosse um professor real.

## 5. Como usar

```jinja
{% import "templates/includes/v2/macros_base.html" as v2 %}
{% import "templates/includes/v2/macros_editorial.html" as v2e %}

{{ v2.v2_button("Matricular", href="/matricula", variant="primary") }}

{{ v2e.v2_course_card(
  title="Inglês A1", outcome="...", href="/curso/ingles-basico-a1",
  image_src="...", image_alt="...", level_badge="A1",
  price="R$ 240", price_period="/mês"
) }}
```

Ver `www/design_system_v2.html` para um exemplo completo de uso de todos os 31 componentes.

## 6. Dependências

**Nenhuma nova, nenhuma remota.** CSS/JS 100% próprios (vanilla). Desde a Fase B.1, **zero requisição a domínio externo de fonte**: o `<link>` do Google Fonts foi removido; Playfair Display 700 é auto-hospedada local; Poppins/Inter ainda não têm arquivo local (ver seção 3) e usam o fallback Arial da própria pilha até serem licenciadas -- não um link remoto temporário.

## 7. Acessibilidade

- Foco visível (`:focus-visible`, anel de 3px em `color-focus`, nunca removido sem substituto).
- `prefers-reduced-motion: reduce` zera todas as durações de transição/animação (tokens + regra global).
- Landmarks semânticos: `<header>`, `<nav>`, `<footer>` nos componentes de Header/Footer v2.
- FAQAccordion: botão real (`<button>`), `aria-expanded`, `aria-controls`, painel com `role="region"` e `aria-labelledby`; funciona sem JS (conteúdo visível por padrão via CSS, JS só adiciona o comportamento de accordion).
- Modal: `role="dialog"`, `aria-modal`, `aria-labelledby`, foco preso (`Tab`/`Shift+Tab`), `Escape` fecha, foco retorna ao elemento que abriu.
- Ícones puramente decorativos (`v2_icon(decorative=true)`, padrão) recebem `aria-hidden="true"`; ícones que substituem texto (ex. ícone social sozinho) usam `role="img"` + `aria-label`.
- **Achado corrigido durante esta própria fase**: os 3 macros de Hero renderizavam `<h1>` fixo. Empilhados na página de preview, isso geraria 4 `<h1>` na mesma página (regressão de acessibilidade real, pega ao renderizar o preview e verificar o HTML gerado). Corrigido com um parâmetro `heading_level` (padrão `"h1"`, hoje usado como `"h2"` na galeria) -- também é uma melhoria de API pensando na produção real, não só no preview: nem todo Hero é o H1 da página onde vai entrar.
- **Meta inicial**: WCAG 2.2 AA, sem alegar conformidade auditada (04-design-system-plan.md item 11) -- validação nesta fase foi automatizada (contraste calculado, estrutura de heading verificada no HTML renderizado) e por inspeção de código, **não** por leitor de tela real nem ferramenta tipo axe-core/WAVE (fora do escopo/acesso desta fase).

## 8. Header v2 e Footer v2 -- contrato preservado, lógica de locale NÃO reimplementada

Conforme instrução explícita da missão ("Não implementar uma lógica nova de locale nesta fase"):
- O Header v2 aceita as **mesmas duas variáveis de contexto** que o header atual usa pro CTA de teste de nível dinâmico (`vd_level_test_url_override`/`vd_level_test_contact_override`, aqui nomeadas `v2_level_test_url_override`/`v2_level_test_contact_override`) -- mesmo fallback por idioma, mesma troca de rótulo pra "Fale conosco" quando aplicável.
- O botão de idioma do Header v2 já carrega os atributos de dado real que `vedium-language.js` sabe ler (`data-vd-nav-current`, `data-vd-nav-urls`) -- a lógica de troca de idioma em si **não foi portada nem reimplementada**; o contrato de dado só está preparado para quando essa integração for aprovada.
- Menu simplificado conforme pedido: Logo · Cursos (mega menu: Inglês/Iorubá/PLE/Espanhol/Hebraico/Para empresas) · Como funciona · Professores · Para empresas · Blog · Entrar · CTA "Descubra seu nível" -- **mais enxuto que o header atual** (que tem também Início/Sobre/FAQ/Contato na barra principal); ver `11-component-migration-matrix.md` para a decisão de quais itens migram e quais ficam só no footer/rodapé no v2.
- WhatsApp: mesmo número (+55 11 91129-3075) e mesmo texto pré-codificado já usado hoje (reaproveitado literalmente do header/footer atuais, não gerado por filtro Jinja não verificado neste ambiente).
- Footer: legal (Termos/Privacidade/Cookies/Cancelamento) continua hardcoded em português -- mesma decisão já registrada em memória de projeto anterior, não uma omissão.

## 9. Responsivo (mobile first)

Breakpoints documentados em `tokens.css` (comentário, já que CSS puro não tem custom media sem PostCSS): 360 / 576 / 768 / 992 / 1200 / 1400px -- cobre os 7 pontos pedidos pela missão (360/375/390/430 caem dentro da faixa `< 576` e usam o layout mobile de base; 768/1024/desktop amplo mapeiam pra 768/992-1200/1400).

**Limitação desta fase**: a validação foi feita por leitura do CSS responsivo (grid 4→8→12 colunas, hero split empilhando em coluna única abaixo de 992px, mega menu virando painel mobile abaixo de 992px, cards de card-grid quebrando 1→2→3 colunas) e pela renderização HTML bem-sucedida do preview -- **não houve teste visual real em dispositivo/emulador** (sem acesso a browser automatizado nesta sessão). Títulos longos em alemão e nomes compridos foram exercitados no conteúdo de exemplo do preview (`"Brasilianisches Portugiesisch..."`, `"Idiomas para equipes que trabalham com o mundo"`) mas não capturados em screenshot.

## 10. Locale / RTL

- Propriedades lógicas usadas consistentemente (`margin-inline`, `padding-inline`, `inset-inline-start/end`, `text-align: start` via herança natural) em vez de `left`/`right` -- os componentes já funcionam em `dir="rtl"` sem CSS separado, na maioria dos casos.
- `FeatureMedia--reverse` foi corrigido durante esta fase: a primeira versão usava `direction: rtl` como truque de inversão visual, o que teria alterado a semântica de RTL real por engano. Corrigido para usar `order` do grid (efeito visual idêntico em LTR, sem interferir com uma página real em RTL).
- Exemplo real de hebraico (`lang="he" dir="rtl"`) renderizado na seção Typography do preview, incluindo a troca de fonte via `:lang(he)`.
- **Não foi lançada nenhuma página RTL nova** (fora do escopo desta fase, conforme instrução) -- só a prontidão estrutural.

## 11. Mídia

Seguidas as regras de `06-photography-system.md`/`07`/`08`/`09`:
- **Nenhum asset Envato foi copiado para produção nesta fase.**
- **Redesenhado na Fase B.1 (item 13)**: "sem mídia" agora é um **estado real e suportado do próprio componente**, não um placeholder de desenvolvimento. `HeroSplit`, `HeroFullBleed`, `CourseCard`, `FeatureMedia` e `VideoSection` ganharam `image_src`/`poster_src` **opcional** (`none` por padrão); sem imagem, renderizam `.v2-media-empty` -- fundo neutro (`surface-alt`) + ícone pequeno, `aria-hidden`, nunca um SVG fingindo ser foto. A galeria principal do preview demonstra esse estado como o comportamento padrão (não uma exceção).
- **Duas referências técnicas de proporção** (SVG abstrato, não fotográfico) seguem existindo, mas só na seção "Teste de conteúdo extremo" do preview, para validar `aspect-ratio`/`object-fit` com imagem vertical (4:5) e horizontal (4:3) de verdade -- rotuladas explicitamente como "referência técnica de proporção... não representa professor/aluno/aula Vedium" em todo uso.
- **Único exemplo de imagem real "REAL VEDIUM"** no preview: a foto autorizada do Prof. Almir Soares da Silva (já publicada na ficha do curso de PLE em sessão anterior desta mesma branch), usada no `TeacherCard`/`TeacherProfileSummary`.
- Aspect ratios por componente seguem a tabela da seção 7 de `06-photography-system.md` (HeroSplit 4:5/3:2, CourseCard 4:3, TeacherCard 4:5, BlogCard 3:2 etc.).
- `alt=""` só em imagens puramente decorativas (bandeiras do seletor de idioma, ícones, media-empty); imagens informativas recebem `alt` literal passado pelo chamador -- nenhum macro gera texto alternativo automaticamente.
- **Não validado nesta fase**: crop real de rosto/mãos com uma fotografia de verdade em tamanho de produção -- o asset de referência mais próximo disponível (E06, biblioteca Envato) tem 29,4 MB, incompatível com uso web, e não há ferramenta de processamento de imagem (PIL/Pillow) disponível neste ambiente para gerar um derivado seguro sem instalar dependência nova. Fica como pendência explícita, não como validação feita.

## 12. Limitações desta fase

1. ~~Conflito de tipografia~~ -- **RESOLVIDO na Fase B.1** (seção 3 acima).
2. Poppins/Inter ainda não auto-hospedadas (não existem localmente) -- fallback Arial em uso; Playfair Display já resolvida.
3. Sem teste visual real (browser/dispositivo) -- só validação estrutural via CSS + render HTML + auditoria de código por breakpoint (ver `12-design-system-visual-qa.md`). Confirmado na B.1: não há Playwright/Puppeteer/ferramenta de browser automation configurada neste projeto, e a instrução foi explícita em não instalar uma só para isso.
4. Sem auditoria de acessibilidade com ferramenta real (axe/WAVE) nem leitor de tela.
5. Lógica de locale switching **não portada** -- Header v2 só carrega o contrato de dado, não troca idioma de fato.
6. `Testimonials`/`VideoSection` não têm conteúdo real disponível ainda (aguardando aprovação de depoimentos e captação real -- ver `09-real-vedium-shoot-list.md`), então o preview só demonstra o formato com dado fictício rotulado como exemplo.
7. Nenhum componente foi testado dentro de uma página Frappe real renderizada (o teste de renderização desta e da B.1 usou `jinja2.Environment` com `FileSystemLoader` fora do bench -- reproduz o parser/render Jinja padrão, mas não o ambiente completo de contexto/hooks do Frappe; recomendado um smoke test real via `bench` antes da Fase C).
8. Crop de rosto/mãos com fotografia real não validado (ver seção 11) -- asset de referência disponível é grande demais (29,4 MB) e não há ferramenta de processamento de imagem no ambiente.

## 13. Próximos passos sugeridos

1. Providenciar Poppins/Inter (licença + arquivos `.woff2`) e auto-hospedar, seguindo o padrão já usado para Playfair Display.
2. Rodar o preview num ambiente `bench` real (smoke test verdadeiro, não só `jinja2.Environment`).
3. Auditoria de acessibilidade real (teclado, leitor de tela, zoom 200%, reflow 320px) nos fluxos de FAQ/Modal/Form.
4. Teste visual em dispositivo/navegador real nos 8 breakpoints (360 a 1440px) -- ver metodologia de auditoria por código em `12-design-system-visual-qa.md`, que substitui screenshot real nesta fase.
5. Aprovar a taxonomia CEFR pública (A1/A2/B1/B1+/B2/C1) antes de conectar `LevelTimeline`/`LevelCard` a dado real.
6. Providenciar um asset fotográfico real em tamanho web (não os 29 MB brutos do Envato) para validar crop/safe-area de verdade.
7. Ver `11-component-migration-matrix.md` para o plano de migração página por página, faseado, e `12-design-system-visual-qa.md` para o relatório completo de QA da Fase B.1.
