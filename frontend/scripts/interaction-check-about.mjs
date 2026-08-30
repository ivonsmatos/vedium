import { chromium } from "playwright";

const URL = "http://localhost:3000/sobre";
const browser = await chromium.launch();
const results = {};

{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(URL, { waitUntil: "networkidle" });

  const courseHrefs = await page.$$eval('nav[aria-label="Índice de cursos"] a', (els) => [...new Set(els.map((el) => el.getAttribute("href")))]);
  const empresasLinks = await page.$$eval('a[href="/empresas"]', (els) => els.length);
  const comoFuncionaLinks = await page.$$eval('a[href="/como-funciona"]', (els) => els.length);
  const professoresPageLinks = await page.$$eval('a[href="/professores"]', (els) => els.length);

  results.desktop = {
    courseHrefsFound: courseHrefs,
    empresasLinksCount: empresasLinks,
    comoFuncionaLinksCount: comoFuncionaLinks,
    // Header/Footer sao componentes compartilhados e ja tem esse link
    // (que resolve /professores -> /sobre em producao); a pagina Sobre em
    // si NAO deve adicionar nenhum link novo para /professores (missao:
    // sem pagina de catalogo de professores).
    professoresPageLinksFromSharedNav: professoresPageLinks,
    errors,
  };
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
