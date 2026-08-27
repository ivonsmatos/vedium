/*
 * VEDIUM WEBMCP -- piloto (Fase C.2 da missao). Modulo ISOLADO, separado de
 * design-system-v2.js (secao 10 da missao). Progressive enhancement puro:
 * o site inteiro (Home, Pathfinder, navegacao humana) funciona 100% sem
 * este arquivo -- nada aqui e um pre-requisito de nenhum link/form/rota.
 *
 * API usada: document.modelContext (API atual, NAO navigator.modelContext,
 * que a missao marca como depreciada). Referencia:
 * https://developer.chrome.com/docs/ai/webmcp/imperative-api
 *
 * As 4 tools deste piloto sao READ-ONLY / navegacao -- nenhuma escreve
 * banco, cria lead, envia mensagem ou inicia pagamento (secao 15 da
 * missao). Fonte de dado: o MESMO data island que o Pathfinder humano usa
 * (ver design-system-v2.js, resolveLearningPath) -- nenhuma tool tem uma
 * segunda base de dados hardcoded.
 *
 * Decisao de contrato (documentada tambem em
 * docs/redesign/51-webmcp-tool-contracts.md): a API real de
 * document.modelContext.registerTool espera que `execute` retorne uma
 * STRING (ou null em navegacao) -- nao um objeto. Por isso toda tool
 * retorna JSON.stringify(...) de uma estrutura pequena e factual (secao 14
 * da missao), nunca HTML/markup do site. Erros (idioma/objetivo invalido,
 * dado indisponivel) tambem retornam uma STRING JSON `{"error": "..."}` em
 * vez de lancar excecao -- a doc oficial nao especifica o contrato de erro
 * (verificado nesta fase), entao optamos pelo formato mais previsivel pro
 * agente consumidor: sempre uma string parseável, nunca um throw que possa
 * virar stack trace exposto.
 */
(function () {
  "use strict";

  // Secao 11 da missao: feature detection obrigatoria, sem excecao em
  // Firefox/Safari/Chrome sem flag/bots/crawlers.
  if (!document.modelContext || typeof document.modelContext.registerTool !== "function") {
    return;
  }

  // Secao 13 da missao: idempotencia -- nunca registrar a mesma tool duas
  // vezes se o script rodar de novo (ex.: navegacao client-side futura).
  if (window.__vediumWebMcpToolsRegistered) {
    return;
  }

  function readCourseData() {
    var el = document.getElementById("vedium-webmcp-course-data");
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return null;
    }
  }

  var DATA = readCourseData();
  // Sem data island (pagina sem WebMCP wired, ou falha de parse): nao
  // registra nenhuma tool. Nao ha "modo degradado" com dado inventado.
  if (!DATA || !DATA.courses) {
    return;
  }

  var LANGUAGE_ENUM = Object.keys(DATA.language_enum_to_display_name || {});
  var GOAL_ENUM = DATA.pathfinder_goals || [];

  function errorResult(message) {
    return JSON.stringify({ error: message });
  }

  function getCourseOrError(language) {
    if (LANGUAGE_ENUM.indexOf(language) === -1) {
      return { error: errorResult("No published course information is available for that language.") };
    }
    var course = DATA.courses[language];
    if (!course) {
      return { error: errorResult("No published course information is available for that language.") };
    }
    return { course: course };
  }

  // ---------------------------------------------------------------------
  // 1. find_course
  // ---------------------------------------------------------------------
  document.modelContext.registerTool({
    name: "find_course",
    title: "Find a Vedium language course",
    description:
      "Find a Vedium language course by language. Returns the real, published " +
      "course page for that language -- no price, no class schedule, no " +
      "teacher assignment (those are not published data).",
    inputSchema: {
      type: "object",
      properties: {
        language: {
          type: "string",
          enum: LANGUAGE_ENUM,
          description: "The language the learner wants to study.",
        },
      },
      required: ["language"],
    },
    annotations: { readOnlyHint: true },
    execute: async function (input) {
      var input_ = input || {};
      var resolved = getCourseOrError(input_.language);
      if (resolved.error) return resolved.error;
      var course = resolved.course;
      return JSON.stringify({
        language: course.language,
        course_name: course.course_name,
        level_summary: course.level_summary,
        url: course.url,
        next_step: course.next_step.text,
      });
    },
  });

  // ---------------------------------------------------------------------
  // 2. recommend_learning_path (agentic version of the Pathfinder)
  // ---------------------------------------------------------------------
  document.modelContext.registerTool({
    name: "recommend_learning_path",
    title: "Recommend a Vedium learning path",
    description:
      "Recommend a Vedium course and next step from a language and a goal. " +
      "Uses the exact same resolution logic and data as the on-page " +
      "Pathfinder -- never a second, independent set of rules.",
    inputSchema: {
      type: "object",
      properties: {
        language: {
          type: "string",
          enum: LANGUAGE_ENUM,
          description: "The language the learner wants to study.",
        },
        goal: {
          type: "string",
          enum: GOAL_ENUM,
          description: "The learner's main goal, using Vedium's existing Pathfinder goal taxonomy.",
        },
      },
      required: ["language", "goal"],
    },
    annotations: { readOnlyHint: true },
    execute: async function (input) {
      var input_ = input || {};
      var resolved = getCourseOrError(input_.language);
      if (resolved.error) return resolved.error;
      if (GOAL_ENUM.indexOf(input_.goal) === -1) {
        return errorResult("No published learning path is available for that goal.");
      }
      var course = resolved.course;
      var displayName = DATA.language_enum_to_display_name[input_.language];
      var destination =
        (window.VediumPathfinder && window.VediumPathfinder.resolve(displayName, input_.goal)) || course.url;
      return JSON.stringify({
        language: course.language,
        goal: input_.goal,
        course_recommended: course.course_name,
        url: destination,
        next_step: course.next_step.text,
        next_step_url: course.next_step.kind === "level_test" ? course.next_step.url : null,
        explanation:
          "Curso e percurso indicados a partir do idioma e do objetivo informados; " +
          "não substitui uma avaliação de nível.",
      });
    },
  });

  // ---------------------------------------------------------------------
  // 3. get_course_information
  // ---------------------------------------------------------------------
  document.modelContext.registerTool({
    name: "get_course_information",
    title: "Get Vedium course information",
    description:
      "Get published, factual information about a Vedium language course: summary, " +
      "delivery mode, teacher profile and progression. Never includes price, " +
      "guaranteed outcomes or timelines.",
    inputSchema: {
      type: "object",
      properties: {
        language: {
          type: "string",
          enum: LANGUAGE_ENUM,
          description: "The language of the course.",
        },
      },
      required: ["language"],
    },
    annotations: { readOnlyHint: true },
    execute: async function (input) {
      var input_ = input || {};
      var resolved = getCourseOrError(input_.language);
      if (resolved.error) return resolved.error;
      var course = resolved.course;
      return JSON.stringify({
        course_name: course.course_name,
        language: course.language,
        summary: course.summary,
        level_summary: course.level_summary,
        delivery_mode: course.delivery_mode,
        teacher_profile: course.teacher_profile,
        progression: course.progression,
        url: course.url,
      });
    },
  });

  // ---------------------------------------------------------------------
  // 4. get_levels
  // ---------------------------------------------------------------------
  document.modelContext.registerTool({
    name: "get_levels",
    title: "Get Vedium course levels",
    description:
      "Get the real levels or tracks published for a Vedium language course. Not " +
      "every language uses a sequential CEFR-style progression -- check " +
      "is_sequential before assuming order implies prerequisite.",
    inputSchema: {
      type: "object",
      properties: {
        language: {
          type: "string",
          enum: LANGUAGE_ENUM,
          description: "The language to list levels/tracks for.",
        },
      },
      required: ["language"],
    },
    annotations: { readOnlyHint: true },
    execute: async function (input) {
      var input_ = input || {};
      var resolved = getCourseOrError(input_.language);
      if (resolved.error) return resolved.error;
      var course = resolved.course;
      return JSON.stringify({
        language: course.language,
        is_sequential: course.levels_are_sequential,
        levels: course.levels.map(function (level) {
          return { label: level.label, url: level.url };
        }),
      });
    },
  });

  window.__vediumWebMcpToolsRegistered = true;
})();
