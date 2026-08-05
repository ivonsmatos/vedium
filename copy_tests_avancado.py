import re

with open("vedium_core/vedium_core/tests/test_pure_ioruba_intermediario_catalog_seeding.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('IorubaIntermediario', 'IorubaAvancado')
content = content.replace('seed_ioruba_intermediario_catalog', 'seed_ioruba_avancado_catalog')
content = content.replace('iorub-intermedi-rio', 'iorub-avan-ado')
content = content.replace('Iorubá Intermediário', 'Iorubá Avançado')

with open("vedium_core/vedium_core/tests/test_pure_ioruba_avancado_catalog_seeding.py", "w", encoding="utf-8") as f:
    f.write(content)
