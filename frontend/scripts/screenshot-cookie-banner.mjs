import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const BASE = "http://localhost:3000";
const outDir = "C:\\Users\\ivonm\\AppData\\Local\\Temp\\claude\\c--Users-ivonm-OneDrive---CONDOMINIO-CONJUNTO-RESIDENCIAL-PARQUE-BRASIL-Github-vedium\\7646b823-7710-4af2-9956-612f24686f40\\scratchpad";
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();

for (const [name, width, height] of [["desktop", 1440, 900], ["mobile", 375, 812]]) {
  const context = await browser.newContext({ viewport: { width, height } });
  const page = await context.newPage();
  await page.goto(`${BASE}/`, { waitUntil: "networkidle" });
  await page.screenshot({ path: `${outDir}\\cookie-banner-${name}.png` });
  await page.click("#vd-cookie-manage");
  await page.waitForTimeout(200);
  await page.screenshot({ path: `${outDir}\\cookie-prefs-${name}.png` });
  await context.close();
}

await browser.close();
console.log("done");
