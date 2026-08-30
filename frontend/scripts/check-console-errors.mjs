// Varredura de erros de console (Fase G.2 gate report) -- todas as rotas
// migradas, depois do GTM/consent/WhatsApp entrarem no layout.
import { chromium } from "playwright";

const BASE = "http://localhost:3000";
const ROUTES = [
  "/", "/curso-de-ioruba-online", "/curso-de-ingles-online", "/portugues-para-estrangeiros",
  "/curso-de-espanhol-online", "/curso-de-hebraico-online", "/empresas", "/como-funciona",
  "/sobre", "/contato", "/privacidade", "/termos", "/cancelamento-reembolso", "/blog",
  "/blog/ingles/aula-de-ingles-online-ao-vivo-como-funciona-e-para-quem-vale-a-pena",
];

const browser = await chromium.launch();
const results = [];

for (const route of ROUTES) {
  const context = await browser.newContext();
  const page = await context.newPage();
  const errors = [];
  page.on("console", (msg) => { if (msg.type() === "error") errors.push(msg.text()); });
  page.on("pageerror", (err) => errors.push(String(err)));
  await page.goto(`${BASE}${route}`, { waitUntil: "networkidle" });
  if (errors.length) results.push({ route, errors });
  await context.close();
}

await browser.close();
console.log(JSON.stringify({ totalRoutes: ROUTES.length, routesWithErrors: results.length, results }, null, 2));
