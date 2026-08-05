import re

with open("vedium_core/vedium_core/scripts/migrations/oneshot/seed_ioruba_avancado_catalog.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('course_name = "iorub-intermedi-rio"', 'course_name = "iorub-avan-ado"')
content = content.replace('product_id = "prod_UznRl193oyLvrF"', 'product_id = "prod_UznRl193oyLvrF"') # Wait, I need to check intermediario's product_id to replace it correctly.

# Let's just rewrite the whole file, it's safer.
