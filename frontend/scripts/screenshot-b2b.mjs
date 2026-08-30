// QA visual: screenshots full-page e por seção de /empresas em 1440px e
// 390px, mais contagem de console errors.
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3000/empresas";
const OUT_DIR = "qa-screenshots";
mkdirSync(OUT_DIR, { recursive: true });

// main > * : 0 header, 1 hero, 2 breadcrumb, 3 challenge (VediumMethod),
// 4 diagnosis section, 5 solution section, 6 howItWorks section,
// 7 management section, 8 formats (VediumMethod), 9 implementation
// section, 10 whyVedium (VediumMethod), 11 diagnosisCta section,
// 12 faq section, 13 final cta section, 14 footer.
const GROUPS_1440 = [
  { name: "01-header-hero", startIndex: 0, endIndex: 2, fromTop: true },
  { name: "02-desafio", startIndex: 3, endIndex: 3 },
  { name: "03-diagnostico", startIndex: 4, endIndex: 4 },
  { name: "04-solucao", startIndex: 5, endIndex: 5 },
  { name: "05-como-funciona", startIndex: 6, endIndex: 6 },
  { name: "06-gestao-acompanhamento", startIndex: 7, endIndex: 7 },
  { name: "07-formatos", startIndex: 8, endIndex: 8 },
  { name: "08-implementacao", startIndex: 9, endIndex: 9 },
  { name: "09-por-que-vedium", startIndex: 10, endIndex: 10 },
  { name: "10-diagnostico-cta", startIndex: 11, endIndex: 11 },
  { name: "11-faq", startIndex: 12, endIndex: 12 },
  { name: "12-cta-final-footer", startIndex: 13, endIndex: 14 },
];

const GROUPS_390 = [
  { name: "01-hero", startIndex: 0, endIndex: 1, fromTop: true },
  { name: "02-diagnostico", startIndex: 4, endIndex: 4 },
  { name: "03-como-funciona", startIndex: 6, endIndex: 6 },
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

  await page.screenshot({ path: `${OUT_DIR}/b2b-${viewport.name}-full.png`, fullPage: true });

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
      path: `${OUT_DIR}/b2b-${viewport.name}-${group.name}.png`,
      fullPage: true,
      clip: { x: 0, y: Math.max(0, top), width: viewport.width, height: Math.max(1, bottom - top) },
    });
  }

  report[viewport.name] = { consoleErrors, sectionCount: rects.length };
  await context.close();
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
