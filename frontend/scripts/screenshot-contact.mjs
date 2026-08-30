// QA visual: screenshots full-page e por seção de /contato em 1440px e
// 390px, mais contagem de console errors.
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3000/contato";
const OUT_DIR = "qa-screenshots";
mkdirSync(OUT_DIR, { recursive: true });

// main > * : 0 utility bar, 1 header, 2 intro/hero (brand), 3 breadcrumb,
// 4 escolha do assunto, 5 whatsapp/contato direto (warm), 6 formulario,
// 7 b2b (brand), 8 proximos passos (alt), 9 faq, 10 footer.
// (Header sem overlay nesta pagina -- ver page.tsx -- por isso sao 2
// filhos em vez de 1 v2-header-overlay-wrap.)
const GROUPS_1440 = [
  { name: "01-header-intro", startIndex: 0, endIndex: 2, fromTop: true },
  { name: "02-escolha-assunto", startIndex: 4, endIndex: 4 },
  { name: "03-whatsapp-contato", startIndex: 5, endIndex: 5 },
  { name: "04-formulario", startIndex: 6, endIndex: 6 },
  { name: "05-empresas", startIndex: 7, endIndex: 7 },
  { name: "06-faq", startIndex: 8, endIndex: 9 },
  { name: "07-footer", startIndex: 10, endIndex: 10 },
];

const GROUPS_390 = [
  { name: "01-intro", startIndex: 0, endIndex: 2, fromTop: true },
  { name: "02-whatsapp", startIndex: 5, endIndex: 5 },
  { name: "03-formulario", startIndex: 6, endIndex: 6 },
  { name: "04-cta-footer", startIndex: 7, endIndex: 10 },
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

  await page.screenshot({ path: `${OUT_DIR}/contact-${viewport.name}-full.png`, fullPage: true });

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
      path: `${OUT_DIR}/contact-${viewport.name}-${group.name}.png`,
      fullPage: true,
      clip: { x: 0, y: Math.max(0, top), width: viewport.width, height: Math.max(1, bottom - top) },
    });
  }

  report[viewport.name] = { consoleErrors, sectionCount: rects.length };
  await context.close();
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
