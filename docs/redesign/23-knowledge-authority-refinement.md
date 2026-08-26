# 23 — Autoridade editorial de "Conhecimento Vedium" (Fase B.6E, Parte A)

> **Origem**: a seção "Conhecimento Vedium" (Home) estava conceitualmente correta desde B.6B, mas os textos secundários ainda pareciam microconteúdo, sem peso intelectual/editorial. Referência conceitual: a lógica de Insights da Bain ("conteúdo também constrói autoridade institucional") — nunca o layout literal da Bain.

## 1. Problema identificado

Grid genérico de 4 colunas (`v2_blog_grid`: 1 artigo principal ocupando 2 colunas + 2 secundários de 1 coluna cada, lado a lado numa única linha) tratava os 3 artigos como se tivessem o mesmo peso visual. Metadata em 12px fixo (`--v2-text-xs`), resumo em 14px fixo (`--v2-text-sm`), sem CTA visível no artigo principal — tudo lia como "lista de blog", não "publicação institucional".

## 2. Novo componente: `v2_insights_editorial`

Substitui `v2_blog_grid` + 3× `v2_blog_card` (mantidos no arquivo de macros para não quebrar nenhum outro uso futuro, mas sem uso ativo nesta página). Composição "1 grande insight + 2 complementares":

- **Desktop (≥992px)**: grid `54fr 46fr`. Artigo principal à esquerda, coluna de 2 secundários empilhados à direita, com linha divisória vertical (`border-inline-start`) entre as colunas e uma linha horizontal fina entre os 2 secundários. Nunca card, nunca radius, nunca shadow.
- **Mobile**: empilha em 1 coluna, mesma ordem (principal → secundário 1 → secundário 2).

### Escala tipográfica

| Elemento | Antes | Depois |
|---|---|---|
| Headline da seção ("Aprenda também fora da aula.") | já ajustado em fase anterior (`.v2-insights-intro__title`) | `max-width` 46rem → 47.5rem (~760px, dentro dos "aproximadamente 760px" pedidos); resto sem mudança (já testado em 3 breakpoints: 38-44/48-56/58-68px) |
| Artigo principal — título | `clamp(1.75rem, 1.4rem+1.6vw, 2.5rem)` (28-40px) | `clamp(2.125rem, 1.85rem+0.6vw, 2.5rem)` (34-40px) |
| Artigo principal — resumo | 16-17px (`--v2-text-base`) | `clamp(1.125rem, 1.05rem+0.3vw, 1.25rem)` (18-20px) |
| Artigo principal — metadata | 12px fixo | `clamp(0.875rem, 0.85rem+0.1vw, 0.9375rem)` (14-15px) |
| Artigo principal — CTA | **não existia** (card inteiro era link, sem texto visível) | novo `.v2-insights__cta`: "Leia o artigo →", `clamp(1.0625rem, 1rem+0.2vw, 1.125rem)` (17-18px), weight 700 |
| Secundários — título | 17-19px (`--v2-text-lg`) | `clamp(1.5rem, 1.4rem+0.35vw, 1.75rem)` (24-28px), `line-height:1.3` (era herdado, mais apertado) |
| Secundários — resumo | 14px fixo | `clamp(1.0625rem, 1rem+0.2vw, 1.125rem)` (17-18px) |
| Secundários — metadata | 12px fixo | mesma escala do principal (14-15px) |
| "Ver todos os conteúdos →" | já usava `size="lg"` (17-19px, weight 600) — já dentro do pedido | mantido; só o espaço acima aumentado de `--v2-space-8` (32px) para `--v2-space-12` (48px) |

## 3. Conteúdo — sem invenção

Os mesmos 3 artigos reais já usados desde B.6/B.6B (`blog_content.py`): "Como saber seu nível real de inglês..." (Inglês, principal), "Iorubá: conheça o idioma..." (Iorubá, secundário), "Como funciona a alfabetização em hebraico..." (Hebraico, secundário). Nenhum título, data ou categoria foi alterado — só a composição visual.

## 4. Verificação

- Screenshot 1440px confirma: hierarquia clara entre principal/secundários, divisórias finas visíveis, CTA "Leia o artigo →" legível, sem overflow.
- `flake8`/`pytest` (330 passed, 11 skipped) sem regressão.
- Hero (`.v2-editorial-hero`), CTA final e Footer confirmados intactos (hash MD5 do Hero idêntico ao baseline `1acd805606a5cd559f92969de0437315`; CTA final e Footer verificados por screenshot — idênticos ao estado aprovado na fase anterior).
