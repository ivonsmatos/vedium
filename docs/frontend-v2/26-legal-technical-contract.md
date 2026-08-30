# 26 — Contrato técnico das páginas legais

## Arquitetura

As páginas usam App Router e são Server Components estáticos:

- `src/app/privacidade/page.tsx`
- `src/app/termos/page.tsx`
- `src/app/cancelamento-reembolso/page.tsx`
- `src/content/legal/*.ts` — conteúdo jurídico estruturado.
- `src/components/legal/LegalDocumentPage.tsx` — renderer único.
- `src/components/legal/LegalDocumentPage.module.css` — CSS isolado.
- `scripts/legal-audit.mjs` — paridade, SEO, SSR, links, viewports e regressão.

Não há fetch de conteúdo, dependência de banco, MDX/CMS, Client Component ou Frappe para renderizar as três páginas. O build classificou todas como `○ Static (prerendered as static content)`.

## Contrato de SEO

Cada rota preserva:

- URL pública e status 200.
- Title e meta description atuais.
- Self canonical.
- `robots: index, follow`.
- Um H1 e a hierarquia H1 → H2.

O HTML obtido diretamente pelo servidor contém `data-legal-source-content`, a última seção e o carimbo `Base legal:`. O documento não depende de hidratação para existir.

## Contrato visual e de leitura

- Header institucional existente, page header simples, documento, navegação legal e Footer.
- Coluna limitada a 78ch.
- Sem hero fotográfico, cards comerciais, testimonial, CTA agressivo ou animação.
- Índice opcional derivado apenas dos headings existentes.
- Links longos quebram dentro da coluna; tabelas têm rolagem local em telas estreitas.
- Foco visível em links e regiões de tabela.
- Tabelas usam `th scope="col"` e região nomeada.
- CSS Module não altera páginas congeladas.

## Rotas Frappe preservadas

O escopo não autoriza migrar `/cookies`, `/gravacao-imagem-voz`, `/privacidade/meus-dados` ou `/propriedade-intelectual`, nem duplicar PDFs jurídicos. `next.config.ts` mantém somente esses destinos referenciados por rewrites explícitos para `https://app.vediums.com`. Os três documentos desta fase continuam locais e têm prioridade sobre os rewrites.

Resultado após build: todos os dez destinos HTTP únicos dos documentos respondem 200 no servidor Next; os dois `mailto:` são válidos.

## QA executado

### Build e lint

- `npm run lint`: 0 errors; 11 warnings preexistentes de `<img>` em componentes compartilhados.
- `npm run build`: PASS; TypeScript PASS; 17 páginas estáticas geradas.

### SSR e semântica

| Rota | HTTP | H1 | H2 | Tabelas com headers/label | SSR |
|---|---:|---:|---:|---:|---|
| `/privacidade` | 200 | 1 | 13 | 3/3 | PASS |
| `/termos` | 200 | 1 | 14 | n/a | PASS |
| `/cancelamento-reembolso` | 200 | 1 | 10 | n/a | PASS |

### Viewports

| Viewport | Conteúdo legal | Tabelas fora da viewport | Links fora da viewport | Console errors |
|---|---|---:|---:|---:|
| 390×844 | PASS | 0 | 0 | 0 |
| 768×1024 | PASS | 0 | 0 | 0 |
| 1440×1000 | PASS | 0 | 0 | 0 |

O documento inteiro mede exatamente a viewport em 390 e 1440. Em 768, o `documentElement` mede 830 px por causa do débito global já conhecido no Footer. As tabelas e links legais continuam contidos; o mesmo Footer compartilhado já existia e não foi modificado. Registrar novamente no backlog pré-cutover: `GLOBAL FOOTER OVERFLOW @ 768 = OPEN / NOT A LEGAL REGRESSION`.

### Regressão das páginas congeladas

Smoke test em build de produção, 1440 px:

- Home: 200, 1 H1, 0 console errors.
- Idiomas (Inglês, Iorubá, PLE, Espanhol, Hebraico): todos 200, 1 H1, 0 console errors.
- B2B `/empresas`: 200, 1 H1, 0 console errors.
- `/como-funciona`: 200, 1 H1, 0 console errors.
- `/sobre`: 200, 1 H1, 0 console errors.
- `/contato`: 200, 1 H1, 0 console errors.

Nenhum arquivo dessas páginas nem CSS global/shared foi alterado. Inspeção visual das rotas legais em 390/768/1440 confirmou hierarquia, leitura, tabelas, índice, passos e Footer.

## Contratos de consistência

### Contato

`CONTACT DATA: PASS`. `contato@vediums.com`, `dpo@vediums.com`, CNPJ e endereço foram preservados. O backend do formulário e a página de contato confirmam `contato@vediums.com`; o contrato institucional confirma o telefone global, embora ele não seja acrescentado ao documento jurídico.

Observação separada: `LEGAL ENTITY SPELLING: LEGAL REVIEW REQUIRED`, pois o Footer Next congelado usa `EDUCAÇÃO` e a fonte jurídica/contrato institucional usa `EDUCACAO`.

### Formulário

`FORM/PRIVACY CONSISTENCY: PASS`. Categorias, finalidade, CRM/suporte, comunicações e retenção do formulário estão cobertas pela política atual. Nenhuma cláusula nova foi inventada.

### Cookies

`COOKIE/PRIVACY CONSISTENCY: LEGAL REVIEW REQUIRED`. O Consent Mode v2 existe no Frappe, mas não foi portado ao runtime Next; o Next também não carrega analytics hoje. Decisão técnica/jurídica necessária antes do deploy.

### Billing

`BILLING/LEGAL CONSISTENCY: LEGAL REVIEW REQUIRED`. Permanência mínima de planos semestral/anual cobrados mensalmente pode conflitar ou ser confundida com a afirmação “planos mensais B2C não têm fidelidade”. Nenhuma alteração automática foi feita.

## Resultado final F.4

```text
PRIVACY ROUTE: PASS
PRIVACY CONTENT PARITY: PASS

TERMS ROUTE: PASS
TERMS CONTENT PARITY: PASS

CANCELLATION ROUTE: PASS
CANCELLATION CONTENT PARITY: PASS

LEGAL LINKS: PASS
CONTACT DATA: PASS
FORM/PRIVACY CONSISTENCY: PASS
COOKIE/PRIVACY CONSISTENCY: LEGAL REVIEW REQUIRED
BILLING/LEGAL CONSISTENCY: LEGAL REVIEW REQUIRED
SSR: PASS
MOBILE: PASS (legal content; known global Footer overflow at 768 remains open)
SITE REGRESSION: PASS
CONSOLE ERRORS: 0
DEPLOY: NOT PERFORMED
```

Depois desta entrega, parar. Blog, DNS, produção, Stripe e Frappe permanecem fora do escopo.
