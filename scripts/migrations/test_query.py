import frappe

# Testar a query de cursos com os campos corrigidos
try:
    courses = frappe.get_all(
        "LMS Course",
        fields=[
            "name",
            "title",
            "short_introduction",
            "image",
            "category",
            "paid_course",
            "course_price",
            "currency",
        ],
        filters={"published": 1},
        limit=50,
    )
    print(f"✅ Query OK — {len(courses)} cursos encontrados")
    for c in courses:
        print(f"  • {c.name} | {c.title} | R${c.course_price}")
except Exception as e:
    print(f"❌ Erro: {e}")
