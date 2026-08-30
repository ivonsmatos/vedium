import { createHash } from "node:crypto";
import { chromium } from "playwright";

const localOrigin = process.env.LEGAL_LOCAL_ORIGIN || "http://localhost:3104";
const productionOrigin = process.env.LEGAL_PRODUCTION_ORIGIN || "https://vediums.com";
const routes = ["privacidade", "termos", "cancelamento-reembolso"];
const viewports = [
  { name: "mobile", width: 390, height: 844 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1440, height: 1000 },
];

function normalize(value) {
  return value.normalize("NFC").replace(/\s+/g, " ").trim();
}

function hash(value) {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

async function metadataFor(url) {
  const response = await fetch(url, { redirect: "follow" });
  const html = await response.text();
  const pick = (regexp) => html.match(regexp)?.[1]?.trim() ?? null;
  return {
    status: response.status,
    finalUrl: response.url,
    title: pick(/<title[^>]*>([\s\S]*?)<\/title>/i),
    description: pick(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)/i),
    canonical: pick(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']*)/i),
    robots: pick(/<meta[^>]+name=["']robots["'][^>]+content=["']([^"']*)/i),
    ssrMarkers: {
      sourceContent: html.includes("data-legal-source-content"),
      finalSection: /13\. Atualizações|14\. Alterações|10\. Como solicitar cancelamento ou reembolso/.test(html),
      legalStamp: html.includes("Base legal:"),
    },
  };
}

async function validateLink(href) {
  if (href.startsWith("mailto:")) return { href, kind: "mailto", status: "VALID", httpStatus: null, finalUrl: href, localStatus: "VALID" };
  const url = new URL(href, productionOrigin).toString();
  const localUrl = new URL(href, localOrigin).toString();
  try {
    const localResponse = await fetch(localUrl, { redirect: "follow", signal: AbortSignal.timeout(20_000) });
    const initial = await fetch(url, { redirect: "manual", signal: AbortSignal.timeout(20_000) });
    if (initial.status >= 300 && initial.status < 400) {
      const followed = await fetch(url, { redirect: "follow", signal: AbortSignal.timeout(20_000) });
      return { href, kind: "http", status: followed.ok ? "REDIRECTED" : "BROKEN", httpStatus: followed.status, finalUrl: followed.url, localStatus: localResponse.ok ? "VALID" : "BROKEN", localHttpStatus: localResponse.status };
    }
    return { href, kind: "http", status: initial.ok ? "VALID" : "BROKEN", httpStatus: initial.status, finalUrl: initial.url, localStatus: localResponse.ok ? "VALID" : "BROKEN", localHttpStatus: localResponse.status };
  } catch (error) {
    return { href, kind: "http", status: "BROKEN", httpStatus: null, finalUrl: url, localStatus: "BROKEN", error: error instanceof Error ? error.message : String(error) };
  }
}

const browser = await chromium.launch({ headless: true });
const report = { localOrigin, productionOrigin, routes: {}, links: [], frozenPages: {} };
const allDocumentLinks = new Set();

for (const route of routes) {
  const parityPage = await browser.newPage();
  await parityPage.goto(`${productionOrigin}/${route}`, { waitUntil: "domcontentloaded" });
  const source = normalize(await parityPage.locator(".vd-legal .container").innerText());
  const productionLinks = await parityPage.locator(".vd-legal .container a").evaluateAll((anchors) => anchors.map((anchor) => anchor.getAttribute("href")).filter(Boolean));
  productionLinks.forEach((href) => allDocumentLinks.add(href));

  await parityPage.goto(`${localOrigin}/${route}`, { waitUntil: "domcontentloaded" });
  const target = normalize(await parityPage.locator("[data-legal-source-content]").evaluate((node) => {
    const clone = node.cloneNode(true);
    clone.querySelectorAll("[data-parity-ignore]").forEach((ignored) => ignored.remove());
    clone.style.position = "absolute";
    clone.style.left = "-100000px";
    clone.style.width = "800px";
    document.body.appendChild(clone);
    const text = clone.innerText || "";
    clone.remove();
    return text;
  }));
  const headingAudit = await parityPage.locator("article[data-legal-document]").evaluate((article) => ({
    h1Count: article.querySelectorAll("h1").length,
    h2Count: article.querySelectorAll("h2").length,
    h3Count: article.querySelectorAll("h3").length,
    emptyLinks: [...article.querySelectorAll("a")].filter((link) => !(link.textContent || "").trim()).length,
    tables: [...article.querySelectorAll("table")].map((table) => ({
      headers: table.querySelectorAll("th[scope='col']").length,
      regionLabel: table.parentElement?.getAttribute("aria-label") || null,
    })),
  }));
  await parityPage.close();

  const viewportResults = [];
  for (const viewport of viewports) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on("console", (message) => { if (message.type() === "error") errors.push(`console: ${message.text()}`); });
    page.on("pageerror", (error) => errors.push(`page: ${error.message}`));
    const response = await page.goto(`${localOrigin}/${route}`, { waitUntil: "domcontentloaded" });
    const layout = await page.evaluate(() => ({
      viewportWidth: window.innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
      tablesOutsideViewport: [...document.querySelectorAll("table")].filter((table) => {
        const rect = table.parentElement?.getBoundingClientRect();
        return rect ? rect.left < 0 || rect.right > window.innerWidth : false;
      }).length,
      longLinksOutsideViewport: [...document.querySelectorAll("article a")].filter((link) => {
        const rect = link.getBoundingClientRect();
        return rect.left < 0 || rect.right > window.innerWidth;
      }).length,
    }));
    viewportResults.push({ viewport, httpStatus: response?.status() ?? null, layout, errors });
    await page.close();
  }

  report.routes[route] = {
    metadata: await metadataFor(`${localOrigin}/${route}`),
    sourceWordCount: source.split(/\s+/).length,
    targetWordCount: target.split(/\s+/).length,
    sourceHash: hash(source),
    targetHash: hash(target),
    parity: source === target ? "PASS" : "FAIL",
    firstDifference: source === target ? null : (() => {
      let index = 0;
      while (index < source.length && source[index] === target[index]) index += 1;
      return { index, source: source.slice(Math.max(0, index - 80), index + 160), target: target.slice(Math.max(0, index - 80), index + 160) };
    })(),
    headingAudit,
    viewports: viewportResults,
  };
}

report.links = await Promise.all([...allDocumentLinks].sort().map(validateLink));

for (const route of ["/", "/curso-de-ingles-online", "/curso-de-ioruba-online", "/portugues-para-estrangeiros", "/curso-de-espanhol-online", "/curso-de-hebraico-online", "/empresas", "/como-funciona", "/sobre", "/contato"]) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const errors = [];
  page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); });
  page.on("pageerror", (error) => errors.push(error.message));
  const response = await page.goto(`${localOrigin}${route}`, { waitUntil: "domcontentloaded" });
  report.frozenPages[route] = { status: response?.status() ?? null, h1Count: await page.locator("h1").count(), errors };
  await page.close();
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
