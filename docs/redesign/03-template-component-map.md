> **IMPORTANTE:**
>
> - O único projeto que pode receber novos arquivos é `vedium`.
> - `edumon` e `eduall` são referências SOMENTE PARA LEITURA.
> - Não modifique nenhum arquivo dentro de `edumon` ou `eduall`.
> - Nesta fase, não modifique nenhum arquivo existente do projeto `vedium`.
> - A única escrita permitida é criar os 5 arquivos solicitados em `vedium/docs/redesign/`.

# 03 — Mapa de templates e componentes

## Objetivo

Este documento converte o inventário atual em uma arquitetura de apresentação para o redesign. É uma especificação, não uma implementação. A proposta mantém Frappe/Jinja como camada de renderização, preserva contratos de dados e integrações e usa Edumon e EduAll apenas como referências visuais.

## 1. Como o frontend público está organizado hoje

| Camada atual | Origem principal | Papel | Diretriz |
|---|---|---|---|
| Shell genérico Frappe | `vedium_core/vedium_core/templates/base.html` | Estrutura base de páginas Frappe | Preservar compatibilidade; não torná-lo dependente do tema das páginas de marketing |
| Cabeçalho público | `templates/includes/site_navbar.html` | Marca, navegação, idioma, login e CTAs | Substituir a composição visual; preservar destinos e comportamento |
| Rodapé público | `templates/includes/site_footer.html` | Navegação, consentimento, GTM e scripts do site | Refatorar futuramente com extremo cuidado: contém integrações, não apenas apresentação |
| Landing reutilizável | `templates/includes/marketing_landing.html` | Estrutura compartilhada das páginas-pilar e de objetivo | Preservar o contrato de conteúdo; dividir em componentes menores no redesign |
| Catálogo e home | `www/index.*`, `www/catalogo.*` | Consultas de cursos, planos e conteúdo editorial | Manter controllers como fonte inicial de dados; substituir a apresentação por etapas |
| Curso público | `www/curso.*` e regras em `hooks.py` | Página pública ligada ao DocType LMS Course | Preservar resolução do slug público e o vínculo com LMS |
| Blog | `www/blog*`, includes de blog, `blog_content.py` e DocType | Índice, categorias e artigos | Unificar visual sem romper as duas fontes de conteúdo |
| Páginas autônomas | Diversos `www/*.html` e `www/*.py` | Institucional, conversão, legal e idiomas | Migrar para shells compartilhados; manter controllers e ações |
| Estilos | CSS do tema, Bootstrap, Tailwind gerado e estilos locais | Tokens e componentes parcialmente sobrepostos | Consolidar após inventário visual; evitar uma quarta camada |
| Interação | JavaScript progressivo e bibliotecas vendor | Menus, sliders, formulários, consentimento e mídia | Reimplementar em JavaScript leve; manter nomes de eventos e contratos de API |

Não há uma aplicação React ou Vue responsável pelo site público. As referências em Next.js não devem ditar a arquitetura de produção.

## 2. Templates-alvo

### T1 — Homepage

- Rotas: `/` e homepages localizadas.
- Objetivo: apresentar proposta de valor, idiomas, método, professores, progressão e próximos passos.
- Blocos: header, hero, proof bar verificável, cards de idiomas, processo, professores reais, vídeo opcional, depoimentos verificados, planos resumidos, conteúdo editorial, CTA e footer.
- Dados preservados: cursos publicados, planos/frequências, links para matrícula, login, teste e blog.
- Regra editorial: remover estrelas, contadores e indicadores sem fonte auditável.

### T2 — Hub de cursos

- Rota canônica: `/cursos-de-idiomas-online`.
- Aliases atuais: `/cursos` e `/trilhas`; `/catalogo` redireciona.
- Objetivo: permitir descoberta por idioma, nível e objetivo sem aparência de marketplace.
- Blocos: hero compacto, filtros acessíveis, cards de idioma, trilhas/níveis, orientação de escolha e CTA de diagnóstico.
- Dados preservados: catálogo real do LMS, slugs públicos e preços/planos quando aplicáveis.

### T3 — Página-pilar de idioma

- Rotas: inglês, iorubá, português para estrangeiros, espanhol e hebraico, além das versões localizadas existentes.
- Objetivo: explicar contexto, método, trilha e diferenciais de cada idioma.
- Blocos: breadcrumb, hero contextual, benefícios, visão da trilha, cards de nível, professores vinculados, processo, FAQ específica, artigos relacionados e CTA.
- Origem: wrappers em `www/`, `marketing_landing_content.py` e `marketing_landing.html`.
- Gate cultural: conteúdo de `/curso-de-ioruba-online` que envolva língua, história, cultura, práticas, produção cultural ou contexto afro-brasileiro exige revisão do professor/especialista responsável antes da publicação.

### T4 — Página de nível ou trilha

- Rotas: `/curso/<slug-publico>`.
- Objetivo: dar segurança sobre nível, conteúdo, progressão, agenda e matrícula.
- Blocos: breadcrumb, hero do curso, metadados verificáveis, resultados de aprendizagem, currículo, professor(es) reais, funcionamento, preço/frequência, FAQ, cursos adjacentes e CTA de matrícula.
- Origem: `www/curso.html`, `www/curso.py`, DocTypes LMS e mapeamentos em `course_urls.py`.
- Atenção: a sequência pública a validar é A1, A2, B1, B1+, B2 e C1. ID interno, slug histórico, rótulo público e nível CEFR são conceitos separados. A taxonomia pedagógica precisa ser aprovada antes de implementar `ProgressionTimeline`, cards ou nova copy; URLs, IDs, registros LMS e redirects permanecem inalterados.

### T5 — Página por objetivo

- Rotas: conversação, viagem, trabalho, entrevistas, provas, intercâmbio, leitura, negócios e demais objetivos inventariados no mapa de rotas.
- Objetivo: conectar uma necessidade concreta às trilhas já existentes.
- Blocos: hero orientado ao problema, cenários, recomendação de percurso, método, prova real, FAQ e CTA.
- Origem: landings orientadas por `marketing_landing_content.py`.
- Regra: não criar cursos, resultados, garantias ou depoimentos que não existam.
- Gate cultural: a mesma revisão especializada é obrigatória para `/ioruba-para-iniciantes` e `/ioruba-cultura-e-ancestralidade`; nenhuma dessas páginas será alterada nesta fase.

### T6 — Professores

- Situação atual: `/professores` redireciona para `/sobre`; não existe uma página pública dedicada consolidada.
- Direção aprovada: `/professores` deve futuramente ser índice canônico próprio 200 (P1) e `/professores/<slug>` deve suportar perfis canônicos (P2).
- Condições de ativação: professores confirmados, autorização de imagem, dados profissionais verificados e conteúdo editorial aprovado.
- Blocos do índice: hero, critérios de seleção, grid de professores, idiomas/níveis vinculados, abordagem e CTA.
- Blocos do perfil: breadcrumb, foto autorizada, nome, biografia verificada, idiomas/áreas, cursos vinculados, abordagem e CTA.
- Fonte obrigatória: `Course Instructor`, `User` e conteúdo aprovado. Nunca usar perfis fictícios da referência.
- Migração: manter o 301 atual durante a Fase 0; sua retirada e a criação das novas rotas exigem plano SEO de alto risco.

### T7 — B2B

- Rotas: `/empresas` e `/parcerias`, com equivalentes localizados quando existentes.
- Objetivo: separar claramente a compra corporativa da jornada individual.
- Blocos: hero B2B, problemas atendidos, formatos, processo, diferenciais, casos somente quando documentados, formulário/contato e FAQ.
- Integrações: submissão de interesse, CRM, Brevo e eventos de analytics.

### T8 — Blog, categoria e artigo

- Rotas: `/blog`, `/blog/<categoria>`, `/blog/<slug>`, `/blog/<categoria>/<slug>` e versões localizadas.
- Subtemplates: índice, categoria e artigo.
- Blocos: header editorial, cards, filtros/categorias, artigo, autor/data quando existentes, breadcrumbs, conteúdo relacionado e CTA contextual.
- Fontes: conteúdo em código e DocType `Vedium Blog Post`.
- Regra: preservar canonicals, redirects e a estratégia atual para posts em idiomas sem família completa de rotas.

### T9 — Institucional, conversão e legal

- Institucional: `/sobre`, `/como-funciona`, `/metodologia`, `/diferenciais`, `/certificado`, `/comunidade` e correlatas.
- Conversão: `/planos`, `/matricula`, `/aula-diagnostica`, `/teste-de-nivel`, `/contato`, `/programa-de-indicacao`, `/carreiras` e formulários associados.
- Suporte: `/faq`.
- Legal e privacidade: termos, privacidade, cookies e gestão de dados.
- Estratégia: um shell flexível com variantes editorial, formulário, FAQ e legal, sem forçar todas as páginas à mesma sequência de blocos.

## 3. Exceções que não devem ser absorvidas pelos nove templates

| Exceção | Exemplos | Tratamento |
|---|---|---|
| Autenticação e produto | `app.vediums.com/login`, LMS, Desk e checkout | Permanecem na aplicação Frappe/produto; só alinhar marca e transições em fase própria |
| Páginas autenticadas | `/aluno`, `/onboarding`, `/minhas-indicacoes` | Preservar autenticação, redirects e `noindex` |
| Utilitários de privacidade | `/privacidade/meus-dados` | Manter funcionalidade e `noindex,follow` |
| Conteúdo recorrente | `/pratica-diaria` | Manter `noindex` enquanto essa for a política vigente |
| Infraestrutura pública | `/sitemap.xml`, `/robots.txt`, `/llms.txt` | Não aplicar template visual |
| PWA | `/sw.js`, `/manifest.json` | Não mover nem envolver em HTML |
| APIs e webhooks | métodos whitelisted, checkout e Stripe | Não alterar contratos como efeito colateral do redesign |
| Login local Frappe | `/login` no domínio público | Definir estratégia de domínio antes de qualquer redirect |

## 4. Inventário dos componentes atuais

| Componente | Estado observado | Preservar | Substituir ou evoluir |
|---|---|---|---|
| Header/menu | Compartilhado, com destinos críticos | Rotas, login, seleção de idioma, semântica | Layout, hierarquia, mobile menu e estados de foco |
| Footer | Compartilhado e carregado de scripts | Links legais, consentimento, GTM e eventos | Estrutura visual; separar apresentação de integrações |
| Hero | Varia entre slider e blocos próprios | Mensagens úteis e CTAs válidos | Slider promocional, excesso de movimento e composições inconsistentes |
| Cards de curso | Alimentados por catálogo real, mas com ruído de marketplace | Slug, idioma, nível, preço real e matrícula | Estrelas fixas, números sem fonte e controles de e-commerce |
| Cards de nível | Existem em landings e catálogo | Progressão e links canônicos | Padronizar anatomia e relação entre níveis |
| Professores | Dados disponíveis por curso | Pessoas e vínculos reais | Criar apresentação consistente; não preencher lacunas com mocks |
| FAQ | Conteúdo e schema em páginas elegíveis | Perguntas/respostas e JSON-LD coerente | Acordeão acessível único, sem duplicação invisível |
| Blog | Funcional, com duas fontes | Slugs, canonicals, categorias e conteúdo | Cards, índice, legibilidade e relações entre artigos |
| Formulários | Chamam métodos públicos e CRM | Campos, consentimento, validação, endpoint e parâmetros | Composição, mensagens de estado e acessibilidade |
| CTAs | Levam a WhatsApp, teste, login, planos e checkout | Destinos, UTMs e eventos | Texto, prioridade visual e consistência |
| Modais | Usados em fluxos e mídia | Somente quando necessários ao fluxo | Preferir conteúdo inline; reimplementar foco, Escape e retorno de foco |
| Imagens | Mistura de ativos próprios e referências genéricas | Ativos licenciados, reais e contextualizados | Imagens genéricas, personagens infantis e arquivos pesados |
| Fontes | Kumbh Sans, Playfair Display, Kanit, Inter e Bodoni Moda coexistem | Arquivos locais adequados | Consolidar a dupla tipográfica e eliminar imports redundantes |

## 5. Biblioteca-alvo de componentes

### Globais

- `SiteHeader`: navegação principal, seletor de idioma, login e CTA.
- `MobileNavigation`: painel controlado por botão, foco contido e fechamento previsível.
- `SiteFooter`: navegação, contatos, redes, legal e preferências de consentimento.
- `Breadcrumbs`: visual e semântico, sincronizado com `BreadcrumbList` quando aplicável.
- `LocaleSwitcher`: usa rotas equivalentes conhecidas; não traduz slug por heurística.
- `ConsentControls`: preserva a chave e o evento que liberam pixels.

### Conteúdo e descoberta

- `Hero` com variantes home, pilar, curso, objetivo e B2B.
- `ProofBar` apenas para fatos verificáveis.
- `LanguageCard`, `CourseCard`, `LevelCard` e `ObjectiveCard`.
- `TeacherCard` com dados reais e estado seguro quando não houver biografia/foto.
- `ProcessSteps` e `ProgressionTimeline`.
- `FeatureList`, `ContentSection`, `MediaSection` e `VideoEmbed`.
- `Tabs` somente onde reduzem complexidade; conteúdo essencial continua acessível.
- `TestimonialCard` somente com depoimentos aprovados e rastreáveis.
- `PricingCard` e `FrequencySelector` ligados aos identificadores reais de plano.
- `FAQAccordion`, `BlogCard`, `RelatedContent` e `CTASection`.

### Conversão

- `LeadForm` com variantes contato, diagnóstico, empresa e carreira.
- `LevelTest` preservando pontuação, captura opcional e resultado.
- `EnrollmentCTA` e `WhatsAppCTA` com UTMs e `dataLayer`.
- `CheckoutLauncher` preservando parâmetros de curso, período e frequência.
- `FormStatus` para carregamento, sucesso e erro anunciado a tecnologia assistiva.

## 6. Contratos que os componentes não podem quebrar

### Contrato transversal de locale

Todo componente nasce preparado na Fase B para:

- receber locale e conteúdo traduzido do controller/contexto, sem traduzir no navegador;
- suportar expansão/redução de texto sem altura fixa ou truncamento destrutivo;
- renderizar caracteres internacionais e combinar corretamente fontes por script;
- usar fallback de fontes testado em todos os idiomas existentes;
- aceitar RTL quando o conteúdo/locale exigir, sem inverter semanticamente ícones, números ou mídia;
- receber canonical e conjunto de hreflang do template/controller como contrato, sem inferir slugs;
- manter URL e tradução existentes; ausência de tradução usa o comportamento documentado, nunca conteúdo artificial.

| Área | Contrato a preservar |
|---|---|
| Catálogo | IDs/nomes internos do LMS não devem ser confundidos com slugs públicos |
| Checkout | `course_name`, `billing_period`, `classes_per_week`, moeda, origem, plano e objetivo |
| Analytics | nomes de eventos, parâmetros úteis, consentimento e sequência de `dataLayer` |
| Meta Pixel | só carregar após consentimento armazenado ou evento de consentimento |
| WhatsApp | número oficial, mensagem contextual e atribuição da origem |
| Formulários | nomes de campos aceitos pelos métodos públicos, consentimento e proteção antispam |
| CRM/Brevo | criação de lead/ticket e sincronizações disparadas pelos hooks existentes |
| SEO | title, description, canonical, hreflang, breadcrumbs e indexação por página; JSON-LD deve representar o conteúdo visível |
| Autenticação | domínio `app.vediums.com`, URL de retorno e estado de sessão |
| PWA | escopo do service worker e caminhos absolutos do manifesto |

### Contrato de structured data

- Priorizar `Organization`, `BreadcrumbList`, `BlogPosting` e outras entidades pertinentes ao conteúdo real.
- Manter `Course` e `FAQPage` existentes somente quando semanticamente corretos e coerentes com conteúdo visível.
- Não criar, duplicar ou esconder conteúdo para obter rich results.
- Structured data não define a composição visual e não é objetivo isolado do redesign.
- Breadcrumb visual, canonical, locale e JSON-LD devem descrever a mesma página.

## 7. Mapa de CTAs e dependências atuais

O mapa agrupa CTAs por função, incluindo as versões localizadas que repetem o mesmo contrato. “Sem evento explícito uniforme” não significa ausência de medição no GTM; significa que o markup auditado não garante um `dataLayer.push` dedicado em todas as ocorrências. O container publicado do GTM ainda precisa ser congelado/exportado antes da implementação.

| CTA ou ação | `dataLayer`/evento atual | Destino imediato | Dependência posterior | Sistema final afetado |
|---|---|---|---|---|
| Login do header/footer | Sem evento explícito uniforme | `https://app.vediums.com/login` | Sessão Frappe e eventual return URL | `app.vediums.com` / Frappe auth |
| Cadastro/“Registrar” | Sem evento explícito uniforme | `https://app.vediums.com/login#signup` | Criação de usuário pelo fluxo nativo | `app.vediums.com` / Frappe auth |
| Hero/CTA genérico para WhatsApp | `public_cta_click` com `location` e `cta` | `wa.me/5511911293075` com texto contextual | Atendimento manual; não há criação automática de CRM comprovada pelo clique | WhatsApp; GTM/GA4 conforme tags publicadas |
| Ver catálogo/cursos em páginas institucionais | `public_cta_click` em parte das ocorrências; outras sem evento dedicado | `/catalogo`, `/cursos-de-idiomas-online` ou alias localizado | `/catalogo` redireciona ao hub; navegação para curso | Site público/Frappe; GTM quando instrumentado |
| Abrir/detalhar curso | `view_course` existe no módulo de analytics; cobertura do clique precisa ser confirmada | `/curso/<slug-publico>` | Controller resolve slug → ID de `LMS Course` | Frappe/LMS + GTM/GA4 |
| Acessar curso já disponível | `course_platform_click` | URL `lms_url` no host/app | Sessão e permissão do aluno | `app.vediums.com` / LMS |
| Matricular mensal em página de curso | `course_enrollment_intent_click` com `course`, `billing_period=monthly` e `location` | `checkout_url`; override aponta para `public_frequency_checkout.start` no host `app` | Cria sessão Stripe; webhook confirma pagamento e matrícula | `app.vediums.com` → Stripe → Frappe/LMS; analytics de purchase |
| Matricular anual em página de curso | `course_enrollment_intent_click` com `billing_period=annual` | `annual_checkout_url` | Mesmo contrato, com periodicidade anual | `app.vediums.com` → Stripe → Frappe/LMS |
| Escolher frequência em `/planos` | `plan_select_click` com `plan` e `location=planos` | Atualmente WhatsApp com mensagem do plano | Atendimento confirma idioma/curso; sem Stripe direto neste CTA | WhatsApp + GTM/GA4 |
| “Escolher curso e seguir” em `/planos` | `plan_platform_click` | `/matricula` ou versão localizada | Seleção de curso/plano/objetivo | Site público → `app.vediums.com` |
| Continuar na plataforma em `/matricula` | `enrollment_intent_click` com `course`, `plan`, `goal` e `location` | `https://app.vediums.com/lms/courses/<id>?source=public_funnel&plan=...&goal=...` | Login/LMS e, conforme curso, checkout | `app.vediums.com` / LMS / possível Stripe |
| Tirar dúvida de matrícula | `enrollment_whatsapp_click` e também `public_cta_click` | WhatsApp com contexto de curso/plano/objetivo | Atendimento manual | WhatsApp + GTM/GA4 |
| Concluir teste de nível | `level_test_completed` com idioma, nível/resultado e dados de pontuação previstos no script | Resultado na própria página | Captura opcional via `save_placement_result` | `public_funnel` → CRM quando dados são enviados; GTM/GA4 |
| Enviar resultado do teste | `level_test_whatsapp_click` | WhatsApp com resumo/diagnóstico | Atendimento humano usa o resultado | WhatsApp + GTM/GA4 |
| Ver planos após o teste | `level_test_plan_click` | `/planos` | Seleção de frequência/matrícula | Site público → app/Stripe em passos posteriores |
| Escolher curso após o teste | `level_test_catalog_click` | `/catalogo` → hub canônico | Seleção de curso | Site público/Frappe |
| Agendar diagnóstico por idioma | `diagnostic_schedule_click` | WhatsApp com idioma, objetivo e disponibilidade | Confirmação manual | WhatsApp + GTM/GA4 |
| Selecionar horário diagnóstico | `diagnostic_slot_click` | WhatsApp com slot retornado por `get_available_diagnostic_slots` | Confirmação manual; não cria reserva/pagamento automático | Frappe API → WhatsApp |
| Enviar formulário B2B/comunidade/parceria/intenção | clique pode gerar `public_cta_click`; sucesso gera `public_intent_submit` com `intent` e `location` | `/api/method/vedium_core.public_funnel.submit_public_intent` | Criação/atualização de lead e hooks de sincronização | Frappe/CRM → Brevo quando aplicável |
| Enviar contato | Sem evento de sucesso uniforme identificado | `/api/method/vedium_core.api.send_contact_message` | Mensagem/ticket/lead conforme lógica do endpoint | Frappe/CRM; cobertura de GTM a confirmar |
| Candidatar-se | Evento uniforme não confirmado | endpoint/controlador de carreiras | Registro de candidatura e dados pessoais | Frappe/CRM/fluxo interno |
| Acessar painel de indicação | `referral_platform_click` | `https://app.vediums.com/minhas-indicacoes` | Login quando Guest e painel/código real | `app.vediums.com` / Frappe |
| WhatsApp do programa de indicação | `public_cta_click` pode vir do handler comum por `data-vd-location`; confirmar por locale | WhatsApp | Atendimento manual | WhatsApp + GTM/GA4 |
| Compra concluída | Não é CTA de marketing; evento `purchase` client/server-side | retorno/webhook do checkout | Measurement Protocol quando configurado e criação da matrícula | Stripe → Frappe/LMS → GA4/Brevo |

### Contrato mínimo para migrar um CTA

- preservar destino, host, query string, fragmento e UTMs;
- preservar o nome do evento e seus parâmetros até um plano de analytics aprovar mudança;
- não disparar evento em renderização, duplicar clique ou contornar consentimento;
- preservar IDs internos quando o destino é LMS/checkout e slugs públicos quando o destino é SEO;
- testar a consequência final, não apenas o clique: lead no CRM, mensagem no WhatsApp, sessão no app, checkout no Stripe e matrícula via webhook;
- tratar qualquer futura alteração de login, checkout ou integração como **risco alto**;
- registrar CTAs sem evento explícito como lacuna, não inventar um evento durante o redesign sem plano de mensuração.

## 8. Uso das referências

### Edumon — referência principal

| Elemento observado | Classificação | Aplicação segura |
|---|---|---|
| Containers e grid | Adaptar | Traduzir proporções para os tokens e breakpoints da Vedium |
| Header e footer | Reutilizar ideia visual + reimplementar | Aproveitar clareza e ritmo, mantendo navegação e integrações locais |
| Hero Home One/Two | Adaptar | Usar hierarquia, não copiar conteúdo, ilustrações nem sliders |
| Grades de cursos | Adaptar | Remover estética de marketplace e usar catálogo real |
| Working Process | Reutilizar ideia visual | Aplicar ao funcionamento das aulas e progressão |
| Instructors | Adaptar | Exibir professores reais obtidos do LMS |
| Vídeo | Reimplementar na stack atual | Player leve, consentimento quando necessário e fallback |
| FAQ | Reimplementar na stack atual | Acordeão acessível em JavaScript progressivo |
| Review/testimonials | Adaptar | Somente registros verificados; sem métricas decorativas |
| Blog e breadcrumb | Adaptar | Preservar taxonomia, metadata e dados estruturados atuais |
| Carrinho, busca de loja e badges comerciais | Descartar | Não correspondem ao modelo educacional da Vedium |
| Next.js/React e dependências | Descartar | A produção continua em Frappe/Jinja nesta proposta |

### EduAll — referência complementar

| Elemento observado | Classificação | Aplicação segura |
|---|---|---|
| Cards de professores | Adaptar | Simplificar e alimentar apenas com dados reais |
| Pricing/subscription | Reutilizar ideia visual | Reorganizar frequência e planos sem inventar desconto |
| Steps/work process | Adaptar | Usar linguagem e sequência da Vedium |
| Testimonials | Adaptar | Somente prova social auditável |
| Demais shells e páginas | Descartar como fonte estrutural | Edumon e o sistema da Vedium têm prioridade |
| jQuery, Select2, Slick e plugins vendor | Descartar | Reimplementar interação necessária sem essas dependências |
| Ativos e textos demonstrativos | Descartar | Não incorporar placeholders, identidades ou licenças desconhecidas |

## 9. Recomendação de arquitetura futura

Sem mudar arquivos nesta fase, a direção recomendada é:

1. Manter controllers e DocTypes como fontes de verdade.
2. Criar, em fase aprovada, um shell público Jinja e includes pequenos por componente.
3. Definir contratos de contexto explícitos para cada template; componentes não devem consultar dados por conta própria.
4. Centralizar tokens e estilos de componentes em uma camada própria, reduzindo a convivência entre tema legado, Tailwind e CSS inline.
5. Usar JavaScript progressivo por comportamento, sem criar uma SPA para páginas indexáveis.
6. Separar scripts de integração de scripts puramente visuais.
7. Migrar template por template, mantendo a página antiga disponível para rollback até passar pelos gates.

## 10. Matriz de preservação

| Preservar sem alteração funcional | Evoluir de forma controlada | Não transportar |
|---|---|---|
| URLs canônicas, slugs, controllers e DocTypes | Layout, hierarquia, responsividade e estados | Código React/Next.js das referências |
| Eventos, consentimento, UTMs e endpoints | Includes Jinja e CSS compartilhado | jQuery, Select2, Slick e plugins pesados |
| Conteúdo útil e dados estruturados corretos | Componentes de cards, FAQ, vídeo e formulários | Conteúdo fictício e ativos demonstrativos |
| Login, matrícula, checkout e CRM | Mensagens, acessibilidade e feedback de erro | Carrinho e metáforas de marketplace |
| Pessoas, preços e provas reais | Curadoria de imagens e narrativa | Estrelas, contadores e depoimentos sem fonte |

## 11. Critérios para aceitar um componente no redesign

- Possui função clara em pelo menos um dos nove templates.
- Funciona sem JavaScript quando a função principal puder ser server-rendered.
- Tem estados de carregamento, vazio, erro, foco, hover e disabled definidos.
- Recebe dados reais por contrato, sem conteúdo demonstrativo embutido.
- Preserva analytics e consentimento quando participa de conversão.
- É navegável por teclado e tem semântica adequada.
- Não adiciona uma dependência apenas para um efeito visual.
- Tem comportamento mobile definido antes do desktop.
- Não altera canonical, slug ou hierarquia de headings por acidente.

Este mapa deve ser aprovado junto com o plano de design system antes de qualquer implementação.

## 12. Dados reais confirmados — proof bar da Home

Fonte auditável para o bloco "proof bar verificável" citado na seção T1 (Homepage, item 38) e liberado pela regra da seção 8/10 ("remover estrelas, contadores e indicadores sem fonte auditável"). Números confirmados pelo dono do produto em 2026-08-24, pendentes apenas de definir a metodologia de cálculo exata (período, base de clientes ativos vs. históricos) antes da publicação.

| Indicador | Valor confirmado | Observação |
|---|---|---|
| Estudantes satisfeitos | 98% | — |
| Anos de experiência | 9 | — |
| Alunos matriculados | +2M | — |
| Clientes empresariais | +8mil | — |

Referência visual de layout (não usar como fonte de dado): mockup de template em `vedium-references/`, com números de exemplo (95% / +15 / +3,5M / +14K) que **não são da Vedium** e não devem ser reaproveitados.
