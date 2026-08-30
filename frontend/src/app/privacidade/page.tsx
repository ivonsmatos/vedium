import type { Metadata } from "next";
import { LegalDocumentPage } from "@/components/legal/LegalDocumentPage";
import { PRIVACY_DOCUMENT } from "@/content/legal/privacy";

export const metadata: Metadata = {
  title: PRIVACY_DOCUMENT.seo.title,
  description: PRIVACY_DOCUMENT.seo.description,
  alternates: { canonical: PRIVACY_DOCUMENT.seo.canonical },
  robots: PRIVACY_DOCUMENT.seo.robots,
};

export default function PrivacyPage() {
  return <LegalDocumentPage document={PRIVACY_DOCUMENT} />;
}
