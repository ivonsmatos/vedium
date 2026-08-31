# 53 — Language Pillar V2: Arquitetura (Fase D)

A arquitetura do Language Pillar V2 (Fase D) consolida 5 landing pages
(Iorubá, Inglês, PLE, Espanhol, Hebraico) num único template reutilizável e
orientado a dados. Nenhuma página pública foi sobrescrita no lançamento desta 
arquitetura; o piloto validou-se na rota `/_language_ioruba_v2` (noindex).

## Componentes

1. **`templates/includes/v2/language_pillar_body.html`**
   O template único. Estrutura rígida de blocos sem duplicação de layout 
   (Hero, Live Class, Percurso/Níveis, Professor, Cultura, Insights, FAQ).
   O conteúdo é completamente governado por `context.pillar`.

2. **`vedium_core/language_pillar_data.py`**
   Controlador de dados. Fornece `build_language_pillar_context()`,
   que funde dados locais (definidos por arquivo via `config_override`)
   com as fontes oficiais e imutáveis: `webmcp_course_data` (WebMCP Pilot, 
   para URLs e níveis), `v2_home_data` (para blogs e insights reais) 
   e `catalog_registry`.

3. **`templates/includes/v2/macros_media.html`**
   Novo componente que isola o tratamento de imagem/vídeo para garantir 
   lazy loading, alt text acessível, e direções de `object-position`.

## Progressão e Regras
Nenhum dado é inventado (ex: preços fictícios, testes de nível que não existem,
avaliações falsas). Toda a arquitetura consome fontes da verdade do Frappe.
O template é locale-aware por design.
