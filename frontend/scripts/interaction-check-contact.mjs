import { chromium } from "playwright";

const URL = "http://localhost:3000/contato";
const browser = await chromium.launch();
const results = {};

{
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));

  // Guard de seguranca: NUNCA deixar este teste automatizado alcancar o
  // Frappe de producao de verdade (nao criar ticket/CRM Lead/e-mail real
  // com dados de teste). Qualquer chamada pra app.vediums.com e abortada
  // aqui -- o proprio /api/contact roda local (mockado abaixo pro caso
  // "sucesso"), entao isso so protegeria contra um bug que vazasse a
  // chamada real por engano.
  await page.route("**/app.vediums.com/**", (route) => route.abort());

  await page.goto(URL, { waitUntil: "networkidle" });

  // 1) Validacao client-side: envio vazio nao chama a API, mostra erro.
  await page.click('button[type="submit"]');
  await page.waitForTimeout(200);
  const nameError = await page.locator("#contact-name-error").count();
  const emailError = await page.locator("#contact-email-error").count();

  // 2) Honeypot: preenche nome/email validos + honeypot -- /api/contact
  // deve responder ok:true SEM repassar nada ao Frappe (nunca sai do
  // localhost). Intercepta a chamada real a /api/contact pra confirmar
  // o payload enviado inclui o honeypot preenchido.
  let apiCallBody = null;
  await page.route("**/api/contact", async (route) => {
    apiCallBody = route.request().postDataJSON();
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true }) });
  });
  await page.fill("#contact-name", "Teste QA");
  await page.fill("#contact-email", "qa@example.com");
  await page.fill("#contact-company-website", "bot-filled-this");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(300);
  const successVisible = await page.locator(".v2-alert--success").count();

  // 3) Link do WhatsApp principal existe e aponta pro numero oficial.
  const mainWhatsapp = await page.$$eval('a[href^="https://wa.me/5511911293075"]', (els) => els.length);

  // 4) Cada um dos 5 assuntos tem seu proprio link de WhatsApp.
  const subjectLinks = await page.locator(".v2-b2b-list__item a").count();

  const privacyLink = await page.$$eval('a[href="/privacidade"]', (els) => els.length);
  const empresasLink = await page.$$eval('a[href="/empresas"]', (els) => els.length);

  results.desktop = {
    validationShowsNameError: nameError > 0,
    validationShowsEmailError: emailError > 0,
    honeypotPayloadCaptured: apiCallBody?.companyWebsite === "bot-filled-this",
    successMessageAfterHoneypotMock: successVisible > 0,
    mainWhatsappLinkCount: mainWhatsapp,
    subjectWhatsappLinksCount: subjectLinks,
    privacyLinkCount: privacyLink,
    empresasLinkCount: empresasLink,
    errors,
  };
  await page.close();
}

{
  const page = await browser.newPage({ viewport: { width: 768, height: 1024 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.route("**/app.vediums.com/**", (route) => route.abort());
  await page.goto(URL, { waitUntil: "networkidle" });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  results.tablet768 = { horizontalOverflow: overflow, errors };
  await page.close();
}

{
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.route("**/app.vediums.com/**", (route) => route.abort());
  await page.goto(URL, { waitUntil: "networkidle" });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  await page.click(".v2-header__burger");
  const menuOpen = await page.getAttribute("[data-v2-header]", "data-menu-open");
  results.mobile390 = { horizontalOverflow: overflow, burgerWorks: menuOpen === "true", errors };
  await page.close();
}

await browser.close();
console.log(JSON.stringify(results, null, 2));
