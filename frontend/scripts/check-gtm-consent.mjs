// Verificacao GTM + Consent Mode v2 no Next (Fase G.2, Parte A secao 14).
import { chromium } from "playwright";

const BASE = "http://localhost:3000";
const report = {};

const browser = await chromium.launch();

// --- 1. Consent DEFAULT antes do GTM, container correto, sem erro de console ---
{
  const context = await browser.newContext();
  const page = await context.newPage();
  const consoleErrors = [];
  page.on("console", (msg) => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
  page.on("pageerror", (err) => consoleErrors.push(String(err)));

  await page.goto(`${BASE}/`, { waitUntil: "networkidle" });

  const state = await page.evaluate(() => {
    const dl = window.dataLayer || [];
    // gtag() empurra `arguments` (array-like, NAO Array.isArray) -- checar
    // por indice, nao por Array.isArray (mesmo jeito que o proprio loader
    // do GTM le cada entrada do dataLayer).
    const consentEvents = dl.filter((e) => e && e[0] === "consent");
    const gtmScriptTag = document.querySelector('script[src*="googletagmanager.com/gtm.js"]');
    const gtmSrc = gtmScriptTag ? gtmScriptTag.src : null;
    return {
      dataLayerLength: dl.length,
      consentEventsCount: consentEvents.length,
      firstConsentEvent: consentEvents[0] || null,
      gtmScriptPresent: !!gtmScriptTag,
      gtmSrc,
      cookieBarPresent: !!document.getElementById("vd-cookie-bar"),
      guardFlag: window.__vediumConsentDefaultSet === true,
    };
  });

  report.gtmContainer = state.gtmSrc && state.gtmSrc.includes("GTM-P6Q2FXLK") ? "PASS" : "FAIL";
  report.consentDefaultBeforeGtm = state.consentEventsCount >= 1 && state.firstConsentEvent && state.firstConsentEvent[1] === "default" ? "PASS" : "FAIL";
  report.consentDefaultPayload = state.firstConsentEvent ? state.firstConsentEvent[2] : null;
  report.cookieBanner = state.cookieBarPresent ? "PASS" : "FAIL";
  report.guardFlagSet = state.guardFlag;
  report.consoleErrorsHome = consoleErrors;

  await context.close();
}

// --- 2. ACCEPT flow ---
{
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(`${BASE}/`, { waitUntil: "networkidle" });
  await page.click("#vd-cookie-ok");
  await page.waitForTimeout(300);
  const after = await page.evaluate(() => {
    const dl = window.dataLayer || [];
    const updates = dl.filter((e) => e && e[0] === "consent" && e[1] === "update");
    return {
      updatesCount: updates.length,
      lastUpdate: updates[updates.length - 1] || null,
      localStorageConsent: localStorage.getItem("vedium_cookie_consent"),
      localStoragePrefs: localStorage.getItem("vedium_cookie_preferences"),
      barGone: !document.getElementById("vd-cookie-bar"),
    };
  });
  const granted = after.lastUpdate && after.lastUpdate[2] &&
    after.lastUpdate[2].analytics_storage === "granted" && after.lastUpdate[2].ad_storage === "granted";
  report.acceptFlow = granted && after.barGone ? "PASS" : "FAIL";
  report.acceptFlowDetail = after;
  await context.close();
}

// --- 3. REJECT flow ---
{
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(`${BASE}/`, { waitUntil: "networkidle" });
  await page.click("#vd-cookie-reject");
  await page.waitForTimeout(300);
  const after = await page.evaluate(() => {
    const dl = window.dataLayer || [];
    const updates = dl.filter((e) => e && e[0] === "consent" && e[1] === "update");
    return {
      lastUpdate: updates[updates.length - 1] || null,
      localStorageConsent: localStorage.getItem("vedium_cookie_consent"),
      barGone: !document.getElementById("vd-cookie-bar"),
    };
  });
  const denied = after.lastUpdate && after.lastUpdate[2] &&
    after.lastUpdate[2].analytics_storage === "denied" && after.lastUpdate[2].ad_storage === "denied";
  report.rejectFlow = denied && after.localStorageConsent === "rejected" && after.barGone ? "PASS" : "FAIL";
  report.rejectFlowDetail = after;
  await context.close();
}

// --- 4. MANAGE (granular: analytics sim, marketing nao) ---
{
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(`${BASE}/`, { waitUntil: "networkidle" });
  await page.click("#vd-cookie-manage");
  await page.waitForTimeout(200);
  await page.check("#vd-cookie-pref-analytics");
  await page.uncheck("#vd-cookie-pref-marketing");
  await page.click("#vd-cookie-prefs-save");
  await page.waitForTimeout(300);
  const after = await page.evaluate(() => {
    const dl = window.dataLayer || [];
    const updates = dl.filter((e) => e && e[0] === "consent" && e[1] === "update");
    return {
      lastUpdate: updates[updates.length - 1] || null,
      localStoragePrefs: localStorage.getItem("vedium_cookie_preferences"),
    };
  });
  const mixed = after.lastUpdate && after.lastUpdate[2] &&
    after.lastUpdate[2].analytics_storage === "granted" && after.lastUpdate[2].ad_storage === "denied";
  report.manageFlow = mixed ? "PASS" : "FAIL";
  report.manageFlowDetail = after;
  await context.close();
}

// --- 5. Persistencia entre reload e entre paginas ---
{
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(`${BASE}/`, { waitUntil: "networkidle" });
  await page.click("#vd-cookie-ok");
  await page.waitForTimeout(200);
  await page.reload({ waitUntil: "networkidle" });
  const afterReload = await page.evaluate(() => ({
    barPresent: !!document.getElementById("vd-cookie-bar"),
    lastUpdate: (window.dataLayer || []).filter((e) => e && e[0] === "consent" && e[1] === "update").pop() || null,
  }));
  await page.goto(`${BASE}/como-funciona`, { waitUntil: "networkidle" });
  const afterNav = await page.evaluate(() => ({
    barPresent: !!document.getElementById("vd-cookie-bar"),
    lastUpdate: (window.dataLayer || []).filter((e) => e && e[0] === "consent" && e[1] === "update").pop() || null,
  }));
  report.consentPersistence =
    !afterReload.barPresent && !afterNav.barPresent &&
    afterReload.lastUpdate && afterReload.lastUpdate[2].analytics_storage === "granted" &&
    afterNav.lastUpdate && afterNav.lastUpdate[2].analytics_storage === "granted"
      ? "PASS" : "FAIL";
  report.consentPersistenceDetail = { afterReload, afterNav };
  await context.close();
}

// --- 6. WhatsApp: 1 clique = 1 emissao, em varios pontos ---
{
  const touchpoints = [
    { route: "/", selector: '.v2-hdr-utility__link[href*="wa.me"]', name: "Header utility bar" },
    { route: "/", selector: '.v2-footer__whatsapp', name: "Footer" },
    { route: "/curso-de-hebraico-online", selector: 'a[href*="wa.me"]:not(.v2-hdr-utility__link):not(.v2-footer__whatsapp)', name: "Curso (pillar) secondary CTA" },
    { route: "/empresas", selector: 'a[href*="wa.me"]:not(.v2-hdr-utility__link):not(.v2-footer__whatsapp)', name: "B2B" },
    { route: "/contato", selector: '#whatsapp a[href*="wa.me"]', name: "Contato CTA final" },
  ];
  const whatsappResults = [];
  for (const tp of touchpoints) {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(`${BASE}${tp.route}`, { waitUntil: "networkidle" });
    await page.click("#vd-cookie-ok").catch(() => {});
    await page.waitForTimeout(150);
    const before = await page.evaluate(() => (window.dataLayer || []).length);
    const target = page.locator(tp.selector).first();
    const exists = await target.count();
    if (exists === 0) {
      whatsappResults.push({ ...tp, found: false });
      await context.close();
      continue;
    }
    // Todo link de WhatsApp real usa target="_blank" (TrackedWhatsappLink) --
    // o clique abre uma aba NOVA, a pagina original nao navega, entao o
    // dataLayer desta pagina continua intacto pra leitura logo abaixo.
    const popupPromise = context.waitForEvent("page").catch(() => null);
    await target.click();
    const popup = await popupPromise;
    if (popup) await popup.close().catch(() => {});
    await page.waitForTimeout(200);
    const events = await page.evaluate(() => (window.dataLayer || []).filter((e) => e && e.event === "public_cta_click"));
    whatsappResults.push({ ...tp, found: true, publicCtaClickCount: events.length, events });
    await context.close();
  }
  report.whatsappTouchpoints = whatsappResults;
  const allFoundAndSingle = whatsappResults.every((r) => r.found && r.publicCtaClickCount === 1);
  report.whatsappTracking = allFoundAndSingle ? "PASS" : "FAIL";
  report.duplicateEvents = whatsappResults.filter((r) => r.found && r.publicCtaClickCount !== 1).length;
}

await browser.close();
console.log(JSON.stringify(report, null, 2));
