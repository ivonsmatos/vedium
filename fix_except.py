import os

files = [
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_elementary_catalog.py",
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_pr_intermediario_catalog.py",
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_upper_intermediario_catalog.py",
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_c1_catalog.py"
]

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace(
        "                except Exception as e:",
        "            except Exception as e:"
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Fixed except in {filepath}")
