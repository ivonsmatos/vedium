// QA visual: screenshots do /blog (hub) e do artigo migrado, 1440 e 390.
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const OUT_DIR = "qa-screenshots";
mkdirSync(OUT_DIR, { recursive: true });

const PAGES = [
  { name: "blog-hub", url: "http://localhost:3000/blog" },
  { name: "blog-article", url: "http://localhost:3000/blog/ingles/aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-vale-a-pena" },
];

const VIEWPORTS = [
  { name: "1440", width: 1440, height: 900 },
  { name: "390", width: 390, height: 844 },
];

const browser = await chromium.launch();
const report = {};

for (const pageDef of PAGES) {
  report[pageDef.name] = {};
  for (const viewport of VIEWPORTS) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });
    const page = await context.newPage();
    const consoleErrors = [];
    page.on("console", (msg) => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
    page.on("pageerror", (err) => consoleErrors.push(String(err)));

    await page.goto(pageDef.url, { waitUntil: "networkidle" });
    await page.waitForTimeout(300);
    await page.evaluate(async () => {
      const step = 400, delay = 50;
      let scrolled = 0;
      const height = document.body.scrollHeight;
      while (scrolled < height) {
        window.scrollBy(0, step);
        scrolled += step;
        await new Promise((r) => setTimeout(r, delay));
      }
      window.scrollTo(0, 0);
    });
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(300);

    await page.screenshot({ path: `${OUT_DIR}/${pageDef.name}-${viewport.name}-full.png`, fullPage: true });
    report[pageDef.name][viewport.name] = { consoleErrors };
    await context.close();
  }
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
