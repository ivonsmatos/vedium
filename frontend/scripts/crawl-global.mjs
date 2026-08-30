// Crawler global local (Fase G.1, secao 55). Roda contra o dev server
// (http://localhost:3000), le o HTML renderizado no servidor (SSR) de
// cada rota conhecida do Next e reporta: status, canonical, H1,
// title/description (+ duplicatas), JSON-LD (parseavel + sem
// localhost), links internos quebrados e imagens quebradas.
//
// Links para vediums.com (producao real) NAO sao tratados como
// quebrados -- o site ainda nao foi cortado pra ca, entao apontar pra
// producao real e o comportamento correto hoje (missao secao 20 pede
// pra achar host errado tipo "vedium.com"/localhost hardcoded, nao
// links legitimos pra producao).

const BASE = "http://localhost:3000";

const ROUTES = [
  "/",
  "/curso-de-ioruba-online",
  "/curso-de-ingles-online",
  "/portugues-para-estrangeiros",
  "/curso-de-espanhol-online",
  "/curso-de-hebraico-online",
  "/empresas",
  "/como-funciona",
  "/sobre",
  "/contato",
  "/privacidade",
  "/termos",
  "/cancelamento-reembolso",
  "/blog",
  "/blog/ingles/aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-vale-a-pena",
];

const KNOWN_LOCAL_PATHS = new Set(ROUTES);
// Aceitos mesmo sem existir como rota Next ainda: link real pra artigo
// irmao do cluster, ainda nao migrado (ver docs 24-27), e ancoras.
const KNOWN_EXCEPTIONS = new Set(["/blog/ingles/como-estudar-phrasal-verbs-sem-decorar-listas-infinitas"]);

function extractAll(html, regex) {
  return [...html.matchAll(regex)].map((m) => m[1]);
}

async function checkImage(src, cache) {
  if (cache.has(src)) return cache.get(src);
  try {
    const url = src.startsWith("http") ? src : `${BASE}${src}`;
    const res = await fetch(url, { method: "GET" });
    const ok = res.ok;
    cache.set(src, ok);
    return ok;
  } catch {
    cache.set(src, false);
    return false;
  }
}

async function main() {
  const report = {
    routes: [],
    canonicalErrors: [],
    h1Errors: [],
    titleErrors: [],
    descriptionErrors: [],
    schemaErrors: [],
    brokenInternalLinks: [],
    brokenImages: [],
    oldWhatsappRefs: [],
    oldInstagramRefs: [],
    wrongDomainRefs: [],
  };

  const titleMap = new Map();
  const descriptionMap = new Map();
  const imageCache = new Map();

  for (const route of ROUTES) {
    const url = `${BASE}${route}`;
    let res;
    try {
      res = await fetch(url);
    } catch (e) {
      report.routes.push({ route, status: "ERR", error: String(e) });
      continue;
    }
    const html = await res.text();
    const status = res.status;

    const titleMatch = html.match(/<title>(.*?)<\/title>/s);
    const title = titleMatch ? titleMatch[1].trim() : null;
    const descMatch = html.match(/<meta name="description" content="(.*?)"/s);
    const description = descMatch ? descMatch[1] : null;
    const canonicalMatch = html.match(/<link rel="canonical" href="(.*?)"/);
    const canonical = canonicalMatch ? canonicalMatch[1] : null;
    const h1Count = (html.match(/<h1[\s>]/g) || []).length;

    // --- Title/description checks ---
    if (!title) report.titleErrors.push({ route, issue: "MISSING_TITLE" });
    else if (title.length > 65) report.titleErrors.push({ route, issue: `TOO_LONG (${title.length} chars)`, title });
    if (!description) report.descriptionErrors.push({ route, issue: "MISSING_DESCRIPTION" });

    if (title) {
      if (titleMap.has(title)) report.titleErrors.push({ route, issue: `DUPLICATE_TITLE with ${titleMap.get(title)}`, title });
      else titleMap.set(title, route);
    }
    if (description) {
      if (descriptionMap.has(description)) report.descriptionErrors.push({ route, issue: `DUPLICATE_DESCRIPTION with ${descriptionMap.get(description)}` });
      else descriptionMap.set(description, route);
    }

    // --- Canonical checks ---
    if (!canonical) {
      report.canonicalErrors.push({ route, issue: "MISSING_CANONICAL" });
    } else {
      if (!canonical.startsWith("https://vediums.com")) report.canonicalErrors.push({ route, issue: `WRONG_HOST: ${canonical}` });
      if (canonical.includes("localhost") || canonical.includes("app.vediums.com")) report.canonicalErrors.push({ route, issue: `BAD_HOST: ${canonical}` });
      if (canonical.includes("?")) report.canonicalErrors.push({ route, issue: `QUERY_STRING: ${canonical}` });
    }

    // --- H1 checks ---
    if (h1Count === 0) report.h1Errors.push({ route, issue: "ZERO_H1" });
    if (h1Count > 1) report.h1Errors.push({ route, issue: `MULTIPLE_H1 (${h1Count})` });

    // --- JSON-LD checks ---
    const jsonLdBlocks = extractAll(html, /<script type="application\/ld\+json">(.*?)<\/script>/gs);
    for (const block of jsonLdBlocks) {
      try {
        const parsed = JSON.parse(block);
        const str = JSON.stringify(parsed);
        if (str.includes("localhost") || str.includes("app.vediums.com")) {
          report.schemaErrors.push({ route, issue: "SCHEMA_HAS_BAD_HOST", type: parsed["@type"] });
        }
      } catch {
        report.schemaErrors.push({ route, issue: "INVALID_JSON" });
      }
    }

    // --- Domain/WhatsApp/Instagram reference checks ---
    if (/vedium\.com(?!\.br)(?!s)/i.test(html.replace(/vediums\.com/g, ""))) {
      // (checagem grosseira: procura "vedium.com" que NAO seja "vediums.com" -- ja removido acima)
    }
    if (html.includes("127.0.0.1") || /localhost:(?!3000)/.test(html)) {
      report.wrongDomainRefs.push({ route, issue: "LOCALHOST_OR_WRONG_PORT_REF" });
    }
    const waMatches = extractAll(html, /wa\.me\/(\d+)/g);
    for (const num of waMatches) {
      if (num !== "5511911293075") report.oldWhatsappRefs.push({ route, number: num });
    }
    if (/@vedium\.idiomas|@vediumidiomas/i.test(html)) {
      report.oldInstagramRefs.push({ route });
    }

    // --- Internal links ---
    const hrefs = extractAll(html, /href="(\/[^"#?]*)"/g);
    for (const href of new Set(hrefs)) {
      if (href.startsWith("/api/") || href.startsWith("/_next/") || href.startsWith("/assets/")) continue;
      if (KNOWN_LOCAL_PATHS.has(href) || KNOWN_EXCEPTIONS.has(href)) continue;
      report.brokenInternalLinks.push({ route, href });
    }

    // --- Images ---
    const imgSrcs = extractAll(html, /<img[^>]+src="([^"]+)"/g);
    for (const src of new Set(imgSrcs)) {
      const ok = await checkImage(src, imageCache);
      if (!ok) report.brokenImages.push({ route, src });
    }

    report.routes.push({ route, status, title, hasCanonical: Boolean(canonical), h1Count, jsonLdCount: jsonLdBlocks.length });
  }

  console.log(JSON.stringify(report, null, 2));
}

main();
