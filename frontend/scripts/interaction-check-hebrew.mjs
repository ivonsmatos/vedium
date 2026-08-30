import { chromium } from "playwright";

const URL = "http://localhost:3000/curso-de-hebraico-online";
const browser = await chromium.launch();
const results = {};

{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });

  const trigger = page.locator(".v2-faq__trigger").first();
  await trigger.click();
  const expandedAfterClick = await trigger.getAttribute("aria-expanded");

  const anchors = ["percursos", "moderno", "biblico", "particular"];
  const anchorResults = {};
  for (const anchor of anchors) {
    await page.click(`a[href="#${anchor}"]`);
    await page.waitForTimeout(400);
    anchorResults[anchor] = await page.evaluate((id) => {
      const el = document.getElementById(id);
      if (!el) return false;
      const r = el.getBoundingClientRect();
      return r.top >= -80 && r.top <= 200;
    }, anchor);
  }

  const courseHrefs = await page.$$eval('a[href^="/curso/hebraico-"]', (els) => [...new Set(els.map((el) => el.getAttribute("href")))]);

  results.desktop = { faqExpandsOnClick: expandedAfterClick === "true", anchors: anchorResults, courseHrefsFound: courseHrefs, errors };
  await page.close();
}

{
  const page = await browser.newPage({ viewport: { width: 768, height: 1024 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  results.tablet768 = { horizontalOverflow: overflow, errors };
  await page.close();
}

{
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  await page.click(".v2-header__burger");
  const menuOpen = await page.getAttribute("[data-v2-header]", "data-menu-open");
  results.mobile390 = { horizontalOverflow: overflow, burgerWorks: menuOpen === "true", errors };
  await page.close();
}

await browser.close();
console.log(JSON.stringify(results, null, 2));
