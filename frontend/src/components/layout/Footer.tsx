import Link from "next/link";
import { Icon } from "@/components/ui/Icon";
import { TrackedWhatsappLink } from "@/components/ui/TrackedWhatsappLink";
import { LEVEL_TEST_HREF, WHATSAPP_HREF } from "@/content/site/header";
import {
  FOOTER_BOTTOM_LEFT,
  FOOTER_BRAND_SIGNATURE,
  FOOTER_COURSE_LINKS,
  FOOTER_HELP_LINKS,
  FOOTER_LEGAL_LINKS,
  FOOTER_SEO_GROUPS,
  FOOTER_SOCIAL_LINKS,
  FOOTER_VEDIUM_LINKS,
  FOOTER_WHATSAPP_NUMBER,
} from "@/content/site/footer";

export function Footer() {
  return (
    <footer className="v2-footer">
      <div className="v2-container v2-container--wide">
        <div className="v2-footer__grid">
          <div>
            <Link href="/" aria-label="Vedium">
              <img
                className="v2-footer__logo"
                src="/assets/vedium_core/vedium_assets/images/logos/logo-branca-reta.png"
                alt="Vedium"
                width={132}
                height={32}
              />
            </Link>
            <p className="v2-footer__brand-signature">{FOOTER_BRAND_SIGNATURE}</p>
            <div className="v2-footer__social">
              {FOOTER_SOCIAL_LINKS.map((social) => (
                <a key={social.href} href={social.href} target="_blank" rel="noopener" aria-label={social.label}>
                  <Icon name={social.icon} decorative={false} label={social.label} />
                </a>
              ))}
            </div>
          </div>

          <div>
            <p className="v2-footer__heading">Cursos</p>
            <nav className="v2-footer__links" aria-label="Cursos">
              {FOOTER_COURSE_LINKS.map((link) => (
                <Link key={link.href} href={link.href}>
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>

          <div>
            <p className="v2-footer__heading">Vedium</p>
            <nav className="v2-footer__links" aria-label="Vedium">
              {FOOTER_VEDIUM_LINKS.map((link) => (
                <Link key={link.href} href={link.href}>
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>

          <div>
            <p className="v2-footer__heading">Ajuda</p>
            <nav className="v2-footer__links" aria-label="Ajuda">
              {FOOTER_HELP_LINKS.map((link) => (
                <Link key={link.href} href={link.href === "/teste-de-nivel" ? LEVEL_TEST_HREF : link.href}>
                  {link.label}
                </Link>
              ))}
            </nav>
            <TrackedWhatsappLink href={WHATSAPP_HREF} label={FOOTER_WHATSAPP_NUMBER} className="v2-footer__whatsapp">
              <Icon name="whatsapp" decorative={false} label="WhatsApp" />{" "}
              <span className="v2-footer__whatsapp-number">{FOOTER_WHATSAPP_NUMBER}</span>
            </TrackedWhatsappLink>
          </div>

          <div>
            <p className="v2-footer__heading">Legal</p>
            <nav className="v2-footer__links" aria-label="Legal">
              {FOOTER_LEGAL_LINKS.map((link) => (
                <Link key={link.href} href={link.href}>
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
        </div>

        {FOOTER_SEO_GROUPS.map((group) => (
          <div className="v2-footer__seo" key={group.heading}>
            <p className="v2-footer__seo-heading">{group.heading}</p>
            <nav className="v2-footer__seo-links" aria-label={group.heading}>
              {group.links.map((link) => (
                <Link key={link.href} href={link.href}>
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
        ))}

        <div className="v2-footer__bottom">
          <span>{FOOTER_BOTTOM_LEFT}</span>
          <span>
            © 2026 Vedium · Desenvolvido por{" "}
            <a href="https://scaledata.com.br" target="_blank" rel="noopener">
              Scaledata
            </a>
          </span>
        </div>
      </div>
    </footer>
  );
}
