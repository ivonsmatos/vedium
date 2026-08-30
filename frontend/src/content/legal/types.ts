export interface LegalInline {
  text: string;
  strong?: boolean;
  underline?: boolean;
  href?: string;
  newTab?: boolean;
}

export type LegalRichText = LegalInline[];

export type LegalBlock =
  | { type: "paragraph"; content: LegalRichText }
  | { type: "list"; ordered?: boolean; items: LegalRichText[] }
  | { type: "notice"; tone?: "info" | "success" | "danger" | "warning" | "neutral"; lines: LegalRichText[] }
  | { type: "table"; label: string; headers: string[]; rows: string[][] }
  | { type: "steps"; items: { number: string; text: string }[] };

export interface LegalSection {
  id: string;
  heading: string;
  blocks: LegalBlock[];
}

export interface LegalLink {
  label: string;
  href: string;
  newTab?: boolean;
}

export interface LegalDocument {
  slug: "privacidade" | "termos" | "cancelamento-reembolso";
  title: string;
  lastUpdated: string;
  seo: {
    title: string;
    description: string;
    canonical: string;
    robots: string;
  };
  introduction: LegalBlock[];
  sections: LegalSection[];
  actions: LegalLink[];
  relatedLinks: LegalLink[];
  stamp: string;
}
