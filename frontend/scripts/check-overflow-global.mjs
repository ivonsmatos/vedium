// Varredura global de overflow horizontal (Fase G.1, secao 30) -- todas
// as rotas conhecidas x 320/375/390/768/1024/1440.
import { chromium } from "playwright";

const BASE = "http://localhost:3000";
const ROUTES = [
  "/", "/curso-de-ioruba-online", "/curso-de-ingles-online", "/portugues-para-estrangeiros",
  "/curso-de-espanhol-online", "/curso-de-hebraico-online", "/empresas", "/como-funciona",
  "/sobre", "/contato", "/privacidade", "/termos", "/cancelamento-reembolso", "/blog",
  "/blog/ingles/aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-vale-a-pena",
];
const WIDTHS = [320, 375, 390, 768, 1024, 1440];

const browser = await chromium.launch();
const context = await browser.newContext();
const page = await context.newPage();
const results = [];

for (const route of ROUTES) {
  for (const width of WIDTHS) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto(`${BASE}${route}`, { waitUntil: "networkidle" });
    const { scrollWidth, clientWidth } = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    const overflow = scrollWidth - clientWidth;
    if (overflow > 1) {
      results.push({ route, width, scrollWidth, clientWidth, overflow });
    }
  }
}

await browser.close();
console.log(JSON.stringify({ totalChecks: ROUTES.length * WIDTHS.length, overflowsFound: results.length, results }, null, 2));
