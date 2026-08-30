# 18 — SEO Parity: `/sobre` (CURRENT vs Next local)

Mesmo método dos docs anteriores: snapshot do HTML real de produção,
comparado campo a campo com `frontend/src/app/sobre/page.tsx`. Rota Next
só existe localmente.

## 1. Rota — auditoria ANTES de construir

Confirmado por HTTP nesta sessão:

| URL | Status |
|---|---|
| `/sobre` | **200** |
| `/sobre-a-vedium` | 404 |
| `/quem-somos` | 404 |
| `/professores` | 200 (redireciona para `/sobre` em produção) |

`/sobre` já é a rota real, já indexada, e já é para onde `Header.tsx`
(nav desktop e mobile) e `content/site/footer.ts` apontam nesta base de
código local. Nenhuma rota concorrente criada.

## 2. Fonte oficial consultada

`01_Vedium_Identidade_Organizacional_Completa_v4.docx`
(`Cliente/Vedium/Documentação/Vedium_Documentos_Revisados/`), extraído e
lido nesta sessão. Usado como fonte para Fundamentos, Posicionamento,
Propósito, Missão, Visão, Manifesto, Valores, Arquitetura Acadêmica e
Princípios da Experiência — ver `19-about-content-contract.md` para o
mapeamento campo a campo.

**Nenhuma história institucional inventada** (missão seção 1 e 20): o
documento oficial não cita ano de fundação, fundadores, número de
alunos/professores/países, prêmios ou certificações institucionais.
Nada disso foi publicado nesta página. Sem timeline.

## 3. Metadados

| Campo | CURRENT (produção) | NEXT | Status |
|---|---|---|---|
| `<title>` | "Sobre a Vedium - Escola de Idiomas Online ao Vivo" | idêntico (recuperado literalmente) | ✅ |
| description | "Conheça a Vedium: escola online com aulas ao vivo de inglês, espanhol, hebraico, iorubá e português para estrangeiros, professores e certificado." | idêntica | ✅ |
| canonical | `https://vediums.com/sobre` | idêntico | ✅ |
| robots | `index, follow, max-image-preview:large` | idêntico | ✅ |

## 4. Hreflang

Produção tem hreflang completo (pt-br, en, es, fr, de, x-default) —
nenhuma dessas traduções existe nesta base Next (mesmo achado já
documentado em `16-how-it-works-seo-parity.md`, seção 5). Contrato
mínimo usado: só `pt-br` (self) + `x-default` (self).

## 5. H1

Único H1 confirmado no HTML renderizado: "Educação linguística ao vivo
para participar de novos contextos." — copy literal da missão F.2
(seção 6).

## 6. Schema (JSON-LD)

| Schema | Conteúdo |
|---|---|
| `EducationalOrganization` | Mesmo contrato exato já usado em `/` (app/page.tsx): `name`, `url`, `logo`, `description`, `address` (`addressCountry: "BR"`), `contactPoint` (telefone/e-mail/tipo/idiomas), `sameAs` (Instagram + LinkedIn, ambos já reais e aprovados na Home) |
| `BreadcrumbList` | Início → Sobre (2 níveis) |

Produção usa `AboutPage` + `EducationalOrganization`. O Next usa só
`EducationalOrganization` (mesmo tipo, contrato global já aprovado) +
`BreadcrumbList` — `AboutPage` não está no contrato pedido pela missão
(seção 25) e foi omitido por não agregar campo verificável novo. Nenhum
`sameAs`/`foundingDate`/`founder`/`award`/`numberOfEmployees` inventado
— os dois `sameAs` usados já existiam e já estão em produção via Home.

## 7. Estratégia interna NÃO publicada

A tabela "Arquitetura Acadêmica" do documento oficial tem uma coluna
"Papel de marca" com a função estratégica de cada idioma (ex.: "Volume,
recorrência e expansão de base" para Inglês; "Ticket alto e reputação
institucional" para B2B). Essa coluna **não aparece em nenhum lugar da
página** — só a direção formativa pública (o que cada trilha
desenvolve), já usada nas próprias páginas de curso.

## 8. Internal links (testados nesta sessão)

Confirmados via `scripts/interaction-check-about.mjs`: os 5
`/curso-de-*`/`/portugues-para-estrangeiros` (via `CourseIndexIntro`,
mesmo componente e mesma fonte `HEADER_COURSES` da Home), `/empresas`,
`/como-funciona` (Hero + CTA final). O link para `/professores` que
aparece na contagem (3 ocorrências) vem do Header/Footer compartilhados
— pré-existente, não algo adicionado por esta página (ver seção 9).

## 9. Sem página de catálogo de professores

Por instrução explícita do usuário durante esta mesma fase
(2026-08-29): a Vedium não terá uma página institucional de catálogo de
professores. A seção "Professores e Tecnologia" desta página explica o
papel institucional da condução pedagógica, sem CTA e sem link para
nenhuma rota `/professores`. O link já existente em `content/site/
footer.ts` (`{ label: "Professores", href: "/professores" }`) é
compartilhado por todas as páginas e não foi alterado nesta fase — está
fora do escopo desta tarefa.

## Veredito

**SEO PARITY: PASS.** Título/description/canonical/robots recuperados
literalmente; hreflang mínimo e verdadeiro; schema consistente com o
contrato global já usado na Home; nenhuma informação estratégica
interna publicada; nenhuma história/número inventado.
