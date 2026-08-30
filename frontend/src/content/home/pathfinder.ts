export const PATHFINDER_EYEBROW = "Encontre seu ponto de partida";
export const PATHFINDER_TITLE = "Um curso para o seu idioma e o seu objetivo.";
export const PATHFINDER_LEAD =
  "Responda a duas perguntas e veja qual percurso pode fazer mais sentido para você.";
export const PATHFINDER_STEPS = ["Idioma", "Objetivo"];
export const PATHFINDER_LANGUAGE_QUESTION = "Qual idioma você quer aprender?";
export const PATHFINDER_LANGUAGES = ["Inglês", "Iorubá", "Português para Estrangeiros", "Espanhol", "Hebraico"];
export const PATHFINDER_OBJECTIVE_QUESTION = "Qual é o seu principal objetivo?";
export const PATHFINDER_OBJECTIVES = [
  "Trabalho e carreira",
  "Comunicação cotidiana",
  "Viagens",
  "Estudos e cultura",
  "Viver e trabalhar no Brasil",
];
export const PATHFINDER_CTA = { text: "Encontrar meu caminho", href: "/teste-de-nivel" };

/**
 * Idioma + objetivo -> URL real mais específica. Combinação sem página
 * objetivo-específica cai na página-pilar do idioma (`_pillar`). Fonte:
 * vedium_core/vedium_core/v2_home_data.py (PATHFINDER_MATRIX) -- mesmas
 * URLs, todas validadas HTTP 200 na fonte original.
 */
export const PATHFINDER_MATRIX: Record<string, Record<string, string>> = {
  Inglês: {
    _pillar: "/curso-de-ingles-online",
    "Trabalho e carreira": "/ingles-executivo",
    "Comunicação cotidiana": "/curso-de-ingles-online",
    Viagens: "/ingles-para-viagens",
    "Estudos e cultura": "/curso-de-ingles-online",
    "Viver e trabalhar no Brasil": "/curso-de-ingles-online",
  },
  Iorubá: {
    _pillar: "/curso-de-ioruba-online",
    "Trabalho e carreira": "/curso-de-ioruba-online",
    "Comunicação cotidiana": "/curso-de-ioruba-online",
    Viagens: "/curso-de-ioruba-online",
    "Estudos e cultura": "/ioruba-cultura-e-ancestralidade",
    "Viver e trabalhar no Brasil": "/curso-de-ioruba-online",
  },
  "Português para Estrangeiros": {
    _pillar: "/portugues-para-estrangeiros",
    "Trabalho e carreira": "/portugues-para-executivos",
    "Comunicação cotidiana": "/portugues-para-estrangeiros",
    Viagens: "/portugues-para-estrangeiros",
    "Estudos e cultura": "/preparatorio-celpe-bras",
    "Viver e trabalhar no Brasil": "/portugues-para-estrangeiros",
  },
  Espanhol: {
    _pillar: "/curso-de-espanhol-online",
    "Trabalho e carreira": "/curso-de-espanhol-online",
    "Comunicação cotidiana": "/curso-de-espanhol-online",
    Viagens: "/curso-de-espanhol-online",
    "Estudos e cultura": "/curso-de-espanhol-online",
    "Viver e trabalhar no Brasil": "/curso-de-espanhol-online",
  },
  Hebraico: {
    _pillar: "/curso-de-hebraico-online",
    "Trabalho e carreira": "/curso-de-hebraico-online",
    "Comunicação cotidiana": "/curso-de-hebraico-online",
    Viagens: "/curso-de-hebraico-online",
    "Estudos e cultura": "/curso-de-hebraico-online",
    "Viver e trabalhar no Brasil": "/curso-de-hebraico-online",
  },
};
