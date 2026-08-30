import { FAQAccordion } from "./FAQAccordion";
import type { FaqItem } from "@/types/language";

interface FAQSectionProps {
  faqId: string;
  eyebrow: string;
  title: string;
  items: FaqItem[];
}

export function FAQSection({ faqId, eyebrow, title, items }: FAQSectionProps) {
  return (
    <div className="v2-faq-section">
      <div className="v2-faq-section__intro">
        <p className="v2-eyebrow">{eyebrow}</p>
        <h2 className="v2-heading v2-h2">{title}</h2>
      </div>
      <div className="v2-faq-section__accordion">
        <FAQAccordion faqId={faqId} items={items} />
      </div>
    </div>
  );
}
