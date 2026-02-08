import frappe

frappe.connect(site='vedium.local')

categories = [
    {
        "category": "Inglês Executivo",
        "description": "Cursos de inglês para profissionais e negócios globais"
    },
    {
        "category": "Hebraico Tech",
        "description": "Hebraico moderno para tecnologia e startups"
    },
    {
        "category": "Iorubá Ancestral",
        "description": "Língua e cultura iorubá tradicional"
    }
]

for cat in categories:
    try:
        doc = frappe.get_doc({
            "doctype": "LMS Category",
            "category": cat["category"],
            "description": cat["description"]
        })
        doc.insert(ignore_if_duplicate=True)
        frappe.db.commit()
        print(f"✓ Categoria '{cat['category']}' criada com sucesso")
    except Exception as e:
        print(f"✗ Erro ao criar '{cat['category']}': {str(e)}")

print("\n✅ Processo concluído!")
