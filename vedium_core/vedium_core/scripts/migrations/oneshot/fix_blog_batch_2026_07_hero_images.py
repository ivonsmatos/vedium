"""Corrige a repeticao de imagens de capa no lote de 33 artigos publicado
por publish_blog_batch_2026_07.py (so 3 imagens distintas pra 33 posts --
o usuario notou e pediu correcao). data/blog_posts_batch_2026_07.json ja
foi atualizado com 27 imagens distintas (round-robin por data, sem duas
publicacoes adjacentes repetindo a mesma foto); este script so aplica o
UPDATE nos registros que ja estao no banco (o oneshot de publicacao original
e insert-only e nao mexe em posts existentes).

Idempotente: sempre reescreve hero_image pro valor atual do JSON.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.fix_blog_batch_2026_07_hero_images.run
"""
import json
import os

import frappe

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "data", "blog_posts_batch_2026_07.json"
)


def run():
    with open(DATA_FILE, encoding="utf-8") as f:
        posts = json.load(f)

    updated, skipped = [], []
    for post in posts:
        slug = post["slug"]
        if not frappe.db.exists("Vedium Blog Post", slug):
            skipped.append(slug)
            continue
        frappe.db.set_value(
            "Vedium Blog Post", slug, "hero_image", post["hero_image"]
        )
        updated.append(slug)

    frappe.db.commit()

    print(f"Resumo: {len(updated)} imagens atualizadas, {len(skipped)} posts nao encontrados.")
    for slug in skipped:
        print("  - nao encontrado:", slug)
