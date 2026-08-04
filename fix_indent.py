import os

files = [
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_elementary_catalog.py",
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_pr_intermediario_catalog.py",
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_upper_intermediario_catalog.py",
    "vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_c1_catalog.py"
]

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out = []
    in_try = False
    for line in lines:
        if line.startswith('            try:'):
            in_try = True
            out.append(line)
            continue
            
        if in_try:
            if line.startswith('            except Exception as e:'):
                out.append('    ' + line)
                continue
            elif line.startswith('                frappe.throw(f"Erro ao integrar com Stripe para a chave {catalog_key}: {str(e)}")'):
                out.append('    ' + line)
                in_try = False
                continue
            elif line.strip() == '':
                out.append(line)
            else:
                out.append('    ' + line)
        else:
            out.append(line)
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(out)
        
    print(f"Fixed {filepath}")
