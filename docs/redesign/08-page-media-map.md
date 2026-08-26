# 08 — Mapa de mídia por página

> **Escopo da Fase 0.5:** recomendação documental. Nenhum asset foi copiado, transformado ou implementado. Todo candidato `E` é stock e, portanto, não pode servir como prova de professor, aula, aluno, plataforma ou experiência real da Vedium.
>
> **⚠️ Atualizado na Fase B.6C (implementação real, não mais só recomendação)**: a Home V2 (`/design_system_v2`) passou a usar mídia real em todos os 5 idiomas de Cursos + vídeo em "Aula ao vivo" — as linhas abaixo ainda descrevem o planejamento original da Fase 0.5 (mantidas como histórico), mas o **estado atual implementado** está em `docs/redesign/21-course-media-selection.md`, com tabela completa (asset selecionado, por que, o que comunica, o que NÃO deve ser inferido, crop, substituição futura). Resumo do que mudou: Home—idiomas ganhou mídia em Iorubá e Hebraico pela primeira vez (novos assets E12/E15 no inventário, seção 21); Home—aula ao vivo ganhou vídeo real da biblioteca (E08); Home—B2B trocou de E07 (meio duplicado com o Hero) para E01-alt (a foto de videochamada em grupo, não o vídeo de sala física); PLE trocou de asset pra evitar duplicar o Hero. Os gates **P0 — REAL VEDIUM REQUIRED** continuam todos válidos e não foram satisfeitos por nenhuma dessas mudanças — elas são todas "ponte com stock aprovado", nunca prova real.

## 1. Legenda e prioridades

| Código | Asset resumido | Nível / categoria |
|---|---|---|
| E01 | Grupo adulto com instrutora em sala física | B / STOCK SUPPORT |
| E02 | Adulto com laptop, fones e caderno | B / STOCK APPROVED |
| E03 | Profissional usando laptop no escritório, vídeo portrait | C / STOCK APPROVED |
| E04 | Homem ensinando inglês, vídeo landscape | A / STOCK APPROVED |
| E04D | Duplicata byte a byte de E04 | A / STOCK APPROVED; não produzir derivados em duplicidade |
| E05 | Adulta falando e estudando em biblioteca, vídeo portrait | B / STOCK APPROVED |
| E06 | Adulta em cadeira de rodas estudando online | A / STOCK APPROVED |
| E07 | Profissional em videoconferência | A / STOCK APPROVED |
| E08 | Mulher ensinando inglês, vídeo landscape | A / STOCK APPROVED |
| E10 | Adulta com fones, laptop e caderno | D / STOCK SUPPORT |
| E11 | Ensino de matemática com linguagem infantil | REJECT |

Prioridades de produção e uso:

- **P0 — REAL VEDIUM REQUIRED:** a seção faz uma afirmação de identidade ou prova; não deve ser publicada com stock no papel principal.
- **P1 — ponte forte:** stock alinhado pode sustentar o layout temporariamente, com linguagem estritamente contextual.
- **P2 — apoio:** mídia editorial ou secundária; não é essencial à compreensão nem à conversão.
- **BLOQUEADO:** não usar o asset ou não publicar a mídia sem cumprir o gate indicado.

## 2. Homepage

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Home — hero | Foto humana editorial em `HeroSplit`; vídeo curto real como evolução | **E07 — principal stock temporário**; **E06 — alternativa/editorial**; E04/E08 apenas como alternativa de vídeo contextual | P1 agora; migrar para P0 real | E07 comunica aplicação profissional e é a escolha padrão do hero institucional. E06 comunica estudo online e serve como alternativa editorial — **não deve ser escolhida apenas para comunicar diversidade ou inclusão sem contexto real**; usá-la como hero exige que a cena (estudo online) seja o motivo da escolha, não a identidade da pessoa retratada, sob risco de tokenismo. Não chamar pessoas stock de alunos/professores. Preferir split, pois monitor e pessoa ocupam o quadro. |
| Home — idiomas | Série coerente de ações de aprender/aplicar, não retratos usados como código étnico | E02, E03, E05, E10 | P2 | Distribuir por situação, não “uma aparência por idioma”. Repetição da mesma pessoa entre cursos deve ser evitada. |
| Home — como funciona | Foto ou vídeo de aula online e acompanhamento | E04 ou E08; E02/E06 como fallback fotográfico | P1; substituir por R01/R02 | Stock pode explicar a modalidade, mas não comprova a aula Vedium. Incluir poster e controles em vídeo. |
| Home — aula ao vivo | Captura real de professor e aluno em interação | E04/E08 somente como apoio contextual | **P0 — REAL VEDIUM REQUIRED** | A promessa “ao vivo de verdade” exige aula real autorizada, não um ator stock. |
| Home — professores | Retratos reais, consistentes e identificados | Nenhum | **P0 — REAL VEDIUM REQUIRED** | E04/E08 não podem ocupar cards com nomes ou cargos. Depende de professores confirmados, imagem autorizada e dados verificados. |
| Home — B2B | Equipe/reunião online ou caso real | E07 principal; E03 vertical; E01 apenas apoio | P1 para contexto; P0 para case/prova | E01 é presencial e não deve ilustrar a modalidade como se fosse uma aula Vedium. |
| Home — CTA final | Retrato humano acolhedor ou detalhe real de aula | E02 ou E03 | P2; migrar para real | Usar `CTAWithMedia`, sem pose apontando para o botão e sem atribuição institucional. |

## 3. Hub de cursos

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Hub — abertura | Cena ampla de aprendizagem adulta | E06 ou E02 | P1 | A mídia estabelece o universo da escola, sem representar um idioma específico. |
| Hub — cards de idiomas | Ações de fala, leitura, escrita, trabalho e estudo | E02, E03, E05, E10 | P2 | Não usar rosto, tom de pele, roupa, bandeira ou religião como identificador de idioma. Usar crop uniforme por coleção. |
| Hub — progressão/metodologia | Material, feedback e acompanhamento reais | Nenhum asset comprova | **P0 — REAL VEDIUM REQUIRED** para prova | Produzir materiais e interface reais; stock pode apenas ambientar uma explicação. |

## 4. Inglês

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Inglês — hero | Adulto em uso profissional/aplicação, não professor em vídeo | E02, E05 ou E07 como ponte temporária | P1 | **E04 e E08 não devem ser tratados como primeira opção para hero principal enquanto forem stock** — mostrar uma pessoa "ensinando" no hero cria risco de confusão com professor Vedium. Para o hero temporário, priorizar mídia de aplicação/estudo (uso do idioma, trabalho, conversa) que não possa ser confundida com "professor Vedium". **R05 permanece como solução definitiva** e deve substituir esta linha assim que aprovado. |
| Inglês — aula/demonstração | Vídeo de explicação, gramática e interação | E04 ou E08 | P1; substituir por R05 | Aqui, sim, é o uso preferencial de E04/E08: `VideoSection`, "Como funciona" e demonstração contextual de ensino online — nunca como hero principal. Legenda/transcrição quando houver fala; não dublar para fabricar uma aula Vedium. |
| Inglês — professor | Retrato e pequeno trecho de professor confirmado | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Stock proibido em `TeacherCard` e `TeacherProfile`. |
| Inglês — objetivos | Estudo, comunicação, reunião e autonomia | E02, E05, E06 | P2 | Relacionar imagem à ação visível, não a nível CEFR presumido. |
| Inglês — carreira/aplicação | Reunião, apresentação e trabalho | E07; E03 | P1 | Não afirmar que a empresa, os colegas ou a formação sejam casos Vedium. |

## 5. Iorubá

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Iorubá — hero | Professor real, aula real ou material real culturalmente validado | **Nenhum** | **P0 — REAL VEDIUM REQUIRED** | Nenhuma pessoa stock pode representar Iorubá por aparência. Não usar E03 ou E07 como atalho racial. |
| Iorubá — experiência de estudo | Apoio neutro de adulto estudando | E02 ou E06, somente se a copy for genérica | P2 | A mídia não deve sugerir identidade, origem ou domínio cultural da pessoa retratada. |
| Iorubá — língua, história, cultura e ancestralidade | Professor/especialista, materiais e produção cultural reais | **Nenhum** | **BLOQUEADO até revisão cultural** | Conteúdo e mídia exigem revisão do professor/especialista responsável antes da publicação, especialmente nas três páginas prioritárias de Iorubá já mapeadas na Fase 0. |
| Iorubá — prova | Foto/vídeo autorizado de aula, professor ou material Vedium | **Nenhum** | **P0 — REAL VEDIUM REQUIRED** | Registrar origem, consentimento, contexto e aprovação cultural. Stock nunca é prova. |

## 6. Português para Estrangeiros (PLE)

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| PLE — hero | Pessoa adulta vivendo/aplicando português no Brasil; preferencialmente experiência real | E06 como ponte neutra | P1 agora; P0 real para versão definitiva | A biblioteca não contém contexto brasileiro verificável. Evitar turismo como substituto de integração. |
| PLE — work | Contexto profissional e comunicação | E03 ou E07 | P1 | Usar como aplicação genérica; não inferir que a pessoa seja estrangeira no Brasil. |
| PLE — daily life | Cotidiano, serviço, vizinhança, mobilidade e relações reais | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Planejar captação contextual no Brasil, sem encenação folclórica. |
| PLE — integration | Conversa e participação social/profissional | Nenhum; E01 apenas apoio remoto e cauteloso | **P0 — REAL VEDIUM REQUIRED** | E01 é uma sala física genérica e não representa integração brasileira nem operação online. |
| PLE — Brazil context | Situação cotidiana brasileira comprovada | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Não preencher a lacuna com carnaval, praia, monumentos ou pessoa cuja nacionalidade foi presumida. |

## 7. Espanhol

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Espanhol — hero | Conversa/aula adulta ou aplicação contemporânea | E05 como vídeo de estudo; E03 como trabalho | P1 | O nome de E05 não comprova identidade latina ou hispânica; não o usar como validação cultural. |
| Espanhol — experiência | Estudo, fala e anotação | E05; E02 | P2 | Evitar bandeiras, flamenco ou país genérico como atalho. |
| Espanhol — professor/prova | Professor real e aula real | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Produzir mídia com professor confirmado e consentimento. |

## 8. Hebraico

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Hebraico — hero | Professor real em leitura/escrita e orientação | Nenhum específico; E02 somente como apoio neutro | **P0 — REAL VEDIUM REQUIRED** para identidade do curso | E02 não comprova identidade, língua, religião ou contexto hebraico. |
| Hebraico — estudo adulto | Leitura, escrita e anotação genéricas | E02 ou E06 | P2 | Símbolos religiosos não entram como decoração. |
| Hebraico — trilha religiosa/cultural | Professor e material relevante, com validação específica | Nenhum | **BLOQUEADO até validação** | A pertinência deve ser confirmada por trilha; não generalizar uma tradição para toda a página. |

## 9. B2B

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| B2B — hero | Colaboração profissional em videoconferência | E07 | P1 | Forte para `HeroSplit`; preservar monitor e gesto. Não apresentar a reunião como cliente real. |
| B2B — formação | Grupo em treinamento | E01, somente como apoio | P2 | A cena é presencial; acompanhar de texto que não contradiga a escola 100% online. |
| B2B — aplicação | Profissional concentrada no trabalho | E03 | P1 | Excelente variante portrait/mobile; não forçar crop horizontal. |
| B2B — caso e resultados | Equipe e depoimento de cliente autorizados | Nenhum | **P0 — REAL VEDIUM REQUIRED** | `B2BCase` exige cliente, contexto e resultados verificáveis. Stock é apenas contextual. |

## 10. Professores

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Professores — diretório | Retratos 4:5 reais e consistentes | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Só publicar professores confirmados, autorização de imagem, dados profissionais verificados e conteúdo editorial aprovado. |
| Professores — perfil `/professores/<slug>` | Retrato 4:5, retrato ambiental 3:2 e vídeo curto | Nenhum | **P0 — REAL VEDIUM REQUIRED** | E04/E08 são referências de situação, não professores Vedium. A mídia integra o gate para futura página canônica 200. |
| Professores — em aula | Foto/vídeo real de explicação, escuta e feedback | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Garantir consentimento dos demais participantes e privacidade das telas. |

## 11. Blog

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Blog — listagem | Imagem editorial 3:2 por assunto | E10; E02; detalhes derivados de produções reais futuras | P2 | Manter crop estável e evitar repetir rosto como autor/aluno de matérias diferentes. |
| Blog — artigo sobre estudo/escuta | Adulto com fones, notebook e anotações | E10 ou E02 | P2 | Alt text deve descrever o visível, sem declarar idioma ou método. |
| Blog — cultura/idioma específico | Imagem contextual comprovada e revisada | Nenhum genérico por padrão | P0/P1 conforme assunto | Para Iorubá, aplicar gate cultural. Não usar stock genérico como evidência histórica/cultural. |

## 12. Sobre

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Sobre — abertura | Equipe/fundadores reais em ambiente de trabalho | Nenhum | **P0 — REAL VEDIUM REQUIRED** | A página institucional precisa mostrar quem a Vedium é; stock não serve como retrato da organização. |
| Sobre — visão humana | Estudo adulto como apoio | E06 | P2 | Pode apoiar a narrativa de acesso, sem chamar a pessoa de aluna. |
| Sobre — equipe e história | Retratos, encontro e arquivos reais | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Verificar nomes, funções, datas e autorizações. |

## 13. Como funciona

| Página / seção | Tipo de mídia | Candidatos atuais | Prioridade | Observações |
|---|---|---|---|---|
| Como funciona — hero | Aula online ou pessoa em aprendizagem | E06; E04/E08 em vídeo | P1 | Hero pode explicar modalidade, mas não deve parecer prova real se for stock. |
| Como funciona — aula ao vivo | Interação real professor–aluno | E04/E08 somente como ponte de experiência | **P0 — REAL VEDIUM REQUIRED** para prova | Produzir aula Vedium com autorizações; não expor dados em tela. |
| Como funciona — diagnóstico/progressão | Conversa, feedback, materiais e interface reais | Nenhum | **P0 — REAL VEDIUM REQUIRED** | Captar etapas verdadeiras; não inventar tela ou resultado. |
| Como funciona — prática/aplicação | Estudo e trabalho | E02, E03 ou E07 | P2 | Escolher conforme a promessa textual e não inferir identidade das pessoas. |

## 14. Regras transversais de composição

- Limite padrão: uma mídia principal por seção; cards podem formar coleções, mas não mosaicos decorativos.
- `HeroFullBleed` só é aprovado depois de testar contraste e área segura em desktop e mobile. Na dúvida, usar `HeroSplit`.
- Vídeo horizontal não vira portrait por crop automático; oferecer enquadramento vertical captado separadamente ou poster estático.
- E04D não é alternativa criativa: é cópia de E04. Selecionar um único master operacional em fase posterior, sem apagar nenhum agora.
- E11 permanece bloqueado em todas as páginas e componentes.
- Todo uso deve manter registro de licença, categoria, crop por breakpoint, alt text, locale, revisão cultural e plano de substituição por conteúdo real.
- Conteúdo real precisa ser priorizado em professores, depoimentos, aula ao vivo, plataforma, Iorubá, contexto brasileiro de PLE e cases B2B.

O inventário técnico e de curadoria está em `07-envato-asset-inventory.csv`. As captações necessárias para preencher as lacunas estão especificadas em `09-real-vedium-shoot-list.md`.
