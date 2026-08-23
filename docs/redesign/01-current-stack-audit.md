> **IMPORTANTE:**
>
> - O único projeto que pode receber novos arquivos é `vedium`.
> - `edumon` e `eduall` são referências SOMENTE PARA LEITURA.
> - Não modifique nenhum arquivo dentro de `edumon` ou `eduall`.
> - Nesta fase, não modifique nenhum arquivo existente do projeto `vedium`.
> - A única escrita permitida é criar os 5 arquivos solicitados em `vedium/docs/redesign/`.

# 01 — Auditoria da stack atual

Data da auditoria: 23/08/2026  
Branch auditada: `redesign/vedium-v2`  
Escopo: leitura do repositório, das duas referências e validação HTTP do ambiente público. Nenhuma página, configuração, dependência ou arquivo existente foi alterado.

## Resumo executivo

O site que responde hoje em `https://vediums.com` é gerado pelo app Frappe `vedium_core`, principalmente por `vedium_core/vedium_core/www/`, controllers Python, templates Jinja e dados de `LMS Course`. Não é um frontend React/Next e não é o conteúdo estático de `deploy/site/`.

`vediums.com` e `app.vediums.com` chegam ao mesmo site Frappe/MariaDB, mas cumprem papéis diferentes:

- `vediums.com`: aquisição, SEO, catálogo, páginas de curso, conteúdo, teste de nível e conversão;
- `app.vediums.com`: login, LMS, checkout, área do aluno, Desk/ERP/CRM e APIs transacionais.

Em produção, a home de `vediums.com` respondeu `200`, com `X-Page-Name: index`, cookies de sessão Frappe (`sid=Guest`, `system_user`, `user_id`) e conteúdo de cursos vindo do LMS. `www.vediums.com` redirecionou por `301` para o host sem `www`. Isso confirma a renderização Frappe atrás de Cloudflare e Nginx.

Existe uma divergência crítica de documentação/infraestrutura: `.github/workflows/deploy.yml`, `deploy/nginx/vediums.com.conf` e `deploy/README.md` ainda descrevem/publicam `deploy/site/` em `/opt/vedium/site`, enquanto `docs/ARCHITECTURE.md`, o código e a resposta real de produção apontam o marketing para Frappe via host rewrite. O Nginx efetivamente ativo não está integralmente versionado. Antes do redesign, a configuração real do host deve ser exportada e incorporada ao checklist de cutover.

## Evidências e fontes de verdade

Ordem de confiança usada nesta auditoria:

1. resposta HTTP atual de `vediums.com`;
2. rotas, templates e controllers de `vedium_core`;
3. `hooks.py`, configuração de produção e workflow de deploy;
4. documentação operacional recente em `docs/ARCHITECTURE.md` e `docs/plataforma/`;
5. scripts antigos apenas como histórico, nunca como prova isolada da produção.

Há artefatos históricos conflitantes. `init.sh` e `install_apps.sh`, por exemplo, ainda mencionam Frappe/ERPNext v15, enquanto a imagem e os documentos verificados de produção são v16. Esses scripts não devem definir decisões do redesign.

## Estrutura relevante do repositório

| Área | Papel real | Observação para o redesign |
|---|---|---|
| `vedium_core/vedium_core/www/` | Páginas públicas SSR e seus controllers | Fonte principal do site atual. Arquivos `.html` usam Jinja; `.py` preparam contexto, acesso e SEO. |
| `vedium_core/vedium_core/templates/includes/` | Header, footer, landings, blog e formulários reutilizados | É a camada mais segura para criar componentes compartilhados numa fase futura. |
| `vedium_core/vedium_core/templates/base.html` | Override do shell Frappe genérico | Nem todas as páginas públicas o herdam: muitas são documentos HTML completos que incluem navbar/footer diretamente. |
| `vedium_core/vedium_core/public/` | CSS, JS, fontes, imagens, PWA e tema legado | Mistura Tailwind compilado, tema próprio, Bootstrap e vendors antigos. |
| `vedium_core/vedium_core/hooks.py` | Rotas, redirects, includes globais, Jinja, eventos e permissões | Contrato central de rotas e integrações; mudança de layout não pode remover esses hooks. |
| `marketing_landing_content.py` | Conteúdo estruturado das páginas-pilar e por objetivo | Deve ser preservado como fonte de conteúdo, não convertido em texto duplicado por template. |
| `blog_content.py` | Posts em código, categorias e redirects antigos | Divide a fonte de conteúdo com o DocType `Vedium Blog Post`. |
| `course_urls.py` | Slugs públicos, navegação de níveis e redirects dos IDs internos | Contrato SEO dos cursos; não renomear registros `LMS Course`. |
| `course_translations.py` | Traduções das páginas dinâmicas de curso | A cobertura varia por curso/idioma. |
| `catalog_registry.py` / `catalog_pricing.py` | IDs comerciais e regras de catálogo/preço | Não colocar preço inventado ou hardcoded no novo layout. |
| `public_funnel.py` | Leads, intenção, diagnóstico, certificado e resultado de teste | Acoplado aos formulários e CTAs públicos. |
| `api.py`, `frequency_checkout.py`, `public_frequency_checkout.py` | Checkout, Stripe e matrícula | O redesenho deve manter parâmetros, endpoints e transição entre hosts. |
| `analytics_events.py`, `docs/gtm/` | Eventos GA4/GTM client e server-side | Nomes e payloads são contratos de medição. |
| `brevo.py` | Sincronização Frappe → Brevo | Recebe leads/matrículas/eventos; não é um formulário independente no frontend. |
| `patches.txt` | Patches de catálogo já aplicáveis | Contém seeds one-shot; não é CMS nem sistema de páginas. |
| `vedium_core/vedium_core/doctype/` | DocTypes customizados versionados | Parte da operação, não da apresentação pública. Outros DocTypes/campos são garantidos por `install.py`/`custom_setup.py`. |
| `deploy/site/` | Site estático legado e PWA alternativo | Não é a fonte da home atual; manter fora da arquitetura visual futura até reconciliar o Nginx real. |
| `deploy/` | Compose, imagem de produção, Nginx e runbook | Parte da infraestrutura; há drift documentado com o servidor. |
| `scripts/` | Operação, auditoria e migrações | Não gera o site em tempo de request. |

Não existe um diretório de fixtures Frappe ativo nem um frontend SPA próprio dentro de `vedium_core`. O conteúdo público vem de arquivos Python/HTML versionados e do banco Frappe.

## Stack confirmada

| Camada | Tecnologia confirmada | Versão/origem | Como foi confirmada |
|---|---|---|---|
| Framework backend/SSR | Frappe Framework | v16, documentação de produção registra 16.18.x | imagem `frappe/erpnext:v16`, `hooks.py`, controllers e headers HTTP |
| ERP | ERPNext | v16, documentação registra 16.19.x | imagem e `deploy/apps.txt` |
| LMS | Frappe Learning/LMS | 2.x, branch `main` no ambiente descrito | `LMS Course`, `Course Instructor`, `Course Chapter`, `LMS Course Review` e `deploy/apps.txt` |
| Apps operacionais | Payments, CRM, Helpdesk, HRMS, Insights, Wiki, Telephony | instalados/previstos no bench de produção | `deploy/apps.txt` e documentação operacional |
| Backend | Python | 3.14 em produção | `deploy/Dockerfile`, `deploy/docker-compose.yml` |
| Runtime de assets | Node.js | 24 em produção | `deploy/Dockerfile`; usado no build de apps/assets |
| Rendering público | Server-side | Jinja/Frappe | `www/*.html`, `get_context()` e resposta HTML pronta |
| Frontend público | HTML/Jinja + JavaScript progressivo | sem React/Vue no site institucional | templates e scripts públicos |
| CSS/layout | Bootstrap do tema + CSS Vedium + Tailwind 3.4 compilado | Bootstrap vendor; Tailwind `^3.4.1` | templates, `package.json`, `tailwind.config.js` |
| JS legado no marketing | jQuery 3.5.1, Bootstrap bundle, WOW, Swiper; Isotope no catálogo; Jarallax na home | arquivos locais em `public/vedium_assets/vendors/` | includes dos templates |
| Bundling/minificação local | Tailwind CLI, PurgeCSS, clean-css-cli, Terser e script Node de SEO | scripts npm; sem Vite/Webpack próprio do site | `vedium_core/package.json` |
| Banco | MariaDB | 10.6 | compose dev/prod |
| Cache/filas/realtime | Redis | três instâncias: cache, queue, socketio | compose prod |
| Servidor de aplicação | Gunicorn | workers Frappe | `deploy/docker-compose.yml` |
| Proxy/edge | Nginx + Cloudflare | configuração real do host parcialmente fora do Git | headers públicos e arquivos de deploy |
| Containers | Docker Compose v2 | imagem oficial ERPNext v16 com overlay Vedium/Raven | `deploy/Dockerfile`, compose |
| CMS/conteúdo | código + MariaDB/Frappe | `LANDINGS`, `BLOG_POSTS`, DocType `Vedium Blog Post`, `LMS Course` | controllers e helpers |

### Frontend React/Vue

Não há React ou Vue controlando o marketing. Apps oficiais instalados podem usar seus próprios frontends, mas isso pertence à plataforma `app.vediums.com`, não ao shell público auditado. O redesign deve ser reimplementado em Jinja/HTML/CSS/JS da stack atual, salvo decisão arquitetural posterior explicitamente aprovada.

### Fontes e CSS em uso

Há quatro camadas tipográficas conflitantes:

- `public-foundations.css` hospeda localmente Kumbh Sans e Playfair Display;
- `templates/base.html` carrega Kanit do Google Fonts;
- `luxo_theme.css` importa Inter e Bodoni Moda do Google Fonts;
- o tema vendor inclui `reey-font` e icon fonts.

Também há tokens conflitantes: o Tailwind ainda chama verde `#166534` de primário, enquanto o marketing usa principalmente azul `#2E6DA4`/`#26528C`, azul claro `#84A9D9`, bege `#BFA288` e terracota. Esse conflito é uma causa direta de inconsistência entre páginas.

## Como uma requisição pública é resolvida

1. Cloudflare recebe a requisição e encaminha ao Nginx.
2. Para o ambiente atual, o Nginx encaminha a rota de marketing ao Gunicorn/Frappe usando o site `app.vediums.com` por host rewrite.
3. Frappe aplica `website_redirects` antes de `website_route_rules`.
4. Rotas explícitas podem apontar para `catalogo`, `curso`, `blog` ou `blog_post`; rotas simples são resolvidas pelos arquivos de `www/`.
5. O controller `.py`, quando existe, monta `context`, consulta MariaDB e pode redirecionar/autenticar.
6. Jinja renderiza HTML no servidor. JavaScript acrescenta filtros, menu móvel, teste de nível, checkout, consentimento e analytics.

O header e footer públicos são `templates/includes/site_navbar.html` e `site_footer.html`. O GTM é inserido no footer. As páginas standalone incluem esses dois arquivos; páginas Frappe genéricas podem passar por `templates/base.html` e Web Blocks padrão.

## Dados e CMS

| Conteúdo | Fonte | Consequência |
|---|---|---|
| Cursos, preços base, publicação, currículo, instrutores e reviews | DocTypes LMS em MariaDB | O template deve continuar tolerando campos ausentes e dados em tempo real. |
| Slugs públicos de cursos | `course_urls.py` | Separados dos IDs internos para proteger matrículas e SEO. |
| Páginas-pilar/objetivo | `marketing_landing_content.py` | Um template compartilhado renderiza conteúdo por slug e idioma. |
| Blog | `blog_content.py` + DocType `Vedium Blog Post` | O redesign precisa suportar as duas origens até haver migração editorial. |
| Institucional/legal | arquivos em `www/` | Conteúdo versionado e, em vários casos, repetido por idioma. |
| Catálogo comercial | registry/regras em código + LMS/Stripe | Preço mostrado e preço cobrado não podem divergir. |

## Integrações que o layout toca

| Integração | Ponto de acoplamento atual | Risco de redesign |
|---|---|---|
| GTM/GA4 | GTM `GTM-P6Q2FXLK` no footer; eventos no `dataLayer`; ID GA4 vem de variável/configuração externa | Alto: trocar markup/handlers pode silenciar conversões sem erro visual. |
| GA4 server-side | `analytics_events.py` envia `purchase` via Measurement Protocol quando configurado | Médio: preservar IDs de curso, valor, moeda e transação. |
| Meta Pixel | ID `1539456614495904`, carregado só após `vedium_cookie_consent` | Alto: consentimento e evento `vedium:consent` não podem ser removidos. |
| WhatsApp | links `wa.me/5511911293075`, texto contextual e eventos | Alto: é canal comercial manual, não apenas link decorativo. |
| Testes de nível | lógica client-side, `dataLayer`, captura opcional de e-mail e `save_placement_result` | Alto: respostas, scoring e nível recomendado são funcionalidade. |
| Formulários públicos | `send_contact_message`, `submit_public_intent`, `request_diagnostic_class`, candidatura e LGPD | Alto: criam CRM Lead/ticket/candidatura; preservar campos, CSRF/rate limit e mensagens de erro. |
| CRM | leads originados por contato/intenção/teste; campos customizados | Alto: páginas podem continuar bonitas enquanto o pipeline quebra. |
| Brevo | hooks sobre CRM Lead/LMS Enrollment e eventos de ciclo de vida | Médio-alto: depende dos dados criados pelo funil, não do DOM diretamente. |
| Stripe | CTA público → endpoint em `app.vediums.com` → sessão → webhook → matrícula | Crítico: preservar `course_name`, período, frequência, moeda, origem e redirects. |
| Frappe/LMS | login, cadastro em `login#signup`, cursos e matrícula | Crítico: não transformar `vediums.com` em aplicação paralela. |
| PWA/push | `pwa-register`, service worker, manifest e push notifications | Médio: há histórico de conflito Nginx/alias e escopo entre hosts. |

## Achados que condicionam o redesign

1. A fonte de verdade visual está fragmentada entre CSS vendor, estilos inline, `public-foundations`, Tailwind e `luxo_theme`.
2. Muitas páginas são documentos HTML completos; mudar apenas `base.html` não redesenha o site inteiro.
3. Existem vendors pesados já no Vedium. A restrição de não importar jQuery/Slick/Select2 do EduAll deve ser mantida; uma fase futura deve reduzir, não ampliar, essa superfície.
4. A home mostra estrelas e contagens fixas em cards, embora o princípio do redesign proíba prova social fictícia. Só dados verificados podem sobreviver.
5. `/professores` não tem página: hoje é `301` para `/sobre`. A direção aprovada para o redesign é torná-la futuramente uma página canônica própria `200`, com perfis em `/professores/<slug>`, somente após confirmar docentes, autorização de imagem, dados profissionais e conteúdo editorial. O redirect não muda na Fase 0.
6. O sitemap de produção tinha 336 URLs no momento da auditoria, incluindo conteúdo multilíngue, cursos e muitos artigos; uma migração manual página a página é impraticável sem templates compartilhados.
7. O Nginx real não está inteiramente versionado e os artefatos de deploy divergem do comportamento observado. Isso é bloqueador de cutover, não de desenho.
8. A sequência pública de inglês pretendida para validação é A1, A2, B1, B1+, B2 e C1, mas código, conteúdo e comunicação não usam hoje os mesmos rótulos. ID interno, slug histórico, rótulo público e nível CEFR são campos conceitualmente distintos; nenhum URL, ID, registro LMS ou redirect deve ser renomeado para resolver a apresentação.
9. Localização não pode ser acrescentada apenas ao fim: a fundação de componentes precisa aceitar locale, texto de comprimento variável, caracteres internacionais, fallback de fontes e RTL quando necessário. Hreflang e canonical são contratos de template desde a fundação.
10. Structured data é uma representação do conteúdo visível, não um objetivo visual. `Organization`, `BreadcrumbList` e `BlogPosting` são prioridades quando pertinentes; `Course` e `FAQPage` podem permanecer quando semanticamente corretos, sem orientar o redesign em busca de rich results.

## Registro explícito de divergências

Data da comparação: 23/08/2026. “Produção” abaixo significa comportamento HTTP observado no domínio público, não acesso ao servidor. A configuração Nginx efetivamente carregada e o estado dos containers não estão disponíveis integralmente no repositório.

| Tema | Código versionado | Deploy legado/versionado | Documentação | Nginx/proxy conhecido | Produção observada | Classificação e ação futura |
|---|---|---|---|---|---|---|
| Fonte do site público | `vedium_core/vedium_core/www/`, controllers e Jinja geram o marketing | Workflow e `deploy/site/` ainda descrevem/copiavam site estático para `/opt/vedium/site` | `docs/ARCHITECTURE.md` descreve marketing Frappe SSR | `deploy/nginx/vediums.com.conf` representa a hipótese estática; configuração ativa não está toda no Git | Home responde como Frappe (`X-Page-Name: index` e cookies Guest) | **Divergência crítica. Não corrigir na Fase 0.** Exportar configuração ativa e definir uma única arquitetura antes do cutover |
| Roteamento entre hosts | Controllers distinguem `vediums.com` e `app.vediums.com`; produto/login ficam no host `app` | Artefatos estáticos não representam todos os fluxos de LMS/auth/checkout | Arquitetura atual documenta host rewrite para o site Frappe | O rewrite efetivo que preserva o host público não está completamente versionado | Marketing é servido no host público; login e transações seguem para `app.vediums.com` | **Risco alto.** Não alterar host, login ou proxy sem plano e teste de sessão/return URL |
| Redirect do host `www` | Não há uma regra equivalente em `website_redirects` | Não é determinado pelo app | Documentação não é a fonte normativa desta regra | Provável regra de edge/Nginx, mas a camada exata não foi comprovada | `www.vediums.com/*` responde 301 para `vediums.com/*` | **Divergência de ownership.** Manter comportamento e descobrir a camada antes de editar |
| PWA: `/manifest.json` e `/sw.js` | `website_route_rules` encaminha para handlers Frappe | Comentários registram alias Nginx antigo para `/opt/vedium/pwa/manifest.json`, caminho inexistente | Há pendência histórica de PWA/Nginx | Regra ativa não foi exportada; código foi criado para contornar o alias | Ambos os caminhos respondem 200 | **Drift histórico parcialmente contornado.** Não remover route rule nem “corrigir” Nginx nesta fase |
| `/pratica-diaria` por host | `pratica_diaria.py` tenta redirecionar hosts públicos para `app.vediums.com/pratica-diaria` | Não há contrato equivalente no site estático | A intenção produto versus marketing não está consolidada em uma fonte única | Host rewrite pode alterar o valor de host visto pelo controller | `https://vediums.com/pratica-diaria` respondeu 200, não redirect, na verificação | **Divergência direta código/comportamento.** Não corrigir; investigar headers encaminhados, versão implantada e canonical antes de decidir |
| Versões da stack | Dockerfiles/composes atuais apontam Frappe/ERPNext v16, Python 3.14 e Node 24 | Scripts históricos `init.sh`/`install_apps.sh` ainda mencionam v15 | `docs/ARCHITECTURE.md` e runbook atual dizem v16; documentos em `docs/archive/` preservam conclusões antigas de v15 | Não aplicável diretamente | Headers HTTP confirmam Frappe, mas não expõem todas as versões | **Divergência histórica.** Tratar documentação arquivada e scripts antigos como não normativos; confirmar `bench version` antes de implementar |
| Caminho de build/publicação | Assets e páginas do app dependem do build/serving Frappe | `.github/workflows/deploy.yml` e README legado têm fluxo de publicação estática | Arquitetura vigente descreve containers e app Frappe | Nginx versionado e proxy ativo não estão reconciliados | Alterações atuais de `www/` aparecem no site Frappe, segundo a resposta observada | **Risco crítico de publicar no destino errado.** Não alterar workflow/deploy na Fase 0 |
| `/stripe_checkout` | `website_redirects` envia para `/catalogo` | Sem fluxo correspondente no estático | Documentação comercial promove checkout no host `app` | Não aplicável/indeterminado | Responde 301 para `/catalogo`, que responde outro 301 para o hub canônico | **Cadeia legada.** Manter agora; revisar só com plano de redirect e checkout aprovado |
| Fonte de preço e catálogo | Controllers combinam LMS, registry e helpers de checkout | O site estático contém conteúdo que pode envelhecer separado do LMS | Documentação aponta LMS/Stripe como sistemas operacionais | Cache/proxy pode ampliar defasagem se mal configurado | Catálogo SSR expõe dados do LMS; cobrança ocorre no host `app` | **Risco alto.** Nunca substituir dados reais pelo conteúdo demonstrativo/estático |
| Estado de URLs traduzidas | `hooks.py` combina páginas reais, route rules, redirects e fallbacks | Deploy estático não representa a matriz dinâmica | Comentários/documentos registram evolução de placeholders para traduções reais | A ordem proxy → Frappe precisa ser preservada | Famílias próprias e redirects regionais respondem; `/pt-br` continua como alias 200 | **Drift de complexidade.** Não normalizar slugs/prefixos durante o redesign |

Conclusão operacional: nenhuma linha desta tabela é uma tarefa de correção da Fase 0. Toda divergência deve permanecer registrada como hipótese ou dívida até que haja export da configuração ativa, evidência de produção e plano de mudança aprovado.

## Decisão arquitetural recomendada para a próxima fase

Manter Frappe SSR e os contratos de dados/rotas. Criar, dentro de `vedium_core`, uma camada de componentes Jinja e CSS tokens para substituir gradualmente os documentos standalone, sem introduzir um segundo CMS ou uma SPA. Componentes interativos pequenos devem usar JavaScript nativo; Bootstrap pode permanecer transitoriamente enquanto páginas são migradas. Edumon e EduAll fornecem apenas referências de composição, nunca código de runtime.

Essa conclusão técnica permanece inalterada pelos ajustes finais: controllers e DocTypes continuam como fontes de verdade; URLs, integrações e matriz de redirects são preservadas; nenhum runtime Next/React será importado. A prontidão para locale e os gates editoriais são requisitos dessa mesma arquitetura Frappe/Jinja, não justificativa para trocá-la.

## Questões que exigem confirmação antes do cutover

- exportar a configuração Nginx efetivamente ativa e reconciliá-la com Git;
- registrar `bench version`/`bench list-apps` no mesmo dia do cutover;
- exportar do Search Console as URLs com impressões/cliques e unir ao sitemap;
- confirmar no GTM publicado o valor real da variável GA4 e quais tags estão live;
- validar quais depoimentos, números, fotos e perfis de professor têm autorização e evidência;
- reunir os pré-requisitos aprovados para `/professores` e `/professores/<slug>` antes de planejar a retirada do redirect atual;
- aprovar a taxonomia pedagógica e o mapeamento entre ID interno, slug histórico, rótulo público e CEFR antes do componente de progressão;
- validar cores contra logos/ativos oficiais, contraste WCAG e cobertura tipográfica de todos os locales;
- decidir se aliases 200 (`/cursos`, `/trilhas`, `/pt-br/...`) serão convertidos em 301, com plano SEO aprovado.
