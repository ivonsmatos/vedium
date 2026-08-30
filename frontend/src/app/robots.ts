import type { MetadataRoute } from "next";
import { headers } from "next/headers";

/**
 * Contrato de robots (Fase G.1 seção 8). A checagem é pelo HOST real da
 * requisição, não por NODE_ENV -- um build de produção rodando em
 * preview/staging também teria NODE_ENV=production, então checar isso
 * não distingue "é preview" de "é vediums.com de verdade". Checar o host
 * é a única forma de nunca publicar `Disallow: /` acidentalmente em
 * produção nem liberar crawl num ambiente de preview por engano.
 */
const PRODUCTION_HOST = "vediums.com";

export default async function robots(): Promise<MetadataRoute.Robots> {
  const headerList = await headers();
  const host = (headerList.get("host") || "").toLowerCase().replace(/:\d+$/, "");
  const isProduction = host === PRODUCTION_HOST || host === `www.${PRODUCTION_HOST}`;

  if (!isProduction) {
    return { rules: { userAgent: "*", disallow: "/" } };
  }

  return {
    rules: { userAgent: "*", allow: "/", disallow: ["/api/"] },
    sitemap: `https://${PRODUCTION_HOST}/sitemap.xml`,
  };
}
