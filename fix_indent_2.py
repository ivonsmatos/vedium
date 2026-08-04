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
    
    # Let's fix the try-except indentation by searching for "        else:\n            try:\n"
    # and then matching lines until except.
    # It's easier to just fix the whole block using replace
    old_block = """        else:
            try:
                # 1. Procurar pelo lookup_key
            prices = stripe.Price.list(lookup_keys=[p_data['lookup_key']], active=True)
            if prices.data:
                existing_price = prices.data[0]
                # 3. Confirmar Product, moeda, valor e recorrência
                if existing_price.product != product_id:
                    frappe.throw(f"Conflito no Stripe: Price {existing_price.id} associado ao produto {existing_price.product}, esperado {product_id}.")
                if existing_price.currency != "brl":
                    frappe.throw(f"Conflito no Stripe: Price {existing_price.id} moeda {existing_price.currency}, esperado brl.")
                if existing_price.unit_amount != int(p_data['unit_amount'] * 100):
                    frappe.throw(f"Conflito no Stripe: Price {existing_price.id} valor {existing_price.unit_amount}, esperado {int(p_data['unit_amount'] * 100)}.")
                if existing_price.recurring.interval != "month":
                    frappe.throw(f"Conflito no Stripe: Price {existing_price.id} intervalo {existing_price.recurring.interval}, esperado month.")
                
                stripe_price_id = existing_price.id
                print(f"[{catalog_key}] Encontrado Price no Stripe: {stripe_price_id}")
            else:
                # 2. Se não existe, criar
                metadata = {
                    "vedium_course_id": course_name,
                    "classes_per_week": str(p_data['classes']),
                    "frequency_discount_percent": "10",
                    "interval": period,
                    "minimum_term_months": "12" if period == "annual" else "0",
                    "catalog_version": "1",
                    "system": "frappe"
                }
                if period == "annual":
                    metadata["charge_count"] = "12"
                    
                new_price = stripe.Price.create(
                    product=product_id,
                    currency="brl",
                    unit_amount=int(p_data['unit_amount'] * 100),
                    recurring={"interval": "month", "interval_count": 1, "usage_type": "licensed"},
                    billing_scheme="per_unit",
                    nickname=p_data['nickname'],
                    lookup_key=p_data['lookup_key'],
                    metadata=metadata,
                    active=True
                )
                stripe_price_id = new_price.id
                print(f"[{catalog_key}] Criado novo Price no Stripe: {stripe_price_id}")
                
            except Exception as e:
                frappe.throw(f"Erro ao integrar com Stripe para a chave {catalog_key}: {str(e)}")"""
                
    new_block = """        else:
            try:
                # 1. Procurar pelo lookup_key
                prices = stripe.Price.list(lookup_keys=[p_data['lookup_key']], active=True)
                if prices.data:
                    existing_price = prices.data[0]
                    # 3. Confirmar Product, moeda, valor e recorrência
                    if existing_price.product != product_id:
                        frappe.throw(f"Conflito no Stripe: Price {existing_price.id} associado ao produto {existing_price.product}, esperado {product_id}.")
                    if existing_price.currency != "brl":
                        frappe.throw(f"Conflito no Stripe: Price {existing_price.id} moeda {existing_price.currency}, esperado brl.")
                    if existing_price.unit_amount != int(p_data['unit_amount'] * 100):
                        frappe.throw(f"Conflito no Stripe: Price {existing_price.id} valor {existing_price.unit_amount}, esperado {int(p_data['unit_amount'] * 100)}.")
                    if existing_price.recurring.interval != "month":
                        frappe.throw(f"Conflito no Stripe: Price {existing_price.id} intervalo {existing_price.recurring.interval}, esperado month.")
                    
                    stripe_price_id = existing_price.id
                    print(f"[{catalog_key}] Encontrado Price no Stripe: {stripe_price_id}")
                else:
                    # 2. Se não existe, criar
                    metadata = {
                        "vedium_course_id": course_name,
                        "classes_per_week": str(p_data['classes']),
                        "frequency_discount_percent": "10",
                        "interval": period,
                        "minimum_term_months": "12" if period == "annual" else "0",
                        "catalog_version": "1",
                        "system": "frappe"
                    }
                    if period == "annual":
                        metadata["charge_count"] = "12"
                        
                    new_price = stripe.Price.create(
                        product=product_id,
                        currency="brl",
                        unit_amount=int(p_data['unit_amount'] * 100),
                        recurring={"interval": "month", "interval_count": 1, "usage_type": "licensed"},
                        billing_scheme="per_unit",
                        nickname=p_data['nickname'],
                        lookup_key=p_data['lookup_key'],
                        metadata=metadata,
                        active=True
                    )
                    stripe_price_id = new_price.id
                    print(f"[{catalog_key}] Criado novo Price no Stripe: {stripe_price_id}")
                    
            except Exception as e:
                frappe.throw(f"Erro ao integrar com Stripe para a chave {catalog_key}: {str(e)}")"""
                
    content = content.replace(old_block, new_block)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Indented {filepath}")
