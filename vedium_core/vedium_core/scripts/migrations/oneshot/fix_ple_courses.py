"""Corrige os cursos PLE criados: preço → $120 USD, título da aula, descrições sem referência ao livro.

bench execute vedium_core.scripts.migrations.oneshot.fix_ple_courses.run
"""

import frappe

PLE_SLUGS = [
    "portugues-para-estrangeiros-basico",
    "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-avancado",
]

DESCRIPTIONS = {
    "portugues-para-estrangeiros-basico": (
        "<p>O curso <strong>PLE Básico</strong> é destinado a quem não tem nenhum conhecimento "
        "ou tem contato muito limitado com o português. Você aprenderá as estruturas essenciais "
        "e o vocabulário necessário para se comunicar em situações do dia a dia, com "
        "forte imersão na cultura brasileira.</p>"
        "<p><strong>Ao final do curso você será capaz de:</strong></p>"
        "<ul>"
        "<li>Usar saudações, apresentações e despedidas</li>"
        "<li>Fornecer e solicitar informações pessoais (nome, nacionalidade, idade, profissão)</li>"
        "<li>Formular frases simples no presente do indicativo</li>"
        "<li>Pedir em restaurantes, fazer compras e perguntar direções</li>"
        "<li>Compreender aspectos culturais básicos do Brasil</li>"
        "</ul>"
    ),
    "portugues-para-estrangeiros-intermediario": (
        "<p>O curso <strong>PLE Intermediário</strong> é para quem já tem uma base sólida em "
        "português e deseja expandir a capacidade de comunicação em contextos mais variados "
        "e complexos. Este nível aprofunda a gramática, amplia o vocabulário e desenvolve "
        "a fluência em situações sociais e profissionais.</p>"
        "<p><strong>Ao final do curso você será capaz de:</strong></p>"
        "<ul>"
        "<li>Participar de conversas longas e detalhadas sobre variados tópicos</li>"
        "<li>Dominar os tempos verbais do passado (perfeito, imperfeito e mais-que-perfeito)</li>"
        "<li>Lidar com situações como planejar viagens, procurar moradia e falar sobre saúde</li>"
        "<li>Ler e compreender textos de dificuldade moderada (notícias, artigos de opinião)</li>"
        "<li>Reconhecer e discutir aspectos culturais aprofundados do Brasil</li>"
        "</ul>"
    ),
    "portugues-para-estrangeiros-avancado": (
        "<p>O curso <strong>PLE Avançado</strong> é para quem já tem fluência significativa "
        "e deseja aprimorar o uso da língua em contextos acadêmicos, profissionais e culturais "
        "complexos. Este nível traz o modo subjuntivo, análise de textos autênticos e "
        "aprofundamento na cultura e sociedade brasileiras.</p>"
        "<p><strong>Ao final do curso você será capaz de:</strong></p>"
        "<ul>"
        "<li>Compreender e produzir textos complexos — artigos de opinião, ensaios e relatórios</li>"
        "<li>Dominar o modo subjuntivo em suas diversas formas</li>"
        "<li>Participar ativamente de debates sobre temas abstratos e controversos</li>"
        "<li>Utilizar expressões idiomáticas, gírias e nuances da linguagem coloquial e formal</li>"
        "<li>Analisar criticamente aspectos da história, política, literatura e artes do Brasil</li>"
        "</ul>"
    ),
}


def run():
    # 1. Preço e moeda
    for slug in PLE_SLUGS:
        if not frappe.db.exists("LMS Course", slug):
            print(f"  ⚠ Curso '{slug}' não encontrado, pulando.")
            continue
        frappe.db.set_value("LMS Course", slug, {
            "course_price": 120,
            "currency": "USD",
            "description": DESCRIPTIONS[slug],
        })
        print(f"  ✓ {slug}: preço → $120 USD, descrição atualizada.")

    # 2. Título da aula errado
    wrong = "Tudo o Santo Dia — Rotinas diárias e horários"
    correct = "Todo Santo Dia — Rotinas diárias e horários"
    updated = frappe.db.sql(
        "UPDATE `tabCourse Lesson` SET title=%s WHERE title=%s",
        (correct, wrong),
    )
    print(f"  ✓ Aula renomeada: '{wrong}' → '{correct}'")

    frappe.db.commit()
    print("\n✅ Correções aplicadas.")
