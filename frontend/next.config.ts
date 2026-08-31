import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  output: "standalone",
  // Silencia o aviso de multiplos lockfiles: o repo tem um package-lock.json
  // na raiz (vedium_core/scripts Python) alem do de frontend/ -- este app
  // Next fica isolado no proprio diretorio.
  turbopack: {
    root: path.join(__dirname),
  },
  // A Fase F.4 migra somente as três rotas legais aprovadas. Os demais
  // documentos e PDFs continuam sob responsabilidade do Frappe; estes
  // rewrites preservam os URLs públicos referenciados pelos textos sem
  // duplicar conteúdo jurídico nem iniciar uma migração global.
  async rewrites() {
    return [
      { source: "/cookies", destination: "https://app.vediums.com/cookies" },
      { source: "/gravacao-imagem-voz", destination: "https://app.vediums.com/gravacao-imagem-voz" },
      { source: "/privacidade/meus-dados", destination: "https://app.vediums.com/privacidade/meus-dados" },
      { source: "/propriedade-intelectual", destination: "https://app.vediums.com/propriedade-intelectual" },
      { source: "/assets/vedium_core/legal/:path*", destination: "https://app.vediums.com/assets/vedium_core/legal/:path*" },
    ];
  },
};

export default nextConfig;
