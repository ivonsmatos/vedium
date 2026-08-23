# 06 — Sistema fotográfico e de mídia Vedium

> **Escopo da Fase 0.5:** documento de direção. Nenhum asset foi alterado, copiado para produção, comprimido ou implementado. Os arquivos em `vedium-references/envato-assets/` foram analisados somente para leitura.

## 1. Papel da fotografia

A fotografia é parte estrutural do design system: ela deve tornar visíveis a relação humana, a aula ao vivo, o acompanhamento, a progressão e o uso real do idioma. Não é preenchimento posterior de espaços vazios.

A Vedium deve parecer humana, profissional, contemporânea, culta, institucional, acessível e premium sem ostentação. A imagem deve ser séria sem ser fria e espontânea sem parecer casual demais.

### O que a imagem precisa comunicar

- adultos aprendendo e ensinando;
- atenção, escuta, fala, escrita e leitura;
- relação entre professor e aluno;
- ambiente online reconhecível, sem depender de interfaces falsas;
- aplicação em trabalho, cotidiano e integração;
- diversidade natural de pessoas e situações;
- repertório cultural validado, não estereótipos.

### O que deve ser recusado

- sorriso publicitário ou comemoração encenada;
- pose de marketplace/infoproduto;
- pessoa apontando para copy space sem contexto;
- crianças/adolescentes como linguagem dominante;
- ilustração infantil, avatar, globo, formatura genérica;
- bandeiras e cartões-postais como principal código de idioma;
- símbolos culturais ou religiosos usados como decoração;
- imagem stock apresentada como professor, aluno, aula, plataforma ou experiência real da Vedium.

## 2. Hierarquia de verdade

Esta ordem prevalece sobre conveniência de layout:

| Categoria | Definição | Pode servir como prova Vedium? | Regra |
|---|---|---|---|
| **REAL VEDIUM** | Professores, alunos autorizados, aulas, plataforma, equipe e materiais reais | Sim, com consentimento e verificação | Prioridade máxima para hero, professores, depoimentos e prova |
| **STOCK APPROVED** | Stock alinhado à marca, usado para representar uma situação ou contexto genérico | **Não** | Pode ser mídia principal quando não afirma identidade ou evidência |
| **STOCK SUPPORT** | Stock aceitável apenas como apoio editorial/ambiental | **Não** | Não usar como principal prova ou rosto de uma oferta |
| **REJECT** | Conteúdo incompatível, enganoso, clichê, infantil ou culturalmente arriscado | Não | Não publicar |

Todo arquivo atual de `envato-assets` é stock. Portanto, a coluna “Pode servir como prova Vedium?” é **NÃO** para os 11 arquivos.

## 3. Níveis fotográficos

| Nível | Função | Critérios |
|---|---|---|
| **A — HERO / SIGNATURE** | Home, pilar, B2B e campanha institucional | Presença humana forte, composição sofisticada, contexto coerente, qualidade alta e recorte responsivo viável |
| **B — EXPERIENCE** | Aula, conversa, professor genérico, aluno, orientação, notebook, videoconferência e prática | Ação de aprendizagem legível e expressão natural |
| **C — APPLICATION** | Trabalho, reunião, cotidiano, mobilidade, integração, leitura e relações profissionais | Mostra onde o idioma é aplicado, sem fingir ser uma aula |
| **D — SUPPORT / EDITORIAL** | Blog, detalhes, cards e fundos discretos | Mãos, caderno, livros, notebook, anotações, ambiente e textura narrativa |

O nível descreve a força/função da imagem; a categoria de verdade decide se ela pode ser usada. Um asset pode ter forma de nível B e ainda ser `REJECT` por conteúdo inadequado.

## 4. Direção visual

### Pessoas e expressão

- Adultos em ação, não modelos “apresentando um produto”.
- Olhar pode estar na pessoa, caderno ou tela; contato direto com a câmera só quando fizer sentido editorial.
- Gestos espontâneos, mãos visíveis quando explicam a ação.
- Roupa contemporânea e realista, sem figurino cultural.
- Professores reais devem ser identificados somente com nome/cargo verificados.

### Luz e cor

- Luz natural ou suave, pele preservada e contraste moderado.
- Temperatura levemente quente é aceitável; evitar filtros laranja/azul intensos.
- Fundos com madeira, livros, plantas e espaços de trabalho podem apoiar a marca, sem transformar toda cena em “biblioteca cenográfica”.
- Tratamento deve conviver com azul, terracota e neutros candidatos da Vedium; não recolorir pele, roupa ou objetos para “caber” na paleta.

### Composição

- Preferir profundidade real e camadas discretas.
- Para `HeroSplit`, a imagem não precisa de copy space interno; a pessoa pode ocupar o quadro.
- Para `HeroFullBleed`, exigir área segura comprovada para texto e contraste sem cobrir rosto/mãos.
- Não espelhar pessoas ou telas para fabricar direção; texto em tela, gestos e assimetrias tornam o espelhamento enganoso.
- Evitar mosaico excessivo. Uma imagem forte é preferível a muitas miniaturas.

### Vídeo

- Sem autoplay com áudio.
- Autoplay silencioso só quando curto, não essencial, pausável e respeitando `prefers-reduced-motion`.
- `VideoSection` institucional deve ter poster, play explícito, legenda e transcrição quando houver fala útil.
- Stock falado em outro contexto não deve receber dublagem que o transforme falsamente em professor Vedium.
- Arquivos ProRes/4K são masters; derivados web serão planejados em fase própria, nunca sobrescrevendo o original.

## 5. Regras por frente

### Inglês

Priorizar adultos, carreira, reunião, apresentação, estudo e videoconferência. A biblioteca tem bons candidatos de professor genérico ensinando gramática e de profissional em reunião online. Evitar bandeiras, Londres/NY como atalho e visual infantil.

**E04 e E08 não devem ser tratados como primeira opção para hero principal enquanto forem stock** — mostram uma pessoa em postura de "professor", e usá-los como hero cria risco de confusão com um professor real da Vedium. Seu uso preferencial é em `VideoSection`, "Como funciona" e demonstração contextual de ensino online. Para o hero temporário de Inglês, priorizar mídia de aplicação/estudo (E02, E05 ou E07) que não possa ser confundida com professor Vedium. R05 (professor de Inglês real, ver `09-real-vedium-shoot-list.md`) permanece como solução definitiva para o hero.

### Iorubá — gate crítico

Uma pessoa negra ou percebida como africana não representa automaticamente Iorubá. Não usar “África genérica”, tecidos, máscaras, símbolos religiosos ou objetos ritualísticos sem relação comprovada.

Ordem obrigatória para hero/prova:

1. professor real da Vedium;
2. aula real da Vedium;
3. materiais reais e culturalmente validados;
4. stock neutro de aprendizagem adulta somente como apoio.

Nenhum asset atual está autorizado como hero ou prova de Iorubá. Em especial, os assets E03 e E07 não podem ser associados a Iorubá pela cor da pele das pessoas.

Conteúdo de língua, história, cultura, práticas, produção cultural ou contexto afro-brasileiro exige revisão do professor/especialista responsável.

### Português para Estrangeiros (PLE)

Comunicar viver, trabalhar, participar, integrar-se e manter relações no Brasil. Stock de trabalho/estudo pode apoiar, mas a biblioteca não contém contexto brasileiro comprovado. Hero de integração e prova de experiência precisam de produção real.

Evitar carnaval, praia e Cristo Redentor como eixo, exotização e “Brasil turístico”.

### Espanhol

Preferir vida profissional, conversa, aula, estudo e aplicação latino-americana contemporânea. O vídeo E05 pode representar uma adulta estudando, mas o nome do arquivo não autoriza classificá-la como “latina” nem como prova cultural. Evitar sombrero, flamenco e bandeiras.

### Hebraico

Priorizar leitura, escrita, estudo adulto, professor e orientação. E02 pode servir como apoio neutro de estudo, nunca como contexto hebraico. Símbolo religioso só entra quando for relevante à trilha específica e validado.

### B2B

Priorizar colaboração, formação, discussão, reunião, apresentação e concentração. E07 é o principal stock fotográfico; E03 cobre aplicação profissional vertical. E01 mostra treinamento presencial e deve ser apoio cauteloso, pois a Vedium é 100% online.

Evitar braços cruzados, apertos de mão, boardroom luxuoso e celebração artificial.

## 6. Diversidade como conjunto

A biblioteca atual mostra adultos de gêneros, tons de pele, idades percebidas e contextos diversos, incluindo uma pessoa usuária de cadeira de rodas. Ainda assim:

- predomina o indivíduo diante de notebook; há pouca conversa real entre adultos;
- falta representação verificável dos professores e alunos da Vedium;
- falta contexto brasileiro cotidiano para PLE;
- falta material legítimo de Iorubá;
- faltam diferentes faixas de idade adulta em aulas online reais;
- há risco de transformar uma pessoa em “representante” de raça, país ou idioma.

A curadoria final deve observar ritmo e repetição: não usar a mesma pessoa stock como se participasse de vários cursos. Diversidade deve emergir de pessoas e situações reais, não de distribuição mecânica por cards.

## 7. Proporções por componente

Proporções são envelopes de layout; o original permanece intacto. Cada uso exige derivado próprio em fase posterior.

| Componente | Desktop | Tablet | Mobile | Regra de conteúdo/safe area |
|---|---|---|---|---|
| `HeroSplit` | 4:5 ou 3:2 no painel de mídia | 3:2 | 4:5 | Sem texto sobre a foto; preservar rosto, mãos e objeto de ação |
| `HeroFullBleed` | 16:9 | 3:2 | 4:5 | Área segura de texto ≥ 35% do quadro; fallback para split se não houver |
| `TeacherCard` | 4:5 | 4:5 | 4:5 | Cabeça, ombros e gesto; espaço acima da cabeça sem corte apertado |
| `TeacherProfile` | 4:5 + opção 3:2 ambiental | 4:5 | 4:5 | Retrato real; fundo coerente e sem elementos identificáveis indesejados |
| `LanguageCard` | 3:2 | 4:3 | 4:5 ou 3:2 | Não usar rosto como código de idioma/etnia |
| `CourseCard` | 4:3 | 4:3 | 3:2 | Ação simples, leitura em tamanho pequeno, sem texto gravado na imagem |
| `VideoSection` | 16:9 | 16:9 | 16:9; 9:16 só em variante explícita | Poster e controles; não cortar quadro horizontal em portrait automaticamente |
| `FeatureMedia` | 3:2 | 3:2 | 4:5 | Foco no gesto/objeto; pode alternar lado |
| `EditorialCard` | 3:2 | 4:3 | 3:2 | Detalhe legível, baixa dependência de rosto |
| `Testimonial` | 1:1 ou 4:5 | 1:1 | 1:1 | Somente pessoa real/autorizada; stock proibido |
| `B2BCase` | 3:2 | 3:2 | 4:5 | Caso real exige cliente/equipe autorizados; stock só contextual |
| `BlogCard` | 3:2 | 3:2 | 3:2 | Crop uniforme por coleção; assunto não depende de estereótipo |
| `CTAWithMedia` | 3:2 | 4:3 | 4:5 | Pessoa olha/age para dentro da composição, sem pose de apontar para CTA |

## 8. Cropping e safe area

### Regras gerais

- Manter rosto inteiro e margem natural acima da cabeça.
- Não cortar mãos quando elas escrevem, apontam para material ou explicam a ação.
- Preservar notebook, caderno, quadro ou material quando eles tornam o contexto pedagógico legível.
- Definir `object-position` por derivado; não usar sempre `center center`.
- Criar preview separado para 16:9, 3:2, 4:5 e mobile antes de aprovar.
- Se o crop retirar a relação pessoa–objeto, trocar o componente, não insistir no asset.

### Candidatos A para hero/signature

| Asset | Pessoa e composição | Texto | 16:9 | 3:2 | 4:5/mobile | Risco e decisão |
|---|---|---|---|---|---|---|
| **E07** — homem em videoconferência | Pessoa à direita; monitor à esquerda; mãos/gesto centrais | Preferir `HeroSplit`; overlay à esquerda disputa com o monitor | Viável com corte vertical leve | Nativo | Crop à direita preserva rosto/mãos, mas perde parte da videoconferência | **Principal stock temporário do hero institucional (Home)**; aprovado também para B2B/Inglês profissional; nunca associar a Iorubá |
| **E06** — adulta estudando em cadeira de rodas | Pessoa à direita; monitor à esquerda; escrita e cadeira dão contexto | Há respiro superior esquerdo, mas o monitor limita overlay; split é mais seguro | Viável | Nativo | Crop à direita pode preservar rosto, mãos e cadeira, perdendo monitor | **Alternativa/editorial do hero institucional** (não a principal); aprovado para experiência/inclusão — **não escolher apenas para comunicar diversidade ou inclusão sem contexto real** (risco de tokenismo) |
| **E04/E04D** — homem ensinando inglês em vídeo | Professor genérico, monitor com verbos e material impresso | Validar frames antes de overlay; preferir `VideoSection` | Nativo | Possível após seleção de frame | Alto risco de cortar monitor ou gesto; não converter automaticamente | **Não é primeira opção para hero de Inglês enquanto for stock**; usar em `VideoSection`/Como funciona/demonstração contextual; R05 é a solução definitiva para o hero; arquivos são duplicados byte a byte |
| **E08** — mulher ensinando inglês em vídeo | Professora genérica, laptop, livros e quadro “present simple” | Preferir vídeo com controles; não rotular como professora Vedium | Nativo | Possível | Exige revisão quadro a quadro para preservar rosto/quadro/mãos | **Não é primeira opção para hero de Inglês enquanto for stock**; usar em `VideoSection`/Como funciona/demonstração contextual; R05 é a solução definitiva para o hero; não é prova Vedium |

E01, E02, E03, E05 e E10 não são candidatos principais a hero: funcionam melhor como experiência, aplicação ou apoio. E11 está rejeitado.

## 9. Governança de uso

Cada associação asset → página precisa registrar:

- categoria REAL/STOCK e se há permissão de prova;
- pessoa/contexto que a imagem realmente mostra;
- página, componente e locale;
- crop aprovado por breakpoint;
- alt text baseado no conteúdo visível, sem atribuir identidade não comprovada;
- licença/origem e master preservado;
- consentimento, quando REAL VEDIUM;
- revisão cultural, quando aplicável;
- data para substituição progressiva por conteúdo real.

### Proibições de copy e alt text para stock

Não escrever: “nosso professor”, “uma aula Vedium”, “nossos alunos”, “nossa plataforma” ou nomes/cargos inventados. Preferir descrições literais, por exemplo: “Pessoa adulta participa de uma chamada de vídeo enquanto faz anotações”.

### Regras de alt text

- **Imagem informativa** (transmite conteúdo próprio, ex.: retrato de professor, cena de aula): alt literal e contextual, descrevendo o que está de fato visível.
- **Imagem funcional** (ex.: ícone clicável, imagem dentro de um link ou botão): alt coerente com a função/destino do elemento, não com a cena retratada.
- **Imagem puramente decorativa** (não acrescenta informação, só composição): `alt=""`, para que leitores de tela a ignorem.
- Não usar alt text para keyword stuffing (empilhar termos de SEO em vez de descrever a imagem).
- Não atribuir identidade, nacionalidade, vínculo institucional ou idioma não comprovados — vale tanto para o alt text quanto para qualquer copy ao redor da imagem (ver seção acima).

## 10. Leitura da biblioteca atual

- 11 arquivos: 5 fotos e 6 vídeos.
- 4 vídeos landscape 16:9, 2 vídeos portrait.
- As 5 fotos são landscape próximas de 3:2.
- E04 e E04D têm o mesmo SHA-256 e são cópias idênticas; não apagar nesta fase.
- Principais forças: ensino de inglês reconhecível, estudo adulto, videoconferência e trabalho.
- Principais lacunas: prova real Vedium, professores reais, Iorubá legítimo, vida no Brasil/PLE, contexto hebraico específico, aula online real em grupo e casos B2B reais.
- E11 deve ser rejeitado por mostrar matemática e adereços com linguagem infantil, incompatíveis com a escola de idiomas adulta.

O inventário arquivo a arquivo está em `07-envato-asset-inventory.csv`; o uso recomendado por página está em `08-page-media-map.md`; as lacunas de produção real estão em `09-real-vedium-shoot-list.md`.
