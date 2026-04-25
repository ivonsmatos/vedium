import frappe

# Cursos de inglês criados
COURSE_NAMES = [
    "ingl-s-beginner",
    "ingl-s-elementary",
    "ingl-s-pr-intermedi-rio",
    "ingl-s-intermedi-rio",
    "ingl-s-upper-intermedi-rio",
    "ingl-s-avan-ado",
]

print("=== Limpando Course Lessons sem chapter válido ===")
# Busca lessons sem chapter (chapter vazio ou None)
orphan_lessons = frappe.db.sql(
    "SELECT name, title, chapter FROM `tabCourse Lesson` WHERE chapter IS NULL OR chapter = ''",
    as_dict=True,
)
print(f"  Lessons sem chapter: {len(orphan_lessons)}")
for les in orphan_lessons:
    frappe.delete_doc("Course Lesson", les.name, force=True, ignore_permissions=True)
    print(f"  ✗ Deletada lesson sem chapter: {les.name} | {les.title}")

print("\n=== Limpando Course Chapters sem lessons ===")
for cn in COURSE_NAMES:
    chapters = frappe.get_all(
        "Course Chapter", filters={"course": cn}, fields=["name", "title"]
    )
    for ch in chapters:
        lesson_refs = frappe.get_all("Lesson Reference", filters={"parent": ch.name})
        if not lesson_refs:
            frappe.delete_doc(
                "Course Chapter", ch.name, force=True, ignore_permissions=True
            )
            print(f"  ✗ Deletado chapter vazio: {ch.name} | {ch.title}")

frappe.db.commit()
print("\n✅ Limpeza concluída!")

# Mostrar status atual
print("\n=== Status dos capítulos por curso ===")
for cn in COURSE_NAMES:
    chapters = frappe.get_all(
        "Course Chapter", filters={"course": cn}, fields=["name", "title"]
    )
    print(f"  {cn}: {len(chapters)} chapters")
