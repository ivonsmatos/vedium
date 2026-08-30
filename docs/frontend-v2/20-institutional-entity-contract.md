# 20 — Institutional Entity Contract

Referência única para como a Vedium se identifica como entidade em todo
o frontend Next: nome, razão social, schema e o parágrafo factual usado
para GEO/entity SEO. Criado na Fase F.2 (`/sobre`), mas vale para
qualquer página futura que precise citar a instituição.

## 1. Nome institucional

- **Nome de marca, sempre**: **Vedium**. É o que aparece em headlines,
  H1, eyebrows, CTAs, boilerplate e qualquer texto voltado ao usuário.
- **Razão social, só onde juridicamente necessário**: **VEDIUM GLOBAL
  EDUCACAO E TECNOLOGIA LTDA**. Não aparece em nenhuma headline desta
  página nem de nenhuma outra construída até agora. Reservada para
  footer/legal/schema institucional (ex.: um campo `legalName` num
  JSON-LD, ou o rodapé de copyright) — nenhuma dessas aplicações foi
  necessária ainda nas páginas já construídas.

## 2. Schema — Organization vs EducationalOrganization

Dois padrões coexistem no código, cada um correto no seu contexto:

| Contexto | Tipo usado | Onde |
|---|---|---|
| Entidade completa da instituição (página inteira é "sobre a empresa") | `EducationalOrganization` | `/` (Home, `app/page.tsx`) e `/sobre` (`app/sobre/page.tsx`) — **mesmo objeto, mesmos campos** |
| Referência à organização dentro de um schema de outra coisa (curso, serviço) | `Organization` (forma mínima `{ name, url }`) | `provider` dentro do `Course` de cada página de idioma e do `Service` da página B2B |

Não use os dois tipos como se fossem intercambiáveis. Uma página que
fala *sobre a Vedium como instituição* usa `EducationalOrganization`
completo. Uma página que fala sobre *um produto da Vedium* (curso,
programa B2B) só precisa do `Organization` mínimo como `provider`.

### Contrato `EducationalOrganization` (copiar exatamente estes campos)

```json
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "Vedium",
  "url": "https://vediums.com",
  "logo": "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
  "description": "<description da própria página, não fixa>",
  "address": { "@type": "PostalAddress", "addressCountry": "BR" },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+55-11-91129-3075",
    "email": "contato@vediums.com",
    "contactType": "Customer Service",
    "availableLanguage": ["Portuguese", "English"]
  },
  "sameAs": ["https://www.instagram.com/vediumsglobal/", "https://www.linkedin.com/company/vediums"]
}
```

Só `description` muda de página para página (o resto é fato da
entidade, não copy). **Nunca adicionar** `foundingDate`, `founder`,
`award` ou `numberOfEmployees` a este objeto — nenhuma fonte confirma
esses dados (ver `19-about-content-contract.md`, seção UNVERIFIED). Se
um documento oficial futuro confirmar algum desses campos, atualizar
este contrato primeiro, depois propagar para as páginas que o usam.

## 3. Parágrafo factual para GEO / motores generativos

A missão F.1 e F.2 pedem trechos em linguagem natural que um motor
generativo consiga extrair como fato, sem criar um bloco artificial
"resumo para IA". O parágrafo que cumpre esse papel hoje é o support do
Hero de `/sobre` (`content/about.ts`, `ABOUT_HERO.support`):

> "A Vedium é uma escola de idiomas 100% online que une aulas ao vivo,
> professores nativos e especialistas, progressão estruturada e
> profundidade cultural."

Frase única, sem superlativo, sem número não verificado, cobrindo
categoria (escola de idiomas 100% online) + os 4 diferenciais reais
(aulas ao vivo, professores nativos e especialistas, progressão
estruturada, profundidade cultural). Reutilizável como base para
`description` de metadata em páginas institucionais futuras — não
precisa ser reescrita do zero a cada página nova.

## 4. Onde este contrato já está aplicado

- `app/page.tsx` (Home) — `EducationalOrganization` (original, já
  aprovado antes desta fase).
- `app/sobre/page.tsx` — `EducationalOrganization` (mesmo objeto,
  `description` própria da página).
- `app/curso-de-*/page.tsx`, `app/portugues-para-estrangeiros/page.tsx`,
  `app/empresas/page.tsx` — `Organization` mínimo como `provider`
  dentro do `Course`/`Service`.
- `app/como-funciona/page.tsx` — `Organization` mínimo standalone (não
  `EducationalOrganization` completo, porque a página fala do processo
  de estudo, não da entidade em si — ver `16-how-it-works-seo-parity.md`).

Qualquer página institucional nova (ex.: uma futura página de
contato/legal) deve decidir entre os dois padrões usando a mesma regra
da seção 2 acima, não inventar um terceiro formato.
