"""
Atualiza imagens dos cursos Vedium com fotos humanizadas (pessoas reais).

Fontes: Unsplash (free, sem autenticação)
Critério: imagens com pessoas visíveis, diversidade étnica, contexto educacional/profissional.

Uso:
  Copiar para /home/frappe/frappe-bench/sites/
  bench --site app.vediums.com execute → via run_update_images.sh
"""

import frappe

# ─────────────────────────────────────────────────────────────────────────────
# MAPA: name do LMS Course → nova URL de imagem humanizada
# ─────────────────────────────────────────────────────────────────────────────
COURSE_IMAGES = {
    # ── Iorubá ── foco em pessoas afro-brasileiras / africanas / diáspora ──────
    # Jovem mulher negra sorrindo com livro — aprendizado inicial acolhedor
    "iorub-b-sico": "https://images.unsplash.com/photo-1529390079861-591de354faf5?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Duas mulheres negras em conversa animada — troca cultural / nível médio
    "iorub-intermedi-rio": "https://images.unsplash.com/photo-1573496799652-408c2ac9fe98?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Profissional afro em reunião / contexto acadêmico — Avançado (imagem panorâmica)
    "iorub-avan-ado": "https://images.unsplash.com/photo-1521737852567-6949f3f9f2b5?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Curso antigo "Iorubá para Iniciantes" — mesma imagem do Básico
    "iorub-para-iniciantes": "https://images.unsplash.com/photo-1529390079861-591de354faf5?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # ── Inglês ── foco em adultos diversos em ambiente educacional/executivo ───
    # Mulher jovem com fones, aprendendo online — Beginner
    "ingl-s-beginner": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Grupo diverso de jovens estudando juntos, energia positiva — Elementary
    "ingl-s-elementary": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Pessoa estudando com laptop — Pré-Intermediário (imagem panorâmica)
    "ingl-s-pr-intermedi-rio": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Estudantes colaborando em mesa — Intermediário
    "ingl-s-intermedi-rio": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Profissionais em reunião de negócios — Upper Intermediário
    "ingl-s-upper-intermedi-rio": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # Executivo confiante, retrato profissional — Avançado
    "ingl-s-avan-ado": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
    # ── Português para Estrangeiros ────────────────────────────────────────────
    # Pessoas em ambiente urbano brasileiro — diversidade e brasilidade
    "portugu-s-para-estrangeiros": "https://images.unsplash.com/photo-1543269865-cbf427effbad?w=800&h=450&fit=crop&crop=faces,entropy&q=80",
}


def execute():
    print("\n🖼️  Atualizando imagens dos cursos (fotos humanizadas)")
    print("=" * 58)

    ok = 0
    skip = 0

    for course_name, new_image in COURSE_IMAGES.items():
        exists = frappe.db.exists("LMS Course", course_name)
        if not exists:
            print(f"  ⚠ Curso não encontrado: {course_name}")
            skip += 1
            continue

        frappe.db.set_value("LMS Course", course_name, "image", new_image)
        frappe.db.commit()
        title = frappe.db.get_value("LMS Course", course_name, "title")
        print(f"  ✓ {title}")
        ok += 1

    print(f"\n✅ Concluído: {ok} imagens atualizadas | {skip} ignorados")
    print("=" * 58)


if __name__ == "__main__":
    execute()
