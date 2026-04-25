import frappe

COURSE_NAMES = [
    ("ingl-s-beginner", "Beginner A1"),
    ("ingl-s-elementary", "Elementary A2"),
    ("ingl-s-pr-intermedi-rio", "Pré-Intermediário B1-"),
    ("ingl-s-intermedi-rio", "Intermediário B1"),
    ("ingl-s-upper-intermedi-rio", "Upper Intermediário B2"),
    ("ingl-s-avan-ado", "Avançado C1"),
]

total_chapters = 0
total_lessons = 0

for cn, label in COURSE_NAMES:
    chapters = frappe.get_all(
        "Course Chapter", filters={"course": cn}, fields=["name", "title"]
    )
    lesson_count = frappe.db.count("Course Lesson", filters={"course": cn})
    print(f"  [{label}] {len(chapters)} chapters | {lesson_count} lessons")
    total_chapters += len(chapters)
    total_lessons += lesson_count

print(f"\n  TOTAL: {total_chapters} chapters | {total_lessons} lessons")
