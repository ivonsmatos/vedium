"""Publica o lote de 33 artigos prontos de Cliente/Vedium/Artigos no
doctype nativo "Vedium Blog Post", respeitando o calendário editorial
(vedium_calendario_editorial_seo_geo_318_posts.xlsx).

Escopo deste lote: os 33 .md encontrados na pasta de artigos, todos com
`Data <= 2026-07-03` no calendário. Inclui os 2 artigos em zh-CN e ru-RU
(90-day / 90-дневный plano de português para estrangeiros) -- o campo
`Vedium Blog Post.lang` foi ampliado (options pt-BR/en/es/fr/de/zh-CN/ru-RU)
a pedido do usuário para acomodá-los.

Cada post foi convertido de Markdown para HTML (título, meta description e
corpo extraídos do próprio .md), com pelo menos 2 links internos reais para
páginas existentes do site, mapeados por idioma + assunto (cluster inglês/
iorubá/português-para-estrangeiros). Ver data/blog_posts_batch_2026_07.json
para o conteúdo já processado.

Idempotente: se o slug já existir como Vedium Blog Post, pula (não
sobrescreve edições feitas depois pelo painel).

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.publish_blog_batch_2026_07.run
"""
import json
import os

import frappe

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "blog_posts_batch_2026_07.json")


def run():
    with open(DATA_FILE, encoding="utf-8") as f:
        posts = json.load(f)

    created, skipped = [], []
    for post in posts:
        slug = post["slug"]
        if frappe.db.exists("Vedium Blog Post", slug):
            skipped.append(slug)
            continue

        doc = frappe.get_doc({
            "doctype": "Vedium Blog Post",
            "title": post["title"],
            "slug": slug,
            "published": 1,
            "tag": post["tag"],
            "date": post["date"],
            "lang": post["lang"],
            "meta_description": post["meta_description"],
            "hero_image": post["hero_image"],
            "hero_alt": post["hero_alt"],
            "lead": post.get("lead") or "",
            "content": post["content"],
            "cta_title": post.get("cta_title") or "",
            "cta_text": post.get("cta_text") or "",
            "cta_label": post["cta_label"],
            "cta_url": post["cta_url"],
            "faqs": [
                {"question": faq["question"], "answer": faq["answer"]}
                for faq in post.get("faqs", [])
            ],
        })
        doc.insert(ignore_permissions=True)
        created.append(slug)

    frappe.db.commit()

    print("=== Publicados agora ===")
    for slug in created:
        print("  +", slug)
    print("=== Já existiam (ignorados) ===")
    for slug in skipped:
        print("  -", slug)
    print(f"\nResumo: {len(created)} publicados, {len(skipped)} já existiam.")
