// QA visual: screenshots full-page e por seção de /sobre em 1440px e
// 390px, mais contagem de console errors.
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3000/sobre";
const OUT_DIR = "qa-screenshots";
mkdirSync(OUT_DIR, { recursive: true });

// main > * : 0 header, 1 hero, 2 breadcrumb, 3 quem somos (VediumMethod),
// 4 por que existimos, 5 no que acreditamos (VediumMethod), 6 selo
// visual (divisor entre os 2 VediumMethod navy seguidos), 7 experiencia
// (VediumMethod), 8 conducao pedagogica, 9 rigor cultural, 10 portfolio
// (CourseIndexIntro), 11 nota b2b, 12 principios (VediumMethod),
// 13 cta final, 14 footer.
const GROUPS_1440 = [
  { name: "01-header-hero", startIndex: 0, endIndex: 1, fromTop: true },
  { name: "02-quem-somos", startIndex: 3, endIndex: 3 },
  { name: "03-proposito", startIndex: 4, endIndex: 4 },
  { name: "04-no-que-acreditamos", startIndex: 5, endIndex: 6 },
  { name: "05-experiencia", startIndex: 7, endIndex: 7 },
  { name: "06-professor-tecnologia", startIndex: 8, endIndex: 8 },
  { name: "07-rigor-cultural", startIndex: 9, endIndex: 9 },
  { name: "08-portfolio", startIndex: 10, endIndex: 11 },
  { name: "09-principios", startIndex: 12, endIndex: 12 },
  { name: "10-cta-footer", startIndex: 13, endIndex: 14 },
];

const GROUPS_390 = [
  { name: "01-hero", startIndex: 0, endIndex: 1, fromTop: true },
  { name: "02-experiencia", startIndex: 7, endIndex: 7 },
  { name: "03-portfolio", startIndex: 10, endIndex: 11 },
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

  await page.screenshot({ path: `${OUT_DIR}/about-${viewport.name}-full.png`, fullPage: true });

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
      path: `${OUT_DIR}/about-${viewport.name}-${group.name}.png`,
      fullPage: true,
      clip: { x: 0, y: Math.max(0, top), width: viewport.width, height: Math.max(1, bottom - top) },
    });
  }

  report[viewport.name] = { consoleErrors, sectionCount: rects.length };
  await context.close();
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
