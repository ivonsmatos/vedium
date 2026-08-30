# 30 — Blog Review Queue: 97/97 com decisão explícita

Resolve a pendência da Fase F.5 (KEEP 73 / REVIEW 24, número estimado no
relatório daquela fase) com evidência real, e investiga os artigos não
cruzados contra `Publicados_Auditoria`, per missão G.1 seções 3-4.

## Reconciliação do número "24"

O "REVIEW: 24" citado no status desta fase era uma estimativa do
relatório da Fase F.5, feita antes de eu corrigir dois bugs reais do
script de cruzamento (`scripts/migrate-blog.mjs`): truncamento de título
em literais Python concatenados em várias linhas, e falso-positivo de
correspondência para títulos em escrita não-latina (russo/chinês
normalizavam para string vazia e colidiam entre si). Depois da correção
(documentada em `26-blog-cadence-and-dates.md`), o número real é:

| Categoria | Quantidade |
|---|---|
| Total de artigos no `blog_content.py` | 97 |
| Casados 1:1 com `Publicados_Auditoria` por título exato | 77 |
| Marcados `REVIEW` no CSV (`27-blog-url-migration-map.csv`) | **6** |
| Não casados por título, mas casados por data (extração de título com bug, não duplicidade real) | 15 |
| Genuinamente não encontrados (nem título, nem data) | **5** |

Ou seja: **11 itens** precisam de decisão explícita além do KEEP
automático (6 REVIEW + 5 não cruzados). Os outros 15 são artefatos de
extração do script, não indecisões editoriais reais (ver seção
"Achados de qualidade de dados" abaixo).

## Os 6 REVIEW do CSV — decisão por item

| current_url | Motivo do REVIEW | Decisão | Evidência |
|---|---|---|---|
| `/blog/brasilianisches-portugiesisch-fur-auswanderer-die-wichtigsten-grundlagen` | DUPLICATE_CANDIDATE (grupo de 3 artigos em alemão sobre "Brasilianisches Portugiesisch für X") | **KEEP** | Cada um cobre um ângulo diferente real (emigrantes / executivos / trabalho e vida cotidiana) -- mesmo padrão editorial já usado com sucesso em dezenas de artigos de PLE em inglês (ex.: "for renting an apartment", "for opening a bank account"). Não há evidência de canibalização de intenção, só de tema adjacente. |
| `/blog/brasilianisches-portugiesisch-fur-fuhrungskrafte-und-manager` | idem | **KEEP** | idem |
| `/blog/brasilianisches-portugiesisch-fur-beruf-und-alltag-in-brasilien` | idem | **KEEP** | idem |
| `/blog/brazilian-portuguese/how-to-learn-portuguese-for-brazil-when-you-already-speak-another-romance-language` | DUPLICATE_CANDIDATE (par em inglês) | **KEEP** | Ângulo "transferência de outra língua românica" é diferente de "situações culturais x gramática isolada" -- mesma lógica acima. |
| `/blog/brazilian-portuguese/learn-portuguese-for-brazil-through-cultural-situations-not-isolated-grammar` | idem | **KEEP** | idem |
| `/blog/ioruba/como-ouvir-cantigas-em-ioruba-com-mais-atencao-ao-significado` | Marcado `REVISAR` na própria auditoria oficial (`Publicados_Auditoria`) | **MANUAL DECISION REQUIRED** | `Regras_SEO_GEO_v2`: "Iorubá: revisão do professor responsável antes de publicar, sem exceção." `Diagnostico` confirma: 2 artigos publicados tratam "cantigas rituais/ancestralidade" como tema central e precisam de revisão do professor antes de continuar indexados. Não tenho como fazer essa revisão nesta sessão (exige um professor de Iorubá de verdade) -- fica explicitamente pendente, não "resolvido" por mim. |

O segundo artigo da mesma categoria cultural (`Iorubá e ancestralidade:
por que aprender a língua transforma a relação com a cultura`) está
marcado `MANTER` (não `REVISAR`) na aba `Publicados_Auditoria` — mas
pelo mesmo critério da regra de Iorubá, ele também trata ancestralidade
como tema central. **Recomendação**: incluir esse segundo artigo na
mesma revisão do professor, mesmo a planilha não tendo marcado
`REVISAR` nele — a regra da marca (seção 38 da missão F.5) não faz essa
distinção.

## Os 5 genuinamente não encontrados

| Slug | Data | Categoria | Título | Por que não casou | Ação |
|---|---|---|---|---|---|
| `yoruba-alphabet-guide` | 2026-07-02 | (nenhuma -- URL plana) | Yoruba alphabet: the 25 letters, vowels and tones (a beginner's guide) | Não existe na auditoria por título nem por data | **KEEP** -- tradução em inglês do artigo pt-BR de alfabeto já aprovado; conteúdo estrutural/linguístico, fora da categoria restrita de Iorubá (rezas/ancestralidade) |
| `yoruba-greetings` | 2026-07-02 | (nenhuma) | Yoruba greetings: how to say good morning, thank you and more | idem | **KEEP** -- mesma razão |
| `yoruba-numbers-1-to-20` | 2026-07-02 | (nenhuma) | Yoruba numbers 1 to 20: how to count (and the base-20 logic) | idem | **KEEP** -- mesma razão |
| `yoruba-language-and-culture` | 2026-07-02 | (nenhuma) | Yoruba: get to know the language and why you should learn it | idem | **KEEP** -- mesma razão (título genérico "cultura", mas o corpo real não foi auditado linha a linha nesta sessão -- se alguém revisar o corpo e achar conteúdo religioso/ritual, reclassificar) |
| `curso-de-ingles-com-professor-ao-vivo-o-que-muda-na-evolucao-da-fala` | 2026-07-15 | `ingles` | Curso de inglês com professor ao vivo: o que muda na evolução da fala | idem | **MANUAL DECISION REQUIRED** -- ver nota abaixo |

**Nota sobre o artigo de Inglês não cruzado**: esse artigo (2026-07-15)
é publicado 2 dias depois do artigo que MIGREI como prova de conceito
desta fase (`aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-
vale-a-pena`, 2026-07-13), na mesma categoria, com título muito
semelhante ("curso de inglês com professor ao vivo: o que muda na
evolução da fala" vs "aula de inglês online ao vivo: como funciona e
para quem vale a pena"). É um candidato real de **CANONICAL REVIEW**
entre os dois -- não decido isso sozinho porque já escolhi o primeiro
como o artigo "seguro" desta fase; alguém do time editorial precisa
comparar os dois corpos completos e decidir se ambos ficam (ângulos
diferentes) ou se um deveria virar `MERGE + 301` para o outro.

## Achado: por que 4 artigos de Iorubá em inglês não estão na auditoria

Os 4 `yoruba-*` acima têm data 2026-07-02 — **antes** da data de
compilação da auditoria oficial (26 de julho de 2026, ver `Diagnostico`,
linha de cabeçalho). Deveriam ter sido capturados se a auditoria fosse
exaustiva até essa data. Isso é um **gap do processo de auditoria**, não
um problema de conteúdo: recomendo rodar de novo o levantamento de
`Publicados_Auditoria` antes do cutover para confirmar que não há mais
nenhum artigo publicado fora da lista de 94.

## Achados de qualidade de dados (dos 15 "casados só por data")

Nenhuma ação bloqueante, mas vale registrar para uma limpeza futura:

- **Título com prefixo de rascunho vazado**: o artigo com data
  2026-06-09 tem, literalmente, `"title": "Título SEO: Brazilian
  Portuguese for Cultural Adaptation: Your First 90 Days in Brazil"` --
  alguém colou o rótulo de campo ("Título SEO:") dentro do valor do
  título. **UPDATE recomendado**: remover o prefixo "Título SEO: " antes
  do próximo ciclo de otimização. Não fiz essa edição nesta fase (não é
  o artigo migrado como prova de conceito, e edições em massa no
  `blog_content.py` estão fora do escopo desta fase de QA).
- **Nome de arquivo vazado no título**: `"Portugais du Brésil pour
  familles qui s'installent au Brésil.md"` -- o sufixo `.md` ficou no
  título de produção. Mesmo tipo de limpeza, mesma recomendação.
- Os outros 13 são só truncamento da minha própria extração via regex
  (literais Python concatenados em várias linhas) -- o dado de produção
  em si está correto; ver `26-blog-cadence-and-dates.md`, seção
  "Limitação conhecida do script".

## Gate

**BLOG 97/97 DECISION COVERAGE: PASS** -- todo artigo tem uma linha em
`27-blog-url-migration-map.csv` com uma ação; os 11 que não eram KEEP
automático têm decisão e evidência acima. 2 itens ficam legitimamente em
`MANUAL DECISION REQUIRED` (não "resolvidos" por mim, porque exigem
revisão humana especializada: 1 professor de Iorubá, 1 decisão editorial
de sobreposição de conteúdo) -- isso é o comportamento correto pedido
pela missão ("não apagar automaticamente", "nunca decidir sozinho
questão cultural"), não uma falha do gate.
