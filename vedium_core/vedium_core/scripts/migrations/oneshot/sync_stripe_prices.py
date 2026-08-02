import frappe
import stripe
import json

def run(mode="audit"):
    print(f"--- Iniciando sincronizacao de precos (modo: {mode}) ---")
    
    if mode not in ["audit", "apply", "archive-legacy"]:
        print("Modo invalido. Use 'audit', 'apply' ou 'archive-legacy'.")
        return
        
    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        print("STRIPE_SECRET_KEY não configurada!")
        return

    if mode == "archive-legacy":
        run_archive_legacy()
        return

    is_apply = (mode == "apply")
    
    prices_map = {
        "ingles": 24000,
        "espanhol-basico": 29700,
        "espanhol-intermediario": 39700,
        "espanhol-avancado": 49700,
        "ioruba": 32000,
        "portugues-para-estrangeiros-basico": 9000,
        "portugues-para-estrangeiros-intermediario": 12000,
        "portugues-para-estrangeiros-avancado": 12000,
        "hebraico-a0-alfabetizacao": 19700,
        "hebraico-moderno-a1": 39700,
        "hebraico-moderno-a2-b1": 44700,
        "hebraico-biblico-leitura-guiada": 49700,
        "hebraico-particular": 112000
    }
    
    def get_monthly_price(slug):
        if "ingl" in slug or "ingles" in slug: return prices_map["ingles"]
        if "iorub" in slug or "ioruba" in slug: return prices_map["ioruba"]
        if slug in prices_map: return prices_map[slug]
        return None

    def get_stripe_gateway_reference(currency):
        gateways = frappe.get_all("Payment Gateway", fields=["name", "gateway_controller"])
        stripe_gateways = [row.name for row in gateways if "stripe" in (row.gateway_controller or "").lower()]
        if not stripe_gateways:
            frappe.throw("Nenhum gateway Stripe encontrado.")
            
        meta = frappe.get_meta("Subscription Plan")
        field = meta.get_field("payment_gateway")
        target_doctype = field.options if field else None
        
        if target_doctype == "Payment Gateway":
            return stripe_gateways[0]
            
        if target_doctype == "Payment Gateway Account":
            accounts = frappe.get_all(
                "Payment Gateway Account",
                filters={"payment_gateway": ["in", stripe_gateways]},
                fields=["name", "currency"]
            )
            valid = [a for a in accounts if not a.currency or a.currency.upper() == currency.upper()]
            if not valid:
                frappe.throw(f"Conta Stripe para a moeda {currency} não encontrada.")
            return valid[0].name
            
        return stripe_gateways[0]

    courses = frappe.get_all('LMS Course', fields=['name', 'title', 'custom_stripe_monthly_plan', 'custom_stripe_annual_plan', 'paid_course'])
    all_items = {i.name: i for i in frappe.get_all('Item', fields=['name', 'item_name'])}
    
    # Preload Stripe data
    existing_products = {}
    for p in stripe.Product.list(limit=100).auto_paging_iter():
        existing_products[p.name] = p.id
        
    all_stripe_prices = {}
    for p in stripe.Price.list(limit=100, active=True).auto_paging_iter():
        if p.product not in all_stripe_prices:
            all_stripe_prices[p.product] = []
        all_stripe_prices[p.product].append(p)
        
    results = {
        "Products created": 0,
        "Products updated": 0,
        "Prices created": 0,
        "Prices updated": 0,
        "Plans created": 0,
        "Plans updated": 0,
        "Items created": 0,
        "Courses updated": 0,
        "Legacy objects pending review": 0
    }
    
    for c in courses:
        if "teste" in c.name.lower() or not c.paid_course:
            continue
            
        monthly_cents = get_monthly_price(c.name)
        if not monthly_cents:
            continue
            
        currency = "usd" if "portugues" in c.name else "brl"
        product_name = c.title
        product_id = existing_products.get(product_name)
        
        if not product_id:
            results["Products created"] += 1
            if is_apply:
                prod = stripe.Product.create(name=product_name, statement_descriptor="VEDIUM CURSO")
                product_id = prod.id
                existing_products[product_name] = product_id
                all_stripe_prices[product_id] = []
        
        item_id = f"CURSO-{c.name.upper().replace(' ', '-')}"
        if len(item_id) > 140: item_id = item_id[:140]
        
        if "hebraico-particular" in c.name: item_id = "CURSO-HEBRAICO-PARTICULAR"
        elif "espanhol-avancado" in c.name: item_id = "CURSO-ESPANHOL-AVANCADO"
        elif "espanhol-intermediario" in c.name: item_id = "CURSO-ESPANHOL-INTERMEDIARIO"
        elif "espanhol-basico" in c.name: item_id = "CURSO-ESPANHOL-BASICO"
        elif "hebraico-a0" in c.name: item_id = "CURSO-HEBRAICO-A0"
        elif "hebraico-moderno-a1" in c.name: item_id = "CURSO-HEBRAICO-A1"
        elif "hebraico-moderno-a2-b1" in c.name: item_id = "CURSO-HEBRAICO-A2-B1"
        elif "hebraico-biblico" in c.name: item_id = "CURSO-HEBRAICO-BIBLICO"
        elif "portugues-para-estrangeiros-avancado" in c.name: item_id = "CURSO-PLE-AVANCADO"
        elif "portugues-para-estrangeiros-intermediario" in c.name: item_id = "CURSO-PLE-INTERMEDIARIO"
        elif "portugues-para-estrangeiros-basico" in c.name: item_id = "CURSO-PLE-BASICO"
            
        if item_id not in all_items:
            results["Items created"] += 1
            if is_apply:
                item_doc = frappe.new_doc("Item")
                item_doc.item_code = item_id
                item_doc.item_name = c.title
                item_doc.item_group = "Cursos e Serviços"
                item_doc.stock_uom = "Nos"
                item_doc.is_stock_item = 0
                item_doc.insert(ignore_permissions=True)
                all_items[item_id] = item_doc
                
        expected_gateway = get_stripe_gateway_reference(currency)

        def process_plan(period_name, cents, is_annual):
            plan_name = f"Vedium — {c.title} — {period_name}"
            
            price_id = None
            if product_id:
                prices_for_prod = all_stripe_prices.get(product_id, [])
                for p in prices_for_prod:
                    if p.recurring and p.recurring.interval == 'month' and p.recurring.interval_count == 1 and p.unit_amount == cents and p.currency == currency:
                        price_id = p.id
                        break
                        
            if not price_id:
                results["Prices created"] += 1
                if is_apply and product_id:
                    new_price = stripe.Price.create(product=product_id, unit_amount=cents, currency=currency, recurring={"interval": "month", "interval_count": 1}, nickname=plan_name)
                    price_id = new_price.id
                    if product_id not in all_stripe_prices:
                        all_stripe_prices[product_id] = []
                    all_stripe_prices[product_id].append(new_price)
            
            plan_exists = frappe.db.exists('Subscription Plan', plan_name)
            cost = cents / 100.0
            
            if not plan_exists:
                results["Plans created"] += 1
                if is_apply and price_id:
                    doc = frappe.new_doc('Subscription Plan')
                    doc.plan_name = plan_name
                    doc.product_price_id = price_id
                    doc.cost = cost
                    doc.currency = currency.upper()
                    doc.billing_interval = "Month"
                    doc.billing_interval_count = 1
                    doc.item = item_id
                    doc.price_determination = "Fixed Rate"
                    doc.payment_gateway = expected_gateway
                    doc.insert(ignore_permissions=True)
            else:
                plan_doc = frappe.get_doc('Subscription Plan', plan_name)
                diff = {}
                if price_id and plan_doc.product_price_id != price_id: diff['product_price_id'] = price_id
                if float(plan_doc.cost) != float(cost): diff['cost'] = cost
                if plan_doc.item != item_id: diff['item'] = item_id
                if plan_doc.price_determination != "Fixed Rate": diff['price_determination'] = "Fixed Rate"
                if plan_doc.payment_gateway != expected_gateway: diff['payment_gateway'] = expected_gateway
                
                if diff:
                    results["Plans updated"] += 1
                    if is_apply:
                        frappe.db.set_value('Subscription Plan', plan_name, diff)
                        
            field = 'custom_stripe_annual_plan' if is_annual else 'custom_stripe_monthly_plan'
            if getattr(c, field) != plan_name:
                results["Courses updated"] += 1
                if is_apply:
                    frappe.db.set_value('LMS Course', c.name, field, plan_name)

        process_plan("Mensal", monthly_cents, False)
        annual_cents = int(monthly_cents * 10 / 12)
        process_plan("Anual", annual_cents, True)
        
    if is_apply:
        frappe.db.commit()
        print("✅ Aplicacao finalizada e comitada.")
        
    print("### RUN RESULT ###")
    print(json.dumps(results, indent=2))


def run_archive_legacy():
    print("--- Auditoria de Arquivamento Legado ---")
    prices_to_archive = []
    
    for p in stripe.Price.list(limit=100, active=True).auto_paging_iter():
        if p.lookup_key and p.lookup_key.startswith("vedium_prod_"):
            prices_to_archive.append(p)
            
    if not prices_to_archive:
        print("Nenhum Price legado (vedium_prod_) ativo encontrado.")
        return
        
    safe_to_archive = []
    has_dependency = []
    
    for p in prices_to_archive:
        plans = frappe.get_all("Subscription Plan", filters={"product_price_id": p.id}, fields=["name"])
        if plans:
            has_dependency.append((p.id, plans[0].name))
        else:
            safe_to_archive.append(p)
            
    print(f"Prices legados encontrados: {len(prices_to_archive)}")
    print(f"Prices legados com dependências Frappe: {len(has_dependency)}")
    print(f"Prices legados SEGUROS para arquivar: {len(safe_to_archive)}")
    
    for p in safe_to_archive:
        print(f"Arquivando {p.id} ({p.lookup_key})")
        stripe.Price.modify(p.id, active=False)
    print("✅ Arquivamento aplicado.")
