import { TextLink } from "@/components/ui/TextLink";
import { LiveClassVideo } from "./LiveClassVideo";

interface LiveClassExperienceProps {
  title: string;
  lead?: string;
  points: { label: string; text: string }[];
  videoSrc?: string;
  videoPoster?: string;
  imageSrc?: string;
  imageAlt?: string;
  cta?: { text: string; href: string };
  onDark?: boolean;
}

export function LiveClassExperience({
  title,
  lead,
  points,
  videoSrc,
  videoPoster,
  imageSrc,
  imageAlt = "",
  cta,
  onDark = false,
}: LiveClassExperienceProps) {
  return (
    <div className={`v2-live-class${onDark ? " v2-live-class--on-dark" : ""}`}>
      {videoSrc && videoPoster ? (
        <div className="v2-live-class__media">
          <LiveClassVideo src={videoSrc} poster={videoPoster} />
        </div>
      ) : imageSrc ? (
        <div className="v2-live-class__media">
          <img src={imageSrc} alt={imageAlt} width={800} height={600} loading="lazy" />
        </div>
      ) : null}
      <div>
        <h2 className="v2-heading v2-h2 v2-live-class__title">{title}</h2>
        {lead ? <p className="v2-body v2-body-lg v2-live-class__lead">{lead}</p> : null}
        <ul className="v2-live-class__list">
          {points.map((point) => (
            <li className="v2-live-class__list-item" key={point.label}>
              <span className="v2-live-class__list-label">{point.label}</span>
              <span className="v2-live-class__list-text">{point.text}</span>
            </li>
          ))}
        </ul>
        {cta ? (
          <div style={{ marginBlockStart: "var(--v2-space-6)" }}>
            <TextLink href={cta.href} size="lg" onDark={onDark}>
              {cta.text}
            </TextLink>
          </div>
        ) : null}
      </div>
    </div>
  );
}
