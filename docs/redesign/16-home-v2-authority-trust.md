# 16 — Reset institucional, autoridade e confiança (Fase B.5)

> **Origem**: a Fase B.4 acertou a arquitetura da Home (ordem de seções, ausência de professor individual/preço/FAQ), mas a revisão humana identificou um problema diferente: a página não transmitia "escola de idiomas séria, autoridade acadêmica, confiança, clareza institucional, experiência pedagógica, qualidade percebida" — parecia conceitual, publicitária, genérica, dependente de stock, próxima de template educacional. A B.5 foi um **reset de linguagem institucional** (copy, tipografia, tom, densidade), não uma mudança de arquitetura — a ordem de seções da B.4 continua válida, só ganhou 2 seções novas.
>
> **⚠️ Arquitetura substituída na Fase B.6 (reset Bain-inspired)**: a Home passou por uma segunda reestruturação de arquitetura (não só de tom) — Hero sem foto, VediumPathfinder, Cursos em blocos grandes alternados, nova ordem de seção. Muito do tom/vocabulário/copy institucional descrito aqui (seções 1, 3) continua valendo — a B.6 manteve o registro concreto/acadêmico e o vocabulário preferido. **Para a arquitetura e copy atuais, ver `18-bain-inspired-direction.md`.**

## 1. Mudança de tom

| | Fase B.4 | Fase B.5 |
|---|---|---|
| Registro | Conceitual/inspiracional ("participar de novos contextos", "a evolução acontece na troca") | Concreto/acadêmico ("escola", "aulas", "professores", "nível") |
| Pontuação | Travessão como recurso estilístico frequente | Zero travessão na copy de interface — ponto, vírgula ou frase nova |
| Vocabulário evitado | — | "contexto"/"contextos" (0 ocorrências, meta era ≤1), "professor real" (soa defensivo), "exemplo" em títulos de demonstração |
| Vocabulário preferido | — | escola, cursos, aulas, professor, nível, progressão, turma, prática, correção, orientação, acompanhamento |

## 2. Hero — antes e depois

**Antes (B.4)**: eyebrow "Cursos de idiomas online ao vivo"; H1 "Idiomas ao vivo para participar de novos contextos."; CTA primário "Descubra seu nível".

**Depois (B.5)**:
- Eyebrow: "Escola de idiomas 100% online"
- H1: "Aprenda idiomas ao vivo com professores nativos e especialistas."
- Apoio: "Aulas em tempo real, progressão por nível e acompanhamento para você avançar com clareza no trabalho, nos estudos e na vida."
- CTA primário: "Conheça os cursos" (era secundário na B.4 — trocado de posição, ver seção 8)
- CTA secundário: "Descubra seu nível"
- Lista discreta dos 5 idiomas abaixo do CTA: "Inglês · Iorubá · Português para Estrangeiros · Espanhol · Hebraico"

### Ajuste de escala feito por evidência de screenshot (não por número abstrato)

A missão pedia H1 "aprox. 60 a 68px" **e**, separadamente, "objetivo ideal em desktop: 3 ou no máximo 4 linhas... não quebrar o H1 artificialmente em 5 linhas". Essas duas metas colidiram na prática: com o H1 real da Home (9 palavras, incluindo "professores" e "especialistas", ambas longas) numa coluna de 47% de um container de 1216px (~578px), 68px de fonte quebrava em **6 linhas**; 60px quebrava em **5**. Só em **52px** (`--v2-text-h1` com teto reduzido de `4.25rem` para `3.25rem`) o H1 real ficou em exatamente **4 linhas** — confirmado por 3 rodadas de screenshot real (não estimativa). Priorizei a meta de linhas (mais específica, com anti-padrão nomeado explicitamente) sobre o teto de pixel abstrato, e documentei a decisão no próprio token em `tokens.css`.

### Imagem do Hero

Trocada de E02 (pessoa sozinha com fones/notebook, sem sinal claro de "aula") para **E06** — o asset se chama literalmente `listening-to-online-university-course` ("ouvindo um curso universitário online"), mostra pessoa adulta diante de um monitor com caderno: o sinal de "aula online" mais forte disponível nos 4 assets locais processados nesta sessão. **Nenhum asset local mostra um professor visível na tela** (prioridade 2 do briefing da missão) — registrado como pendência abaixo.

**`REAL VEDIUM CLASS MEDIA REQUIRED`**: nem o Hero nem a seção "Aula ao vivo" (Live Experience) têm hoje uma foto/vídeo que mostre uma aula Vedium real com professor visível. Isso é esperado e correto — `06-photography-system.md` e `08-page-media-map.md` classificam "aula ao vivo real" como **P0, REAL VEDIUM REQUIRED**, e nenhum dos 4 stocks locais processados serve como prova disso. Antes do rollout, essas duas seções precisam de captação real (ver `09-real-vedium-shoot-list.md`, R01/R02/R05).

## 3. Linguagem concreta — termos reduzidos vs. reforçados

**Reduzidos a zero no Presentation Mode** (confirmado por scan no HTML renderizado, não por inspeção visual): "contexto"/"contextos", travessão (`—`), "professor real", "Título de exemplo", "exemplo".

**Substituições feitas seção a seção**:
- "A evolução acontece na troca." → "Veja como uma aula ao vivo funciona." (Live Experience)
- "Do primeiro diagnóstico à evolução contínua." → "Comece pelo nível certo." (How it works → Como começar)
- "Evolução que você consegue acompanhar." → "Você sabe onde está e o que vem depois." (Progressão)
- "Formação linguística para equipes que atuam em contextos globais." → "Idiomas para equipes que precisam se comunicar com mais segurança." (B2B — removeu "contextos globais")
- "Conhecimento para usar o idioma com mais contexto." → "Aprenda também fora da aula." (Blog)
- "Descubra qual é o próximo passo para você." → "Encontre o curso certo para o seu objetivo." (CTA final)
- "Idiomas ao vivo, com professores reais e progressão acompanhada — para participar de novos contextos." → "Escola de idiomas online com aulas ao vivo e progressão por nível." (Footer)

## 4. Tipografia — Playfair removida da Home

A missão determinou: Poppins para headings/interface, Inter para corpo, Arial como fallback — **nenhum uso de Playfair Display no Presentation Mode**. Achado ao auditar o CSS existente (não só o HTML da Home): 3 componentes usados na Home ainda referenciavam `var(--v2-font-display)` (Playfair) na Fase B.4:

1. `.v2-language-card--typographic .v2-language-card__name` (nome do idioma nos cards tipográficos de Iorubá/Espanhol/Hebraico)
2. `.v2-process__number` (números grandes do "Como começar")
3. `.v2-footer__message` (mensagem do rodapé)

Todos os 3 trocados para `var(--v2-font-heading)` (Poppins). Playfair continua auto-hospedada e disponível na biblioteca técnica (`LevelJourney`, `TestimonialCard`, `.v2-display`), que não fazem parte do Presentation Mode.

## 5. Autoridade acadêmica — 2 seções novas

### Como a Vedium ensina (nova)

Reaproveita o macro `v2_proof_bar` (mesmo padrão "sem ícone grande, sem card SaaS" já usado na Trust Strip) em fundo claro, com 4 "provas" — Interação, Prática, Correção, Progressão — cada uma com uma frase objetiva, não um benefício de marketing.

### Institucional Vedium (nova)

Bloco de texto puro (sem foto — os 4 assets já estão alocados em outras seções, ver seção 2) declarando o que a Vedium é: escola 100% online, os 5 idiomas oferecidos, e a proposta acadêmica (aulas ao vivo, professores, progressão). Sem número fictício.

## 6. Trust Strip (era "Institutional Proof Strip")

Itens trocados de {"Ao vivo de verdade", "Professores nativos e especialistas", "Progressão clara", "Idioma + contexto"} para {"Aulas ao vivo", "Professores nativos e especialistas", "Progressão por nível", "Turmas e aulas particulares"} — a missão pediu explicitamente a remoção de "Idioma + contexto" da faixa. Continua sem cards, sem números, fundo azul profundo com texto branco.

## 7. Cursos — de mosaico editorial para catálogo acadêmico

A composição assimétrica dramática da B.4 (Inglês ocupando 2 linhas, cards empilhados em coluna estreita) foi substituída por uma **grade uniforme de 3 colunas** (ver `components-editorial.css`, `.v2-mosaic`) — todos os 5 cursos com a mesma altura/proporção, tratamento visual único independente de ter foto ou ser tipográfico. Copy de cada curso trocada para o formato "linha acadêmica curta" pedido pela missão (nome / nível-ou-tese / descrição prática / CTA), incluindo a copy exata fornecida para os 5 idiomas.

## 8. Header — CTA principal

Testado "Conheça os cursos" como CTA principal da navegação (era "Descubra seu nível"), conforme sugestão da missão para a Home institucional. Implementado via um override opcional (`v2_hdr_primary_cta_override`) em `header.html` — o mecanismo de teste de nível dinâmico continua **intacto e inalterado** para qualquer outra página que reusar o mesmo include; só a instância da Home passa o override.

## 9. Confiança no Footer

Confirmado presente e mantido: razão social (Vedium Global Educação e Tecnologia Ltda.), CNPJ, "Brasil", WhatsApp oficial, Instagram, LinkedIn, Privacidade, Termos, Cancelamento/reembolso. Mensagem principal do footer trocada (seção 3) para remover travessão/"contexto"/"professores reais".

## 10. Radius e escala institucional

`--v2-radius-media` reduzido de 16px para 10px e `--v2-radius-lg` de 22px para 16px (mission seção 25: "instituição séria: radius moderado"). Logo do header aumentado (2.75rem → 3rem no desktop), espaçamento da navegação aumentado (`--v2-space-6` → `--v2-space-8`).

**Não implementado nesta fase**: estado sticky do header (a missão condicionava a "caso o componente já suporte sem JS pesado" — exigiria coordenar `z-index`/offset com a barra fixa do próprio dev-tool de preview, considerado fora do escopo desta passada).

## 11. Copy scan — resultado final (regra 24 da missão)

Contagem no **HTML renderizado** do Presentation Mode (não no código-fonte com comentários Jinja, que não chegam ao navegador):

| Termo | Critério da missão | Resultado |
|---|---|---|
| `—` (travessão) | 0 | **0** |
| "professor real" | 0 | **0** |
| "Título de exemplo" | 0 | **0** |
| "exemplo" | minimizar | **0** |
| "contexto"/"contextos" | ≤1 combinado | **0** |

## 12. Assets de fotografia — alocação final da B.5

| Asset | Uso |
|---|---|
| E06 (ouvindo curso online) | Hero |
| E02 (estudo com fones/notebook) | Card de Inglês |
| E10 (fones, anotações em casa) | Card de Português para Estrangeiros |
| E07 (videoconferência em equipe) | B2B |
| — | Live Experience e Institucional Vedium ficam sem foto — os 4 assets já estão comprometidos em outras seções sem repetição; repetir qualquer um devolveria a sensação de "stock reciclado" que este projeto vem corrigindo desde a Fase B.3 |

Blog usa 3 títulos **reais** de `blog_content.py` (Inglês, Iorubá, Hebraico) com `href` reais (`/blog/<slug>`), sem imagem — os `hero_image` reais desses posts são URLs remotas do Unsplash, que violariam a regra "nenhum asset remoto" deste design system.

## 13. Pendências para antes do rollout

1. `REAL VEDIUM CLASS MEDIA REQUIRED` — Hero e "Aula ao vivo" precisam de foto/vídeo real de aula Vedium (professor + aluno visíveis), não stock (ver seção 2).
2. Poppins/Inter ainda em fallback Arial (pendência desde a Fase B.1).
3. Estado sticky do header não implementado (seção 10).
4. H1 do Hero está em 52px no teto, abaixo da faixa "60-68px" pedida — decisão documentada na seção 2, mas fica como ponto para validação humana explícita (pode ser aceito como está, ou pode-se preferir encurtar o H1 em vez de reduzir a fonte).
