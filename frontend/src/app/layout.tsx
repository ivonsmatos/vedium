import type { Metadata } from "next";
import "./globals.css";
import { AnalyticsScripts } from "@/components/analytics/AnalyticsScripts";

export const metadata: Metadata = {
  metadataBase: new URL("https://vediums.com"),
  robots: "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
  icons: {
    icon: "/assets/vedium_core/vedium_assets/images/logos/Icone-color.png",
    apple: "/assets/vedium_core/vedium_assets/images/logos/Icone-color.png",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR" className="h-full">
      <body className="v2-scope min-h-full flex flex-col">
        <AnalyticsScripts />
        {children}
      </body>
    </html>
  );
}
