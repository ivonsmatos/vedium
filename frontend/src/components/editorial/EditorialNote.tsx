import { TextLink } from "@/components/ui/TextLink";
import type { CtaLink } from "@/types/language";

interface EditorialNoteProps {
  eyebrow: string;
  title: string;
  text: string;
  cta?: CtaLink;
  /**
   * Quando true, renderiza só o conteúdo interno, sem o `.v2-container`
   * próprio nem o padding-block -- para uso dentro de um wrapper externo
   * (ex.: `.v2-notes-pair`), que já cuida do container e do espaçamento.
   */
  bare?: boolean;
}

/**
 * Bloco curto de texto institucional (eyebrow + H2 + parágrafo + CTA
 * opcional), sem mídia, sem nome individual embutido no contrato --
 * usado para capítulos curtos como "Hebraico Particular" ou uma mensagem
 * institucional genérica sobre professores.
 */
export function EditorialNote({ eyebrow, title, text, cta, bare = false }: EditorialNoteProps) {
  const content = (
    <>
      <p className="v2-eyebrow">{eyebrow}</p>
      <h2 className="v2-heading v2-h2" style={{ marginBlockStart: "var(--v2-space-3)", marginBlockEnd: "var(--v2-space-4)", maxWidth: "40rem" }}>
        {title}
      </h2>
      <p className="v2-body v2-body-lg v2-text-muted v2-measure">{text}</p>
      {cta ? (
        <div style={{ marginBlockStart: "var(--v2-space-6)" }}>
          <TextLink href={cta.href} size="lg">
            {cta.text}
          </TextLink>
        </div>
      ) : null}
    </>
  );

  if (bare) return <div>{content}</div>;

  return (
    <div className="v2-container v2-container--content" style={{ paddingBlock: "var(--v2-space-16)" }}>
      {content}
    </div>
  );
}
