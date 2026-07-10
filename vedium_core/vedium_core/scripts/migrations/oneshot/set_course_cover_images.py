# -*- coding: utf-8 -*-
"""Define a imagem de capa (LMS Course.image) dos cursos de Espanhol e
Hebraico com fotos do Unsplash (licença Unsplash — uso livre, comercial,
sem exigir atribuição: https://unsplash.com/license).

URLs verificadas manualmente (200 OK, image/jpeg) antes de entrar aqui:
    - espanhol-basico: letreiro luminoso "Hola" — casa com a promessa do
      curso ("do primeiro hola às conversas do dia a dia").
    - espanhol-intermediario: duas pessoas conversando/revisando papéis —
      combina com o foco do nível em sustentar conversa real.
    - espanhol-avancado: bandeira da Espanha ao vento — tom mais maduro/
      premium do nível avançado.
    - hebraico-moderno-a1: vista aérea de Tel Aviv ao entardecer — a
      proposta interna pede explicitamente para NÃO usar simbologia
      religiosa/bíblica no piloto "Moderno" (isso fica reservado para uma
      futura trilha de Hebraico Bíblico), por isso a imagem é da cidade
      moderna, não de um Sêfer Torá ou Estrela de Davi.

Rodar (idempotente — reaplica o valor, sem duplicar nada):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.set_course_cover_images.run
"""

import frappe

_PARAMS = "?auto=format&fit=crop&w=1200&q=80"

COURSE_IMAGES = {
    "espanhol-basico": f"https://images.unsplash.com/photo-1489945052260-4f21c52268b9{_PARAMS}",
    "espanhol-intermediario": f"https://images.unsplash.com/photo-1589395937658-0557e7d89fad{_PARAMS}",
    "espanhol-avancado": f"https://images.unsplash.com/photo-1652954884281-8fb97179c4f9{_PARAMS}",
    "hebraico-moderno-a1": f"https://images.unsplash.com/photo-1547483036-24bc77c79804{_PARAMS}",
}


def run():
    for course, image_url in COURSE_IMAGES.items():
        if not frappe.db.exists("LMS Course", course):
            print(f"  AVISO: curso '{course}' não existe, pulando.")
            continue
        frappe.db.set_value("LMS Course", course, "image", image_url)
        print(f"  ✓ '{course}' → imagem definida.")

    frappe.db.commit()
    print("\n✓ Imagens de capa atualizadas.")
