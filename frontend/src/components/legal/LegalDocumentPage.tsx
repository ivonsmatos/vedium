import Link from "next/link";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import type { LegalBlock, LegalDocument, LegalLink, LegalRichText } from "@/content/legal/types";
import styles from "./LegalDocumentPage.module.css";

const LEGAL_NAVIGATION: LegalLink[] = [
  { label: "Privacidade", href: "/privacidade" },
  { label: "Termos", href: "/termos" },
  { label: "Cancelamento e Reembolso", href: "/cancelamento-reembolso" },
];

function RichText({ content }: { content: LegalRichText }) {
  return content.map((inline, index) => {
    let node: React.ReactNode = inline.text;
    if (inline.underline) node = <u>{node}</u>;
    if (inline.strong) node = <strong>{node}</strong>;
    if (inline.href) {
      node = (
        <a href={inline.href} target={inline.newTab ? "_blank" : undefined} rel={inline.newTab ? "noopener" : undefined}>
          {node}
        </a>
      );
    }
    return <span key={`${inline.text}-${index}`}>{node}</span>;
  });
}

function LegalBlockView({ block }: { block: LegalBlock }) {
  if (block.type === "paragraph") return <p><RichText content={block.content} /></p>;

  if (block.type === "list") {
    const List = block.ordered ? "ol" : "ul";
    return <List>{block.items.map((item, index) => <li key={index}><RichText content={item} /></li>)}</List>;
  }

  if (block.type === "notice") {
    return (
      <div className={`${styles.notice} ${styles[`notice-${block.tone ?? "info"}`]}`}>
        {block.lines.map((line, index) => <p key={index}><RichText content={line} /></p>)}
      </div>
    );
  }

  if (block.type === "table") {
    return (
      <div className={styles.tableRegion} role="region" aria-label={block.label} tabIndex={0}>
        <table>
          <thead><tr>{block.headers.map((header) => <th key={header} scope="col">{header}</th>)}</tr></thead>
          <tbody>{block.rows.map((row, rowIndex) => (
            <tr key={rowIndex}>{row.map((cell, cellIndex) => <td key={cellIndex}>{cell}</td>)}</tr>
          ))}</tbody>
        </table>
      </div>
    );
  }

  return (
    <div className={styles.steps}>
      {block.items.map((item) => (
        <div className={styles.step} key={item.number}>
          <span className={styles.stepNumber}>{item.number}</span>
          <p>{item.text}</p>
        </div>
      ))}
    </div>
  );
}

function DocumentLink({ link, className }: { link: LegalLink; className?: string }) {
  if (link.href.startsWith("/")) {
    return <Link href={link.href} className={className} target={link.newTab ? "_blank" : undefined} rel={link.newTab ? "noopener" : undefined}>{link.label}</Link>;
  }
  return <a href={link.href} className={className} target={link.newTab ? "_blank" : undefined} rel={link.newTab ? "noopener" : undefined}>{link.label}</a>;
}

export function LegalDocumentPage({ document }: { document: LegalDocument }) {
  return (
    <>
      <Header />
      <main className={styles.page}>
        <article className={styles.article} data-legal-document={document.slug}>
          <div data-legal-source-content>
            <header className={styles.pageHeader}>
              <p className={styles.eyebrow} data-parity-ignore>DOCUMENTOS LEGAIS</p>
              <h1>{document.title}</h1>
              <p className={styles.updated}>{document.lastUpdated}</p>
            </header>

            {document.introduction.map((block, index) => <LegalBlockView block={block} key={index} />)}

            <nav className={styles.toc} aria-label={`Índice de ${document.title}`} data-parity-ignore>
              <p className={styles.tocTitle}>Nesta página</p>
              <ol>{document.sections.map((section) => <li key={section.id}><a href={`#${section.id}`}>{section.heading}</a></li>)}</ol>
            </nav>

            <div className={styles.documentBody}>
              {document.sections.map((section) => (
                <section key={section.id} aria-labelledby={section.id}>
                  <h2 id={section.id}>{section.heading}</h2>
                  {section.blocks.map((block, index) => <LegalBlockView block={block} key={index} />)}
                </section>
              ))}
            </div>

            <div className={styles.actions}>
              {document.actions.map((link) => <DocumentLink key={link.href} link={link} className={styles.actionLink} />)}
            </div>

            <nav className={styles.sourceLinks} aria-label="Referências legais do documento">
              {document.relatedLinks.map((link) => <DocumentLink key={link.href} link={link} />)}
            </nav>

            <p className={styles.stamp}>{document.stamp}</p>
          </div>
        </article>

        <nav className={styles.legalNavigation} aria-label="Navegação entre documentos legais" data-parity-ignore>
          <div className={styles.legalNavigationInner}>
            <p>Documentos legais</p>
            <div>{LEGAL_NAVIGATION.map((link) => <DocumentLink key={link.href} link={link} />)}</div>
          </div>
        </nav>
      </main>
      <Footer />
    </>
  );
}
