import { chromium } from "playwright";

const URL = "http://localhost:3000";
const browser = await chromium.launch();
const results = {};

// Desktop: locale switcher + mega menu (hover)
{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });

  await page.click(".v2-hdr-utility__locale");
  const menuVisible = await page.isVisible("#v2-hdr-locale-menu");
  await page.keyboard.press("Escape");
  const menuHiddenAfterEscape = !(await page.isVisible("#v2-hdr-locale-menu"));

  await page.hover('.v2-header__nav-item button[aria-haspopup="true"]');
  const megaVisible = await page.isVisible(".v2-header__mega");

  results.desktop = { localeMenuOpened: menuVisible, localeMenuClosedOnEscape: menuHiddenAfterEscape, megaMenuVisibleOnHover: megaVisible, errors };
  await page.close();
}

// Mobile: burger menu toggle
{
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });

  await page.click(".v2-header__burger");
  const menuOpenAttr = await page.getAttribute("[data-v2-header]", "data-menu-open");
  const panelVisible = await page.isVisible("#v2-header-mobile-panel");

  results.mobile = { burgerTogglesMenuOpen: menuOpenAttr === "true", mobilePanelVisible: panelVisible, errors };
  await page.close();
}

// Pathfinder: change radio selection, submit, confirm client-side routing
{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });

  await page.check('input[name="pathfinder-idioma"][value="Iorubá"]');
  await page.check('input[name="pathfinder-objetivo"][value="Estudos e cultura"]');
  await page.click('.v2-pathfinder button[type="submit"]');
  await page.waitForURL("**/ioruba-cultura-e-ancestralidade", { timeout: 5000 }).catch(() => {});

  results.pathfinder = { finalUrl: page.url(), errors };
  await page.close();
}

await browser.close();
console.log(JSON.stringify(results, null, 2));
