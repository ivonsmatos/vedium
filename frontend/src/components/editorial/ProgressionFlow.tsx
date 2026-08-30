import Link from "next/link";

interface ProgressionFlowProps {
  title: string;
  text: string;
  steps: { label: string; note?: string; href?: string | null }[];
}

export function ProgressionFlow({ title, text, steps }: ProgressionFlowProps) {
  return (
    <div>
      <h2 className="v2-heading v2-h2 v2-progression-flow__title">{title}</h2>
      <p className="v2-body v2-body-lg v2-text-muted v2-measure" style={{ marginBlockEnd: "var(--v2-space-10)" }}>
        {text}
      </p>
      <div className="v2-progression">
        <div className="v2-progression__rail" aria-hidden="true" />
        <ol className="v2-progression__steps">
          {steps.map((step) => (
            <li className="v2-progression__step" key={step.label}>
              <span className="v2-progression__dot" aria-hidden="true" />
              {step.href ? (
                // .v2-scope a{color:inherit} (0,1,1) tem mais especificidade que uma
                // unica classe (0,1,0) -- mesma armadilha ja documentada pra .v2-btn
                // em components-base.css. Em vez de arriscar a cor errada no <a>,
                // a classe/cor fica no <span> filho (aplicada diretamente a ele).
                <Link href={step.href}>
                  <span className="v2-progression__label">{step.label}</span>
                </Link>
              ) : (
                <span className="v2-progression__label">{step.label}</span>
              )}
              {step.note ? <span className="v2-progression__note">{step.note}</span> : null}
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
