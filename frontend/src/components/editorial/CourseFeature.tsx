import { TextLink } from "@/components/ui/TextLink";
import type { HomeCourse } from "@/content/home/courses";

interface CourseFeatureProps {
  course: HomeCourse;
  index: number;
  tone?: "brand" | "warm";
}

export function CourseFeature({ course, index, tone = "brand" }: CourseFeatureProps) {
  const indexLabel = String(index).padStart(2, "0");

  return (
    <div className={`v2-course-feature-band v2-course-feature-band--${course.bandTone}`}>
      <div className="v2-container v2-container--wide">
        {course.mediaSrc ? (
          <div className={`v2-course-feature${course.reverse ? " v2-course-feature--reverse" : ""}`}>
            <div className="v2-course-feature__media">
              <img
                src={course.mediaSrc}
                alt={course.mediaAlt}
                width={800}
                height={600}
                loading="lazy"
                style={{ objectPosition: course.objectPosition }}
              />
            </div>
            <div className="v2-course-feature__content">
              <p className="v2-eyebrow">
                <span className="v2-course-feature__index">{indexLabel}</span>
                {course.displayName}
              </p>
              {course.levelSummary ? <p className="v2-course-feature__level">{course.levelSummary}</p> : null}
              <h3 className="v2-heading v2-h3 v2-course-feature__headline">{course.headline}</h3>
              <p className="v2-body v2-text-muted v2-course-feature__text">{course.description}</p>
              <TextLink href={course.url} size="lg">
                {course.ctaLabel}
              </TextLink>
            </div>
          </div>
        ) : (
          <div className={`v2-course-feature v2-course-feature--tone-${tone}`}>
            <div className="v2-course-feature__content">
              <p className={`v2-eyebrow${tone === "brand" ? " v2-eyebrow--on-dark" : ""}`}>
                <span className="v2-course-feature__index">{indexLabel}</span>
                {course.displayName}
              </p>
              {course.levelSummary ? <p className="v2-course-feature__level">{course.levelSummary}</p> : null}
              <h3 className="v2-heading v2-h3 v2-course-feature__headline">{course.headline}</h3>
              <p className="v2-body v2-course-feature__text">{course.description}</p>
              <TextLink href={course.url} size="lg" onDark={tone === "brand"}>
                {course.ctaLabel}
              </TextLink>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
