import os

with open("vedium_core/vedium_core/tests/test_pure_c1_catalog_seeding.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace imports and names
content = content.replace("seed_ingls_c1_catalog", "seed_ioruba_basico_catalog")
content = content.replace("ingl-s-avan-ado", "iorub-b-sico")
content = content.replace("prod_UznRM5sYVlZSuH", "prod_UznRrPZ7yuf9yL")
content = content.replace("TestC1CatalogSeeding", "TestIorubaBasicoCatalogSeeding")
content = content.replace("Inglês C1 —", "Iorubá Básico —")
content = content.replace("Inglês Online ao Vivo C1 – Avançado", "Iorubá Básico")

with open("vedium_core/vedium_core/tests/test_pure_ioruba_basico_catalog_seeding.py", "w", encoding="utf-8") as f:
    f.write(content)
