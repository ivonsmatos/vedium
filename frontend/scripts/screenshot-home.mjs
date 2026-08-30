// QA visual: screenshots full-page e por seção da Home (`/`) em 1440px e
// 390px, mais contagem de console errors. Ferramenta de QA local, não faz
// parte do bundle da aplicação (playwright instalado com --no-save).
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3000";
const OUT_DIR = "qa-screenshots";
mkdirSync(OUT_DIR, { recursive: true });

const VIEWPORTS = [
  { name: "1440", width: 1440, height: 900 },
  { name: "390", width: 390, height: 844 },
];

const SECTION_GROUPS = [
  { name: "01-header-hero", startIndex: 1, endIndex: 1, fromTop: true },
  { name: "02-pathfinder-diferenciais", startIndex: 2, endIndex: 3 },
  { name: "03-cursos", startIndex: 4, endIndex: 4 },
  { name: "04-live-progressao", startIndex: 5, endIndex: 6 },
  { name: "05-b2b-conhecimento", startIndex: 7, endIndex: 8 },
  { name: "06-cta-footer", startIndex: 9, endIndex: 10 },
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
  await page.waitForSelector(".v2-editorial-hero__slide.is-active", { timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(300);

  // Imagens abaixo da dobra usam loading="lazy" (mesmo padrão da produção) --
  // sem um scroll real, o navegador nunca dispara o fetch e o screenshot
  // fullPage captura essas seções em branco. Percorre a página inteira pra
  // disparar o IntersectionObserver nativo antes de capturar.
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

  await page.screenshot({ path: `${OUT_DIR}/home-${viewport.name}-full.png`, fullPage: true });

  const rects = await page.evaluate(() => {
    const children = Array.from(document.querySelector("main").children);
    return children.map((el) => {
      const r = el.getBoundingClientRect();
      return { top: r.top + window.scrollY, bottom: r.bottom + window.scrollY };
    });
  });

  for (const group of SECTION_GROUPS) {
    const top = group.fromTop ? 0 : rects[group.startIndex].top;
    const bottom = rects[group.endIndex].bottom;
    await page.screenshot({
      path: `${OUT_DIR}/home-${viewport.name}-${group.name}.png`,
      fullPage: true,
      clip: { x: 0, y: Math.max(0, top), width: viewport.width, height: Math.max(1, bottom - top) },
    });
  }

  report[viewport.name] = { consoleErrors };
  await context.close();
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
