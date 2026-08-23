> **IMPORTANTE:**
>
> - O único projeto que pode receber novos arquivos é `vedium`.
> - `edumon` e `eduall` são referências SOMENTE PARA LEITURA.
> - Não modifique nenhum arquivo dentro de `edumon` ou `eduall`.
> - Nesta fase, não modifique nenhum arquivo existente do projeto `vedium`.
> - A única escrita permitida é criar os 5 arquivos solicitados em `vedium/docs/redesign/`.

# 05 — Plano de migração do site completo

## Resultado esperado

Migrar o site público para o novo sistema visual sem trocar a stack Frappe/Jinja, perder URLs indexadas, romper integrações ou redesenhar inadvertidamente a aplicação em `app.vediums.com`. O rollout deve ocorrer por templates e lotes de rotas, com comparação antes/depois e rollback por lote.

Este plano não autoriza implementação. Ele descreve a sequência para uma fase posterior.

## 1. Regras de migração

1. `vedium` continua sendo a fonte de verdade.
2. Edumon orienta composição; EduAll complementa professores, pricing, steps e testimonials. Nenhum deles fornece código de produção.
3. URL válida/indexada é preservada por padrão. Mudança exige evidência, redirect 301 específico e atualização de canonical, hreflang, sitemap e links internos.
4. Controllers, DocTypes, endpoints e parâmetros são preservados antes de qualquer refatoração.
5. O HTML principal continua server-rendered; interação é progressiva.
6. Nenhuma prova social, métrica, preço ou pessoa entra como placeholder público.
7. Cada lote precisa passar por SEO, acessibilidade, analytics, integração, conteúdo, responsividade e performance.
8. CSS e bibliotecas legadas só são removidos depois que a última rota dependente for identificada.
9. Marketing (`vediums.com`) e produto (`app.vediums.com`) têm papéis distintos, mesmo quando compartilham Frappe.
10. A configuração real de produção deve ser reconciliada antes do cutover: há documentação/workflow de site estático no repositório, enquanto o domínio atual responde pela aplicação Frappe.
11. As divergências registradas na auditoria são evidência e dívida de decisão, não tarefas desta fase. **Não corrigir nenhuma delas na Fase 0.**
12. As conclusões técnicas aprovadas permanecem: Frappe SSR/Jinja, controllers e DocTypes, URLs e integrações atuais, matriz de redirects e separação entre marketing/produto. Edumon e EduAll continuam apenas como referências; nenhum runtime Next/React será importado.

## 2. Prioridades

| Prioridade | Significado |
|---|---|
| P0 | Contrato/fundação que bloqueia todos os lotes |
| P1 | Alto tráfego, descoberta e receita |
| P2 | Suporte importante à decisão e SEO |
| P3 | Cauda longa, institucional ou lote posterior |
| Fora | Não deve receber o redesign público neste programa |

### Regra global de risco alto

Independentemente do risco visual/SEO atribuído a uma linha da matriz, qualquer mudança futura que toque um dos itens abaixo recebe automaticamente **RISCO ALTO** — ou **CRÍTICO** quando puder cobrar, conceder acesso ou retirar o site do ar:

- Nginx, Cloudflare, proxy, host rewrite, cache ou origem de publicação;
- qualquer redirect, inclusive status, destino, regex, preservação de path/query e ordem de resolução;
- slug público, ID interno de curso ou mapeamento entre eles;
- gerador/conteúdo do sitemap e política de inclusão;
- canonical, hreflang, robots ou index/noindex;
- login, cadastro, sessão, return URL ou transição entre `vediums.com` e `app.vediums.com`;
- checkout, preço, moeda, período, frequência, Stripe, webhook ou matrícula;
- GTM, GA4, Meta Pixel, consentimento, `dataLayer`, UTMs, WhatsApp, formulários, CRM, Brevo, APIs ou qualquer outra integração.

Consequência: nenhuma dessas mudanças pode “entrar junto” como ajuste oportunista de um template. Exige inventário antes/depois, responsável, testes contratuais, rollback e plano aprovado. As classificações “Baixo” ou “Médio” da matriz se referem somente à troca de apresentação preservando todos esses contratos.

## 3. Matriz de migração

As famílias dinâmicas representam todas as URLs concretas que resolvem pelo mesmo código. O snapshot de 336 URLs do sitemap deve ser expandido em planilha de cutover antes da implementação.

| URL atual | Tipo de página | Origem no código | Manter URL? | Novo template | Componentes necessários | Prioridade | Risco SEO | Observações |
|---|---|---|---|---|---|---|---|---|
| `/` | Homepage | `www/index.html` + `index.py` | Sim | T1 Homepage | Header, hero, proof bar, idiomas, processo, professores, pricing, blog, CTA, footer | P1 | Alto | Catálogo e planos vêm de dados reais; eliminar ratings fixos sem perder conteúdo útil |
| `/cursos-de-idiomas-online` | Hub | Rule → `www/catalogo.*` | Sim, canônica | T2 Hub | Hero, filtros, language/course cards, orientação, CTA | P1 | Alto | Preservar `ItemList` e links para todos os cursos publicados |
| `/cursos` | Alias 200 | Rule → catálogo | Sim inicialmente | T2 Hub | Mesmo hub | P2 | Médio | Manter canonical para o hub; decidir 301 só com dados de busca/backlinks |
| `/trilhas` | Alias 200 | Rule → catálogo | Sim inicialmente | T2 Hub | Mesmo hub | P2 | Médio | Mesmo tratamento de `/cursos` |
| `/catalogo` | Redirect legado | `website_redirects` | Sim como 301 | Sem página | Redirect | P0 | Alto | Testar destino e ausência de cadeia |
| `/curso-de-ingles-online` | Pilar | Wrapper/controller + `marketing_landing.html` + `LANDINGS` | Sim | T3 Pilar | Breadcrumb, hero, níveis, professores, método, FAQ, artigos, CTA | P1 | Alto | Hreflang e schemas existentes |
| `/curso-de-ioruba-online` | Pilar | Wrapper/controller + `LANDINGS` | Sim | T3 Pilar | Mesmos, com contexto cultural real | P1 | Alto | Preservar grafia/slugs; publicação depende de revisão do professor/especialista responsável |
| `/portugues-para-estrangeiros` | Pilar | Wrapper/controller + `LANDINGS` | Sim | T3 Pilar | Hero, trilha PLE, professores, teste, FAQ, CTA | P1 | Alto | Núcleo das versões traduzidas e do teste PLE |
| `/curso-de-espanhol-online` | Pilar | Wrapper/controller + `LANDINGS` | Sim | T3 Pilar | Breadcrumb, hero, níveis, professores, FAQ, CTA | P1 | Alto | Preservar dados estruturados e alternativas |
| `/curso-de-hebraico-online` | Pilar | Wrapper/controller + `LANDINGS` | Sim | T3 Pilar | Breadcrumb, hero, trilhas, professores, FAQ, CTA | P1 | Alto | Tipografia precisa suportar hebraico quando houver conteúdo no script |
| `/ingles-para-entrevista` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, cenários, percurso, método, FAQ, CTA | P2 | Médio | Não prometer resultado de contratação |
| `/ingles-para-programadores` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, cenários, percurso, prova, CTA | P2 | Médio | Manter intenção de busca e conteúdo técnico útil |
| `/ingles-executivo` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, percurso, diferenciais, CTA | P2 | Médio | Distinguir jornada individual e B2B |
| `/ingles-para-viagens` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, situações, percurso, FAQ, CTA | P2 | Médio | Evitar aparência infantil/turística genérica |
| `/ingles-para-atendimento-ao-cliente` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, casos de uso, percurso, CTA | P2 | Médio | Pode encaminhar B2B sem alterar canonical |
| `/ioruba-para-iniciantes` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, percurso, contexto, FAQ, CTA | P2 | Alto | Relacionar ao nível básico real; gate de revisão do professor/especialista |
| `/ioruba-cultura-e-ancestralidade` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero editorial, contexto, percurso, professores, CTA | P2 | Alto | Gate cultural especializado obrigatório antes da publicação |
| `/portugues-para-executivos` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, casos de uso, percurso, CTA | P2 | Médio | Relacionar a PLE e B2B sem duplicar texto |
| `/preparatorio-celpe-bras` | Objetivo | `LANDINGS` + include | Sim | T5 Objetivo | Hero, preparação, percurso, FAQ, CTA | P2 | Alto | Declarações sobre prova devem ser factuais e atuais |
| `/curso/ingles-basico-a1` | Nível | Rule → `www/curso.*` + LMS | Sim | T4 Nível | Hero, metadados, currículo, professor, pricing, FAQ, matrícula | P1 | Alto | ID interno diferente do slug público |
| `/curso/ingles-elementar-a2` | Nível | Rule → `www/curso.*` + LMS | Sim | T4 Nível | Mesmo template | P1 | Alto | Preservar progressão e schema `Course`/`Offer` |
| `/curso/ingles-pre-intermediario` | Nível | Rule → `www/curso.*` + LMS | Sim | T4 Nível | Mesmo template | P1 | Alto | Conflito A2+/B1/B1+; separar ID, slug, rótulo público e CEFR sem renomear |
| `/curso/ingles-intermediario-b1` | Nível | Rule → `www/curso.*` + LMS | Sim | T4 Nível | Mesmo template | P1 | Alto | Validar ligações anterior/próximo |
| `/curso/ingles-intermediario-superior-b2` | Nível | Rule → `www/curso.*` + LMS | Sim | T4 Nível | Mesmo template | P1 | Alto | Manter slug e ID interno |
| `/curso/ingles-avancado-c1` | Nível | Rule → `www/curso.*` + LMS | Sim | T4 Nível | Mesmo template | P1 | Alto | Manter slug e ID interno |
| `/curso/ioruba-{basico,intermediario,avancado}` | Níveis (3) | `www/curso.*` + LMS | Sim, cada URL | T4 Nível | Curso, currículo, professor, pricing, FAQ, CTA | P1 | Alto | Expandir em três casos de teste |
| `/curso/portugues-para-estrangeiros-{basico,intermediario,avancado}` | Níveis PLE (3) | `www/curso.*` + LMS + traduções | Sim, cada URL | T4 Nível | Curso, currículo, professor, pricing, FAQ, CTA | P1 | Alto | QA em todos os idiomas disponíveis |
| `/curso/espanhol-{basico,intermediario,avancado}` | Níveis (3) | `www/curso.*` + LMS | Sim, cada URL | T4 Nível | Curso, currículo, professor, pricing, FAQ, CTA | P1 | Alto | Preservar faixas A1–C1 apresentadas |
| `/curso/hebraico-a0-alfabetizacao` | Nível | `www/curso.*` + LMS | Sim | T4 Nível | Curso, currículo, professor, pricing, FAQ, CTA | P1 | Alto | Distinguir alfabetização de curso moderno |
| `/curso/hebraico-moderno-a1` | Nível | `www/curso.*` + LMS | Sim | T4 Nível | Mesmo template | P1 | Alto | Testar texto bidirecional se usado |
| `/curso/hebraico-moderno-a2-b1` | Nível | `www/curso.*` + LMS | Sim | T4 Nível | Mesmo template | P1 | Alto | Preservar faixa no título/schema |
| `/curso/hebraico-biblico-leitura-guiada` | Produto específico | `www/curso.*` + LMS | Sim | T4 Nível variante | Curso, formato, professor, pricing, FAQ, CTA | P1 | Alto | Não forçar à progressão linear |
| `/curso/hebraico-particular` | Produto 1:1 | `www/curso.*` + LMS | Sim | T4 Nível variante | Curso, formato, professor, pricing, CTA | P1 | Alto | Pricing e checkout podem diferir |
| `/curso/<id-interno-legado>` | Redirect legado | `course_urls.py`/hooks | Sim como 301 | Sem página | Redirect | P0 | Alto | Gerar lista exata e impedir cadeias/loops |
| `/professores` | Redirect atual; índice futuro | `website_redirects` → `/sobre`; dados em `Course Instructor`/`User` | Manter 301 agora; tornar canônica 200 após gates | T6 Professores | Hero, critérios, teacher cards, vínculos, CTA | P1 | Alto | Direção aprovada por prova/E-E-A-T/confiança/conversão; exige docentes, imagens, dados e conteúdo aprovados |
| Futuro: `/professores/<slug>` | Perfil planejado | `Course Instructor`/`User` + conteúdo editorial aprovado | Criar somente após gates | T6 Perfil de professor | Breadcrumb, foto, bio, idiomas, cursos, CTA | P2 | Alto | Não existe hoje; cada perfil exige autorização de imagem e dados profissionais verificados |
| `/sobre` | Institucional | `www/sobre.html` | Sim | T9 Institucional | Hero, história, pessoas, valores, CTA | P2 | Médio | Hoje recebe intenção de `/professores` |
| `/empresas` | B2B | `www/empresas.*` | Sim | T7 B2B | Hero, formatos, processo, prova, lead form, FAQ | P1 | Alto | Preservar envio de intenção, CRM, Brevo e eventos |
| `/parcerias` | B2B/parcerias | `www/parcerias.*` | Sim | T7 B2B variante | Hero, modelos, processo, formulário, CTA | P2 | Médio | Não misturar lead de parceria com empresa |
| `/blog` | Índice editorial | `www/blog.*` + código/DocType | Sim | T8 Blog índice | Hero editorial, categorias, cards, paginação, CTA | P1 | Alto | Filtros por query continuam `noindex,follow` |
| `/blog/{ingles,ioruba,hebraico,espanhol}` | Categoria | `blog_post.py` + `blog_category.html` | Sim | T8 Categoria | Breadcrumb, título, cards, paginação, CTA | P2 | Alto | Segmentos reservados no controller |
| `/blog/<slug>` | Artigo/legado | `blog_post.py` + template/conteúdo | Sim ou 301 já existente | T8 Artigo | Breadcrumb, artigo, autor/data reais, relacionados, CTA | P2 | Alto | Canonical decide plano; não converter em massa |
| `/blog/<categoria>/<slug>` | Artigo | `blog_post.py` + código/DocType | Sim | T8 Artigo | Mesmo template | P2 | Alto | Preservar schema `BlogPosting` e links internos |
| `/como-funciona` | Institucional/processo | `www/como-funciona.*` | Sim | T9 Institucional | Hero, process steps, FAQ, CTA | P2 | Médio | Pode reutilizar processo, sem duplicar a home |
| `/metodologia` | Institucional | `www/metodologia.*` | Sim | T9 Institucional | Hero, princípios, progressão, professores, CTA | P2 | Médio | Diferenciar método de funcionamento |
| `/diferenciais` | Institucional | `www/diferenciais.*` | Sim | T9 Institucional | Hero, feature list, prova, CTA | P2 | Médio | Afirmações precisam de evidência |
| `/aulas-ao-vivo` | Institucional | `www/aulas-ao-vivo.*` | Sim | T9 Institucional | Hero, funcionamento, processo, FAQ, CTA | P2 | Médio | Diferencial central; manter links para cursos |
| `/certificado` | Institucional/ferramenta | `www/certificado.*` + `verify_certificate` | Sim | T9 Institucional variante | Hero, explicação, verificação, FAQ | P2 | Alto | Não romper endpoint nem exposição segura de dados |
| `/comunidade` | Institucional | `www/comunidade.*` | Sim | T9 Institucional | Hero, benefícios reais, participação, CTA | P3 | Médio | Evitar contagens sem fonte |
| `/planos` | Conversão | `www/planos.*` | Sim | T9 Conversão | Hero, pricing, frequência, FAQ, CTA | P1 | Alto | Preservar IDs, períodos, eventos e transparência |
| `/matricula` | Conversão | `www/matricula.*` | Sim | T9 Conversão | Hero, seleção, resumo, CTA/launcher | P1 | Alto | Preservar curso/plano/objetivo e transição para app |
| `/quanto-custa-curso-de-idiomas` | Conversão/SEO | `www/quanto-custa-curso-de-idiomas.*` | Sim | T9 Conversão | Conteúdo, comparação factual, pricing, FAQ, CTA | P2 | Alto | Valores precisam vir de fonte atual |
| `/aula-diagnostica` | Conversão | `www/aula-diagnostica.*` + API | Sim | T9 Formulário | Hero, explicação, form, status, FAQ | P1 | Alto | Preservar `request_diagnostic_class` e eventos |
| `/teste-de-nivel` | Ferramenta/conversão | `www/teste-de-nivel.*` | Sim | T9 Teste | Intro, questões, progresso, resultado, captura, CTA | P1 | Alto | Scoring e captura opcional não podem mudar por CSS |
| `/teste-de-nivel-ingles` | Ferramenta/conversão | `www/teste-de-nivel-ingles.*` | Sim | T9 Teste | Mesmo conjunto | P1 | Alto | Preservar regras e eventos específicos |
| `/contato` | Conversão | `www/contato.html` + `api.send_contact_message` | Sim | T9 Formulário | Hero, canais, form, status | P2 | Alto | Validar antispam, consentimento e CRM |
| `/faq` | Suporte | `www/faq.*` | Sim | T9 FAQ | Hero, grupos, busca opcional, accordion, CTA | P2 | Médio | Schema deve refletir exatamente o conteúdo visível |
| `/programa-de-indicacao` | Conversão | `www/programa-de-indicacao.*` | Sim | T9 Conversão | Hero, regras, processo, CTA | P3 | Médio | Área real fica em `app.vediums.com` |
| `/carreiras` | Conversão | `www/carreiras.*` + `careers.py` | Sim | T9 Formulário | Hero, cultura, vagas, form, status | P3 | Médio | Preservar candidatura e tratamento de dados |
| `/imprensa` | Institucional | `www/imprensa.*` | Sim | T9 Institucional | Hero, materiais reais, contato | P3 | Baixo | Não criar logos/cobertura fictícios |
| `/termos` | Legal | `www/termos.html` | Sim | T9 Legal | Header simples, sumário, conteúdo, footer | P2 | Alto | Texto jurídico não deve ser resumido por estética |
| `/privacidade` | Legal | `www/privacidade.html` | Sim | T9 Legal | Sumário, conteúdo, preferências/contato | P2 | Alto | Coordenar com consentimento e LGPD |
| `/cookies` | Legal | `www/cookies.html` | Sim | T9 Legal | Conteúdo e controle de preferências | P2 | Alto | Deve refletir tags realmente carregadas |
| `/cancelamento-reembolso` | Legal | `www/cancelamento-reembolso.html` | Sim | T9 Legal | Sumário, conteúdo, contato | P2 | Alto | Manter conteúdo integral e data de vigência |
| `/gravacao-imagem-voz` | Legal | `www/gravacao-imagem-voz.*` | Sim | T9 Legal | Sumário e conteúdo | P3 | Alto | Revisão jurídica antes de alterar texto |
| `/propriedade-intelectual` | Legal | `www/propriedade-intelectual.*` | Sim | T9 Legal | Sumário e conteúdo | P3 | Alto | Revisão jurídica antes de alterar texto |
| `/privacidade/meus-dados` | LGPD funcional | `www/privacidade/meus-dados.*` | Sim | T9 Legal/ferramenta | Explicação, autenticação/form, status | P2 | Alto | Preservar `noindex,follow` e controles de identidade |
| `/pratica-diaria` | Conteúdo funcional | `www/pratica-diaria.*` | Sim | Exceção | Shell mínimo e experiência existente | P3 | Médio | Preservar `noindex`; decidir produto vs marketing |
| `/{en,es,fr,de,ru}` | Homes localizadas | `www/<lang>/index.*` | Sim, cada URL | T1 localizada | Home com conteúdo real por locale | P2 | Alto | Não traduzir automaticamente; russo não aparece em todo hreflang atual |
| `/<lang>/{catalogo,sobre,como-funciona,faq,contato,planos,matricula,aula-diagnostica,certificado,comunidade,programa-de-indicacao,empresas,carreiras,diferenciais,metodologia}` | Famílias localizadas | `www/<lang>/` + `SAME_SLUG_TRANSLATIONS` | Sim, cada URL existente | T2/T7/T9 localizado | Componentes do template correspondente | P2 | Alto | Expandir e testar cada combinação real, sem presumir paridade |
| Slugs localizados de pilares/objetivos | Landing localizada | Wrappers + `LANDINGS` | Sim, cada URL | T3/T5 localizado | Pilar/objetivo localizado | P2 | Alto | Hreflang recíproco e tradução humana |
| `/{en,es,fr,de}/<teste-PLE-localizado>` | Teste localizado | Páginas/controllers reais | Sim | T9 Teste localizado | Teste, resultado, captura, CTA | P2 | Alto | Não inventar equivalente russo |
| `/{en,es,fr,de,ru}/curso/<slug>` | Curso localizado | Rule + `curso.py` + `COURSE_TRANSLATIONS` | Sim quando há conteúdo | T4 localizado | Componentes do curso | P2 | Alto | Preservar redirect ao PT quando tradução não existe |
| `/{en,es}/blog` e categorias/posts prefixados | Blog localizado | `blog.py`/`blog_post.py` | Sim | T8 localizado | Índice/categoria/artigo | P2 | Alto | Famílias prefixadas declaradas apenas para en/es |
| Artigos FR/DE/RU/ZH em `/blog/<slug>` | Artigo localizado plano | Conteúdo + `blog_post.py` | Sim | T8 Artigo | Artigo, breadcrumb, relacionados | P3 | Alto | Não adicionar prefixo sem migração SEO específica |
| `/pt-br` e `/pt-br/<rota>` | Alias duplicado | Rules/controller | Sim inicialmente | Template PT correspondente | Mesmo componente | P3 | Médio | Canonical atual aponta ao não prefixado; avaliar 301 separadamente |
| Prefixos `en-us`, `en-au`, `es-ar`, `es-co`, `fr-ca` | Redirect regional | `website_redirects` | Sim como 301 | Sem página | Redirect | P0 | Alto | Testar preservação de path/query e evitar cadeia |
| `/login` | Login Frappe local | Core Frappe | Sim tecnicamente | Fora | Shell nativo | Fora | Alto | Não promover; estratégia precisa considerar o domínio app |
| `https://app.vediums.com/login` e `#signup` | Auth oficial | Frappe/app | Sim | Fora | Transição de marca apenas em programa próprio | P0 | Alto | Destinos de header/footer |
| `/register` e `/signup` | 404 atual | Sem rota válida | Não criar implicitamente | Fora | Nenhum | Fora | Médio | Não usar em CTAs |
| `/aluno`, `/onboarding`, `/minhas-indicacoes` | Autenticadas | Controllers próprios | Sim | Exceção/produto | Auth redirect e shell do produto | Fora | Alto | Preservar `noindex` e return URL |
| `/lms`, `/lms/courses` e Desk | Produto | Apps Frappe/LMS | Sim | Fora | Componentes do produto | Fora | Alto | Não incluir no rollout do marketing |
| `/robots.txt` | SEO técnico | `www/robots.py`/txt | Sim | Fora | Texto | P0 | Crítico | Snapshot e teste de regras antes/depois |
| `/sitemap.xml` | SEO técnico | `www/sitemap.py`/xml | Sim | Fora | XML | P0 | Crítico | Reconciliar lista estática e conteúdo dinâmico |
| `/llms.txt` | Descoberta técnica | `www/llms.txt` | Sim | Fora | Texto | P3 | Baixo | Conferir links após migração |
| `/sw.js` e `/manifest.json` | PWA | Arquivos/rotas públicas | Sim | Fora | Service worker/manifesto | P0 | Alto | Preservar paths, MIME, escopo e cache |
| APIs públicas, checkout e webhooks | Integração | `api.py`, `public_funnel.py`, checkout, Stripe | Sim | Fora | Contratos HTTP | P0 | Crítico | Redesign só muda consumidores após testes contratuais |

## 4. Fases propostas

### Fase A — Congelamento e linha de base

- Exportar todas as URLs do sitemap e acrescentar rotas públicas fora dele.
- Para cada URL, registrar status, redirect, canonical, robots, title, description, H1, hreflang, schemas, links internos e captura visual.
- Juntar dados de Search Console, Analytics e backlinks para priorização e decisão sobre aliases.
- Registrar eventos e payloads reais por fluxo.
- Capturar requests/responses de formulários, teste, WhatsApp, login, matrícula e Stripe sem dados pessoais.
- Identificar a configuração ativa de Nginx/Cloudflare e reconciliá-la com `deploy/site` e o workflow estático legados.
- Aprovar taxonomia de níveis e inventário de prova social.
- Usar o registro de divergências de `01-current-stack-audit.md` como checklist de investigação; não corrigir seus itens durante o levantamento.

Saída/gate: baseline reproduzível, tabela URL a URL e plano de rollback.

### Fase B — Fundação

- Aprovar tokens, tipografia, grid, imagens e critérios de conteúdo.
- Implementar futuramente o shell Jinja e componentes globais em isolamento.
- Preparar todos os componentes desde o início para receber locale pelo contexto server-side.
- Testar comprimento variável de texto, caracteres internacionais e cobertura/fallback de fontes com conteúdo real.
- Preparar propriedades lógicas e comportamento RTL quando necessário, sem presumir que todo locale é LTR.
- Tratar canonical e hreflang como contratos do template/controller desde a fundação; componentes não inferem ou traduzem slugs.
- Separar integração/consentimento da marcação visual do footer.
- Definir adaptador de contexto para componentes sem mudar contratos dos controllers.
- Criar testes de HTML/metadados, acessibilidade e regressão visual.

Saída/gate: biblioteca mínima aprovada em estados mobile/desktop, expansão de texto, caracteres internacionais, fallback tipográfico e RTL aplicável, sem rota pública migrada.

### Fase C — Piloto de baixo raio de impacto

- Escolher uma página institucional representativa e uma landing de objetivo com tráfego moderado.
- Migrar sem mudar URL, copy essencial ou controller.
- Comparar HTML, analytics, performance e indexabilidade.
- Exercitar rollback.

Saída/gate: duas rotas estáveis por um período acordado e nenhum evento/metadata perdido.

### Fase D — Núcleo de descoberta e conversão

- Migrar home, hub, pilares e templates de curso.
- Incluir as páginas internacionais prioritárias de Português para Estrangeiros, especialmente a jornada principal em inglês: `/en/learn-portuguese-brazil`, `/en/portuguese-placement-test`, `/en/catalogo`, `/en/planos`, `/en/matricula`, `/en/aula-diagnostica` e URLs traduzidas de curso que já existirem.
- Preservar as URLs e traduções existentes de PLE, incluindo pilar, teste, páginas de suporte/matrícula e cursos que já têm conteúdo real; não criar equivalentes ausentes.
- Depois, planos, matrícula, aula diagnóstica e testes de nível.
- Liberar por template/idioma, não todas as rotas em uma única publicação.
- Manter monitoramento de 404, redirects, eventos, leads e checkout.

Saída/gate: jornadas PT e PLE prioritária em inglês — home/pilar → curso → plano/teste → app — funcionam com URLs, traduções, dados e atribuição preservados.

### Fase E — Conteúdo e autoridade

- Migrar blog, categorias, artigos e páginas de método/diferenciais.
- Validar as duas fontes do blog e todas as formas de URL.
- Preservar conteúdo útil mesmo que não se encaixe em blocos visuais preferidos.

Saída/gate: paridade do sitemap e dos schemas editoriais, sem queda de links internos.

### Fase F — B2B, institucional, conversão secundária e legal

- Migrar empresas/parcerias, contato, carreiras, comunidade, indicação e imprensa.
- Migrar páginas legais sem reescrita não aprovada.
- Tratar ferramentas/noindex como lotes separados.

Saída/gate: formulários e políticas validados pelos responsáveis.

### Fase G — Localização

- Completar o rollout das demais famílias localizadas existentes, incluindo francês, alemão, russo e as outras páginas já publicadas.
- Aplicar templates aprovados somente a conteúdos e traduções reais já existentes ou editorialmente aprovados.
- Testar direção/escrita, fonte, comprimento, hreflang recíproco e fallback.
- Manter assimetrias intencionais: não criar traduções ou rotas inexistentes artificialmente apenas para “completar” a grade.

Saída/gate: cada locale existente tem matriz de paridade e revisão humana; lacunas permanecem documentadas em vez de preenchidas automaticamente.

### Fase H — Limpeza e estabilização

- Só então remover CSS, JS, imagens e vendors comprovadamente sem consumidores.
- Decidir aliases 200 versus 301 com dados pós-migração.
- Atualizar documentação de deploy para refletir a arquitetura real em uma mudança própria.
- Monitorar indexação, Core Web Vitals, erros, conversão e leads.

Saída/gate: duas janelas de monitoramento estáveis e rollback encerrado formalmente.

## 5. Gates obrigatórios por lote

### Identidade visual, tipografia e locale

- Tokens de cor continuam candidatos até serem validados contra logos e ativos oficiais da Vedium.
- Todos os pares e estados relevantes passam por contraste WCAG.
- Cobertura e fallback de fontes são testados em todos os idiomas existentes.
- `Playfair Display` é usado apenas de forma seletiva/editorial; legibilidade e consistência de interface têm prioridade.
- Componentes aceitam comprimento variável, caracteres internacionais e RTL quando necessário.
- Canonical e hreflang chegam do contrato do template/controller e permanecem coerentes com o locale real.

### SEO

- Status e URL final iguais ao baseline, salvo mudança aprovada.
- Canonical absoluto e autorreferente na página canônica.
- Hreflang recíproco somente entre páginas reais.
- Title, description, H1 e conteúdo essencial preservados ou aprovados.
- Structured data semanticamente correto, válido e coerente com o conteúdo visível; não implementar schema apenas para perseguir rich results.
- Priorizar `Organization`, `BreadcrumbList`, `BlogPosting` e outras marcações realmente pertinentes.
- `Course` e `FAQPage` existentes podem permanecer quando corretos, sem serem tratados como objetivo do redesign.
- Breadcrumb visual e estruturado alinhados.
- Sitemap, robots e links internos sem regressão.
- Nenhuma nova 404, cadeia, loop ou redirect temporário.

### Analytics e conversão

- GTM carrega sob as mesmas regras.
- Meta Pixel continua bloqueado até consentimento.
- Eventos relevantes aparecem uma vez, com parâmetros esperados.
- UTMs sobrevivem à navegação necessária.
- WhatsApp usa número/mensagem aprovados e registra intenção.
- Testes preservam pontuação, resultado e captura opcional.
- Formulários chegam ao CRM e acionam sincronizações previstas.
- Matrícula/Stripe preservam curso, plano, frequência, período, moeda, origem e objetivo.
- Todos os CTAs relevantes passam pela matriz CTA → evento → destino → sistema final de `03-template-component-map.md`.

### Acessibilidade e UX

- Fluxo completo por teclado e foco visível.
- Menu, modal, tabs, acordeão, teste e formulários com estados anunciados.
- Contraste AA, zoom/reflow e redução de movimento.
- Imagens reais com alternativa e dimensões.
- Conteúdo e ação principal utilizáveis em mobile.

### Performance

- LCP, INP e CLS comparados à linha de base em laboratório e campo.
- Sem regressão material de HTML, CSS, JS, imagens, fontes e requests.
- Nenhum asset pesado das referências é transportado sem necessidade.
- Service worker não mantém HTML/CSS antigo indefinidamente.

### Conteúdo e dados

- Pessoas, preços, disponibilidade e progressão vêm da fonte correta.
- Nenhum placeholder ou prova fictícia.
- ID interno, slug histórico, rótulo público e nível CEFR permanecem campos conceitualmente separados.
- A taxonomia pedagógica de inglês — com sequência pública a validar A1, A2, B1, B1+, B2 e C1 — precisa estar aprovada antes do componente de progressão; URLs, IDs, registros LMS e redirects não são renomeados.
- Tradução revisada.
- Estados vazios não expõem dados demonstrativos.
- Perfis e índice de professores só publicam docentes confirmados, imagens autorizadas, dados profissionais verificados e conteúdo editorial aprovado.
- **Conteúdo de Iorubá que envolva língua, história, cultura, práticas, produção cultural ou contexto afro-brasileiro exige revisão do professor/especialista responsável antes da publicação.**
- Esse gate aplica-se especialmente a `/curso-de-ioruba-online`, `/ioruba-para-iniciantes` e `/ioruba-cultura-e-ancestralidade`, sem alterar essas páginas na Fase 0.

## 6. Estratégia de release e rollback

1. Feature flag ou seleção de template por rota/lote, sem duplicar URL pública.
2. Deploy da fundação sem ativação.
3. Ativação canário nas rotas piloto.
4. Smoke tests server-side e em navegador após cada ativação.
5. Monitoramento de logs, 404/5xx, eventos, leads e checkout.
6. Rollback deve restaurar template e assets compatíveis sem restaurar banco.
7. Migrações de banco não devem ser necessárias para a primeira troca visual; se surgirem, separar release e rollback.
8. Cache de Cloudflare, Nginx, Frappe e service worker precisa de procedimento explícito de purga/versionamento.

## 7. Dependências e decisões bloqueadoras

- Configuração ativa de produção e responsabilidade entre Cloudflare, Nginx, Frappe e workflow legado.
- Lista completa do Search Console e backlinks.
- Taxonomia pedagógica final e mapeamento explícito entre ID interno, slug histórico, rótulo público e CEFR.
- Validação dos tokens candidatos contra logos/ativos, contraste WCAG e licenças/cobertura de fontes, ícones e imagens.
- Professores confirmados, autorizações de imagem, dados profissionais verificados, conteúdo editorial e depoimentos aprovados.
- Regras de preço/frequência e ownership do checkout.
- Plano de ativação da direção aprovada para `/professores` 200 e `/professores/<slug>`, incluindo retirada controlada do redirect atual.
- Escopo de alinhamento visual do domínio `app.vediums.com`.
- Estratégia de convivência e futura retirada de Bootstrap, Tailwind e CSS do tema.

## 8. Definição de pronto do programa

- As 336 URLs do snapshot, mais rotas públicas fora do sitemap, estão classificadas e testadas.
- Todos os templates têm paridade funcional, SEO e de conteúdo.
- A fundação é locale-aware e a jornada prioritária de PLE em inglês foi migrada antes do rollout completo das demais famílias.
- Redirects e canonicals têm uma única fonte de verdade.
- Home, catálogo, cursos, testes, formulários, WhatsApp, login, matrícula e checkout funcionam ponta a ponta.
- Nenhuma integração dispara antes do consentimento aplicável.
- Não há conteúdo fictício nem ativos das referências publicados por engano.
- Índice/perfis de professores cumprem os gates de confirmação, autorização e verificação; conteúdo cultural de Iorubá tem aprovação especializada registrada.
- Métricas de acessibilidade e performance atingem os budgets aprovados.
- Documentação de operação e rollback corresponde ao deploy real.
- A remoção do legado foi feita somente após prova de ausência de dependências.

Até a aprovação deste plano, a ação correta é não alterar frontend, rotas, dependências, infraestrutura ou deploy.
