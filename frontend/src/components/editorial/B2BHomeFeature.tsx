import { Button } from "@/components/ui/Button";
import { TextLink } from "@/components/ui/TextLink";

interface B2BHomeFeatureProps {
  eyebrow: string;
  subEyebrow: string;
  title: string;
  text: string;
  text2?: string;
  proofItems: { label: string; text: string }[];
  primaryCta: { text: string; href: string };
  secondaryCta?: { text: string; href: string };
  imageSrc: string;
  imageAlt: string;
  objectPosition?: string;
}

export function B2BHomeFeature({
  eyebrow,
  subEyebrow,
  title,
  text,
  text2,
  proofItems,
  primaryCta,
  secondaryCta,
  imageSrc,
  imageAlt,
  objectPosition = "center",
}: B2BHomeFeatureProps) {
  return (
    <div className="v2-b2b-feature">
      <div className="v2-b2b-feature__media">
        <img src={imageSrc} alt={imageAlt} width={800} height={600} loading="lazy" style={{ objectPosition }} />
      </div>
      <div className="v2-b2b-feature__content">
        <p className="v2-eyebrow v2-eyebrow--on-dark v2-b2b-feature__eyebrow">{eyebrow}</p>
        <p className="v2-b2b-feature__sub-eyebrow">{subEyebrow}</p>
        <h2 className="v2-heading v2-b2b-feature__title">{title}</h2>
        <p className="v2-b2b-feature__text">{text}</p>
        {text2 ? <p className="v2-b2b-feature__text2">{text2}</p> : null}
        <div className="v2-b2b-feature__proof">
          {proofItems.map((item) => (
            <div className="v2-b2b-feature__proof-item" key={item.label}>
              <p className="v2-b2b-feature__proof-label">{item.label}</p>
              <p className="v2-b2b-feature__proof-text">{item.text}</p>
            </div>
          ))}
        </div>
        <div className="v2-b2b-feature__actions">
          <Button href={primaryCta.href} variant="primary" onDark>
            {primaryCta.text}
          </Button>
          {secondaryCta ? (
            <TextLink href={secondaryCta.href} size="default" onDark>
              {secondaryCta.text}
            </TextLink>
          ) : null}
        </div>
      </div>
    </div>
  );
}
