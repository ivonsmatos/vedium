import Link from "next/link";
import { Icon } from "@/components/ui/Icon";

interface CourseIndexIntroProps {
  eyebrow: string;
  title: string;
  lead?: string;
  courses: { name: string; href: string }[];
}

export function CourseIndexIntro({ eyebrow, title, lead, courses }: CourseIndexIntroProps) {
  return (
    <section className="v2-section v2-course-intro">
      <div className="v2-container v2-container--wide">
        <div className="v2-course-intro__grid">
          <div className="v2-course-intro__copy">
            <p className="v2-eyebrow">{eyebrow}</p>
            <h2 className="v2-heading v2-course-intro__title">{title}</h2>
            {lead ? <p className="v2-body v2-body-lg v2-text-muted v2-course-intro__lead">{lead}</p> : null}
          </div>
          <nav className="v2-course-index" aria-label="Índice de cursos">
            <ol className="v2-course-index__list">
              {courses.map((course, index) => (
                <li className="v2-course-index__item" key={course.href}>
                  <Link className="v2-course-index__link" href={course.href}>
                    <span className="v2-course-index__num">{String(index + 1).padStart(2, "0")}</span>
                    <span className="v2-course-index__name">{course.name}</span>
                    <span className="v2-course-index__arrow" aria-hidden="true">
                      <Icon name="arrow-right" size="1em" />
                    </span>
                  </Link>
                </li>
              ))}
            </ol>
          </nav>
        </div>
      </div>
    </section>
  );
}
