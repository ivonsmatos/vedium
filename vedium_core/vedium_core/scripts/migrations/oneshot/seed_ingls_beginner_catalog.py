import frappe

def execute():
    course_name = "ingl-s-beginner"
    product_id = "prod_UznRGM7yCjT6lg"

    if not frappe.db.exists("LMS Course", course_name):
        frappe.log_error(f"Curso {course_name} não encontrado para seeding de catálogo.")
        return

    # Lista de preços mensais
    monthly_prices = [
        {"classes": 1, "amount": 240.00, "subtotal": 240.00, "unit_amount": 240.00, "discount": 0, "price_id": "price_1TznqXJu78f2k3L0yM0cv01y", "lookup_key": "ingl-s-beginner_monthly"},
        {"classes": 2, "amount": 432.00, "subtotal": 480.00, "unit_amount": 240.00, "discount": 10, "price_id": "price_1U0pqMJu78f2k3L0uZefazHB", "lookup_key": "ingl-s-beginner_monthly_2x"},
        {"classes": 3, "amount": 648.00, "subtotal": 720.00, "unit_amount": 240.00, "discount": 10, "price_id": "price_1U0pqaJu78f2k3L0aONdpEbt", "lookup_key": "ingl-s-beginner_monthly_3x"},
        {"classes": 4, "amount": 864.00, "subtotal": 960.00, "unit_amount": 240.00, "discount": 10, "price_id": "price_1U0pqkJu78f2k3L0zeU080hy", "lookup_key": "ingl-s-beginner_monthly_4x"},
        {"classes": 5, "amount": 1080.00, "subtotal": 1200.00, "unit_amount": 240.00, "discount": 10, "price_id": "price_1U0pqvJu78f2k3L0jUKzxuJH", "lookup_key": "ingl-s-beginner_monthly_5x"},
    ]

    # Lista de preços anuais
    annual_prices = [
        {"classes": 1, "amount": 200.00, "subtotal": 200.00, "unit_amount": 200.00, "discount": 0, "price_id": "price_1TznqYJu78f2k3L0Qod6SnIC", "lookup_key": "ingl-s-beginner_annual"},
        {"classes": 2, "amount": 360.00, "subtotal": 400.00, "unit_amount": 200.00, "discount": 10, "price_id": "price_1U0pr9Ju78f2k3L0Jls4XMMM", "lookup_key": "ingl-s-beginner_annual_2x"},
        {"classes": 3, "amount": 540.00, "subtotal": 600.00, "unit_amount": 200.00, "discount": 10, "price_id": "price_1U0prJJu78f2k3L0scRXx9RG", "lookup_key": "ingl-s-beginner_annual_3x"},
        {"classes": 4, "amount": 720.00, "subtotal": 800.00, "unit_amount": 200.00, "discount": 10, "price_id": "price_1U0prWJu78f2k3L0DdQxTibr", "lookup_key": "ingl-s-beginner_annual_4x"},
        {"classes": 5, "amount": 900.00, "subtotal": 1000.00, "unit_amount": 200.00, "discount": 10, "price_id": "price_1U0prgJu78f2k3L0UA6sp55e", "lookup_key": "ingl-s-beginner_annual_5x"},
    ]

    for p in monthly_prices:
        _create_price_if_not_exists(course_name, "monthly", product_id, p)
        
    for p in annual_prices:
        _create_price_if_not_exists(course_name, "annual", product_id, p)


def _create_price_if_not_exists(course_name, period, product_id, p_data):
    catalog_key = f"{course_name}:{period}:{p_data['classes']}x:live:v1"
    
    existing = frappe.db.get_value("Vedium Course Price", {"catalog_key": catalog_key})
    
    if existing:
        doc = frappe.get_doc("Vedium Course Price", existing)
        # Check if values diverge
        diverges = False
        if doc.amount != p_data['amount'] or doc.stripe_price_id != p_data['price_id']:
            diverges = True
            
        if diverges:
            frappe.throw(f"Conflito de dados no patch para a chave {catalog_key}. Os dados existentes divergem dos dados do patch.")
            
        print(f"[{catalog_key}] Já existe, pulando...")
        return
        
    doc = frappe.get_doc({
        "doctype": "Vedium Course Price",
        "course": course_name,
        "commercial_name": f"Inglês Online ao Vivo A1 – Iniciante ({p_data['classes']}x na semana)",
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
        "stripe_price_id": p_data['price_id'],
        "stripe_lookup_key": p_data['lookup_key'],
    })
    
    # Bypass stripe HTTP validation in patch as API KEY may not be available or network could fail
    doc.flags.ignore_validate = True
    doc.insert(ignore_permissions=True)
    print(f"[{catalog_key}] Criado com sucesso.")
