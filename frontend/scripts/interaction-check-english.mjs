import { chromium } from "playwright";

const URL = "http://localhost:3000/curso-de-ingles-online";
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

  await page.click('a[href="#niveis"]');
  await page.waitForTimeout(500);
  const inViewport = await page.evaluate(() => {
    const el = document.getElementById("niveis");
    if (!el) return false;
    const r = el.getBoundingClientRect();
    return r.top >= -50 && r.top <= 150;
  });

  const levelHrefs = await page.$$eval('a[href^="/curso/ingles-"]', (els) => els.map((el) => el.getAttribute("href")));
  const objectiveHrefs = await page.$$eval(
    'a[href^="/ingles-"]',
    (els) => Array.from(new Set(els.map((el) => el.getAttribute("href"))))
  );

  results.desktop = {
    faqExpandsOnClick: expandedAfterClick === "true",
    anchorScrollsToLevels: inViewport,
    levelHrefsFound: [...new Set(levelHrefs)],
    objectiveHrefsFound: objectiveHrefs,
    errors,
  };
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
