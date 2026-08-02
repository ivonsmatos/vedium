import frappe
import stripe
import json

def run(dry_run=True, apply=False):
    print(f"--- Iniciando sincronizacao final (dry_run={dry_run}, apply={apply}) ---")
    
    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        print("STRIPE_SECRET_KEY não configurada!")
        return
        
    if apply and not dry_run:
        sessions_to_expire = [
            "cs_live_a1D8QLhiILDXUvUg7Kywy1cS27fDP9LaZ6MmOsV799dQHP2pFO9QyUQVHH",
            "cs_live_a1rOHgmGxflJTpaJKWDvvgATCbJqLdATHKsW89sHxqVPELnZyImfZuZcSj",
            "cs_live_a1LuzLWb4bwIHhtIzfdNS1ebxsj9kAkWmhTe95rm08tShzEdlZjklN4wss",
            "cs_live_a1XK6ZFWwIZNfmdDdLxb24doXoO4F3KEv1Jk2hOhQDE6PJPYBkfWhMB7IL",
            "cs_live_a1KhOtoixSiqvBYim9zP9q9ZyO0zuA9eC6NI7gayutSHwgUMSCXj6MUy0c",
            "cs_live_a1e91OTHrDSoul6I2DD8xiuHyxrnlaOPVMDPyL4HNsMF7X42drNf43ilUT"
        ]
        for sid in sessions_to_expire:
            try:
                s = stripe.checkout.Session.retrieve(sid)
                if s.status == "open":
                    stripe.checkout.Session.expire(sid)
            except Exception:
                pass
                
        try:
            open_sessions = stripe.checkout.Session.list(status="open", limit=100)
            for s in open_sessions.auto_paging_iter():
                lines = stripe.checkout.Session.list_line_items(s.id, limit=5)
                is_invalid = False
                for item in lines.data:
                    price = item.price
                    if not price: continue
                    if not price.active or price.unit_amount == 0 or (price.recurring and price.recurring.interval_count == 6):
                        is_invalid = True
                        break
                    if price.recurring and price.recurring.interval_count in [6, 10, 12]:
                        is_invalid = True
                        break
                if is_invalid:
                    stripe.checkout.Session.expire(s.id)
        except Exception:
            pass

    prices = {
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
        if "ingl" in slug or "ingles" in slug: return prices["ingles"]
        if "iorub" in slug or "ioruba" in slug: return prices["ioruba"]
        if slug in prices: return prices[slug]
        return None

    def get_stripe_gateway_reference(currency):
        meta = frappe.get_meta("Subscription Plan")
        field = meta.get_field("payment_gateway")
        target_doctype = field.options if field else None
        
        gateways = frappe.get_all(
            "Payment Gateway",
            fields=["name", "gateway_controller"]
        )
        
        stripe_gateways = [
            row.name
            for row in gateways
            if "stripe" in (row.gateway_controller or "").lower()
        ]
        
        if not stripe_gateways:
            frappe.throw("Nenhum gateway Stripe encontrado no sistema.")
            
        if target_doctype == "Payment Gateway":
            return stripe_gateways[0]
            
        if target_doctype == "Payment Gateway Account":
            accounts = frappe.get_all(
                "Payment Gateway Account",
                filters={"payment_gateway": ["in", stripe_gateways]},
                fields=["name", "currency"]
            )
            
            valid = [
                a for a in accounts
                if not a.currency or a.currency.upper() == currency.upper()
            ]
            
            if not valid:
                frappe.throw(f"Conta Stripe para a moeda {currency} não encontrada de forma inequívoca.")
                
            return valid[0].name
            
        frappe.throw(f"Tipo inesperado em Subscription Plan.payment_gateway: {target_doctype}")

    courses = frappe.get_all('LMS Course', fields=['name', 'title', 'custom_stripe_monthly_plan', 'custom_stripe_annual_plan'])
    all_items = {i.name: i for i in frappe.get_all('Item', fields=['name', 'item_name'])}
    
    existing_products = {}
    for p in stripe.Product.list(limit=100).auto_paging_iter():
        existing_products[p.name] = p.id
        
    dry_run_results = {
        "products_created": 0,
        "prices_created": 0,
        "items_created": [],
        "plans_created": [],
        "plans_updated": [],
        "courses_linked": []
    }
    
    for c in courses:
        if "teste" in c.name.lower():
            continue
            
        monthly_cents = get_monthly_price(c.name)
        if not monthly_cents:
            continue
            
        currency = "usd" if "portugues" in c.name else "brl"
        
        product_name = c.title
        product_id = existing_products.get(product_name)
        if not product_id:
            dry_run_results["products_created"] += 1
            if apply and not dry_run:
                try:
                    prod = stripe.Product.create(name=product_name, statement_descriptor="VEDIUM CURSO")
                    product_id = prod.id
                    existing_products[product_name] = product_id
                except Exception as e:
                    print(f"Erro Product {product_name}: {e}")
                    continue
            else:
                product_id = "prod_dummy"
                
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
            dry_run_results["items_created"].append(item_id)
            if apply and not dry_run:
                item_doc = frappe.new_doc("Item")
                item_doc.item_code = item_id
                item_doc.item_name = c.title
                item_doc.item_group = "Cursos e Serviços"
                item_doc.stock_uom = frappe.db.get_value("Item", "CURSO-ESPANHOL-BASICO", "stock_uom") or "Nos"
                item_doc.is_stock_item = 0
                try:
                    item_doc.insert(ignore_permissions=True)
                    all_items[item_id] = item_doc
                except Exception as e:
                    print(f"Erro criar Item {item_id}: {e}")
        
        monthly_plan_name = f"Vedium — {c.title} — Mensal"
        try:
            stripe_prices = stripe.Price.list(product=product_id, active=True, currency=currency)
            monthly_price = next((p for p in stripe_prices.data if p.recurring.interval == 'month' and p.recurring.interval_count == 1 and p.unit_amount == monthly_cents), None)
            monthly_price_id = "price_dummy"
            
            if not monthly_price:
                dry_run_results["prices_created"] += 1
                if apply and not dry_run:
                    monthly_price = stripe.Price.create(product=product_id, unit_amount=monthly_cents, currency=currency, recurring={"interval": "month", "interval_count": 1}, nickname=monthly_plan_name)
                    monthly_price_id = monthly_price.id
            else:
                monthly_price_id = monthly_price.id
                
            if not frappe.db.exists('Subscription Plan', monthly_plan_name):
                dry_run_results["plans_created"].append(monthly_plan_name)
                if apply and not dry_run:
                    doc = frappe.new_doc('Subscription Plan')
                    doc.plan_name = monthly_plan_name
                    doc.product_price_id = monthly_price_id
                    doc.cost = monthly_cents / 100
                    doc.currency = currency.upper()
                    doc.billing_interval = "Month"
                    doc.billing_interval_count = 1
                    doc.item = item_id
                    doc.price_determination = "Fixed Rate"
                    doc.payment_gateway = get_stripe_gateway_reference(currency)
                    doc.insert(ignore_permissions=True)
            else:
                # Check for diff
                plan_doc = frappe.get_doc('Subscription Plan', monthly_plan_name)
                cost = monthly_cents / 100
                expected_gateway = get_stripe_gateway_reference(currency)
                if plan_doc.product_price_id != monthly_price_id or float(plan_doc.cost) != float(cost) or plan_doc.item != item_id or plan_doc.price_determination != "Fixed Rate" or plan_doc.payment_gateway != expected_gateway:
                    dry_run_results["plans_updated"].append(monthly_plan_name)
                    if apply and not dry_run:
                        frappe.db.set_value('Subscription Plan', monthly_plan_name, {'product_price_id': monthly_price_id, 'cost': cost, 'currency': currency.upper(), 'item': item_id, 'price_determination': "Fixed Rate", 'payment_gateway': expected_gateway})
                    
            if c.custom_stripe_monthly_plan != monthly_plan_name:
                dry_run_results["courses_linked"].append(f"{c.name} (Mensal)")
                if apply and not dry_run:
                    frappe.db.set_value('LMS Course', c.name, 'custom_stripe_monthly_plan', monthly_plan_name)
        except Exception as e:
            print(f"[{c.title}] Erro Mensal: {e}")

        annual_cents = int(monthly_cents * 10 / 12)
        annual_plan_name = f"Vedium — {c.title} — Anual"
        try:
            stripe_prices = stripe.Price.list(product=product_id, active=True, currency=currency)
            annual_price = next((p for p in stripe_prices.data if p.recurring.interval == 'month' and p.recurring.interval_count == 1 and p.unit_amount == annual_cents), None)
            annual_price_id = "price_dummy"
            
            if not annual_price:
                dry_run_results["prices_created"] += 1
                if apply and not dry_run:
                    annual_price = stripe.Price.create(product=product_id, unit_amount=annual_cents, currency=currency, recurring={"interval": "month", "interval_count": 1}, nickname=annual_plan_name)
                    annual_price_id = annual_price.id
            else:
                annual_price_id = annual_price.id
                
            if not frappe.db.exists('Subscription Plan', annual_plan_name):
                dry_run_results["plans_created"].append(annual_plan_name)
                if apply and not dry_run:
                    doc = frappe.new_doc('Subscription Plan')
                    doc.plan_name = annual_plan_name
                    doc.product_price_id = annual_price_id
                    doc.cost = annual_cents / 100
                    doc.currency = currency.upper()
                    doc.billing_interval = "Month"
                    doc.billing_interval_count = 1
                    doc.item = item_id
                    doc.price_determination = "Fixed Rate"
                    doc.payment_gateway = get_stripe_gateway_reference(currency)
                    doc.insert(ignore_permissions=True)
            else:
                # Check for diff
                plan_doc = frappe.get_doc('Subscription Plan', annual_plan_name)
                cost = annual_cents / 100
                expected_gateway = get_stripe_gateway_reference(currency)
                if plan_doc.product_price_id != annual_price_id or float(plan_doc.cost) != float(cost) or plan_doc.item != item_id or plan_doc.price_determination != "Fixed Rate" or plan_doc.payment_gateway != expected_gateway:
                    dry_run_results["plans_updated"].append(annual_plan_name)
                    if apply and not dry_run:
                        frappe.db.set_value('Subscription Plan', annual_plan_name, {'product_price_id': annual_price_id, 'cost': cost, 'currency': currency.upper(), 'item': item_id, 'price_determination': "Fixed Rate", 'payment_gateway': expected_gateway})
                    
            if c.custom_stripe_annual_plan != annual_plan_name:
                dry_run_results["courses_linked"].append(f"{c.name} (Anual)")
                if apply and not dry_run:
                    frappe.db.set_value('LMS Course', c.name, 'custom_stripe_annual_plan', annual_plan_name)
        except Exception as e:
            print(f"[{c.title}] Erro Anual: {e}")
            
    if apply and not dry_run:
        frappe.db.commit()
        print("✅ Sincronizacao final concluida!")
    else:
        print("### DRY RUN RESULT ###")
        print(json.dumps(dry_run_results, indent=2))
