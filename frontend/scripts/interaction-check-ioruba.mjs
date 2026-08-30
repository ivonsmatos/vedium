import { chromium } from "playwright";

const URL = "http://localhost:3000/curso-de-ioruba-online";
const browser = await chromium.launch();
const results = {};

// FAQ accordion + anchor CTA + 768 overflow check
{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });

  const trigger = page.locator(".v2-faq__trigger").first();
  await trigger.click();
  const expandedAfterClick = await trigger.getAttribute("aria-expanded");
  const secondTrigger = page.locator(".v2-faq__trigger").nth(1);
  await secondTrigger.click();
  const firstStillExpanded = await trigger.getAttribute("aria-expanded");
  const secondExpanded = await secondTrigger.getAttribute("aria-expanded");

  await page.click('a[href="#niveis"]');
  await page.waitForTimeout(500);
  const inViewport = await page.evaluate(() => {
    const el = document.getElementById("niveis");
    if (!el) return false;
    const r = el.getBoundingClientRect();
    return r.top >= -50 && r.top <= 150;
  });

  const levelLink = page.locator('a[href="/curso/ioruba-basico"]').first();
  const levelHref = await levelLink.getAttribute("href");

  results.desktop = {
    faqExpandsOnClick: expandedAfterClick === "true",
    faqSingleOpenBehavior: firstStillExpanded === "false" && secondExpanded === "true",
    anchorScrollsToLevels: inViewport,
    levelLinkReal: levelHref,
    errors,
  };
  await page.close();
}

// 768 tablet breakpoint: no horizontal overflow
{
  const page = await browser.newPage({ viewport: { width: 768, height: 1024 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  results.tablet768 = { horizontalOverflow: overflow, errors };
  await page.close();
}

// 390: no horizontal overflow + mobile menu works
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
