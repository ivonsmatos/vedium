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
    - hebraico-a0-alfabetizacao: tábuas com o alef-bet (letras hebraicas) —
      alfabetização, casa com "ler as letras".
    - hebraico-moderno-a2-b1: rua moderna de Tel Aviv (bikes, ciclovia) —
      continuidade do tom "Moderno", cidade contemporânea.
    - hebraico-biblico-leitura-guiada: beco de pedra antiga da cidade velha
      de Jerusalém — patrimônio histórico/textual, sem marco religioso-
      político proeminente (os docs pedem "leitura responsável, sem debate
      religioso ou político"), por isso NÃO um domo/templo/estrela.
    - hebraico-particular: aluno em estudo individual focado — casa com a
      proposta 1:1/plano personalizado.

Todas de images.unsplash.com (Licença Unsplash, uso comercial livre, sem
atribuição). Evitadas as premium_photo de plus.unsplash.com (Unsplash+, que
tem licença paga diferente).

Rodar (idempotente — reaplica o valor, sem duplicar nada):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.set_course_cover_images.run

2026-07-15: w reduzido de 1200 para 900 -- PageSpeed Insights (achado real,
LCP de 6,9s na home) apontou essas imagens sendo entregues em ~1200px de
largura para uma área exibida de ~669px (curso.html renderiza a capa numa
coluna de conteúdo, não em tela cheia), desperdiçando ~383 KiB no total.
900px cobre com folga até telas retina (2x) na largura real exibida.
"""

import frappe

_PARAMS = "?auto=format&fit=crop&w=900&q=80"

COURSE_IMAGES = {
    "espanhol-basico": f"https://images.unsplash.com/photo-1489945052260-4f21c52268b9{_PARAMS}",
    "espanhol-intermediario": f"https://images.unsplash.com/photo-1589395937658-0557e7d89fad{_PARAMS}",
    "espanhol-avancado": f"https://images.unsplash.com/photo-1652954884281-8fb97179c4f9{_PARAMS}",
    "hebraico-moderno-a1": f"https://images.unsplash.com/photo-1547483036-24bc77c79804{_PARAMS}",
    "hebraico-a0-alfabetizacao": f"https://images.unsplash.com/photo-1567941537734-176cd52219e0{_PARAMS}",
    "hebraico-moderno-a2-b1": f"https://images.unsplash.com/photo-1664989461662-c762c8c26e5e{_PARAMS}",
    "hebraico-biblico-leitura-guiada": f"https://images.unsplash.com/photo-1677750844105-446e04b84dad{_PARAMS}",
    "hebraico-particular": f"https://images.unsplash.com/photo-1759984782106-4b56d0aa05b8{_PARAMS}",
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
