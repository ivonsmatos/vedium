> **IMPORTANTE:**
>
> - O único projeto que pode receber novos arquivos é `vedium`.
> - `edumon` e `eduall` são referências SOMENTE PARA LEITURA.
> - Não modifique nenhum arquivo dentro de `edumon` ou `eduall`.
> - Nesta fase, não modifique nenhum arquivo existente do projeto `vedium`.
> - A única escrita permitida é criar os 5 arquivos solicitados em `vedium/docs/redesign/`.

# 02 — Mapa de rotas e SEO

## Convenções deste mapa

- “Direta” significa resolução de um arquivo em `vedium_core/vedium_core/www/`.
- “Rule” significa regra em `vedium_core/vedium_core/hooks.py`.
- “DB” significa dados lidos de DocTypes no MariaDB/Frappe.
- A validação HTTP foi feita contra produção em 23/08/2026.
- O sitemap de produção continha 336 URLs. O mapa abaixo cobre todas por rota concreta ou por família dinâmica; artigos são conteúdo da família, não templates independentes.

## Ordem de resolução

1. `website_redirects` resolve aliases/legados.
2. `website_route_rules` resolve aliases internos e rotas dinâmicas.
3. Frappe resolve arquivos/pastas de `www/`.
4. O controller homônimo prepara o contexto.
5. A página pode redirecionar novamente por idioma, canonical de curso ou autenticação.

## Rotas públicas em português

| URL | Status atual | Origem |
|---|---:|---|
| `/` | 200 | Direta: `www/index.html` + `www/index.py`; consulta `LMS Course` e planos de frequência. |
| `/cursos-de-idiomas-online` | 200 | Rule → `catalogo`; `www/catalogo.html` + `catalogo.py`; consulta cursos/categorias LMS. |
| `/cursos` | 200 | Rule → `catalogo`; canonical aponta para `/cursos-de-idiomas-online`. |
| `/trilhas` | 200 | Rule → `catalogo`; canonical aponta para `/cursos-de-idiomas-online`. |
| `/catalogo` | 301 | Redirect → `/cursos-de-idiomas-online`. |
| `/curso-de-ingles-online` | 200 | `www/curso-de-ingles-online.html` + `curso_de_ingles_online.py` → `templates/includes/marketing_landing.html` + `LANDINGS`. |
| `/curso-de-ioruba-online` | 200 | Wrapper/controller + `marketing_landing.html` + `LANDINGS`. |
| `/portugues-para-estrangeiros` | 200 | Wrapper/controller + `marketing_landing.html` + `LANDINGS`. |
| `/curso-de-espanhol-online` | 200 | Wrapper/controller + `marketing_landing.html` + `LANDINGS`. |
| `/curso-de-hebraico-online` | 200 | Wrapper/controller + `marketing_landing.html` + `LANDINGS`. |
| `/ingles-para-entrevista` | 200 | Landing estruturada em `LANDINGS`. |
| `/ingles-para-programadores` | 200 | Landing estruturada em `LANDINGS`. |
| `/ingles-executivo` | 200 | Landing estruturada em `LANDINGS`. |
| `/ingles-para-viagens` | 200 | Landing estruturada em `LANDINGS`. |
| `/ingles-para-atendimento-ao-cliente` | 200 | Landing estruturada em `LANDINGS`. |
| `/ioruba-para-iniciantes` | 200 | Landing estruturada em `LANDINGS`. |
| `/ioruba-cultura-e-ancestralidade` | 200 | Landing estruturada em `LANDINGS`. |
| `/portugues-para-executivos` | 200 | Landing estruturada em `LANDINGS`. |
| `/preparatorio-celpe-bras` | 200 | Landing estruturada em `LANDINGS`. |
| `/blog` | 200 | `www/blog.html` + `blog.py`; código + DocType `Vedium Blog Post`; filtros/paginação por query string. |
| `/blog/ingles` | 200 | Rule → `blog_post`; `blog_post.py` detecta categoria reservada; `blog_category.html`. |
| `/blog/ioruba` | 200 | Mesmo controller/template de categoria. |
| `/blog/hebraico` | 200 | Mesmo controller/template de categoria. |
| `/blog/espanhol` | 200 | Mesmo controller/template de categoria. |
| `/blog/<slug>` | 200/redirect | Rule → `blog_post`; post legado plano ou categoria reservada. Canonical validado contra o conteúdo. |
| `/blog/<categoria>/<slug>` | 200 | Rule → `blog_post`; artigos novos aninhados. |
| `/professores` | 301 | Redirect em `hooks.py` → `/sobre`; não existe página própria hoje. Direção futura aprovada: página canônica própria 200, condicionada a conteúdo e autorizações verificadas. |
| `/sobre` | 200 | `www/sobre.html`; conteúdo institucional e referências a professores. |
| `/empresas` | 200 | `www/empresas.html` + `empresas.py`; B2B/intenção pública. |
| `/contato` | 200 | `www/contato.html`; envia para `vedium_core.api.send_contact_message`. |
| `/faq` | 200 | `www/faq.html` + `faq.py`; FAQ e JSON-LD. |
| `/teste-de-nivel` | 200 | `www/teste-de-nivel.html` + `teste_de_nivel.py`; PLE, scoring client-side e captura opcional. |
| `/teste-de-nivel-ingles` | 200 | `www/teste-de-nivel-ingles.html` + `teste_de_nivel_ingles.py`; inglês, scoring client-side e captura opcional. |
| `/aula-diagnostica` | 200 | `www/aula-diagnostica.html` + controller; API `request_diagnostic_class`. |
| `/planos` | 200 | `www/planos.html` + controller; CTAs e eventos de escolha de frequência. |
| `/matricula` | 200 | `www/matricula.html` + controller; monta link para `app.vediums.com` com curso/plano/objetivo. |
| `/quanto-custa-curso-de-idiomas` | 200 | Página institucional/conversão específica. |
| `/como-funciona` | 200 | Página institucional/processo. |
| `/metodologia` | 200 | Página de método e progressão. |
| `/diferenciais` | 200 | Página de diferenciação. |
| `/aulas-ao-vivo` | 200 | Página sobre formato ao vivo. |
| `/certificado` | 200 | Página + consulta pública `verify_certificate`. |
| `/comunidade` | 200 | Página institucional/comunidade. |
| `/programa-de-indicacao` | 200 | Página de conversão; área real em `app.vediums.com/minhas-indicacoes`. |
| `/parcerias` | 200 | Página de intenção/parcerias. |
| `/carreiras` | 200 | `www/carreiras.html` + `careers.py`; candidatura pública. |
| `/imprensa` | 200 | `www/imprensa.html` + `imprensa.py`. |
| `/pratica-diaria` | 200, noindex | Página pública funcional, fora do sitemap. |
| `/privacidade/meus-dados` | 200, noindex/follow | Página LGPD; requer cuidado especial com ações autenticadas. |
| `/termos` | 200 | `www/termos.html`. |
| `/privacidade` | 200 | `www/privacidade.html`. |
| `/cookies` | 200 | `www/cookies.html`. |
| `/cancelamento-reembolso` | 200 | `www/cancelamento-reembolso.html`. |
| `/gravacao-imagem-voz` | 200 | Página legal de autorização. |
| `/propriedade-intelectual` | 200 | Página legal. |

### Direção aprovada para professores

- Estado preservado na Fase 0: `/professores` continua 301 para `/sobre`.
- Estado-alvo futuro: `/professores` como índice canônico próprio 200 e `/professores/<slug>` para perfis individuais.
- Pré-condições: professores confirmados, autorização de imagem, dados profissionais verificados e conteúdo editorial aprovado.
- Prioridade de programa: índice P1 por seu papel em prova, E-E-A-T, confiança e conversão; perfis P2, liberados apenas quando cada perfil cumprir as pré-condições.
- A retirada do redirect será uma migração SEO de risco alto, com inventário de backlinks, canonical, sitemap, redirects e rollback. Não alterar rota ou código nesta fase.

## Páginas de nível/trilha: URLs dinâmicas atuais

Existe conflito explícito entre rótulos no código, slugs históricos, registros LMS e comunicação comercial. A sequência de comunicação a validar é **A1, A2, B1, B1+, B2, C1**. Ela ainda não constitui autorização para alterar dados.

Quatro conceitos devem permanecer separados:

| Conceito | Função | Pode mudar como efeito do redesign? |
|---|---|---|
| ID interno | Chave usada pelo `LMS Course`, checkout e integrações | Não |
| Slug histórico | Parte da URL pública e destino de redirects/backlinks | Não |
| Rótulo público | Nome mostrado em headings, cards, navegação e copy | Somente após aprovação pedagógica/editorial |
| Nível CEFR | Classificação pedagógica formal do conteúdo | Somente após validação do responsável pedagógico |

A hipótese de alinhamento abaixo serve apenas para expor o conflito e precisa ser validada antes do componente de progressão:

| Ordem de comunicação a validar | URL histórica preservada | Rótulo encontrado/implícito hoje | Estado |
|---|---|---|---|
| A1 | `/curso/ingles-basico-a1` | A1 | Sem conflito aparente; confirmar |
| A2 | `/curso/ingles-elementar-a2` | A2 | Sem conflito aparente; confirmar |
| B1 | `/curso/ingles-pre-intermediario` | A2+ no código atual | Conflito; não renomear URL ou ID |
| B1+ | `/curso/ingles-intermediario-b1` | B1 no slug/comunicação atual | Conflito; não renomear URL ou ID |
| B2 | `/curso/ingles-intermediario-superior-b2` | B2 | Sem conflito aparente; confirmar |
| C1 | `/curso/ingles-avancado-c1` | C1 | Sem conflito aparente; confirmar |

Não renomear URLs, IDs, registros LMS ou redirects. A taxonomia pedagógica final precisa ser aprovada antes de implementar cards/timelines de progressão, schema ou nova copy de nível.

| URL canônica | Nível/produto | Origem |
|---|---|---|
| `/curso/ingles-basico-a1` | Inglês A1 | Rule `/curso/<course>` → `www/curso.html`/`curso.py`; ID interno `ingl-s-beginner`. |
| `/curso/ingles-elementar-a2` | Inglês A2 | Mesmo template; ID `ingl-s-elementary`. |
| `/curso/ingles-pre-intermediario` | Inglês A2+ no código atual | Mesmo template; ID `ingl-s-pr-intermedi-rio`. |
| `/curso/ingles-intermediario-b1` | Inglês B1 | Mesmo template; ID `ingl-s-intermedi-rio`. |
| `/curso/ingles-intermediario-superior-b2` | Inglês B2 | Mesmo template; ID `ingl-s-upper-intermedi-rio`. |
| `/curso/ingles-avancado-c1` | Inglês C1 | Mesmo template; ID `ingl-s-avan-ado`. |
| `/curso/ioruba-basico` | Iorubá básico | Mesmo template; DB `LMS Course`. |
| `/curso/ioruba-intermediario` | Iorubá intermediário | Mesmo template; DB. |
| `/curso/ioruba-avancado` | Iorubá avançado | Mesmo template; DB. |
| `/curso/portugues-para-estrangeiros-basico` | PLE básico | Mesmo template; traduções de curso em cinco idiomas. |
| `/curso/portugues-para-estrangeiros-intermediario` | PLE intermediário | Mesmo template. |
| `/curso/portugues-para-estrangeiros-avancado` | PLE avançado | Mesmo template. |
| `/curso/espanhol-basico` | Espanhol A1–A2 | Mesmo template. |
| `/curso/espanhol-intermediario` | Espanhol B1–B2.1 | Mesmo template. |
| `/curso/espanhol-avancado` | Espanhol B2.2–C1 | Mesmo template. |
| `/curso/hebraico-a0-alfabetizacao` | Hebraico A0 | Mesmo template. |
| `/curso/hebraico-moderno-a1` | Hebraico A1 | Mesmo template. |
| `/curso/hebraico-moderno-a2-b1` | Hebraico A2/B1 | Mesmo template. |
| `/curso/hebraico-biblico-leitura-guiada` | Produto específico | Mesmo template. |
| `/curso/hebraico-particular` | Produto 1:1 | Mesmo template. |

Os antigos IDs internos em URL, como `/curso/ingl-s-beginner`, recebem `301` para o slug público. O helper `legacy_course_redirects()` também cria equivalentes por idioma.

## Rotas multilíngues

Idiomas com home própria: `en`, `es`, `fr`, `de`, `ru`. Prefixos regionais (`en-us`, `en-au`, `es-ar`, `es-co`, `fr-ca`) redirecionam para a família. `zh-cn` volta para PT na home, embora existam artigos chineses planos no blog.

| Família | URLs atuais | Origem |
|---|---|---|
| Homes | `/en`, `/es`, `/fr`, `/de`, `/ru` | `www/<lang>/index.html` + `.py`. |
| Institucionais traduzidas | `/<lang>/{catalogo,sobre,como-funciona,faq,contato,planos,matricula,aula-diagnostica,certificado,comunidade,programa-de-indicacao,empresas,carreiras,diferenciais,metodologia}` | arquivos reais em `www/<lang>/`; `SAME_SLUG_TRANSLATIONS`. |
| Pilares/objetivos | slugs localizados em `LANDINGS`, por exemplo `/en/learn-english-online`, `/es/curso-de-ingles-online-en-vivo`, `/fr/cours-anglais-en-ligne-en-direct`, `/de/englischkurs-online-live`, `/ru/kurs-angliyskogo-online` | wrappers do idioma + `marketing_landing_content.py`. |
| PLE | `/en/learn-portuguese-brazil`, `/es/portugues-para-extranjeros`, `/fr/portugais-pour-etrangers`, `/de/portugiesisch-fuer-auslaender`, `/ru/portugalskiy-dlya-inostrantsev` | landings localizadas. |
| Teste PLE | `/en/portuguese-placement-test`, `/es/prueba-de-nivel-de-portugues`, `/fr/test-de-niveau-de-portugais`, `/de/portugiesisch-einstufungstest` | páginas reais; não existe teste russo equivalente no mapa atual. |
| Cursos dinâmicos | `/{en,es,fr,de,ru}/curso/<slug>` | Rule → `curso.py`; só responde no idioma se `COURSE_TRANSLATIONS` tiver conteúdo, caso contrário redireciona ao PT. |
| Blog PLE | `/en/blog`, `/es/blog`, categorias `/en/blog/brazilian-portuguese` e `/es/blog/portugues-brasileno`, além de artigos aninhados | `blog.py`, `blog_post.py` e conteúdo. |

Assimetria importante: francês/alemão/russo têm páginas institucionais e landings, mas as route rules de blog prefixado só foram declaradas explicitamente para inglês e espanhol. Artigos franceses, alemães, russos e chineses existentes usam `/blog/<slug>` sem prefixo. Preservar canonical e não “corrigir” isso durante o redesign sem plano de redirect/hreflang.

Localização entra na fundação e no núcleo, não somente no rollout final. A Fase D deve incluir as páginas internacionais prioritárias de Português para Estrangeiros, especialmente a jornada principal em inglês (`/en/learn-portuguese-brazil`, `/en/portuguese-placement-test` e páginas de suporte/matrícula já existentes). Todas as URLs, traduções, canonicals e hreflangs atuais são preservados. Francês, alemão, russo e demais famílias existentes permanecem no rollout completo da Fase G; nenhuma tradução inexistente será criada apenas para obter simetria.

## Classificação das 336 URLs do sitemap por família

Snapshot obtido de `https://vediums.com/sitemap.xml` em 23/08/2026. A classificação abaixo é mutuamente exclusiva e totaliza 336. Para evitar dupla contagem, qualquer URL com prefixo de locale próprio (`/en`, `/es`, `/fr`, `/de` ou `/ru`) recebeu a família primária **multilíngue**; na planilha de cutover ela também deverá receber uma segunda dimensão estrutural, como curso, objetivo, artigo ou institucional.

| Família primária | Quantidade | Assinatura/exemplos | Origem e contexto |
|---|---:|---|---|
| curso | 6 | Hub canônico e cinco pilares PT | lista estática/landings + catálogo LMS |
| nível | 20 | `/curso/<slug-publico>` | `LMS Course` + `course_urls.py` + template dinâmico |
| objetivo | 9 | `/ingles-para-entrevista`, `/preparatorio-celpe-bras` | `LANDINGS` |
| blog | 67 | `/blog` e artigos PT ou artigos não-PT de URL plana | código + `Vedium Blog Post`; categorias são contadas separadamente |
| categoria | 4 | `/blog/{ingles,ioruba,hebraico,espanhol}` | `CATEGORY_PAGES`/controller de blog |
| institucional | 20 | Sobre, método, planos, testes, contato, empresas e correlatas | páginas versionadas em `www/`; inclui conversão/suporte por não haver família separada no adendo |
| legal | 6 | Termos, privacidade, cookies e políticas | páginas versionadas em `www/` |
| LMS/pública | 0 | Nenhuma no sitemap | superfícies `/lms` e autenticadas existem fora do sitemap e devem continuar fora |
| sistema/utilitária | 0 | Nenhuma no sitemap | `robots.txt`, `sitemap.xml`, `llms.txt`, `sw.js` e `manifest.json` existem, mas não devem se autolistar |
| legado | 0 | Nenhuma no sitemap | origens que redirecionam devem permanecer excluídas |
| multilíngue | 203 | Todas as URLs sob `/{en,es,fr,de,ru}` | homes, landings, níveis, blog e institucionais traduzidos; requer subtipo no cutover |
| outra | 1 | `/` | homepage |
| **Total** | **336** | — | contagem fecha com o snapshot |

Regras para a planilha final:

- cada URL recebe uma família primária e, para multilíngue, um template estrutural secundário;
- URLs não indexáveis, endpoints e redirects entram no inventário geral, mas não são adicionados artificialmente ao sitemap;
- uma mudança futura no gerador deve produzir uma comparação de inclusão/remoção por família, não apenas uma diferença de contagem;
- não alterar o sitemap nesta fase.

## Login, registro e páginas autenticadas

| URL | Comportamento atual | Origem |
|---|---|---|
| `https://vediums.com/login` | 200 Frappe Login | rota nativa Frappe; o menu não a usa. |
| `https://app.vediums.com/login` | entrada oficial | menu/header/footer. |
| `https://app.vediums.com/login#signup` | cadastro oficial | link “Registrar”. |
| `/register` e `/signup` em `vediums.com` | 404 no ambiente testado | não tratar como URLs válidas. |
| `/aluno` | 302 para login quando Guest | `www/aluno.py` + `aluno.html`; noindex. |
| `/onboarding` | 301/redirect para login quando Guest | `www/onboarding.py` + `onboarding.html`; noindex. |
| `/minhas-indicacoes` | 301 para login em `app.vediums.com` | controller próprio; noindex. |
| `/lms`, `/lms/courses` | páginas da aplicação LMS | apps oficiais, fora do redesign visual do marketing. |

## SEO atual: mecanismo

| Elemento | Produção atual |
|---|---|
| `title` e description | Em controllers/context ou diretamente no `<head>`; landings vêm de `LANDINGS`, cursos de DB + helpers e blog do conteúdo. |
| canonical | Hardcoded/context por página; cursos usam `course_urls.py`; blog valida path solicitado contra `post.url`. |
| Open Graph | Presente nas famílias principais; usa imagem do curso/post ou logo fallback. |
| Twitter cards | Presente em home, cursos e landings principais; cobertura não é uniforme em todos os institucionais. |
| sitemap | `www/sitemap.py` + `sitemap.xml`; une lista estática, landings, `LMS Course` publicados e blog; produção tinha 336 URLs. |
| robots | `www/robots.txt` servido por `robots.py`; libera `/`, bloqueia `/desk/`, `/app/`, `/api/method/`, `/printview`, `/backups/` e aponta o sitemap. |
| hreflang | Homes, catálogo, landings e vários institucionais; cursos só quando há tradução; `x-default` geralmente PT. |
| structured data | `EducationalOrganization` na home; `ItemList` no catálogo; `Course` + `BreadcrumbList` no curso; `Course`/`FAQPage`/breadcrumbs nas landings; `Blog`, `BlogPosting`, `FAQPage` e breadcrumbs no blog. |
| breadcrumbs | Visuais em várias páginas e JSON-LD nas famílias principais. Não são um único componente compartilhado. |
| redirects | `website_redirects`, helpers de cursos/blog, regras de prefixo e redirects no controller. |
| slugs | páginas estáticas pelo nome do arquivo; landings pelo dicionário; cursos separados do ID interno; posts por conteúdo/DocType. |
| index/noindex | Marketing geralmente `index,follow`; blog filtrado usa `noindex,follow`; aluno/onboarding/indicações/prática usam noindex conforme o caso. |

## Validação de metadados em produção

Foram confirmados em produção:

- home: canonical, hreflang PT/en/es/fr/de, OG, Twitter e `EducationalOrganization`;
- catálogo: canonical, hreflang, OG, Twitter e `ItemList` com cursos do banco;
- curso A1: canonical, OG/Twitter, `Course`, `Offer` e breadcrumb;
- pilar de inglês: hreflang em seis idiomas, `Course`, `FAQPage` e breadcrumb;
- blog/categorias/artigos: `Blog`/`BlogPosting`, canonical e breadcrumbs; FAQ schema quando há FAQs.

### Política de structured data para o redesign

- preservar marcação semanticamente correta e os valores vindos de conteúdo real;
- JSON-LD deve corresponder ao conteúdo visível, à URL canônica e à hierarquia de breadcrumbs;
- não adicionar schema apenas para perseguir rich results;
- priorizar `Organization`, `BreadcrumbList`, `BlogPosting` e outras marcações realmente pertinentes ao tipo de página;
- `Course` e `FAQPage` existentes podem permanecer quando corretos e suportados pelo conteúdo visível;
- `Course` e `FAQPage` não são objetivos do redesign e não justificam repetir, ocultar ou distorcer conteúdo;
- validar JSON-LD no HTML renderizado de cada locale, não apenas no template-fonte.

## Duplicatas, aliases e rotas antigas

### Aliases que hoje respondem 200 com canonical

- `/cursos` e `/trilhas` renderizam o catálogo e canonicalizam para `/cursos-de-idiomas-online`;
- `/pt-br` renderiza a home e canonicaliza para `/`;
- `/pt-br/<rota>` pode renderizar conteúdo PT e canonicalizar para a URL sem prefixo.

Canonical reduz duplicação, mas 301 é mais inequívoco e economiza crawl. Não alterar nesta fase. Avaliar com Search Console e backlinks antes de migrar.

### Redirects confirmados

- `www.vediums.com/*` → `vediums.com/*` (301);
- `/index.html` → `/`;
- `/catalogo` → `/cursos-de-idiomas-online`;
- `/about`, `/sobre.html`, `/teachers-1`, `/mentores`, `/professores` → `/sobre`;
- `/contact`, `/contact.html` → `/contato`;
- `/course-details`, `/course-details.html`, `/news`, `/news-details`, `/news.html` → hub de cursos;
- `/professor-busayo-frank-alonge` → pilar de iorubá;
- IDs internos antigos de curso → slugs públicos;
- posts que migraram para categoria → URL aninhada.

## Redirect Inventory

Inventário consolidado do código e de verificações HTTP feitas em 23/08/2026. “301 esperado” significa que a regra está declarada em `website_redirects`, cuja intenção documentada é SEO 301, mas nem toda expansão dinâmica foi consultada individualmente em produção. A camada “edge/proxy indeterminada” precisa ser confirmada pela configuração efetivamente carregada.

| Origem | Destino | Status HTTP | Camada responsável | Decisão futura |
|---|---|---:|---|---|
| `https://www.vediums.com/*` | `https://vediums.com/*` | 301 observado | Cloudflare/Nginx, ownership exato não comprovado | **Manter**; descobrir e versionar a camada antes de qualquer edição |
| `/index.html` | `/` | 301 esperado | Frappe `website_redirects` | **Manter** |
| `/catalogo` | `/cursos-de-idiomas-online` | 301 observado | Frappe `website_redirects` | **Manter** |
| `/course-details`, `/course-details.html` | `/cursos-de-idiomas-online` | 301 esperado | Frappe `website_redirects` | **Manter**, revisar demanda residual |
| `/news`, `/news-details`, `/news.html` | `/cursos-de-idiomas-online` | 301 esperado | Frappe `website_redirects` | **Revisar futuramente**; destino sem equivalência editorial direta |
| `/about`, `/sobre.html` | `/sobre` | 301; `/about` observado | Frappe `website_redirects` | **Manter** |
| `/contact`, `/contact.html` | `/contato` | 301 esperado | Frappe `website_redirects` | **Manter** |
| `/teachers-1`, `/mentores`, `/professores` | `/sobre` | 301; `/professores` observado | Frappe `website_redirects` | `/professores` tem direção futura aprovada para canônica 200; manter agora e migrar somente após pré-condições, inventário SEO e plano de alto risco. Origens `teachers-1`/`mentores` exigem decisão própria |
| `/professor-busayo-frank-alonge` | `/curso-de-ioruba-online` | 301 esperado | Frappe `website_redirects` | **Manter/revisar** conforme conteúdo real do professor |
| `/curso/<id-interno>` | `/curso/<slug-publico>` | 301; exemplo `ingl-s-beginner` observado | Frappe, `legacy_course_redirects()` | **Manter**; contrato com backlinks e matrículas antigas |
| `/{en,es,fr,de,ru}/curso/<id-interno>` | curso localizado com slug público | 301 esperado | Frappe, `legacy_course_redirects()` | **Manter**; testar cada expansão |
| Curso localizado sem tradução | curso canônico PT | Redirect do controller; status a confirmar por URL | Frappe `www/curso.py` | **Manter/revisar** após inventário de traduções; risco alto |
| URL plana de post migrado | `/blog/<categoria>/<slug>` | 301 esperado | Frappe, `legacy_blog_redirects()` | **Manter**; validar canonical e backlinks |
| `/en-us`, `/en-au` | `/en` | 301; `/en-us` observado | Frappe, redirects gerados de prefixo | **Manter** |
| `/es-ar`, `/es-co` | `/es` | 301 esperado | Frappe, redirects gerados de prefixo | **Manter** |
| `/fr-ca` | `/fr` | 301 esperado | Frappe, redirects gerados de prefixo | **Manter** |
| `/zh-cn` | `/` | 301 esperado | Frappe, redirects gerados de prefixo | **Revisar futuramente** quando houver home chinesa real |
| `/<prefixo-regional>/<rota-PT>` | tradução real na família ou canônica PT | 301; `/en-us/contato → /en/contato` observado | Frappe, `_build_language_prefix_redirects()` | **Manter**; expandir para matriz e testar path/query |
| `/<prefixo-sem-curso>/<curso/...>` | `/curso/...` PT | 301 esperado | Frappe, regex de prefixo | **Manter/revisar** conforme cobertura de tradução |
| `/admin` | `https://app.vediums.com/app` | 301 observado | Frappe `website_redirects` | **Manter**; autenticação é risco alto |
| `/rh` | `https://app.vediums.com/app/employee` | 301 esperado | Frappe `website_redirects` | **Manter**; acesso/permissão fora do marketing |
| `/financeiro` | `https://app.vediums.com/app/accounts` | 301 esperado | Frappe `website_redirects` | **Manter**; acesso/permissão fora do marketing |
| `/stripe_checkout` | `/catalogo` → `/cursos-de-idiomas-online` | Dois 301; primeiro observado | Frappe `website_redirects` | **Revisar futuramente** para eliminar cadeia somente com plano de checkout/SEO |
| `/aluno` para Guest | `/login?redirect-to=/aluno` | 302 observado | Controller Frappe/auth | **Manter** até estratégia de host/login aprovada |
| `/onboarding` para Guest | `/login?redirect=/onboarding` | 301 observado | Controller Frappe/auth | **Revisar** consistência do parâmetro, sem mudar nesta fase |
| `/minhas-indicacoes` para Guest | `https://app.vediums.com/login?redirect-to=/minhas-indicacoes` | 301 observado | Controller Frappe/auth | **Manter** |
| raiz de `app.vediums.com` | `/login` | Redirect de controller; status a confirmar | Controllers de home Frappe | **Manter**; alto risco de sessão/host |
| `/pratica-diaria` no host público | Código indica `https://app.vediums.com/pratica-diaria` | **200 observado, redirect não ocorreu** | Controller versus host rewrite/proxy, causa não determinada | **Revisar futuramente**; divergência explícita, não corrigir na Fase 0 |

### Rotas parecidas que não são redirects

| URL | Resposta | Mecanismo | Decisão futura |
|---|---|---|---|
| `/cursos` e `/trilhas` | 200 | `website_route_rules` renderiza `catalogo`; canonical aponta ao hub | Revisar eventual 301 só com dados; risco alto |
| `/pt-br` e parte de `/pt-br/<rota>` | 200 | alias/route rule com canonical sem prefixo | Revisar eventual 301 só com matriz de hreflang/canonical; risco alto |
| `/sw.js` e `/manifest.json` | 200 | route rule interna para handler Frappe | Manter; não tratar como redirect |

Nenhum item deste inventário deve ser corrigido, removido ou normalizado durante a Fase 0.

### Problemas e riscos encontrados

1. O sitemap é grande e híbrido; listas estáticas e geradas podem ficar desalinhadas se a publicação mudar.
2. Artigos não-PT com URL plana podem parecer PT estruturalmente e complicar hreflang/breadcrumb.
3. `blog_post.html` monta hreflang alternativo com `/blog/<slug>`; conteúdo aninhado/prefixado precisa de QA recíproco.
4. O seletor expõe regiões sem home/conteúdo próprio e depende dos redirects de família.
5. `/login` existe nos dois hosts, mas só `app.vediums.com/login` deve ser promovido.
6. `/professores` perde intenção específica ao redirecionar para `/sobre`.
7. O código atual mistura rótulos A2+, B1 e B1+; conteúdo, catálogo e briefing precisam de uma taxonomia aprovada.
8. O filtro de blog por query string deve permanecer `noindex,follow`; não gerar canonicals diferentes para cada combinação.

## Checklist SEO obrigatório para cada novo template

- preservar URL e status antes/depois;
- preservar title, description, canonical e robots;
- preservar hreflang recíproco apenas entre traduções reais;
- preservar JSON-LD semanticamente equivalente e valores vindos de dados reais;
- manter um único H1 e breadcrumbs visuais/estruturados coerentes;
- manter links internos entre pilar, nível, objetivo, teste e blog;
- manter imagem/alt e dimensões para evitar CLS;
- não inserir ratings, alunos, resultados ou depoimentos sem fonte verificável;
- comparar o HTML renderizado, não apenas o template;
- validar sitemap, redirects e 404 após cada lote.

## Congelamento recomendado antes da implementação

Gerar e versionar fora do runtime uma planilha de controle com: URL do sitemap, status, canonical, title, description, robots, hreflang, schema types, tráfego Search Console, backlinks e novo template. O sitemap de 336 URLs desta auditoria é um snapshot, não substitui esse inventário de cutover.
