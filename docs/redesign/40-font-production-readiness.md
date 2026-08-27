# 40 — Prontidão de fontes de produção (Fase C.1.1, Parte D)

## 1. Gate existente

`V2_FONT_ASSETS_REQUIRED_BEFORE_ROLLOUT` permanece aberto (registrado desde a Fase C.1, `28-home-v2-seo-contract.md`).

## 2. Lista exata (extraída do CSS real, não assumida)

| Font family | Peso | Estilo | Onde é usada |
|---|---|---|---|
| Poppins | 600 (SemiBold) | normal | Headings, labels, eyebrows em todo o sistema V2 |
| Poppins | 700 (Bold) | normal | Headings de maior destaque, botões |
| Inter | 400 (Regular) | normal | Parágrafos, listas, texto de apoio — nenhum `font-weight` explícito diferente de 400 encontrado pro corpo, nenhum `<strong>/<b>` no HTML da Home V2 |

3 arquivos `.woff2` necessários: `Poppins-SemiBold.woff2`, `Poppins-Bold.woff2`, `Inter-Regular.woff2`. Nenhum peso adicional (500, italic) é referenciado em `public/css/v2/*.css` — confirmado por grep de `font-weight:` e `font-style:` em toda a pasta, não assumido de memória de fases anteriores.

## 3. Licenciamento — verificação, não download

Poppins e Inter são ambas fontes do Google Fonts, distribuídas sob a **SIL Open Font License 1.1** — licença pública, permissiva, que autoriza uso comercial, auto-hospedagem e embedding em produtos sem royalties nem atribuição obrigatória no produto final. Esta é uma informação de licenciamento público e verificável (a licença é publicada pelo próprio Google Fonts e pelas fundições de origem), não uma comprovação que precise de evidência interna do projeto — diferente da mídia Envato (Parte A), aqui não há ambiguidade de titularidade a resolver.

**Nenhum arquivo foi baixado nesta fase** (instrução explícita da missão, seção 19: "não baixar automaticamente"). O que falta é puramente operacional: alguém com acesso ao Google Fonts (ou ao repositório oficial das fontes) baixar os 3 arquivos `.woff2` nos pesos exatos acima e colocá-los em `public/vedium_assets/fonts/` (mesmo padrão já usado por Playfair Display, única fonte hoje auto-hospedada no projeto).

## 4. Fallback atual — funcional, não é o estado final

Enquanto os 3 arquivos não existem, o CSS já cai num stack de sistema (Arial/Helvetica Neue) — confirmado visualmente em todas as fases anteriores, sem elemento quebrado ou ilegível.

**Impacto de CLS**: baixo. O fallback de sistema tem métricas de largura de caractere próximas o bastante de Poppins/Inter (ambas são fontes geométricas/humanistas sem contadores extremos) para não empurrar layout de forma perceptível nos testes visuais já feitos (B.6B–C.1). Nenhuma media reflow abrupta foi observada nos screenshots capturados em nenhuma fase.

## 5. Classificação

**NON-BLOCKER para o rollout.** Justificativa: (a) o fallback é funcional e visualmente aceitável, sem quebra de layout ou CLS mensurável; (b) a licença já é conhecida e sem risco (SIL OFL, uso comercial livre) — não há decisão jurídica pendente, só uma tarefa operacional de baixar 3 arquivos; (c) a ausência da fonte final não compromete conversão, SEO ou acessibilidade. Recomendado resolver antes do lançamento público por consistência de marca, mas não é motivo para segurar o cutover técnico da Home.

## 6. Gate de rollout

`FONTS` = **PASS (non-blocking)** — mantendo o registro de que os 3 arquivos ainda precisam ser adicionados antes do lançamento final para fechar a identidade tipográfica pretendida.
