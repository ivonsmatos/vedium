# 54 — Language Pillar: Content Contract (Fase D)

Este documento define o esquema de dados esperado por `language_pillar_body.html` 
através da chave `context.pillar`. Todo idioma deve preencher este contrato.

## Schema de `LanguagePillarConfig`

- **`language_key`**: string (ex: "yoruba", "english"). 
- **`display_name`**: string (ex: "Iorubá").
- **`eyebrow`**: string, para o Hero (ex: "CURSO DE IORUBÁ ONLINE").
- **`hero_headline`**: string, H1 principal focado no idioma.
- **`hero_support`**: string, texto auxiliar no hero.
- **`hero_media`**: dict com `src`, `alt`, `is_video`, `poster`, `caption`.
- **`primary_cta`** e **`secondary_cta`**: dicts com `text` e `href`.
- **`persona_title`** e **`persona_bullets`**: lista de strings transformando
  o perfil da persona em necessidades diretas ("Para quem quer: ...").
- **`live_class`**: dict (title, description) explicando as aulas ao vivo.
- **`culture`**: dict (title, description) ligando a língua ao contexto.
- **`teacher`**: (opcional) dict com dados validados do professor.
- **`faqs`**: lista de dicts (question, answer).
- **`levels`** e **`insights_*`**: Gerados automaticamente pelo controller
  através das bibliotecas do WebMCP e Home V2.

## Limitações
A interface não aceita placeholders visuais; se a chave for `None` ou `[]`,
a seção não será renderizada. Todo texto deve passar pela avaliação de 
compliance (Tone of Voice).
