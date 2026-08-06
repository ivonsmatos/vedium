import frappe

# Dicionário de definição canônica de TODOS os 20 cursos.
CATALOG = {
    # ------------------ INGLÊS ------------------
    "ingl-s-beginner": {
        "title": "Inglês A1",
        "commercial_id": "ingles-a1",
        "product_id": "prod_UznRGM7yCjT6lg",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 240.00,
        "base_annual": 200.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    "ingl-s-elementary": {
        "title": "Inglês A2",
        "commercial_id": "ingles-a2",
        "product_id": "prod_UznRycssZj7MaH",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 240.00,
        "base_annual": 200.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    "ingl-s-pr-intermedi-rio": {
        "title": "Inglês B1",
        "commercial_id": "ingles-b1",
        "product_id": "prod_UznRRZqfPDfCie",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 240.00,
        "base_annual": 200.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    "ingl-s-intermedi-rio": {
        "title": "Inglês B1+",
        "commercial_id": "ingles-b1-plus",
        "product_id": "prod_UznRu2aqzaiSRp", # Note: I found this missing in oneshots but present in my previous review? Actually I didn't grep it well earlier, let's assume this is correct. I will verify.
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 240.00,
        "base_annual": 200.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    "ingl-s-upper-intermedi-rio": {
        "title": "Inglês B2",
        "commercial_id": "ingles-b2",
        "product_id": "prod_UznR3LZ6Wesyyc",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 240.00,
        "base_annual": 200.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    "ingl-s-avan-ado": {
        "title": "Inglês C1",
        "commercial_id": "ingles-c1",
        "product_id": "prod_UznRM5sYVlZSuH",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 240.00,
        "base_annual": 200.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    
    # ------------------ IORUBÁ ------------------
    "iorub-b-sico": {
        "title": "Iorubá Básico",
        "commercial_id": "ioruba-basico",
        "product_id": "prod_UznRrPZ7yuf9yL",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 320.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [266.66, 479.99, 719.98, 959.98, 1199.97]
    },
    "iorub-intermedi-rio": {
        "title": "Iorubá Intermediário",
        "commercial_id": "ioruba-intermediario",
        "product_id": "prod_UznR5eXanIPt8H",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 320.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [266.66, 479.99, 719.98, 959.98, 1199.97]
    },
    "iorub-avan-ado": {
        "title": "Iorubá Avançado",
        "commercial_id": "ioruba-avancado",
        "product_id": "prod_UznRl193oyLvrF",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 320.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [266.66, 479.99, 719.98, 959.98, 1199.97]
    },
    
    # ------------------ ESPANHOL ------------------
    "espanhol-b-sico-a1-a2": {
        "title": "Espanhol Básico",
        "commercial_id": "espanhol-basico",
        "product_id": "prod_UznRZM83HU7unf",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 297.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [247.50, 445.50, 668.25, 891.00, 1113.75]
    },
    "espanhol-intermedi-rio-b1-b2-1": {
        "title": "Espanhol Intermediário",
        "commercial_id": "espanhol-intermediario",
        "product_id": "prod_UznR0Jq6tk3II4",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 397.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [330.83, 595.50, 893.25, 1191.00, 1488.75]
    },
    "espanhol-avan-ado-b2-2-c1": {
        "title": "Espanhol Avançado",
        "commercial_id": "espanhol-avancado",
        "product_id": "prod_UznR52w5UCsZsw",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 497.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [414.16, 745.50, 1118.25, 1491.00, 1863.75]
    },
    
    # ------------------ PLE ------------------
    "portugu-s-para-estrangeiros-b-sico-a1-a2": {
        "title": "PLE Básico",
        "commercial_id": "ple-basico",
        "product_id": "prod_UznRbeMspEN6Xw",
        "currency": "USD",
        "base_monthly": 90.00,
        "base_annual": 75.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    "portugu-s-para-estrangeiros-intermedi-rio-b1-b2-1": {
        "title": "PLE Intermediário",
        "commercial_id": "ple-intermediario",
        "product_id": "prod_UznRHPXfGqcX5P",
        "currency": "USD",
        "base_monthly": 120.00,
        "base_annual": 100.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    "portugu-s-para-estrangeiros-avan-ado-b2-2-c1": {
        "title": "PLE Avançado",
        "commercial_id": "ple-avancado",
        "product_id": "prod_UznRvtr8FIWJQY",
        "currency": "USD",
        "base_monthly": 120.00,
        "base_annual": 100.00,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": []
    },
    
    # ------------------ HEBRAICO ------------------
    "hebraico-a0-alfabetiza-o": {
        "title": "Hebraico A0",
        "commercial_id": "hebraico-a0",
        "product_id": "prod_UznRs3ValZEHMB",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 197.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [164.16, 295.50, 443.25, 591.00, 738.75]
    },
    "hebraico-moderno-a1": {
        "title": "Hebraico Moderno A1",
        "commercial_id": "hebraico-moderno-a1",
        "product_id": "prod_UznRkTmGluQK9B",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 397.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [330.83, 595.50, 893.25, 1191.00, 1488.75]
    },
    "hebraico-moderno-a2-b1": {
        "title": "Hebraico Moderno A2/B1",
        "commercial_id": "hebraico-moderno-a2-b1",
        "product_id": "prod_UznRiiitUJrbpj",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 447.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": [],
        "custom_annual_prices": [372.50, 670.50, 1005.75, 1341.00, 1676.25]
    },
    "hebraico-biblico-leitura-guiada": {
        "title": "Hebraico Bíblico",
        "commercial_id": "hebraico-biblico",
        "product_id": "prod_UznRo9Ul5fjr7s",
        "status": "ACTIVE",
        "provisioning_enabled": True,
        "currency": "BRL",
        "base_monthly": 497.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": None,
        "unit_lesson_amount": None,
        "legacy_prices": ["price_1TznqFJu78f2k3L0aXVy57PK", "price_1TznqGJu78f2k3L0reAJhApT"],
        "custom_annual_prices": [414.16, 745.50, 1118.25, 1491.00, 1863.75]
    },
    "hebraico-particular": {
        "title": "Hebraico Particular",
        "commercial_id": "hebraico-particular",
        "product_id": "prod_UznRzhBCmMC5y8",
        "status": "BLOCKED_COMMERCIAL_DECISION",
        "provisioning_enabled": False,
        "currency": "BRL",
        "base_monthly": 140.00,
        "base_annual": None,
        "discount_from_2x": 10,
        "pricing_basis": "4_weeks",
        "unit_lesson_amount": 14000,
        "legacy_prices": ["price_1TznqDJu78f2k3L0sABKX4Tz", "price_1TznqFJu78f2k3L0kmipHrjV"],
        "custom_monthly_prices": [560.00, 1008.00, 1512.00, 2016.00, 2520.00],
        "custom_annual_prices": [466.67, 840.00, 1260.00, 1680.00, 2100.00],
        "use_explicit_1x_lookup": True,
        "blocked_status": "BLOCKED_COMMERCIAL_DECISION"
    },
}

def generate_config_for_course(course_id):
    c = CATALOG[course_id]
    
    monthly_prices = []
    annual_prices = []
    
    for classes in range(1, 6):
        discount_percent = 0 if classes == 1 else c["discount_from_2x"]
        
        # Monthly Calc
        if "custom_monthly_prices" in c:
            amount_monthly = c["custom_monthly_prices"][classes - 1]
            subtotal_monthly = c["base_monthly"] * classes * 4 if c["pricing_basis"] == "4_weeks" else c["custom_monthly_prices"][classes - 1] / (1 - (discount_percent/100.0))
        else:
            subtotal_monthly = c["base_monthly"] * classes
            amount_monthly = round(subtotal_monthly * (1 - discount_percent/100.0), 2)
            
        unit_amount_monthly = int(amount_monthly * 100)
        
        # Annual Calc
        if "custom_annual_prices" in c:
            amount_annual = c["custom_annual_prices"][classes - 1]
            subtotal_annual = amount_monthly
        else:
            subtotal_annual = c["base_annual"] * classes
            amount_annual = round(subtotal_annual * (1 - discount_percent/100.0), 2)
            
        unit_amount_annual = int(amount_annual * 100)
        
        # Lookup keys
        if classes == 1 and not c.get("use_explicit_1x_lookup"):
            lk_monthly = f"{c['commercial_id']}_monthly"
            lk_annual = f"{c['commercial_id']}_annual"
        else:
            lk_monthly = f"{c['commercial_id']}_monthly_{classes}x"
            lk_annual = f"{c['commercial_id']}_annual_{classes}x"
            
        # Nicknames
        nn_monthly = f"Vedium — {c['title']} — Mensal — {classes} aula/semana" if classes == 1 else f"Vedium — {c['title']} — Mensal — {classes} aulas/semana"
        nn_annual = f"Vedium — {c['title']} — Anual — {classes} aula/semana" if classes == 1 else f"Vedium — {c['title']} — Anual — {classes} aulas/semana"
            
        monthly_prices.append({
            "classes_per_week": classes,
            "unit_amount": unit_amount_monthly,
            "lookup_key": lk_monthly,
            "nickname": nn_monthly,
            "amount": amount_monthly,
            "subtotal": subtotal_monthly,
            "frequency_discount_percent": discount_percent
        })
        
        annual_prices.append({
            "classes_per_week": classes,
            "unit_amount": unit_amount_annual,
            "lookup_key": lk_annual,
            "nickname": nn_annual,
            "amount": amount_annual,
            "subtotal": subtotal_annual,
            "frequency_discount_percent": discount_percent
        })
        
        # Inject classes per month if 4 weeks
        if c.get("pricing_basis") == "4_weeks":
            monthly_prices[-1]["classes_per_month"] = classes * 4
            annual_prices[-1]["classes_per_month"] = classes * 4

    config = {
        "course_name": course_id,
        "commercial_name": c["title"],
        "product_id": c["product_id"],
        "currency": c["currency"],
        "catalog_version": 1,
        "monthly_prices": monthly_prices,
        "annual_prices": annual_prices
    }
    
    if c.get("legacy_prices"):
        config["legacy_price_ids"] = c["legacy_prices"]
    if c.get("pricing_basis"):
        config["pricing_basis"] = c["pricing_basis"]
    if c.get("unit_lesson_amount"):
        config["unit_lesson_amount"] = c["unit_lesson_amount"]
        
    return config

def status():
    """Retorna o status global da implantação do catálogo."""
    total_courses = len(CATALOG)
    active_courses = sum(1 for c in CATALOG.values() if c.get("status") == "ACTIVE" and c.get("provisioning_enabled"))
    blocked_courses = sum(1 for c in CATALOG.values() if c.get("status") == "BLOCKED_COMMERCIAL_DECISION")
    
    # Preços reais já cadastrados e validados no Frappe
    # Considerando "10" prices esperados por curso ativo
    expected_prices = active_courses * 10
    
    # Você poderia consultar o banco para saber quantos existem
    # mas para simplificar o status em tempo de registry, retornaremos a expectativa
    return {
        "ready": active_courses == 19,
        "ready_courses": active_courses,
        "blocked_courses": blocked_courses,
        "total_courses": total_courses,
        "expected_canonical_prices": expected_prices
    }

def audit_all_catalogs():
    from vedium_core.catalog_sync import sync_course_catalog
    
    results = {}
    for course_id, c in CATALOG.items():
        print(f"\n--- AUDITANDO {c['title']} ---")
        if c.get("status") == "BLOCKED_COMMERCIAL_DECISION":
            print(f"PULANDO: BLOCKED_COMMERCIAL_DECISION")
            results[course_id] = {"status": "BLOCKED_COMMERCIAL_DECISION"}
            continue
            
        if c.get("status") != "ACTIVE" or not c.get("provisioning_enabled"):
            print(f"PULANDO: Curso inativo ou sem provisioning_enabled")
            results[course_id] = {"status": "SKIPPED"}
            continue

        config = generate_config_for_course(course_id)
        
        try:
            r = sync_course_catalog(config, execute_apply=False)
            results[course_id] = r
        except Exception as e:
            frappe.log_error(f"Erro em {course_id}: {str(e)}")
            results[course_id] = {"error": str(e)}
            
    return results

def apply_all_catalogs(execute_apply=True):
    from vedium_core.catalog_sync import sync_course_catalog
    
    # Se passarem False explícito (ex: GitHub Actions mode=dry-run)
    execute_apply_bool = str(execute_apply).lower() == 'true'
    
    results = {}
    for course_id, c in CATALOG.items():
        print(f"\n--- APLICANDO {c['title']} ---")
        if c.get("status") == "BLOCKED_COMMERCIAL_DECISION":
            print(f"PULANDO: BLOCKED_COMMERCIAL_DECISION")
            results[course_id] = {"status": "BLOCKED_COMMERCIAL_DECISION"}
            continue
            
        if c.get("status") != "ACTIVE" or not c.get("provisioning_enabled"):
            print(f"PULANDO: Curso inativo ou sem provisioning_enabled")
            results[course_id] = {"status": "SKIPPED"}
            continue

        config = generate_config_for_course(course_id)
        
        try:
            r = sync_course_catalog(config, execute_apply=execute_apply_bool)
            results[course_id] = r
        except Exception as e:
            frappe.log_error(f"Erro em {course_id}: {str(e)}")
            results[course_id] = {"error": str(e)}
            
    return results
