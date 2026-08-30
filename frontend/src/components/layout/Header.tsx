import Link from "next/link";
import { Icon } from "@/components/ui/Icon";
import { Button } from "@/components/ui/Button";
import { TrackedWhatsappLink } from "@/components/ui/TrackedWhatsappLink";
import { MobileMenuToggle } from "./MobileMenuToggle";
import { CoursesMegaTrigger } from "./CoursesMegaTrigger";
import { LocaleSwitcher } from "./LocaleSwitcher";
import { HeaderOverlayScroll } from "./HeaderOverlayScroll";
import {
  HEADER_COURSES,
  HEADER_MEGA_MEDIA_SRC,
  HEADER_NAV_TEXT_PT,
  LEVEL_TEST_HREF,
  LOCALE_NAV_URLS,
  LOCALE_OPTIONS,
  STUDENT_AREA_HREF,
  WHATSAPP_HREF,
  type PrimaryCtaOverride,
} from "@/content/site/header";

interface HeaderProps {
  overlay?: boolean;
  primaryCtaOverride?: PrimaryCtaOverride;
}

export function Header({ overlay = false, primaryCtaOverride }: HeaderProps) {
  const t = HEADER_NAV_TEXT_PT;
  const ctaText = primaryCtaOverride?.text ?? t.testeNivel;
  const ctaHref = primaryCtaOverride?.href ?? LEVEL_TEST_HREF;

  const utilityBar = (
    <div className={`v2-hdr-utility${overlay ? " v2-hdr-utility--overlay" : ""}`}>
      <div className="v2-container v2-container--wide v2-hdr-utility__bar">
        <a className="v2-hdr-utility__link" href={STUDENT_AREA_HREF}>
          {t.aluno}
        </a>
        <div className="v2-hdr-utility__right">
          <TrackedWhatsappLink href={WHATSAPP_HREF} label="WhatsApp" className="v2-hdr-utility__link">
            <Icon name="whatsapp" decorative={false} label="WhatsApp" size="0.95em" />
            <span>WhatsApp</span>
          </TrackedWhatsappLink>
          <LocaleSwitcher options={LOCALE_OPTIONS} navUrls={LOCALE_NAV_URLS} currentLocale="pt-br" />
        </div>
      </div>
    </div>
  );

  const headerEl = (
    <header
      className={`v2-header${overlay ? " v2-header--overlay" : ""}`}
      data-v2-header
      data-menu-open="false"
      data-vd-nav-current="pt-br"
      data-vd-nav-urls={JSON.stringify(LOCALE_NAV_URLS)}
    >
      <div className="v2-container v2-container--wide">
        <div className="v2-header__bar">
          <Link className={`v2-header__logo${overlay ? " v2-header__logo--overlay" : ""}`} href="/" aria-label="Vedium">
            {overlay ? (
              <>
                <img
                  className="v2-header__logo-img v2-header__logo-img--white"
                  src="/assets/vedium_core/vedium_assets/images/logos/logo-branca-reta.png"
                  alt="Vedium"
                  width={132}
                  height={32}
                />
                <img
                  className="v2-header__logo-img v2-header__logo-img--color"
                  src="/assets/vedium_core/vedium_assets/images/logos/logo-color-reta.png"
                  alt=""
                  width={132}
                  height={32}
                  aria-hidden="true"
                />
              </>
            ) : (
              <img
                src="/assets/vedium_core/vedium_assets/images/logos/logo-color-reta.png"
                alt="Vedium"
                width={132}
                height={32}
              />
            )}
          </Link>

          <nav className="v2-header__nav" aria-label="Principal">
            <div className="v2-header__nav-item" data-v2-nav-item data-mega-open="false">
              <CoursesMegaTrigger label={t.cursos} />
              <div className="v2-header__mega" data-v2-mega>
                <div className="v2-header__mega-grid">
                  <div>
                    <p className="v2-header__mega-heading">{t.cursosHeading}</p>
                    <div className="v2-header__mega-links">
                      {HEADER_COURSES.map((course) => (
                        <Link key={course.href} className="v2-header__mega-link" href={course.href}>
                          {course.label}
                        </Link>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="v2-header__mega-heading">{t.atalhosHeading}</p>
                    <div className="v2-header__mega-links">
                      <Link className="v2-header__mega-secondary-link" href="/professores">
                        {t.professores}
                      </Link>
                      <Link className="v2-header__mega-secondary-link" href="/empresas">
                        {t.empresas}
                      </Link>
                      <Link className="v2-header__mega-secondary-link" href={LEVEL_TEST_HREF}>
                        {t.testeNivel}
                      </Link>
                    </div>
                  </div>
                  <div className="v2-header__mega-media">
                    <img src={HEADER_MEGA_MEDIA_SRC} alt="" width={240} height={300} loading="lazy" style={{ objectPosition: "top center" }} />
                  </div>
                </div>
              </div>
            </div>
            <Link className="v2-header__nav-link" href="/como-funciona">
              {t.comoFunciona}
            </Link>
            <Link className="v2-header__nav-link" href="/empresas">
              {t.empresas}
            </Link>
            <Link className="v2-header__nav-link" href="/blog">
              {t.blog}
            </Link>
            <Link className="v2-header__nav-link" href="/sobre">
              {t.sobre}
            </Link>
          </nav>

          <div className="v2-header__actions">
            <Button href={ctaHref} variant="primary" size="compact" style={{ paddingInline: "var(--v2-space-5)" }}>
              {ctaText}
            </Button>
            <MobileMenuToggle />
          </div>
        </div>

        <div className="v2-header__mobile-panel" id="v2-header-mobile-panel">
          {HEADER_COURSES.map((course) => (
            <Link key={course.href} className="v2-header__mobile-link" href={course.href}>
              {course.label}
            </Link>
          ))}
          <Link className="v2-header__mobile-link" href="/como-funciona">
            {t.comoFunciona}
          </Link>
          <Link className="v2-header__mobile-link" href="/professores">
            {t.professores}
          </Link>
          <Link className="v2-header__mobile-link" href="/empresas">
            {t.empresas}
          </Link>
          <Link className="v2-header__mobile-link" href="/blog">
            {t.blog}
          </Link>
          <Link className="v2-header__mobile-link" href="/sobre">
            {t.sobre}
          </Link>
          <a className="v2-header__mobile-link" href={STUDENT_AREA_HREF}>
            {t.aluno}
          </a>
        </div>
      </div>
    </header>
  );

  if (overlay) {
    return (
      <div className="v2-header-overlay-wrap" data-v2-header-overlay>
        {utilityBar}
        {headerEl}
        <HeaderOverlayScroll />
      </div>
    );
  }

  return (
    <>
      {utilityBar}
      {headerEl}
    </>
  );
}
