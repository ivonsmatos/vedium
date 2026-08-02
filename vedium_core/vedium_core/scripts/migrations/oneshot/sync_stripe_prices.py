import frappe
import stripe
import json

def run():
    print("Iniciando sincronizacao final e fechamento de Checkout Sessions...")
    
    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        print("STRIPE_SECRET_KEY não configurada!")
        return
    
    # 1. Expire Checkout Sessions abertas indevidas
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
                print(f"Sessao {sid} expirada com sucesso.")
            else:
                print(f"Sessao {sid} ja esta com status '{s.status}'.")
        except Exception as e:
            print(f"Erro ao expirar {sid}: {e}")

    # Expirar sessoes invalidas listando todas com status open
    try:
        open_sessions = stripe.checkout.Session.list(status="open", limit=100)
        for s in open_sessions.auto_paging_iter():
            # Pegar os line_items para ver os prices
            lines = stripe.checkout.Session.list_line_items(s.id, limit=5)
            is_invalid = False
            for item in lines.data:
                price = item.price
                if not price:
                    continue
                # Inativo, zerado, ou periodo semestral (interval_count=6)
                if not price.active or price.unit_amount == 0 or (price.recurring and price.recurring.interval_count == 6):
                    is_invalid = True
                    break
                # Valor multiplicado por 6, 10 ou 12
                # Isso seria mais dificil de verificar genericamente, mas geralmente
                # se interval_count > 1 ou se o price nickname tiver semestral.
                if price.recurring and price.recurring.interval_count in [6, 10, 12]:
                    is_invalid = True
                    break
            if is_invalid:
                stripe.checkout.Session.expire(s.id)
                print(f"Sessao {s.id} invalidada e expirada.")
    except Exception as e:
        print(f"Erro ao listar/expirar sessoes abertas: {e}")

    # 2. Corrigir Stripe Customer Portal (apenas listando que deveria ser feito no dashboard ou pela API)
    # A API não permite atualizar Customer Portal config default diretamente sem o ID da config.
    # Mas tentaremos atualizar a config default:
    try:
        configs = stripe.billing_portal.Configuration.list(is_default=True, limit=1)
        if configs.data:
            config_id = configs.data[0].id
            stripe.billing_portal.Configuration.modify(
                config_id,
                business_profile={
                    "privacy_policy_url": "https://vediums.com/privacidade",
                    "terms_of_service_url": "https://vediums.com/termos"
                }
            )
            print("Customer Portal Config atualizada com URLs corretas.")
    except Exception as e:
        print(f"Erro ao atualizar Customer Portal config: {e}")

    # 3. Tabela de Preços Oficial (Aprovada)
    # prices em centavos!
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

    courses = frappe.get_all('LMS Course', fields=['name', 'title', 'custom_stripe_monthly_plan', 'custom_stripe_annual_plan'])
    
    # Cache products by name
    existing_products = {}
    for p in stripe.Product.list(limit=100).auto_paging_iter():
        existing_products[p.name] = p.id
        
    for c in courses:
        monthly_cents = get_monthly_price(c.name)
        if not monthly_cents:
            continue
            
        currency = "usd" if "portugues" in c.name else "brl"
        
        # Obter ou criar Product
        product_id = existing_products.get(c.title)
        if not product_id:
            print(f"Criando produto Stripe para: {c.title}")
            try:
                prod = stripe.Product.create(name=c.title, statement_descriptor="VEDIUM CURSO")
                product_id = prod.id
                existing_products[c.title] = product_id
            except Exception as e:
                print(f"Erro ao criar produto para {c.title}: {e}")
                continue
                
        # --- MENSAL ---
        monthly_plan_name = f"Vedium — {c.title} — Mensal"
        try:
            # Buscar price mensal ativo
            stripe_prices = stripe.Price.list(product=product_id, active=True, currency=currency)
            monthly_price = next((p for p in stripe_prices.data if p.recurring.interval == 'month' and p.recurring.interval_count == 1 and p.unit_amount == monthly_cents), None)
            
            if not monthly_price:
                monthly_price = stripe.Price.create(
                    product=product_id,
                    unit_amount=monthly_cents,
                    currency=currency,
                    recurring={"interval": "month", "interval_count": 1},
                    nickname=monthly_plan_name
                )
                print(f"[{c.title}] Price Mensal criado: {monthly_price.id}")
            else:
                print(f"[{c.title}] Price Mensal ja existe: {monthly_price.id}")
                
            # Atualizar ou criar Subscription Plan Frappe
            if not frappe.db.exists('Subscription Plan', monthly_plan_name):
                doc = frappe.new_doc('Subscription Plan')
                doc.plan_name = monthly_plan_name
                doc.product_price_id = monthly_price.id
                doc.cost = monthly_cents / 100
                doc.currency = currency.upper()
                doc.billing_interval = "Month"
                doc.billing_interval_count = 1
                doc.insert(ignore_permissions=True)
            else:
                frappe.db.set_value('Subscription Plan', monthly_plan_name, {
                    'product_price_id': monthly_price.id,
                    'cost': monthly_cents / 100,
                    'currency': currency.upper()
                })
                
            # Atualizar LMS Course
            frappe.db.set_value('LMS Course', c.name, 'custom_stripe_monthly_plan', monthly_plan_name)
            
        except Exception as e:
            print(f"[{c.title}] Erro Mensal: {e}")

        # --- ANUAL ---
        annual_cents = int(monthly_cents * 10 / 12)
        annual_plan_name = f"Vedium — {c.title} — Anual"
        try:
            # Buscar price anual ativo
            stripe_prices = stripe.Price.list(product=product_id, active=True, currency=currency)
            annual_price = next((p for p in stripe_prices.data if p.recurring.interval == 'month' and p.recurring.interval_count == 1 and p.unit_amount == annual_cents), None)
            
            if not annual_price:
                annual_price = stripe.Price.create(
                    product=product_id,
                    unit_amount=annual_cents,
                    currency=currency,
                    recurring={"interval": "month", "interval_count": 1},
                    nickname=annual_plan_name
                )
                print(f"[{c.title}] Price Anual criado: {annual_price.id}")
            else:
                print(f"[{c.title}] Price Anual ja existe: {annual_price.id}")
                
            # Atualizar ou criar Subscription Plan Frappe
            if not frappe.db.exists('Subscription Plan', annual_plan_name):
                doc = frappe.new_doc('Subscription Plan')
                doc.plan_name = annual_plan_name
                doc.product_price_id = annual_price.id
                doc.cost = annual_cents / 100
                doc.currency = currency.upper()
                doc.billing_interval = "Month"
                doc.billing_interval_count = 1
                doc.insert(ignore_permissions=True)
            else:
                frappe.db.set_value('Subscription Plan', annual_plan_name, {
                    'product_price_id': annual_price.id,
                    'cost': annual_cents / 100,
                    'currency': currency.upper()
                })
                
            # Atualizar LMS Course
            frappe.db.set_value('LMS Course', c.name, 'custom_stripe_annual_plan', annual_plan_name)
            
        except Exception as e:
            print(f"[{c.title}] Erro Anual: {e}")
            
    frappe.db.commit()
    print("✅ Sincronizacao final concluida!")
