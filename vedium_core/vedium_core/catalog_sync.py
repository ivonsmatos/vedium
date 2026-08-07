import frappe
from frappe import _
from typing import Dict, List, Any
import time

def ensure_custom_contract_currency_field():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_field
    fields_to_create = [
        {
            "fieldname": "custom_contract_currency",
            "label": "Moeda contratada",
            "fieldtype": "Data",
            "insert_after": "custom_contract_monthly_amount",
            "read_only": 1,
            "default": "BRL"
        },
        {
            "fieldname": "custom_catalog_key",
            "label": "Chave do Catálogo",
            "fieldtype": "Data",
            "insert_after": "custom_stripe_price_id",
            "read_only": 1
        },
        {
            "fieldname": "custom_catalog_version",
            "label": "Versão do Catálogo",
            "fieldtype": "Int",
            "insert_after": "custom_catalog_key",
            "read_only": 1
        }
    ]
    for field in fields_to_create:
        if not frappe.db.exists("Custom Field", f"LMS Enrollment-{field['fieldname']}"):
            create_custom_field("LMS Enrollment", field)
    frappe.db.commit()

def sync_course_catalog(config: Dict[str, Any], execute_apply: bool = False):
    """
    Sincronizador central e idempotente de catálogo Stripe/Frappe.
    Garante a integridade dos Prices (USD/BRL) e evita dízimas e acúmulos de erro.
    
    Expected config structure:
    {
        "course_name": "...",
        "commercial_name": "...",
        "product_id": "prod_...",
        "currency": "usd" | "brl",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 9000, "lookup_key": "...", "nickname": "...", "amount": 90.00, "subtotal": 90.00, "frequency_discount_percent": 0},
            # ...
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 7500, "lookup_key": "...", "nickname": "...", "amount": 75.00, "subtotal": 90.00, "frequency_discount_percent": 0},
            # ...
        ]
    }
    """
    ensure_custom_contract_currency_field()
    
    import stripe
    from stripe.error import AuthenticationError

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        frappe.throw(_("Chave STRIPE_SECRET_KEY não encontrada."))
    
    if not stripe.api_key.startswith("sk_live_"):
        frappe.throw(_("A chave Stripe precisa ser de produção (sk_live_)."))

    try:
        # Validate connection
        stripe.Account.retrieve()
    except AuthenticationError:
        frappe.throw(_("Chave Stripe inválida."))

    course_name = config["course_name"]
    product_id = config["product_id"]
    currency = config["currency"].lower()
    
    print(f"\n[{course_name.upper()}] Iniciando Auditoria Stripe...")

    try:
        product = stripe.Product.retrieve(product_id)
        if not product.active:
            frappe.throw(_(f"O Product {product_id} está inativo."))
        if product.type != "service":
            frappe.throw(_(f"O Product {product_id} precisa ser do tipo 'service'."))
    except Exception as e:
        frappe.throw(_(f"Erro ao buscar Product {product_id}: {str(e)}"))
        
    all_prices = _get_all_active_prices_for_product(stripe, product_id)
    lookup_key_to_price = {p.lookup_key: p for p in all_prices if p.lookup_key}
    
    # Validações estritas de idempotência
    results = {
        "monthly": [],
        "annual": []
    }
    
    if "legacy_price_ids" in config:
        print("\n--- Auditoria de Prices Legados ---")
        for legacy_id in config["legacy_price_ids"]:
            found = False
            for p in all_prices:
                if p.id == legacy_id:
                    print(f" [LEGACY] Identificado Price {legacy_id} ({p.currency.upper()} {p.unit_amount/100:.2f})")
                    found = True
                    break
            if not found:
                print(f" [LEGACY AVISO] Price {legacy_id} não encontrado ou inativo.")
        print("-----------------------------------\n")
    
    for period in ["monthly", "annual"]:
        for price_def in config[f"{period}_prices"]:
            lkey = price_def["lookup_key"]
            expected_amount = price_def["unit_amount"]
            
            existing = lookup_key_to_price.get(lkey)
            if existing:
                if existing.currency != currency:
                    frappe.throw(_(f"Price {lkey} existe mas a moeda diverge. (Stripe: {existing.currency}, Esperado: {currency})"))
                if existing.unit_amount != expected_amount:
                    frappe.throw(_(f"Price {lkey} existe mas o valor diverge. (Stripe: {existing.unit_amount}, Esperado: {expected_amount})"))
                if existing.recurring.interval != "month" or existing.recurring.interval_count != 1:
                    frappe.throw(_(f"Price {lkey} existe mas a recorrência diverge."))

                # Prices legados (pré-catálogo) reaproveitados podem estar sem os
                # metadados exigidos pelo controller (interval, minimum_term_months,
                # charge_count). Ressincroniza o metadata para manter idempotência.
                if execute_apply:
                    stripe.Price.modify(existing.id, metadata=_build_price_metadata(config, period, price_def))

                print(f" [OK] Price reutilizado: {lkey} -> {existing.id} ({currency.upper()} {expected_amount/100:.2f})")
                price_def["stripe_price_id"] = existing.id
            else:
                if not execute_apply:
                    print(f" [DRY-RUN] Criará Price: {lkey} -> {currency.upper()} {expected_amount/100:.2f}")
                    price_def["stripe_price_id"] = f"price_dryrun_{lkey}"
                else:
                    new_price = _create_stripe_price(stripe, config, period, price_def)
                    print(f" [CREATED] Price criado: {lkey} -> {new_price.id} ({currency.upper()} {expected_amount/100:.2f})")
                    price_def["stripe_price_id"] = new_price.id
            
            results[period].append(price_def)
            
    if not execute_apply:
        print("\n[!] Dry run executado com sucesso. Nenhum dado foi salvo. Use execute_apply=True para efetivar.")
        return results

    # Gravar no Frappe
    frappe.db.begin()
    try:
        for period in ["monthly", "annual"]:
            for price_def in results[period]:
                _upsert_vedium_course_price(config, period, price_def)
                
        # Verificar se catálogo está completo e ativar
        _validate_and_activate_catalog(config)
        frappe.db.commit()
        print(f"\n[SUCESSO] Catálogo de {course_name} sincronizado e salvo no banco de dados!")
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(_(f"Erro ao salvar registros no Frappe: {str(e)}"))
        
    return results

def _get_all_active_prices_for_product(stripe, product_id):
    prices = []
    has_more = True
    starting_after = None
    while has_more:
        kwargs = {"product": product_id, "active": True, "limit": 100}
        if starting_after:
            kwargs["starting_after"] = starting_after
        resp = stripe.Price.list(**kwargs)
        prices.extend(resp.data)
        has_more = resp.has_more
        if has_more:
            starting_after = resp.data[-1].id
    return prices

def _build_price_metadata(config, period, price_def):
    metadata = {
        "vedium_course_id": config["course_name"],
        "classes_per_week": str(price_def["classes_per_week"]),
        "frequency_discount_percent": str(price_def["frequency_discount_percent"]),
        "interval": period,
        "catalog_version": str(config["catalog_version"]),
        "system": "frappe"
    }

    if "pricing_basis" in config:
        metadata["pricing_basis"] = str(config["pricing_basis"])
    if "unit_lesson_amount" in config:
        metadata["unit_lesson_amount"] = str(config["unit_lesson_amount"])
    if "classes_per_month" in price_def:
        metadata["classes_per_month"] = str(price_def["classes_per_month"])

    if period == "annual":
        metadata["minimum_term_months"] = "12"
        metadata["charge_count"] = "12"
        if "annual_discount_months" in config:
            metadata["annual_discount_months"] = str(config["annual_discount_months"])
    else:
        metadata["minimum_term_months"] = "0"

    return metadata


def _create_stripe_price(stripe, config, period, price_def):
    return stripe.Price.create(
        product=config["product_id"],
        currency=config["currency"],
        unit_amount=price_def["unit_amount"],
        recurring={
            "interval": "month",
            "interval_count": 1,
            "usage_type": "licensed"
        },
        billing_scheme="per_unit",
        lookup_key=price_def["lookup_key"],
        transfer_lookup_key=False,
        nickname=price_def["nickname"],
        metadata=_build_price_metadata(config, period, price_def)
    )

def _upsert_vedium_course_price(config, period, price_def):
    course_name = config["course_name"]
    freq = price_def["classes_per_week"]
    catalog_version = config["catalog_version"]
    catalog_key = f"{course_name}:{period}:{freq}x:live:v{catalog_version}"
    
    doc_name = frappe.db.exists("Vedium Course Price", catalog_key)
    if doc_name:
        doc = frappe.get_doc("Vedium Course Price", doc_name)
    else:
        doc = frappe.new_doc("Vedium Course Price")
        doc.catalog_key = catalog_key
        
    doc.course = course_name
    doc.commercial_name = config["commercial_name"]
    doc.billing_period = period
    doc.classes_per_week = freq
    doc.catalog_version = catalog_version
    doc.stripe_environment = "live"
    doc.stripe_product_id = config["product_id"]
    doc.stripe_price_id = price_def["stripe_price_id"]
    doc.currency = config["currency"].upper()
    doc.amount = price_def["amount"]
    # price_def["unit_amount"] está em centavos (vai direto pro Stripe); o campo
    # unit_amount é Currency (unidades de moeda) e o controller valida
    # unit_amount * 100 == Stripe.unit_amount, então converte de volta.
    doc.unit_amount = price_def["unit_amount"] / 100
    doc.subtotal = price_def["subtotal"]
    doc.frequency_discount_percent = price_def["frequency_discount_percent"]
    
    if "pricing_basis" in config:
        try: doc.pricing_basis = config["pricing_basis"]
        except Exception: pass
    if "unit_lesson_amount" in config:
        try: doc.unit_lesson_amount = config["unit_lesson_amount"]
        except Exception: pass
    
    # Só valida se o price realmente foi criado/confirmado na Stripe
    if "dryrun" not in doc.stripe_price_id:
        doc.stripe_validated = 1
        
    doc.save(ignore_permissions=True)

def _validate_and_activate_catalog(config):
    course_name = config["course_name"]
    cv = config["catalog_version"]
    
    monthly_count = frappe.db.count("Vedium Course Price", filters={
        "course": course_name, "billing_period": "monthly", 
        "catalog_version": cv, "stripe_validated": 1, "stripe_environment": "live"
    })
    
    annual_count = frappe.db.count("Vedium Course Price", filters={
        "course": course_name, "billing_period": "annual", 
        "catalog_version": cv, "stripe_validated": 1, "stripe_environment": "live"
    })
    
    if monthly_count == 5 and annual_count == 5:
        # Ativar todos
        frappe.db.set_value("Vedium Course Price", {
            "course": course_name, "catalog_version": cv, "stripe_environment": "live"
        }, "enabled", 1)
        print(f"Catálogo completo! {monthly_count + annual_count} registros ativados.")
    else:
        print(f"ATENÇÃO: Catálogo incompleto (M:{monthly_count}/5 A:{annual_count}/5). Não ativado.")
        frappe.db.set_value("Vedium Course Price", {
            "course": course_name, "catalog_version": cv, "stripe_environment": "live"
        }, "enabled", 0)
