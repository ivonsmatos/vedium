# Baseline de Conteúdo Crítico — o que não pode desaparecer por acidente

> **Fase A (baseline técnico) — 2026-08-24.** Documento read-only. Não é um dump do conteúdo (proibido pela missão) — é o CONTRATO ESTRUTURAL: qual elemento vive em qual bloco Jinja, condicionado a quê, e o que foi efetivamente observado na amostra ao vivo (`seo-snapshot.csv`). "Presente hoje" refere-se ao HTML servido em 2026-08-24.

## Metodologia

Duas fontes por página: (1) o **contrato de template** (o que o Jinja garante renderizar SE os dados existirem — de leitura de código desta e de sessões anteriores) e (2) **confirmação em produção** (do que a amostra de 66 URLs de `seo-snapshot.csv` efetivamente mostrou). Quando só (1) está disponível, marco **CONFIRMADO NO CÓDIGO, NÃO AMOSTRADO EM PRODUÇÃO**.

## `/` (Homepage)

- **H1**: CONFIRMADO EM PRODUÇÃO só na versão pt-BR ("Aulas de idiomas online, ao vivo, com professores nativos e especialistas"). **`/en`, `/es`, `/fr`, `/de`, `/ru` responderam SEM NENHUM `<h1>`** na amostra — achado real, ver `performance-baseline.md` (seção acessibilidade). Isso não é uma opinião de auditoria: é o HTML servido hoje.
- **Grid de cursos**: dinâmico via LMS (`get_published_courses`), presente pela arquitetura do template — não depende de conteúdo hardcoded, então "desaparecer" aqui significaria bug de query, não de copy.
- **Diferenciais / modalidades**: seção "Aulas 100% ao vivo" e equivalentes fazem parte do template compartilhado com `curso.html` (mesmos ícones/textos usados na ficha de curso) — ver `route-families.csv`.
- **CTAs**: WhatsApp (3 posições fixas do header/footer) + CTA de teste de nível (dinâmico, ver `ui-contracts.md`) + `public_cta_click` locais na home (4 CTAs confirmados: `home_hero_1..4`).
- **Schema**: CONFIRMADO EM PRODUÇÃO — `EducationalOrganization` + `ContactPoint` + `PostalAddress` presentes em todas as 6 variantes de idioma amostradas.
- **Internal links**: header/footer completos (ver `ui-contracts.md`) + grid de cursos linkando pra `/curso/<slug>`.

## `/cursos-de-idiomas-online` (página geral de cursos) e variantes por idioma

- **H1**: NÃO AMOSTRADO diretamente (a amostra cobriu `/en/catalogo` etc., que respondeu sem H1 também — mesmo padrão da home, ver acima).
- **Grid completo**: todos os cursos publicados no LMS, sem filtro de categoria (diferente das páginas-pilar). Fonte: `www/catalogo.py`.
- **Filtros/ordenação**: existência confirmada no código (INFERIDO da estrutura de `get_published_courses`), comportamento de UI não relido linha a linha nesta auditoria.

## Inglês (`/curso-de-ingles-online` + 6 idiomas + 6 níveis)

- **Estrutura de pilar**: usa `marketing_landing.html` — título, lead, `seo_sections` (profundidade variável por idioma, já auditado historicamente), FAQ, grid de níveis A1→C1.
- **Trilha de níveis**: `ENGLISH_COURSE_NAV_LABELS`/`ENGLISH_COURSE_LEVELS` em `course_urls.py` — rótulos A1 a C1 fixos no código, únicos por nível, comprimento ≤60 caracteres (garantido por teste automatizado `test_pure_course_seo_navigation.py`).
- **Professor**: card na ficha do curso (nome+foto) existe estruturalmente em `curso.html` (adicionado/generalizado na sessão da missão PLE, 2026-08-23) — CONFIRMADO NO CÓDIGO que filtra contas placeholder; se há foto real cadastrada para o professor de Inglês hoje, NÃO CONFIRMADO nesta auditoria (exigiria acesso a produção/bench).
- **Preço**: vem do LMS Course (`course_price`/`currency`), nunca hardcoded no template — não há "preço" pra desaparecer da landing em si, é sempre live.

## Iorubá (`/curso-de-ioruba-online` + variantes)

- Mesma estrutura de pilar. **Gate cultural** documentado em `docs/redesign/06-photography-system.md`: conteúdo de língua/história/cultura/produção cultural afro-brasileira exige revisão de especialista antes de qualquer alteração de conteúdo — vale também como contrato de conteúdo (não é só regra de mídia).
- Professor (Busayo Frank Alonge, conforme redirect `/professor-busayo-frank-alonge → /curso-de-ioruba-online` em `hooks.py:327`) — vínculo confirmado no código via esse redirect histórico; card de professor na landing não confirmado nesta auditoria (mission da landing PLE tratou só o cluster PLE, não o de Iorubá).

## PLE — Português para Estrangeiros (`/portugues-para-estrangeiros` + 3 níveis + 6 idiomas)

- **Já auditado exaustivamente na missão anterior desta mesma sessão** (2026-08-23) — ver commits na branch. Resumo do que está garantido hoje: FAQ em pt-BR corrigido, trilha de níveis language-aware, currículo traduzido en/es/fr/de (ru pendente), x-default apontando pra EN nas 6 variantes de landing + 3 níveis, card de professor (Almir Soares da Silva) com foto real na ficha (pendente de `bench execute` em produção pra aparecer).
- **Preço em USD**: confirmado como intencional pelo dono do produto nesta sessão (2026-08-24) — não é um "conteúdo que desapareceu", é decisão de negócio vigente.

## Espanhol (`/curso-de-espanhol-online`)

- Mesma estrutura de pilar; 3 níveis (Básico/Intermediário/Avançado, sem trilha dedicada como Inglês/PLE — `get_course_navigation` retorna `None` pra Espanhol, CONFIRMADO NO CÓDIGO via teste `test_courses_without_an_approved_linear_trail_hide_navigation`).

## Hebraico (`/curso-de-hebraico-online`)

- Mesma estrutura de pilar; produtos distintos (moderno A1, moderno A2-B1, bíblico, alfabetização A0, particular) — sem trilha linear unificada (mesmo motivo do Espanhol).

## B2B (`/empresas`)

- Estrutura institucional própria (`www/empresas.py`), com formulário de intenção (`public_intent_submit`, `intent: 'b2b'`) — ver `conversion-contracts.md`.

## Páginas de nível principais (`/curso/<slug>`)

Contrato de template (`curso.html`, único arquivo pra todos os clusters/idiomas):
- **H1 único**: `<h1>{{ course.title }}</h1>` — CONFIRMADO NO CÓDIGO, travado por teste automatizado (`template.count("<h1>{{ course.title }}</h1>") == 1`).
- **Descrição/objetivos**: `course.short_introduction` + `course.description` (do LMS Course, sobrepostos por `COURSE_TRANSLATIONS` quando há tradução).
- **Grade de módulos/aulas**: `course.chapters_list` — vem do LMS (Course Chapter/Course Lesson), sempre em pt-BR na origem; só PLE tem tradução aplicada (en/es/fr/de) via `PLE_CURRICULUM_TRANSLATIONS`.
- **Preço**: `course.formatted_price`, sempre live do LMS; nota anual quando aplicável.
- **Alunos matriculados**: só exibido se `>= 10` (`PUBLIC_ENROLLMENT_COUNT_THRESHOLD`, decisão do dono de 2026-08-23) — abaixo disso, o bloco inteiro desaparece intencionalmente (não é bug).
- **Professor**: nome+foto (ou avatar com inicial se sem foto) — condicionado a `course.instructors_list` não vazio, com filtro de contas placeholder.
- **CTAs**: matricular (mensal/anual) ou "Acessar curso" (se já matriculado); teste de nível dinâmico; links de metodologia/diferenciais/certificado/planos/FAQ.
- **Schema**: `Course` + `BreadcrumbList`, `educationalLevel` só quando há trilha definida (Inglês/PLE).

## Páginas de objetivo prioritárias (spokes SEO)

Mesma estrutura de `marketing_landing.html` dos pilares — ver `route-families.csv`, família `objective`. Conteúdo por slug não replicado aqui (proibido pela missão); estrutura garantida: `pain_points`, `outcomes`, `modules`, `format_items`, `faqs`, CTA de WhatsApp/teste, link de volta pro pilar via `content_clusters.cluster_for_category`.

## Blog

- **Fonte dupla de dados** (achado de arquitetura, não desta Fase A — já era conhecido): posts em lote entram via `blog_content.BLOG_POSTS` (dict em código), NÃO via o DocType `Vedium Blog Post` do painel — qualquer ferramenta de migração do redesign que só olhe o DocType vai perder posts.
- **97 entradas confirmadas** em `BLOG_POSTS`; 29 com `category` definida (geram redirect de URL legada, ver `redirects.csv`).
- Estrutura por post (INFERIDO do padrão do template, não relida linha a linha): título, corpo, categoria, idioma (`post.get("lang")`), autor/data — presença exata de cada campo NÃO confirmada individualmente nesta auditoria.

## Avisos legais (transversal)

- Termos, Privacidade, Cookies, Cancelamento e Reembolso: **hardcoded no footer, sempre em português**, sem tradução em nenhum idioma — CONFIRMADO NO CÓDIGO (agente de header/footer). Isso é uma decisão já registrada em memória de outra sessão (`project_termos_privacidade_pt_only_decision`), não uma lacuna a corrigir.
- Razão social/CNPJ no rodapé: hardcoded, nunca traduzido.
