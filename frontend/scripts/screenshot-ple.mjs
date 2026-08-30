// QA visual: screenshots full-page e por seção de /portugues-para-estrangeiros
// em 1440px e 390px, mais contagem de console errors.
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3000/portugues-para-estrangeiros";
const OUT_DIR = "qa-screenshots";
mkdirSync(OUT_DIR, { recursive: true });

// main > * : 0 header, 1 hero, 2 breadcrumb, 3 studyPillars (VediumMethod),
// 4 live class section, 5 levels section, 6 culture section, 7 applications
// (VediumMethod), 8 faq section, 9 cta section, 10 footer. Sem seção de
// Professor nem Conhecimento Vedium (ver portuguese-for-foreigners.ts).
const GROUPS_1440 = [
  { name: "01-hero", startIndex: 0, endIndex: 2, fromTop: true },
  { name: "02-vida-real", startIndex: 3, endIndex: 3 },
  { name: "03-live", startIndex: 4, endIndex: 4 },
  { name: "04-niveis", startIndex: 5, endIndex: 5 },
  { name: "05-idioma-contexto", startIndex: 6, endIndex: 6 },
  { name: "06-aplicacoes", startIndex: 7, endIndex: 7 },
  { name: "07-faq", startIndex: 8, endIndex: 8 },
  { name: "08-cta-footer", startIndex: 9, endIndex: 10 },
];

const GROUPS_390 = [
  { name: "01-hero", startIndex: 0, endIndex: 1, fromTop: true },
  { name: "02-niveis", startIndex: 5, endIndex: 5 },
  { name: "03-cta-footer", startIndex: 9, endIndex: 10 },
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

  await page.screenshot({ path: `${OUT_DIR}/ple-${viewport.name}-full.png`, fullPage: true });

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
      path: `${OUT_DIR}/ple-${viewport.name}-${group.name}.png`,
      fullPage: true,
      clip: { x: 0, y: Math.max(0, top), width: viewport.width, height: Math.max(1, bottom - top) },
    });
  }

  report[viewport.name] = { consoleErrors, sectionCount: rects.length };
  await context.close();
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
