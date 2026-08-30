import { chromium } from "playwright";

const browser = await chromium.launch();
const results = {};

{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto("http://localhost:3000/blog", { waitUntil: "networkidle" });

  const articleLink = await page.$$eval('a[href^="/blog/ingles/"]', (els) => els.length);
  const languageLinks = await page.$$eval('nav[aria-label="Índice de cursos"] a', (els) => [...new Set(els.map((el) => el.getAttribute("href")))]);
  const empresasLink = await page.$$eval('a[href="/empresas"]', (els) => els.length);

  results.hub = { articleLinkCount: articleLink, languageLinksFound: languageLinks, empresasLinkCount: empresasLink, errors };
  await page.close();
}

{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto("http://localhost:3000/blog/ingles/aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-vale-a-pena", { waitUntil: "networkidle" });

  const trigger = page.locator(".v2-faq__trigger").first();
  await trigger.click();
  const expandedAfterClick = await trigger.getAttribute("aria-expanded");

  const pillarLink = await page.$$eval('a[href="/curso-de-ingles-online"]', (els) => els.length);
  const siblingLink = await page.$$eval('a[href="/blog/ingles/como-estudar-phrasal-verbs-sem-decorar-listas-infinitas"]', (els) => els.length);
  const ctaLink = await page.$$eval('a[href="/ingles-para-viagens"]', (els) => els.length);
  const tableCount = await page.locator("table").count();

  results.article = {
    faqExpandsOnClick: expandedAfterClick === "true",
    pillarLinkCount: pillarLink,
    siblingArticleLinkCount: siblingLink,
    ctaLinkCount: ctaLink,
    tableCount,
    errors,
  };
  await page.close();
}

{
  const page = await browser.newPage({ viewport: { width: 768, height: 1024 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto("http://localhost:3000/blog", { waitUntil: "networkidle" });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  results.tablet768 = { horizontalOverflow: overflow, errors };
  await page.close();
}

{
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto("http://localhost:3000/blog/ingles/aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-vale-a-pena", { waitUntil: "networkidle" });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  results.mobile390 = { horizontalOverflow: overflow, errors };
  await page.close();
}

await browser.close();
console.log(JSON.stringify(results, null, 2));
