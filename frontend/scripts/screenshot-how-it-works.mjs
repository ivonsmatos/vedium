// QA visual: screenshots full-page e por seção de /como-funciona em
// 1440px e 390px, mais contagem de console errors.
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3000/como-funciona";
const OUT_DIR = "qa-screenshots";
mkdirSync(OUT_DIR, { recursive: true });

// main > * : 0 header, 1 hero, 2 breadcrumb, 3 visao geral (ProgressionFlow),
// 4 ponto de partida (VediumMethod), 5 percurso (VediumMethod + nota
// hebraico), 6 aulas ao vivo, 7 professor/pratica (VediumMethod),
// 8 idioma+contexto, 9 acompanhamento (inclui proximo nivel, mesma secao),
// 10 formatos (VediumMethod), 11 cursos, 12 faq, 13 cta final, 14 footer.
const GROUPS_1440 = [
  { name: "01-header-hero", startIndex: 0, endIndex: 1, fromTop: true },
  { name: "02-visao-geral", startIndex: 3, endIndex: 3 },
  { name: "03-ponto-de-partida-percurso", startIndex: 4, endIndex: 5 },
  { name: "04-aulas-ao-vivo", startIndex: 6, endIndex: 6 },
  { name: "05-professor-pratica", startIndex: 7, endIndex: 7 },
  { name: "06-idioma-e-contexto", startIndex: 8, endIndex: 8 },
  { name: "07-evolucao", startIndex: 9, endIndex: 9 },
  { name: "08-formatos", startIndex: 10, endIndex: 10 },
  { name: "09-cursos", startIndex: 11, endIndex: 11 },
  { name: "10-faq", startIndex: 12, endIndex: 12 },
  { name: "11-cta-footer", startIndex: 13, endIndex: 14 },
];

const GROUPS_390 = [
  { name: "01-hero", startIndex: 0, endIndex: 1, fromTop: true },
  { name: "02-processo", startIndex: 3, endIndex: 3 },
  { name: "03-aula-ao-vivo", startIndex: 6, endIndex: 6 },
  { name: "04-cta-footer", startIndex: 13, endIndex: 14 },
];

const VIEWPORTS = [
  { name: "1440", width: 1440, height: 900, groups: GROUPS_1440 },
  { name: "390", width: 390, height: 844, groups: GROUPS_390 },
];

const browser = await chromium.launch();
const report = {};

for (const viewport of VIEWPORTS) {
  const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });
  const page = await context.newPage();

  const consoleErrors = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("pageerror", (err) => consoleErrors.push(String(err)));

  await page.goto(URL, { waitUntil: "networkidle" });
  await page.waitForTimeout(300);

  await page.evaluate(async () => {
    const step = 400;
    const delay = 50;
    let scrolled = 0;
    const height = document.body.scrollHeight;
    while (scrolled < height) {
      window.scrollBy(0, step);
      scrolled += step;
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(300);

  await page.screenshot({ path: `${OUT_DIR}/how-it-works-${viewport.name}-full.png`, fullPage: true });

  const rects = await page.evaluate(() => {
    const children = Array.from(document.querySelector("main").children);
    return children.map((el) => {
      const r = el.getBoundingClientRect();
      return { top: r.top + window.scrollY, bottom: r.bottom + window.scrollY };
    });
  });

  for (const group of viewport.groups) {
    const top = group.fromTop ? 0 : rects[group.startIndex].top;
    const bottom = rects[group.endIndex].bottom;
    await page.screenshot({
      path: `${OUT_DIR}/how-it-works-${viewport.name}-${group.name}.png`,
      fullPage: true,
      clip: { x: 0, y: Math.max(0, top), width: viewport.width, height: Math.max(1, bottom - top) },
    });
  }

  report[viewport.name] = { consoleErrors, sectionCount: rects.length };
  await context.close();
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
