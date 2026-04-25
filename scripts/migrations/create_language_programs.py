"""
Script de criação das categorias-pai de idiomas da Vedium.
Estrutura hierárquica extensível:

  Inglês            → 6 níveis (Beginner → Advanced)
  Iorubá            → placeholder (cursos a serem cadastrados)
  Português para Estrangeiros → placeholder (cursos a serem cadastrados)

Uso dentro do container Frappe:
  bench --site vediums.com execute create_language_programs.execute

Ou diretamente no bench shell:
  bench --site vediums.com console
  >>> import create_language_programs; create_language_programs.execute()
"""

import frappe


# ─────────────────────────────────────────────
# Idiomas e suas descrições / metadados
# ─────────────────────────────────────────────
LANGUAGE_PROGRAMS = [
    {
        "title": "Inglês",
        "slug": "ingles",
        "description": (
            "Programa completo de Inglês em 6 níveis: Beginner, Elementary, "
            "Pré-Intermediário, Intermediário, Upper Intermediário e Avançado. "
            "Currículo baseado no quadro CEFR (A1–C1) com foco em fluência para "
            "carreira global, negócios e viagens."
        ),
        "icon": "🇬🇧",
        "status": "active",
    },
    {
        "title": "Iorubá",
        "slug": "ioruba",
        "description": (
            "Programa de Iorubá Ancestral — língua e cultura iorubá para conexão "
            "com as raízes africanas. Módulos de conversação, vocabulário cotidiano "
            "e expressões culturais. Em breve."
        ),
        "icon": "🌍",
        "status": "coming_soon",
    },
    {
        "title": "Português para Estrangeiros",
        "slug": "portugues-estrangeiros",
        "description": (
            "Programa de Português Brasileiro para não-nativos. Do básico ao avançado, "
            "com foco em comunicação real, cultura brasileira e preparo para o CELPE-Bras. "
            "Em breve."
        ),
        "icon": "🇧🇷",
        "status": "coming_soon",
    },
]

# ─────────────────────────────────────────────
# Sub-níveis do Inglês (mapeados como LMS Category)
# ─────────────────────────────────────────────
ENGLISH_LEVELS = [
    {
        "title": "Inglês - Beginner",
        "parent_category": "Inglês",
        "level_code": "A1",
        "description": (
            "Nível Iniciante (A1/CEFR). Vocabulário essencial, cumprimentos, "
            "números, família, rotina. 14 unidades com estruturas gramaticais básicas."
        ),
        "sort_order": 1,
    },
    {
        "title": "Inglês - Elementary",
        "parent_category": "Inglês",
        "level_code": "A2",
        "description": (
            "Nível Elementar (A2/CEFR). Present Simple/Continuous, Past Simple, "
            "can/can't. Conversações cotidianas, habilidades e vida em família. 12 unidades."
        ),
        "sort_order": 2,
    },
    {
        "title": "Inglês - Pré-Intermediário",
        "parent_category": "Inglês",
        "level_code": "B1-",
        "description": (
            "Nível Pré-Intermediário (B1-). Present Perfect, condicionais, "
            "passiva, quantificadores. Expressões do dia a dia. 12 unidades."
        ),
        "sort_order": 3,
    },
    {
        "title": "Inglês - Intermediário",
        "parent_category": "Inglês",
        "level_code": "B1",
        "description": (
            "Nível Intermediário (B1/CEFR). Todos os tempos verbais, modais, "
            "reported speech, conditionals. Situações complexas de comunicação. 12 unidades."
        ),
        "sort_order": 4,
    },
    {
        "title": "Inglês - Upper Intermediário",
        "parent_category": "Inglês",
        "level_code": "B2",
        "description": (
            "Nível Upper Intermediate (B2/CEFR). Sistema de tempos, advérbios, "
            "modais avançados, hipóteses, artigos e linking devices. 12 unidades."
        ),
        "sort_order": 5,
    },
    {
        "title": "Inglês - Avançado",
        "parent_category": "Inglês",
        "level_code": "C1",
        "description": (
            "Nível Avançado (C1/CEFR). Inversão negativa, ênfase, discourse markers, "
            "passive reporting, futuro avançado, phrasal verbs complexos. 12 unidades."
        ),
        "sort_order": 6,
    },
]


def _create_or_update_category(data: dict, parent: str = None) -> None:
    """Cria ou atualiza um LMS Category."""
    category_name = data["title"]

    if frappe.db.exists("LMS Category", category_name):
        print(f"  → Já existe: {category_name}")
        return

    doc = frappe.get_doc(
        {
            "doctype": "LMS Category",
            "category": category_name,
            "description": data.get("description", ""),
        }
    )

    # Tenta atribuir parent se o campo existir no doctype
    try:
        meta = frappe.get_meta("LMS Category")
        field_names = [f.fieldname for f in meta.fields]
        if "parent_category" in field_names and parent:
            doc.parent_category = parent
        if "sort_order" in field_names and "sort_order" in data:
            doc.sort_order = data["sort_order"]
    except Exception:
        pass

    doc.insert(ignore_if_duplicate=True)
    frappe.db.commit()
    print(f"  ✓ Criada: {category_name}")


def execute():
    """Entry point para bench execute."""
    print("\n🌐 Criando estrutura de programas de idiomas Vedium...")
    print("=" * 55)

    # 1. Idiomas principais
    print("\n[ Idiomas principais ]")
    for lang in LANGUAGE_PROGRAMS:
        _create_or_update_category(lang)

    # 2. Sub-níveis do Inglês
    print("\n[ Níveis do Inglês ]")
    for level in ENGLISH_LEVELS:
        _create_or_update_category(level, parent="Inglês")

    print("\n✅ Estrutura de idiomas criada com sucesso!")
    print(
        "   Idiomas disponíveis: Inglês (6 níveis), Iorubá, Português para Estrangeiros"
    )
    print("   Para adicionar cursos: execute create_english_courses.py")
    print("=" * 55)


if __name__ == "__main__":
    # Execução direta via bench console ou após frappe.connect()
    # bench --site vediums.com console
    # >>> exec(open('create_language_programs.py').read())
    execute()
