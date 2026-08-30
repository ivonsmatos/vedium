import type { Metadata } from "next";
import { LegalDocumentPage } from "@/components/legal/LegalDocumentPage";
import { TERMS_DOCUMENT } from "@/content/legal/terms";

export const metadata: Metadata = {
  title: TERMS_DOCUMENT.seo.title,
  description: TERMS_DOCUMENT.seo.description,
  alternates: { canonical: TERMS_DOCUMENT.seo.canonical },
  robots: TERMS_DOCUMENT.seo.robots,
};

export default function TermsPage() {
  return <LegalDocumentPage document={TERMS_DOCUMENT} />;
}
