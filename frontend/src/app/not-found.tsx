import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Button } from "@/components/ui/Button";
import { TrackedWhatsappLink } from "@/components/ui/TrackedWhatsappLink";
import { WHATSAPP_HREF } from "@/content/site/header";

/**
 * Página 404 real (Fase G.1 seção 17). O App Router do Next já responde
 * com status HTTP 404 de verdade para qualquer rota sem match -- este
 * componente só define o QUE aparece nessa resposta (mesmo Design
 * System, sem virar landing page).
 */
export default function NotFound() {
  return (
    <main>
      <Header />
      <section className="v2-section v2-section--brand">
        <div className="v2-container v2-container--content">
          <div className="v2-cta-section v2-cta-section--brand-full">
            <div>
              <p className="v2-eyebrow v2-eyebrow--on-dark" style={{ marginBlockEnd: "var(--v2-space-3)" }}>
                ERRO 404
              </p>
              <h1 className="v2-heading v2-cta-section__title">Essa página não existe.</h1>
              <p className="v2-body v2-body-lg v2-cta-section__text">
                O endereço pode ter mudado ou não estar mais disponível. Volte para a Home, conheça os cursos ou fale com a Vedium.
              </p>
            </div>
            <div className="v2-hero__actions">
              <Button href="/" variant="primary">
                Voltar para a Home
              </Button>
              <Button href="/cursos-de-idiomas-online" variant="secondary" onDark>
                Ver cursos
              </Button>
              <TrackedWhatsappLink href={WHATSAPP_HREF} label="Falar com a Vedium" className="v2-text-link v2-text-link--on-dark">
                <span>Falar com a Vedium</span>
              </TrackedWhatsappLink>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </main>
  );
}
