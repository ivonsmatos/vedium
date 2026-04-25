"""
Cria as categorias base da Vedium no Frappe LMS.

Estrutura:
  Idiomas (raiz - criados por create_language_programs.py)
  ├── Inglês
  │   ├── Inglês - Beginner
  │   ├── Inglês - Elementary
  │   ├── Inglês - Pré-Intermediário
  │   ├── Inglês - Intermediário
  │   ├── Inglês - Upper Intermediário
  │   └── Inglês - Avançado
  ├── Iorubá               (placeholder)
  └── Português para Estrangeiros  (placeholder)

Categorias originais da Vedium (mantidas para retrocompatibilidade):
  - Inglês Executivo
  - Hebraico Tech
  - Iorubá Ancestral

Uso:
  bench --site vediums.com execute create_categories.execute
"""

import frappe


# ── Categorias legadas (retrocompatibilidade) ──────────────────────────────
LEGACY_CATEGORIES = [
    {
        "category": "Inglês Executivo",
        "description": "Cursos de inglês para profissionais e negócios globais",
    },
    {
        "category": "Hebraico Tech",
        "description": "Hebraico moderno para tecnologia e startups",
    },
    {
        "category": "Iorubá Ancestral",
        "description": "Língua e cultura iorubá tradicional",
    },
]

# ── Categorias do Programa de Inglês (6 níveis) ────────────────────────────
ENGLISH_LEVEL_CATEGORIES = [
    {"category": "Inglês - Beginner", "description": "Nível A1 | Inglês do zero"},
    {"category": "Inglês - Elementary", "description": "Nível A2 | Bases consolidadas"},
    {
        "category": "Inglês - Pré-Intermediário",
        "description": "Nível B1- | Comunicação cotidiana",
    },
    {
        "category": "Inglês - Intermediário",
        "description": "Nível B1 | Fluência em construção",
    },
    {
        "category": "Inglês - Upper Intermediário",
        "description": "Nível B2 | Fluência profissional",
    },
    {"category": "Inglês - Avançado", "description": "Nível C1 | Domínio pleno"},
]

# ── Categorias futuras (placeholders para novos idiomas) ──────────────────
FUTURE_LANGUAGE_CATEGORIES = [
    {
        "category": "Iorubá",
        "description": "Língua e cultura iorubá — em breve na Vedium",
    },
    {
        "category": "Português para Estrangeiros",
        "description": "Português Brasileiro para não-nativos — em breve na Vedium",
    },
]


def _insert_category(cat: dict) -> None:
    name = cat["category"]
    if frappe.db.exists("LMS Category", name):
        print(f"  → Já existe: {name}")
        return
    doc = frappe.get_doc(
        {
            "doctype": "LMS Category",
            "category": name,
            "description": cat.get("description", ""),
        }
    )
    doc.insert(ignore_if_duplicate=True)
    frappe.db.commit()
    print(f"  ✓ Criada: {name}")


def execute():
    """Entry point: bench --site vediums.com execute create_categories.execute"""
    print("\n🏷️  Criando categorias da Vedium...")
    print("=" * 50)

    print("\n[ Categorias legadas ]")
    for cat in LEGACY_CATEGORIES:
        _insert_category(cat)

    print("\n[ Níveis do Programa de Inglês ]")
    for cat in ENGLISH_LEVEL_CATEGORIES:
        _insert_category(cat)

    print("\n[ Idiomas futuros (placeholders) ]")
    for cat in FUTURE_LANGUAGE_CATEGORIES:
        _insert_category(cat)

    print("\n✅ Todas as categorias criadas!")
    print("=" * 50)


if __name__ == "__main__":
    # Execução legada direta (mantida para retrocompatibilidade)
    try:
        frappe.connect(site="vediums.com")
    except Exception:
        pass
    execute()
