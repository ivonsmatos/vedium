import sys

def execute():
    import frappe
    import json
    
    courses_to_find = [
        "Inglês A1", "Inglês A2", "Inglês B1", "Inglês B1+", "Inglês B2", "Inglês C1",
        "Iorubá Básico", "Iorubá Intermediário", "Iorubá Avançado",
        "Espanhol Básico", "Espanhol Intermediário", "Espanhol Avançado",
        "PLE Básico", "PLE Intermediário", "PLE Avançado",
        "Hebraico A0", "Hebraico Moderno A1", "Hebraico Moderno A2", "Hebraico Bíblico", "Hebraico Particular"
    ]
    
    results = {}
    for c in frappe.get_all("LMS Course", fields=["name", "title", "published", "paid_course"], limit=0):
        results[c.name] = c
        
    print(json.dumps(results, indent=2))
