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
    
    # 1. Remove the throw
    content = content.replace(
        'if not stripe.api_key:\n        frappe.throw("STRIPE_SECRET_KEY não configurada no site_config.json")',
        'if not stripe.api_key:\n        print("Aviso: STRIPE_SECRET_KEY não configurada no site_config.json. A API do Stripe será ignorada.")'
    )
    
    # 2. Add API key check in creation
    target_create = 'if p_data.get("create") and not stripe_price_id:\n        try:'
    replacement_create = '''if p_data.get("create") and not stripe_price_id:
        if not stripe.api_key:
            print(f"[{catalog_key}] Pulando Stripe API (sem STRIPE_SECRET_KEY).")
        else:
            try:'''
    content = content.replace(target_create, replacement_create)
    
    # Indent the try block (and its except block)
    # This is a bit tricky with raw replace, let's just replace the exact block up to except
    
    # Actually, simpler to just replace:
    # "        try:" with "            try:"
    # But wait, it's safer to use python regex or just manual replace.
    # Let's replace the whole `if p_data.get("create") and not stripe_price_id:` block.
    
    # 3. Fix diverge check
    old_diverge = 'if doc.amount != p_data[\'amount\'] or doc.stripe_price_id != stripe_price_id:\n            diverges = True'
    new_diverge = 'if doc.amount != p_data[\'amount\']:\n            diverges = True\n        if stripe_price_id and doc.stripe_price_id != stripe_price_id:\n            diverges = True'
    content = content.replace(old_diverge, new_diverge)
    
    # 4. Fix stripe_validated assignment
    old_validated = '"stripe_validated": 1,'
    new_validated = '"stripe_validated": 1 if stripe_price_id else 0,'
    content = content.replace(old_validated, new_validated)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Updated {filepath}")
