> **IMPORTANTE:**
>
> - O único projeto que pode receber novos arquivos é `vedium`.
> - `edumon` e `eduall` são referências SOMENTE PARA LEITURA.
> - Não modifique nenhum arquivo dentro de `edumon` ou `eduall`.
> - Nesta fase, não modifique nenhum arquivo existente do projeto `vedium`.
> - A única escrita permitida é criar os 5 arquivos solicitados em `vedium/docs/redesign/`.

# 04 — Plano do design system

## 1. Direção

O novo sistema deve comunicar ensino de idiomas ao vivo, progressão acompanhada, repertório cultural e proximidade com professores. A percepção desejada é adulta, humana, confiável e contemporânea — não uma loja de cursos, uma plataforma infantil ou uma cópia do Edumon.

Princípios:

- conteúdo e pessoas reais antes de ornamento;
- progressão compreensível antes de abundância de opções;
- mobile first, com ações primárias sempre claras;
- consistência entre marketing, matrícula e entrada no produto;
- acessibilidade tratada como requisito de componente;
- SEO, analytics e conversão tratados como contratos do sistema;
- movimento discreto e dispensável;
- nenhum número, avaliação, depoimento ou selo sem fonte verificável.

## 2. Tokens de cor propostos

Os valores abaixo partem das cores encontradas no site atual e permanecem **candidatos**, não tokens aprovados nem autorização de implementação. Antes de qualquer uso, cada cor deve ser confrontada com os logos, arquivos de marca e demais ativos oficiais da Vedium e passar por validação de contraste WCAG nos pares e estados reais.

| Token semântico | Valor inicial | Uso previsto |
|---|---:|---|
| `color-brand-800` | `#1D416F` | Texto/ícones de marca em fundo claro |
| `color-brand-700` | `#26528C` | Header, links fortes, estados ativos |
| `color-brand-600` | `#2E6DA4` | Ações secundárias e elementos institucionais |
| `color-brand-300` | `#84A9D9` | Fundos e detalhes de apoio |
| `color-accent-700` | `#8C260F` | CTA principal e destaque com uso moderado |
| `color-accent-600` | `#A12D1C` | Hover/variante a validar por contraste |
| `color-warm-400` | `#BFA288` | Fundos editoriais e detalhes culturais |
| `color-ink-900` | `#0F1419` | Texto principal |
| `color-ink-700` | `#35404A` | Texto secundário |
| `color-ink-500` | `#66717C` | Metadados, se contraste permitir |
| `color-surface-0` | `#FFFFFF` | Superfície principal |
| `color-surface-50` | `#F7F8FA` | Alternância de seções |
| `color-surface-warm` | `#F6F1EC` | Blocos editoriais quentes |
| `color-border` | `#D9DEE3` | Bordas e divisores |
| `color-success` | `#247A4A` | Sucesso confirmado; verde deixa de ser cor primária |
| `color-warning` | `#9A5B00` | Avisos |
| `color-danger` | `#B42318` | Erros e ações destrutivas |
| `color-focus` | `#1463FF` | Anel de foco de alta visibilidade |

Regras:

- texto normal deve atingir WCAG AA (4,5:1); texto grande e controles, no mínimo 3:1;
- validar contraste de texto, ícone, borda, foco, hover, disabled e mensagem de estado; não aprovar a paleta apenas por amostras isoladas;
- CTA terracota precisa de validação com texto branco e em todos os estados;
- informação nunca depende somente de cor;
- tons claros da marca servem a superfícies, não a texto pequeno;
- o verde legado só permanece para semântica de sucesso, após inventário de ocorrências.

## 3. Tipografia

### Família

- Display: `Playfair Display` apenas de forma seletiva/editorial, em títulos onde a voz de marca justificar; não usar como fonte geral de interface.
- Interface e corpo: `Kumbh Sans`, também local, para navegação, corpo, botões e formulários.
- Fallback: pilhas de fontes de sistema por script. Antes da implementação, verificar cobertura real de todos os idiomas existentes, incluindo latim estendido, cirílico, hebraico e demais alfabetos necessários.
- Legibilidade, consistência de interface e estabilidade entre locales têm prioridade sobre personalidade tipográfica.
- Não manter Kanit, Inter e Bodoni Moda simultaneamente apenas por legado; consolidar depois da auditoria visual.
- Evitar dependência de Google Fonts no caminho crítico.

### Escala fluida inicial

| Token | Faixa proposta | Uso |
|---|---|---|
| `text-xs` | 0,75 rem | Legendas não essenciais |
| `text-sm` | 0,875 rem | Metadados e labels |
| `text-base` | 1 rem–1,125 rem | Corpo |
| `text-lg` | 1,125 rem–1,25 rem | Introduções |
| `text-xl` | 1,25 rem–1,5 rem | Títulos de card/seção curta |
| `text-2xl` | 1,5 rem–2 rem | Título de seção |
| `text-3xl` | 2 rem–3 rem | Título de página |
| `text-display` | 2,5 rem–4,5 rem | Hero da home, com limite de linha |

Corpo usa altura de linha entre 1,5 e 1,7; títulos entre 1,05 e 1,25. Parágrafos longos devem ficar próximos de 65–75 caracteres por linha.

### Prontidão internacional desde a fundação

- Componentes devem aceitar locale e expansão de texto desde a Fase B, sem larguras ou alturas rígidas dependentes do português.
- Caracteres internacionais não podem causar fallback acidental, corte, sobreposição ou mudança indevida de hierarquia.
- A pilha por script deve ser testada com conteúdo real de todas as traduções existentes.
- Layout deve aceitar RTL quando necessário, usando propriedades lógicas e distinguindo direção visual de direção semântica.
- Canonical e hreflang pertencem ao contrato do template; o design system apenas garante slots/estrutura coerentes e não infere URLs.

## 4. Spacing, containers e grid

### Escala

Base de 4 px: `space-1` 4, `space-2` 8, `space-3` 12, `space-4` 16, `space-5` 20, `space-6` 24, `space-8` 32, `space-10` 40, `space-12` 48, `space-16` 64, `space-20` 80 e `space-24` 96.

- Espaçamento de seção deve ser fluido entre 48 e 96 px.
- Alvos de toque: mínimo de 44 × 44 px.
- Ritmo interno de cards: 16–32 px conforme densidade.

### Containers

| Token | Largura máxima | Uso |
|---|---:|---|
| `container-reading` | 760 px | Artigos, FAQ e páginas legais |
| `container-content` | 1120 px | Conteúdo padrão |
| `container-wide` | 1280 px | Grids e hero composto |
| `container-full` | Sem máximo | Faixas de fundo; conteúdo interno continua contido |

Gutters: 16 px em telas estreitas, 24 px em tablet e 32 px no desktop. O container não deve ser recriado por componente.

### Grid

- 4 colunas no mobile, 8 no tablet, 12 no desktop.
- Gap inicial: 16/24/32 px.
- Cards devem quebrar por espaço disponível, não por uma lista extensa de dispositivos.
- Ordem visual e ordem do DOM devem permanecer equivalentes.

## 5. Forma, elevação e ícones

- Raios: 6 px para controles, 12 px para cards, 20–24 px apenas em painéis de destaque.
- Bordas leves são preferíveis a sombras; usar no máximo três níveis de elevação.
- Ícones devem vir de um único conjunto já licenciado ou de SVGs próprios, sempre com função e tamanho consistentes.
- Ícone decorativo recebe tratamento silencioso; ícone que substitui texto precisa de nome acessível.
- Não incorporar o conjunto de ícones das referências sem revisão de licença e peso.

## 6. Especificação dos componentes

### Buttons

- Variantes: primary, secondary, tertiary/text e danger.
- Tamanhos: regular e compact; nenhum botão abaixo do alvo de toque.
- Estados: default, hover, focus-visible, active, loading e disabled.
- Um CTA primário por bloco. Links continuam sendo links quando navegam.

### Forms

- Label visível, ajuda associada, obrigatório indicado em texto e mensagens próximas ao campo.
- Validação não deve depender de placeholder ou cor.
- Preservar campos e endpoints existentes; padronizar feedback de envio.
- Consentimento deve ser específico, registrável e separado de comunicação comercial quando necessário.
- Autocomplete, tipo de teclado e formato devem ser adequados ao campo.

### Breadcrumbs

- Presentes em páginas profundas, exceto quando a hierarquia não agrega.
- Último item não é link; truncamento não pode esconder contexto essencial.
- Estrutura visual e JSON-LD derivam da mesma hierarquia.

### Hero

- Variantes: home, pilar, nível, objetivo, B2B e editorial.
- Título único, texto curto, CTA principal e, quando útil, ação secundária.
- Mídia tem função narrativa e texto alternativo apropriado.
- Evitar carrossel automático, vídeo em autoplay com áudio e conteúdo essencial sobre imagens sem contraste.

### Proof bar

- Até quatro fatos, todos com origem interna documentada.
- Se não houver comprovação, usar diferenciais qualitativos em vez de números.
- Não usar estrelas fixas ou logos de clientes sem autorização.

### Language cards

- Nome, contexto curto, quantidade de níveis somente se calculada e CTA para a página-pilar.
- Diferenciação por conteúdo e imagem, não por arco-íris arbitrário.

### Course cards

- Idioma, nível padronizado, formato, breve resultado e CTA.
- Preço apenas quando atual e acompanhado de periodicidade/condição.
- Sem rating fictício, “alunos” estimados, countdown ou falsa escassez.

### Level cards

- Evidenciam sequência, pré-requisito, objetivo de aprendizagem e duração somente quando registrada.
- Estado atual/seguinte pode ser usado em timelines, sem tornar o card inoperável isoladamente.

### Teacher cards

- Foto aprovada, nome real, idiomas/áreas e biografia curta.
- Links somente se houver página/destino.
- Fallback neutro quando faltar foto; nunca usar pessoa de banco como se fosse docente.

### Process steps

- Três a cinco etapas, com verbos e resultado claro.
- Números indicam ordem, não métricas.
- No mobile, sequência vertical com leitura natural.

### Timelines

- Usadas para progressão de níveis ou jornada de matrícula.
- Não depender de uma linha puramente visual para comunicar ordem.
- Etapas longas devem virar conteúdo normal, não um componente apertado.

### Tabs

- Reservadas a conteúdo paralelo curto, como modalidade ou frequência.
- Teclas direcionais, `aria-selected` e associação painel/controle.
- Não esconder conteúdo crítico de SEO em carregamento client-side.

### Vídeo

- Poster otimizado, play explícito, título e alternativa textual.
- Embed externo carregado sob demanda e respeitando consentimento quando aplicável.
- Legendas/transcrição para material institucional relevante.

### Testimonials

- Nome e contexto autorizados; conteúdo editorialmente aprovado.
- Carrossel não é obrigatório. Se existir, controles manuais e pausa.
- Sem inventar foto, cargo, nota, país ou resultado.

### Pricing

- Nome do plano, frequência, inclusões, preço e período claramente relacionados.
- Destacar recomendação apenas com critério real.
- Preservar identificadores enviados ao checkout e apresentar custos recorrentes sem ambiguidade.
- Comparação em mobile deve permanecer legível sem tabela horizontal extensa.

### FAQ

- Acordeão progressivo com botão real, estado anunciado e foco visível.
- JSON-LD apenas quando pergunta e resposta estão visíveis e coerentes com a página.
- Perguntas específicas têm prioridade sobre um FAQ genérico repetido.

### Blog cards

- Título, resumo, categoria, idioma e data/autor somente quando existentes.
- Imagem com proporção consistente; todo o card não deve criar links aninhados.
- Destaque editorial não altera a canonicalização.

### CTA

- Variante inline, seção final e sticky mobile apenas quando não obstrutiva.
- Texto descreve a próxima ação: testar nível, falar com equipe, ver plano ou matricular.
- Preservar UTMs e eventos, sem disparo duplicado.

### Header

- Uma faixa principal, marca, navegação por tarefas, idioma, login e CTA.
- Menu mobile controlável por teclado e leitor de tela.
- Header fixo somente se não consumir área excessiva nem causar layout shift.
- Destinos canônicos e domínio de login vêm de configuração/contrato, não de texto espalhado.

### Footer

- Navegação agrupada, contato, redes, legal e controle de preferências.
- GTM/pixel/consentimento devem ser tecnicamente desacoplados da marcação visual.
- Não repetir menus extensos sem hierarquia.

## 7. Composição por densidade

| Contexto | Densidade | Regra |
|---|---|---|
| Homepage | Média | Alternar narrativa, descoberta e prova; evitar mural de cards |
| Hub | Alta controlada | Filtros e comparação, mas com orientação |
| Pilar | Média | Conteúdo aprofundado com progressão clara |
| Nível | Alta | Decisão exige currículo, formato, professor e preço |
| Objetivo | Baixa/média | Jornada curta até recomendação |
| B2B | Baixa/média | Clareza, credibilidade e contato |
| Blog/artigo | Baixa | Priorizar leitura |
| Legal | Baixa | Navegação interna e legibilidade |

## 8. Motion

- Duração padrão entre 120 e 240 ms; movimentos maiores até 400 ms quando justificados.
- Respeitar `prefers-reduced-motion`.
- Nenhum conteúdo depende de animação para aparecer.
- Evitar parallax, contadores animados e múltiplas bibliotecas de reveal.
- Mudanças de layout devem privilegiar transform/opacidade somente quando isso não prejudicar leitura.

## 9. Imagens e direção de arte

- Priorizar professores, alunos e contextos reais, com consentimento de uso.
- Representar diversidade de idade, origem e objetivo sem estereótipos.
- Manter tratamento fotográfico natural, adulto e documental.
- Definir aspect ratios por componente e gerar tamanhos responsivos.
- Registrar licença, crédito, texto alternativo e ponto focal.
- Imagens de Edumon/EduAll são referência compositiva, não ativos aprovados.

## 10. Conteúdo e voz

- Português direto, acolhedor e específico.
- Aulas ao vivo, professores, progressão e contexto cultural são diferenciais centrais.
- Evitar superlativos não comprovados, urgência artificial e promessas universais.
- A sequência pública de inglês a validar é A1, A2, B1, B1+, B2 e C1.
- ID interno, slug histórico, rótulo público e nível CEFR são conceitos distintos. A taxonomia pedagógica final deve ser aprovada antes do componente de progressão; o design system não renomeia URLs, IDs, registros LMS ou redirects.
- Traduções precisam de revisão humana; não misturar páginas traduzidas com slug ou hreflang inferido.
- Conteúdo de Iorubá sobre língua, história, cultura, práticas, produção cultural ou contexto afro-brasileiro precisa de revisão do professor/especialista responsável antes da publicação.
- Structured data deve refletir conteúdo visível e semanticamente pertinente. Não criar blocos ou repetir copy para perseguir rich results; `Course` e `FAQPage` não determinam o desenho.

## 11. Acessibilidade e qualidade

Cada componente deve passar por:

- navegação completa por teclado;
- ordem de foco e foco visível;
- headings e landmarks coerentes;
- nomes, estados e mensagens acessíveis;
- contraste e zoom a 200%;
- reflow a 320 CSS px sem perda de função;
- alternativas para mídia;
- teste com redução de movimento;
- validação em leitor de tela nos fluxos de menu, FAQ, formulário, teste e checkout.

Meta inicial: WCAG 2.2 nível AA, sem alegar conformidade antes de auditoria.

## 12. Performance

- HTML útil renderizado no servidor.
- CSS crítico pequeno e folha de componentes sem duplicação.
- JavaScript carregado por necessidade; nada de importar a stack das referências.
- Imagens responsivas, dimensões explícitas e lazy loading fora da dobra.
- Fontes locais com subconjuntos/cobertura verificados e `font-display` apropriado.
- Reservar espaço para embeds e imagens a fim de reduzir CLS.
- Definir budgets na fase de implementação: peso por template, número de requests e limites de LCP/INP/CLS.

## 13. Organização futura sugerida

Quando a implementação for aprovada:

- uma fonte de tokens semânticos;
- uma camada de fundamentos: reset controlado, tipo, cores, grid e utilitários mínimos;
- componentes Jinja com CSS e comportamento documentados;
- exemplos de estados reais, inclusive vazio e erro;
- registro de decisões para exceções;
- testes visuais e de acessibilidade nos templates prioritários.

Essa organização deve coexistir temporariamente com o legado durante a migração. A remoção de CSS/vendor só ocorre depois de comprovar que nenhuma rota ainda depende dele.

## 14. Decisões pendentes antes da implementação

1. Validar os tokens candidatos contra logos e ativos oficiais e confirmar o uso correto do logotipo.
2. Auditar contraste WCAG dos tokens em componentes/estados e cobertura dos arquivos de fonte para todos os idiomas existentes.
3. Aprovar a taxonomia pedagógica A1, A2, B1, B1+, B2 e C1 e seu mapeamento sem renomear IDs, slugs, registros LMS ou redirects.
4. Definir quais métricas, depoimentos, clientes e selos têm evidência publicável.
5. Aprovar banco de imagens e autorização de professores.
6. Reunir os dados e autorizações para a direção já aprovada de `/professores` (índice P1) e `/professores/<slug>` (perfis P2).
7. Definir até onde o visual será estendido a `app.vediums.com`.
8. Escolher a estratégia de convivência e retirada de Bootstrap/Tailwind/tema legado.

Nenhum token ou componente deste plano deve ser aplicado antes dessas decisões e da aprovação da próxima fase.
