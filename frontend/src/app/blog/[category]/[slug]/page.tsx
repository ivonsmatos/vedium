import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ArticleTemplate } from "@/components/blog/ArticleTemplate";
import { getArticle, BLOG_ARTICLES } from "@/content/blog";

interface PageProps {
  params: Promise<{ category: string; slug: string }>;
}

export function generateStaticParams() {
  return BLOG_ARTICLES.filter((a) => a.category).map((a) => ({ category: a.category, slug: a.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { category, slug } = await params;
  const article = getArticle(category, slug);
  if (!article) return {};

  return {
    title: `${article.title} | Vedium`,
    description: article.description,
    alternates: { canonical: article.seo.canonical },
    robots: article.seo.robots,
    openGraph: {
      type: "article",
      url: article.seo.canonical,
      title: article.title,
      description: article.description,
      images: [article.seo.ogImage],
      publishedTime: article.publishedAt,
      modifiedTime: article.updatedAt || article.publishedAt,
    },
    twitter: {
      card: "summary_large_image",
      title: article.title,
      description: article.description,
      images: [article.seo.ogImage],
    },
  };
}

function buildJsonLd(article: NonNullable<ReturnType<typeof getArticle>>) {
  const articleLd: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": article.schema,
    headline: article.title,
    description: article.description,
    datePublished: article.publishedAt,
    dateModified: article.updatedAt || article.publishedAt,
    author: { "@type": "Organization", name: article.author },
    publisher: { "@type": "Organization", name: "Vedium", url: "https://vediums.com" },
    mainEntityOfPage: article.seo.canonical,
    inLanguage: article.language,
  };
  if (article.heroImage) articleLd.image = article.heroImage.src;

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Início", item: "https://vediums.com/" },
      { "@type": "ListItem", position: 2, name: "Blog", item: "https://vediums.com/blog" },
      { "@type": "ListItem", position: 3, name: article.tag, item: article.seo.canonical },
    ],
  };

  const schemas: Record<string, unknown>[] = [articleLd, breadcrumb];

  if (article.faq.length > 0) {
    schemas.push({
      "@context": "https://schema.org",
      "@type": "FAQPage",
      mainEntity: article.faq.map((item) => ({
        "@type": "Question",
        name: item.question,
        acceptedAnswer: { "@type": "Answer", text: item.answer },
      })),
    });
  }

  return schemas;
}

export default async function BlogArticlePage({ params }: PageProps) {
  const { category, slug } = await params;
  const article = getArticle(category, slug);
  if (!article) notFound();

  const jsonLd = buildJsonLd(article);

  return (
    <>
      {jsonLd.map((schema, index) => (
        <script key={index} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      ))}
      <main>
        <Header />
        <ArticleTemplate article={article} />
        <Footer />
      </main>
    </>
  );
}
