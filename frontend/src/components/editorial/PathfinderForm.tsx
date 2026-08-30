"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { PATHFINDER_MATRIX } from "@/content/home/pathfinder";
import { trackPathfinderGoalSelect, trackPathfinderLanguageSelect, trackPathfinderSubmit } from "@/lib/analytics/event";

interface PathfinderFormProps {
  languageQuestion: string;
  languages: string[];
  objectiveQuestion: string;
  objectives: string[];
  cta: { text: string; href: string };
}

export function PathfinderForm({ languageQuestion, languages, objectiveQuestion, objectives, cta }: PathfinderFormProps) {
  const router = useRouter();
  const [language, setLanguage] = useState(languages[0]);
  const [objective, setObjective] = useState(objectives[0]);

  function resolveDestination(): string | null {
    const entry = PATHFINDER_MATRIX[language];
    if (!entry) return null;
    return entry[objective] ?? entry._pillar ?? null;
  }

  function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    const destination = resolveDestination();
    trackPathfinderSubmit(language, objective, destination || null);
    if (!destination) return; // deixa o <form> submeter nativo pro action (fallback seguro)
    event.preventDefault();
    router.push(destination);
  }

  return (
    <form className="v2-pathfinder" action={cta.href} method="get" onSubmit={onSubmit}>
      <fieldset className="v2-pathfinder__group">
        <legend className="v2-pathfinder__question">
          <span className="v2-pathfinder__question-num">01</span>
          <span>{languageQuestion}</span>
        </legend>
        <div className="v2-pathfinder__options">
          {languages.map((option) => (
            <label className="v2-pathfinder__option" key={option}>
              <input
                type="radio"
                name="pathfinder-idioma"
                value={option}
                checked={language === option}
                onChange={() => {
                  setLanguage(option);
                  trackPathfinderLanguageSelect(option);
                }}
              />
              <span>{option}</span>
            </label>
          ))}
        </div>
      </fieldset>
      <fieldset className="v2-pathfinder__group">
        <legend className="v2-pathfinder__question">
          <span className="v2-pathfinder__question-num">02</span>
          <span>{objectiveQuestion}</span>
        </legend>
        <div className="v2-pathfinder__options">
          {objectives.map((option) => (
            <label className="v2-pathfinder__option" key={option}>
              <input
                type="radio"
                name="pathfinder-objetivo"
                value={option}
                checked={objective === option}
                onChange={() => {
                  setObjective(option);
                  trackPathfinderGoalSelect(option);
                }}
              />
              <span>{option}</span>
            </label>
          ))}
        </div>
      </fieldset>
      <Button type="submit" variant="primary">
        {cta.text}
      </Button>
    </form>
  );
}
