# 24 — B2B corporativo: bloco na Home + página V2 exclusiva (Fase B.6E, Parte B/C)

> **Origem**: o bloco B2B da Home ("Para empresas / Idiomas para equipes que precisam se comunicar com mais segurança") podia ser confundido com um curso B2C. Documento oficial determina que B2B não é "curso comum para empresas" — precisa envolver diagnóstico, trilhas, níveis, gestão, acompanhamento, relatórios, solução sob proposta. Regra permanente: nunca preço, nunca card de curso, nunca iconografia genérica (aperto de mãos, executivo de braços cruzados).

## 1. Rota real preservada

`/empresas` (`www/empresas.html` + `empresas.py`, 200, já indexada — confirmado em `02-route-and-seo-map.md`) continua sendo o destino real de todo CTA B2B. Nenhum slug novo foi criado ou inventado; a página pública não foi tocada.

## 2. Bloco B2B da Home — reconstruído

Novo macro `v2_b2b_home_feature` (`macros_editorial.html`), substitui `v2_feature_media` nesta seção específica (o macro genérico continua existindo, sem uso ativo aqui). Seção passou de `.v2-section` (branco) para `.v2-section v2-section--brand` (navy, mesmo padrão já aprovado de VediumMethod/Aula ao vivo/CTA final) — diferenciação clara da área B2C ao redor.

| Elemento | Antes | Depois |
|---|---|---|
| Eyebrow | "Para empresas" | "Vedium para empresas" + linha secundária "Formação linguística corporativa" |
| Headline | "Idiomas para equipes que precisam se comunicar com mais segurança" | "Desenvolva uma equipe mais preparada para se comunicar globalmente." |
| Apoio | 1 linha | 2 linhas: a original (ajustada) + "A solução é estruturada conforme as necessidades da equipe." |
| Prova | inexistente | 4 itens em grade editorial 2×2 (nunca cards): Diagnóstico / Trilhas por nível / Gestão / Relatórios — nenhuma métrica inventada |
| CTA | 1 CTA genérico ("Conheça as soluções para empresas →") | 2 CTAs: primário "Conheça as soluções corporativas" (botão, → `/empresas`) + consultivo "Solicite uma conversa diagnóstica →" (texto, → `/contato`, real/existente) |
| Imagem | E15 (videochamada em grupo) | mantida — já aprovada em B.6C, só a composição ficou maior/mais corporativa |
| Contraste | — | todo texto secundário em 90% branco (mesma margem já auditada matematicamente em `20-bain-editorial-rhythm.md` seção 6: 4.76:1 no pior ponto do gradiente navy) |

## 3. Página B2B V2 — preview isolado

**Rota real: `/design_system_v2_b2b`** — não `/design_system_v2/b2b` como a missão sugeriu conceitualmente. **Bug real encontrado ao tentar a rota aninhada**: uma subpasta `www/design_system_v2/` colide com o arquivo plano `www/design_system_v2.py` já existente no resolvedor de módulos Python do Frappe (`ModuleNotFoundError: 'vedium_core.www.design_system_v2' is not a package`, porque o `.py` já ocupa esse nome no namespace de `vedium_core.www`). Corrigir a rota aninhada exigiria uma `website_route_rule` em `hooks.py` (arquivo de produção compartilhado, fora do escopo de isolamento desta fase) ou renomear o arquivo existente (quebraria a URL `/design_system_v2` já em uso). Rota plana com underscore escolhida em vez disso — mesmo padrão já usado no resto do repo pra controllers `www/` (nunca hífen no nome do arquivo).

Gate de acesso idêntico ao de `/design_system_v2` (`design_system_v2_b2b.py`): `noindex`, `no_sitemap`, restrito a `developer_mode` ou papel "System Manager". Link cruzado adicionado no banner de dev-tool de `/design_system_v2` ("Ver preview B2B").

### Arquitetura implementada (10 seções, arquivo único `www/design_system_v2_b2b.html`)

1. **Header V2** — sem overlay (`v2_header_overlay` não setado). Esta página não tem o Hero-carousel full-bleed (`.v2-editorial-hero`) que o JS `initHeaderOverlay` precisa pra calcular o cruzamento hero/header; sem esse elemento a função não roda, e usar overlay deixaria o header transparente pra sempre. Header sólido evita esse risco.
2. **Hero B2B** (`v2_hero_split`) — eyebrow "Vedium para empresas", H1 "Desenvolva um time mais preparado para atuar globalmente.", apoio, CTA primário (conversa diagnóstica) + secundário ("Conheça a abordagem", âncora `#solucao` na mesma página), imagem E07 (videoconferência profissional — diferente da E15 já usada no bloco B2B da Home, evita repetição na mesma jornada de clique Home→B2B).
   - **Bug real encontrado por screenshot**: `--v2-text-h1` (token compartilhado, até 76px) foi calibrado na Fase B.6 pro Hero-carousel full-bleed (coluna larga, headline de 5 palavras — comentário no próprio token em `tokens.css`). Na coluna de ~48% do `v2_hero_split` com um H1 de 9 palavras, o headline quebrava em **5 linhas**. Corrigido com um `font-size` próprio escopado a `.v2-hero--split .v2-hero__title` (`clamp(2rem, 1.7rem+1.4vw, 3rem)`, 32-48px) — não mexe no token nem no Hero-carousel congelado (seletor diferente, `--split` vs `.v2-editorial-hero`). Resultado: 3 linhas, confirmado por novo screenshot.
3. **Desafio** — título + texto + exemplos de situação de uso (reuniões/apresentações/relacionamento com clientes/comunicação entre equipes/atuação internacional) em lista horizontal discreta (`.v2-b2b-tags`), sem cards.
4. **Diagnóstico** — 6 bullets (nível atual/objetivo da empresa/situações de uso/perfil das equipes/disponibilidade/necessidade de acompanhamento) em grade editorial 2 colunas (`.v2-b2b-list`, novo padrão reutilizável) + CTA discreto "Solicite um diagnóstico →" (`/contato`).
5. **Solução** (`id="solucao"`, âncora do Hero) — 6 itens (trilhas por nível/aulas ao vivo/professores/turmas/acompanhamento/relatórios), mesma grade editorial.
6. **Como funciona** — a missão lista esta seção na arquitetura (seção 17) mas não dá copy dedicada pra ela (as seções 18-25 do texto pulam de Solução direto pra Gestão). Pra não inventar conteúdo B2B novo que só duplicaria o Processo de Implantação mais abaixo, virou uma ponte curta e honesta pra página institucional REAL já existente (`/como-funciona`) — não fabrica um "como funciona" B2B-específico sem base.
7. **Gestão e acompanhamento** — título "Acompanhamento para RH e liderança.", fundo navy. 4 itens: Participação e Evolução por nível (**reais**, já confirmados — a Home já tem uma seção "Progressão" com o mesmo tipo de acompanhamento individual) vs. Adesão da turma e Relatório para RH (marcados com a tag visível `(proposta)` — **não confirmei uma feature de relatório agregado por empresa pronta em produção hoje**, então a missão pede explicitamente não publicar como fato). Parágrafo de honestidade abaixo da lista reforça a distinção. Este é o ponto onde a regra "nunca inventar dashboard/indicador inexistente" foi aplicada de forma mais visível.
8. **Formatos corporativos** — 4 conceitos (programas por turma/trilhas por nível/formações por objetivo/soluções sob proposta), nunca preço, nunca pacote fixo.
9. **Processo de implantação** — reaproveita `v2_progression_flow` (mesmo componente já usado na "Progressão" da Home) com as 5 etapas reais da missão (Diagnóstico → Desenho da solução → Formação das turmas → Aulas e acompanhamento → Revisão com a empresa).
10. **Conversa diagnóstica (CTA final)** — reaproveita `v2_cta_section(variant="brand-full")`, mesmo padrão navy centralizado já aprovado no CTA final da Home (fase anterior). CTA único, consultivo ("Solicite uma conversa diagnóstica") — nunca "Compre agora"/"Assine agora".
11. **Footer V2** — include padrão, idêntico ao da Home.

### Componentes novos (reutilizáveis, `components-editorial.css`)

- `.v2-b2b-tags` — lista horizontal curta com separador `·`, usada no Desafio.
- `.v2-b2b-list` (+ `--on-dark`) — grade editorial 2 colunas com divisória fina, usada em Diagnóstico/Solução/Gestão/Formatos. `.v2-b2b-list__flag` renderiza a tag `(proposta)`.

## 4. Verificação

- `/design_system_v2_b2b` → 200; único `<h1>` na página; `docScrollWidth <= innerWidth` em 1440/390px (sem overflow).
- `flake8` limpo em `design_system_v2_b2b.py`; `pytest` 330 passed / 11 skipped, sem regressão.
- Hero, CTA final e Footer da **Home** confirmados intactos (esta fase só adicionou uma seção nova em página separada + o bloco B2B da própria Home, que não é uma das 3 áreas congeladas).
