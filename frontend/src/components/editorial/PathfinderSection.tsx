import { PathfinderForm } from "./PathfinderForm";

interface PathfinderSectionProps {
  eyebrow: string;
  title: string;
  lead: string;
  steps: string[];
  languageQuestion: string;
  languages: string[];
  objectiveQuestion: string;
  objectives: string[];
  cta: { text: string; href: string };
}

export function PathfinderSection({
  eyebrow,
  title,
  lead,
  steps,
  languageQuestion,
  languages,
  objectiveQuestion,
  objectives,
  cta,
}: PathfinderSectionProps) {
  return (
    <section className="v2-pathfinder-section">
      <div className="v2-pathfinder-section__panel">
        <div className="v2-pathfinder-section__panel-inner">
          <p className="v2-eyebrow v2-eyebrow--on-dark">{eyebrow}</p>
          <h2 className="v2-heading v2-h2 v2-pathfinder-section__panel-title">{title}</h2>
          <p className="v2-body v2-pathfinder-section__panel-lead">{lead}</p>
          <div className="v2-pathfinder-section__panel-rule" aria-hidden="true" />
          <ol className="v2-pathfinder-section__panel-steps">
            {steps.map((step, index) => (
              <li key={step}>
                <span className="v2-pathfinder-section__panel-step-num">{String(index + 1).padStart(2, "0")}</span>
                <span className="v2-pathfinder-section__panel-step-label">{step}</span>
              </li>
            ))}
          </ol>
        </div>
      </div>
      <div className="v2-pathfinder-section__form-wrap">
        <div className="v2-pathfinder-section__form-inner">
          <PathfinderForm
            languageQuestion={languageQuestion}
            languages={languages}
            objectiveQuestion={objectiveQuestion}
            objectives={objectives}
            cta={cta}
          />
        </div>
      </div>
    </section>
  );
}
