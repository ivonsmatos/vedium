export interface CtaLink {
  text: string;
  href: string;
}

export interface HeroMedia {
  src: string;
  alt: string;
  width: number;
  height: number;
}

export interface EditorialRow {
  title: string;
  text: string;
  href?: string;
  ctaLabel?: string;
}

export interface EditorialNoteContent {
  eyebrow: string;
  title: string;
  text: string;
  cta?: CtaLink;
}

export interface LiveClassContent {
  title: string;
  lead?: string;
  points: { label: string; text: string }[];
  media: HeroMedia;
}

export interface LanguageLevel {
  code: string;
  publicLabel: string;
  title: string;
  competencySummary: string;
  focuses: string[];
  href: string | null;
}

export interface CultureContent {
  eyebrow: string;
  title: string;
  description: string;
  media: HeroMedia;
  relatedLink?: CtaLink;
}

export interface IndexLink {
  name: string;
  href: string;
}

export interface ObjectivesContent {
  eyebrow: string;
  title: string;
  lead?: string;
  items: IndexLink[];
}

export interface ProgressionConceptContent {
  title: string;
  text: string;
  steps: { label: string; note?: string }[];
}

export interface FaqItem {
  question: string;
  answer: string;
}

export interface InsightCardContent {
  title: string;
  summary: string;
  href: string;
  category: string;
  date: string;
}

export interface BreadcrumbItem {
  label: string;
  href: string | null;
}

export interface LanguagePillarSeo {
  title: string;
  description: string;
  canonical: string;
  robots: string;
  ogImage: string;
  hreflang: Record<string, string>;
}

/**
 * Contrato de conteúdo para uma página-pilar de idioma
 * (`/curso-de-<idioma>-online`). Um arquivo por idioma em
 * `src/content/languages/`; a página só compõe, nunca hardcoda copy.
 */
export interface LanguagePillarContent {
  languageKey: string;
  displayName: string;
  seo: LanguagePillarSeo;
  breadcrumb: BreadcrumbItem[];
  hero: {
    eyebrow: string;
    headline: string;
    support: string;
    primaryCta: CtaLink;
    secondaryCta: CtaLink;
    media: HeroMedia;
  };
  studyPillars?: {
    eyebrow: string;
    headline: string;
    lead?: string;
    rows: EditorialRow[];
    cta?: CtaLink;
  };
  liveClass: LiveClassContent;
  levels: {
    title: string;
    lead: string;
    sequential: boolean;
    items: LanguageLevel[];
  };
  culture?: CultureContent;
  objectives?: ObjectivesContent;
  applications?: {
    eyebrow: string;
    headline: string;
    rows: EditorialRow[];
  };
  progressionConcept?: ProgressionConceptContent;
  // Percursos não-sequenciais (ex.: Hebraico -- Primeiro contato / Moderno /
  // Bíblico / Particular não são níveis de uma única trilha). Reusa
  // EditorialRow (title/text) + href/ctaLabel opcionais por item.
  tracks?: {
    eyebrow: string;
    headline: string;
    items: EditorialRow[];
  };
  // Segundo bloco de mídia+texto (reusa CultureContent) quando um idioma
  // precisa de 2 capítulos editoriais distintos (ex.: Hebraico Moderno vs
  // Hebraico Bíblico) em vez de só 1 ("culture").
  secondaryFeature?: CultureContent;
  // Blocos curtos de texto institucional (eyebrow+título+parágrafo+CTA
  // opcional) -- ex.: "Hebraico Particular", "Professores/Abordagem"
  // genérico (sem nome individual, ver feedback_no_teacher_name_on_course_pages).
  editorialNotes?: EditorialNoteContent[];
  insights?: {
    headline: string;
    featured: InsightCardContent;
    secondary: InsightCardContent[];
  };
  faq: FaqItem[];
  finalCta: {
    headline: string;
    support: string;
    primaryCta: CtaLink;
    secondaryCta: CtaLink;
  };
}
