import frappe

# Verificar campos obrigatórios de Course Lesson e Course Chapter
cl_meta = frappe.get_meta("Course Lesson")
print("=== Course Lesson - campos reqd ===")
for f in cl_meta.fields:
    if f.reqd:
        print(f"  REQD: {f.fieldname} ({f.fieldtype})")

print("\n=== Course Lesson - TODOS os campos ===")
for f in cl_meta.fields[:20]:
    print(f"  {f.fieldname} ({f.fieldtype}) reqd={f.reqd}")

cc_meta = frappe.get_meta("Course Chapter")
print("\n=== Course Chapter - campos reqd ===")
for f in cc_meta.fields:
    if f.reqd:
        print(f"  REQD: {f.fieldname} ({f.fieldtype})")

print("\n=== Course Chapter - TODOS ===")
for f in cc_meta.fields[:15]:
    print(f"  {f.fieldname} ({f.fieldtype}) reqd={f.reqd}")
