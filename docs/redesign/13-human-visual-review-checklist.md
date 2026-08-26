# 13. Checklist de revisão visual humana — Design System V2 (Fase B.2)

> Este documento é para **uso humano em navegador real**. Nenhum item abaixo foi marcado — a Fase B.2 apenas disponibilizou o ambiente e confirmou que o preview carrega; a avaliação visual em si é humana, não automatizada (ver `12-design-system-visual-qa.md` para o que já foi validado por auditoria de código).

## Como acessar

```
http://localhost:8005/design_system_v2
```

Alternativa (mesmo destino, sem depender de resolução de nome): `http://127.0.0.1:8005/design_system_v2`

Pré-requisito: ambiente local já iniciado (containers `vedium-*` no ar + `bench start` rodando dentro do container `vedium-frappe`). Ver relatório de saída desta fase para o comando exato.

Não é necessário login — o preview foi liberado temporariamente via `developer_mode` local (ver nota no relatório de saída).

---

## Geral
- [ ] Impressão institucional (parece organização séria, não projeto pessoal)
- [ ] Aparência humana (não robótica/genérica)
- [ ] Premium sem ostentação
- [ ] Parece escola de idiomas, não marketplace/SaaS/infoproduto
- [ ] Identidade Vedium reconhecível (mesmo sem logo visível na tela)
- [ ] Uso equilibrado de azul (`#2E6DA4`) e terracota (`#A12D1C`) — terracota como acento, nunca dominante
- [ ] Espaço em branco/negativo suficiente (não denso demais)

## Tipografia
- [ ] H1 (peso, tamanho, hierarquia clara)
- [ ] H2
- [ ] Corpo de texto (legibilidade, `line-height`)
- [ ] Labels (formulário, badge, breadcrumb)
- [ ] CTAs (peso visual adequado ao botão)
- [ ] Títulos longos (ver seção "Conteúdo extremo" do preview)
- [ ] Textos multilíngues (ver bloco PT/DE/Hebraico e cards de idioma no preview)

## Hero
- [ ] Altura (nem curto demais nem dominando a tela toda)
- [ ] Proporção foto/texto
- [ ] CTA (destaque correto, não competindo com CTA secundário)
- [ ] Espaço negativo
- [ ] Leitura em mobile (título não quebra de forma estranha)

## Cards
Verificar em **LanguageCard**, **CourseCard**, **LevelCard**, **TeacherCard**, **BlogCard**, **PricingCard**:
- [ ] Densidade de informação
- [ ] Raio de borda (consistente, não exagerado)
- [ ] Sombras (sutis, não efeito "app de estoque")
- [ ] Alinhamento (texto, ícone, badge)
- [ ] Comportamento com quantidade de texto variável (ver seção "Conteúdo extremo": grids de 1/2/3/5/6 cards, título curto vs. longo)

## Header (Header v2 — visual apenas, NÃO ativado em produção)
- [ ] Logo
- [ ] Menu (Cursos com mega menu: Inglês / Iorubá / Português para Estrangeiros / Espanhol / Hebraico / Para empresas — Como funciona — Professores — Para empresas — Blog)
- [ ] CTA ("Descubra seu nível" + Entrar)
- [ ] Mega menu (abertura, legibilidade, densidade)
- [ ] Densidade geral da barra
- [ ] Comportamento mobile (menu hambúrguer, acessibilidade de toque)

## Footer (Footer v2 — visual apenas, NÃO ativado em produção)
- [ ] Organização das colunas/links
- [ ] Legibilidade (contraste, tamanho)
- [ ] Volume de conteúdo (nem escasso, nem poluído)
- [ ] Comportamento mobile (empilhamento)

## Fotografia
- [ ] Proporções (4:5 vertical, 4:3 horizontal — ver seção "Conteúdo extremo")
- [ ] Crops
- [ ] `object-position` (enquadramento correto do sujeito)
- [ ] Espaço reservado para texto sobre imagem (quando aplicável)
- [ ] Aparência humana (não stock genérico)
- [ ] **Nenhuma foto de banco de imagens deve ser interpretada como prova visual de professor/aluno/turma real** — a única foto real da Vedium no sistema hoje é a do Prof. Almir Soares da Silva (card de professor); os dois SVGs de referência de proporção na seção "Conteúdo extremo" são deliberadamente abstratos, não fotográficos

## Mobile (validar manualmente no navegador, redimensionando a janela ou via DevTools)
- [ ] 360px
- [ ] 390px
- [ ] 430px
- [ ] 768px

## Desktop
- [ ] 1280px
- [ ] 1440px

---

## Pendência registrada — Tipografia

Poppins e Inter continuam sendo as fontes oficiais aprovadas para produção (decisão da Fase B.1). Os arquivos `.woff2` dessas duas famílias **ainda não existem localmente** neste projeto — não foram baixados automaticamente, não há `@import` remoto do Google Fonts, e o preview **não fica bloqueado**: o fallback atual (`Arial`/`Helvetica Neue`) permanece ativo até as fontes serem auto-hospedadas antes do rollout. **Ao revisar tipografia no navegador agora, o que você vê é Arial no lugar de Poppins/Inter — isso é esperado e não deve ser confundido com a decisão final de marca.** Playfair Display já está auto-hospedada e é a única família com uso editorial/seletivo (hero, citações) — essa você já vê corretamente no navegador.

## Pendência registrada — Fotografia real

Crops definitivos com rosto/mãos ainda dependem dos assets reais da lista P0-LAUNCH (fotografia própria da Vedium), que ainda não foram capturados/entregues. Nenhum crop de banco de imagens (stock) deve ser considerado validação definitiva do sistema de fotografia da Vedium — serve apenas para checar a matemática de proporção/`object-position`, nunca a direção de arte final.
