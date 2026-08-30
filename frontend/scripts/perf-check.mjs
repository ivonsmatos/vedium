import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

await page.addInitScript(() => {
  window.__cls = 0;
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      window.__lcp = entry.startTime;
    }
  }).observe({ type: "largest-contentful-paint", buffered: true });
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (!entry.hadRecentInput) window.__cls += entry.value;
    }
  }).observe({ type: "layout-shift", buffered: true });
});

await page.goto("http://localhost:3000", { waitUntil: "load" });
await page.waitForTimeout(1500);

const metrics = await page.evaluate(() => {
  const paint = performance.getEntriesByType("paint");
  const fcp = paint.find((e) => e.name === "first-contentful-paint")?.startTime ?? null;
  const nav = performance.getEntriesByType("navigation")[0];
  return {
    fcp,
    domContentLoaded: nav ? nav.domContentLoadedEventEnd : null,
    loadEvent: nav ? nav.loadEventEnd : null,
    lcp: window.__lcp ?? null,
    cls: window.__cls ?? null,
  };
});

console.log(JSON.stringify(metrics, null, 2));
await browser.close();
