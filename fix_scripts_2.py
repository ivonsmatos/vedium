import os

files = [
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
    
    # 2. Fix create logic
    target_create = '''    if p_data.get("create") and not stripe_price_id:
        try:
            # 1. Procurar pelo lookup_key'''
    replacement_create = '''    if p_data.get("create") and not stripe_price_id:
        if not stripe.api_key:
            print(f"[{catalog_key}] Pulando Stripe API (sem STRIPE_SECRET_KEY).")
        else:
            try:
                # 1. Procurar pelo lookup_key'''
    content = content.replace(target_create, replacement_create)
    
    # Indent the try block (this is a bit manual, but I can replace specific lines)
    # Actually, we can just let Python's re do a block replacement if needed, but it's simpler to do string replacements.
    
    target_except = '''        except Exception as e:
            frappe.throw(f"Erro ao integrar com Stripe para a chave {catalog_key}: {str(e)}")
            
    if not stripe_price_id:'''
    replacement_except = '''            except Exception as e:
                frappe.throw(f"Erro ao integrar com Stripe para a chave {catalog_key}: {str(e)}")
            
    if stripe.api_key and not stripe_price_id:'''
    content = content.replace(target_except, replacement_except)
    
    # 3. Fix diverge check
    old_diverge = '''        # Check if values diverge
        diverges = False
        if doc.amount != p_data['amount'] or doc.stripe_price_id != stripe_price_id:
            diverges = True
            
        if diverges:'''
    new_diverge = '''        # Check if values diverge
        diverges = False
        if doc.amount != p_data['amount']:
            diverges = True
        if stripe_price_id and doc.stripe_price_id != stripe_price_id:
            diverges = True
            
        if diverges:'''
    content = content.replace(old_diverge, new_diverge)
    
    # 4. Fix stripe_validated assignment
    old_validated = '"stripe_validated": 1,\n    })'
    new_validated = '"stripe_validated": 1 if stripe_price_id else 0,\n    })'
    content = content.replace(old_validated, new_validated)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Updated {filepath}")
