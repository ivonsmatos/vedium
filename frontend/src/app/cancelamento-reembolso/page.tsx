import type { Metadata } from "next";
import { LegalDocumentPage } from "@/components/legal/LegalDocumentPage";
import { CANCELLATION_REFUND_DOCUMENT } from "@/content/legal/cancellation-refund";

export const metadata: Metadata = {
  title: CANCELLATION_REFUND_DOCUMENT.seo.title,
  description: CANCELLATION_REFUND_DOCUMENT.seo.description,
  alternates: { canonical: CANCELLATION_REFUND_DOCUMENT.seo.canonical },
  robots: CANCELLATION_REFUND_DOCUMENT.seo.robots,
};

export default function CancellationRefundPage() {
  return <LegalDocumentPage document={CANCELLATION_REFUND_DOCUMENT} />;
}
