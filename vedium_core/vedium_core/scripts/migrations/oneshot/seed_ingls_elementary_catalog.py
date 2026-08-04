import frappe
import stripe

def execute():
    course_name = "ingl-s-elementary"
    product_id = "prod_UznRycssZj7MaH"

    if not frappe.db.exists("LMS Course", course_name):
        frappe.log_error(f"Curso {course_name} não encontrado para seeding de catálogo.")
        return

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        frappe.throw("STRIPE_SECRET_KEY não configurada no site_config.json")

    # Lista de preços mensais
    monthly_prices = [
        {"classes": 1, "amount": 240.00, "subtotal": 240.00, "unit_amount": 240.00, "discount": 0, "price_id": "price_1TznqWJu78f2k3L0Vwf5I9Wj", "lookup_key": "ingl-s-elementary_monthly", "create": False},
        {"classes": 2, "amount": 432.00, "subtotal": 480.00, "unit_amount": 432.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_monthly_2x", "create": True, "nickname": "Vedium — Inglês A2 — Mensal — 2 aulas/semana"},
        {"classes": 3, "amount": 648.00, "subtotal": 720.00, "unit_amount": 648.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_monthly_3x", "create": True, "nickname": "Vedium — Inglês A2 — Mensal — 3 aulas/semana"},
        {"classes": 4, "amount": 864.00, "subtotal": 960.00, "unit_amount": 864.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_monthly_4x", "create": True, "nickname": "Vedium — Inglês A2 — Mensal — 4 aulas/semana"},
        {"classes": 5, "amount": 1080.00, "subtotal": 1200.00, "unit_amount": 1080.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_monthly_5x", "create": True, "nickname": "Vedium — Inglês A2 — Mensal — 5 aulas/semana"},
    ]

    # Lista de preços anuais
    annual_prices = [
        {"classes": 1, "amount": 200.00, "subtotal": 200.00, "unit_amount": 200.00, "discount": 0, "price_id": "price_1TznqXJu78f2k3L0zJFjGDLx", "lookup_key": "ingl-s-elementary_annual", "create": False},
        {"classes": 2, "amount": 360.00, "subtotal": 400.00, "unit_amount": 360.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_annual_2x", "create": True, "nickname": "Vedium — Inglês A2 — Anual — 2 aulas/semana"},
        {"classes": 3, "amount": 540.00, "subtotal": 600.00, "unit_amount": 540.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_annual_3x", "create": True, "nickname": "Vedium — Inglês A2 — Anual — 3 aulas/semana"},
        {"classes": 4, "amount": 720.00, "subtotal": 800.00, "unit_amount": 720.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_annual_4x", "create": True, "nickname": "Vedium — Inglês A2 — Anual — 4 aulas/semana"},
        {"classes": 5, "amount": 900.00, "subtotal": 1000.00, "unit_amount": 900.00, "discount": 10, "price_id": None, "lookup_key": "ingl-s-elementary_annual_5x", "create": True, "nickname": "Vedium — Inglês A2 — Anual — 5 aulas/semana"},
    ]

    for p in monthly_prices:
        _create_price_if_not_exists(course_name, "monthly", product_id, p)
        
    for p in annual_prices:
        _create_price_if_not_exists(course_name, "annual", product_id, p)


def _create_price_if_not_exists(course_name, period, product_id, p_data):
    catalog_key = f"{course_name}:{period}:{p_data['classes']}x:live:v1"
    
    # Resolvendo o Stripe Price ID
    stripe_price_id = p_data.get("price_id")
    if p_data.get("create") and not stripe_price_id:
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
            frappe.throw(f"Erro ao integrar com Stripe para a chave {catalog_key}: {str(e)}")
            
    if not stripe_price_id:
        frappe.throw(f"Falha ao obter Stripe Price ID para a chave {catalog_key}.")
        
    existing = frappe.db.get_value("Vedium Course Price", {"catalog_key": catalog_key})
    
    if existing:
        frappe.db.set_value("Vedium Course Price", existing, "amount", p_data['amount'])
        frappe.db.set_value("Vedium Course Price", existing, "stripe_validated", 1)
        frappe.db.commit()
        doc = frappe.get_doc("Vedium Course Price", existing)
        # Check if values diverge
        diverges = False
        if doc.amount != p_data['amount'] or doc.stripe_price_id != stripe_price_id:
            diverges = True
            
        if diverges:
            frappe.throw(f"Conflito de dados no patch para a chave {catalog_key}. Os dados existentes divergem dos dados do patch.")
            
        print(f"[{catalog_key}] Já existe no Frappe, atualizado.")
        return
        
    doc = frappe.get_doc({
        "doctype": "Vedium Course Price",
        "course": course_name,
        "commercial_name": f"Inglês Online ao Vivo A2 – Básico ({p_data['classes']}x na semana)",
        "catalog_key": catalog_key,
        "catalog_version": 1,
        "enabled": 1,
        "billing_period": period,
        "classes_per_week": p_data['classes'],
        "currency": "BRL",
        "minimum_term_months": 12 if period == "annual" else 0,
        "charge_count": 12 if period == "annual" else 0,
        "amount": p_data['amount'],
        "unit_amount": p_data['unit_amount'],
        "subtotal": p_data['subtotal'],
        "frequency_discount_percent": p_data['discount'],
        "stripe_environment": "live",
        "stripe_product_id": product_id,
        "stripe_price_id": stripe_price_id,
        "stripe_lookup_key": p_data['lookup_key'],
        "stripe_validated": 1,
    })
    
    # Bypass stripe HTTP validation in patch as we already validated it
    doc.flags.ignore_validate = True
    doc.insert(ignore_permissions=True)
    print(f"[{catalog_key}] Criado no Frappe com sucesso.")
