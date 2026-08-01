import frappe
import stripe
from frappe.utils import cint

def run(*args, **kwargs):
    dry_run = cint(kwargs.get("dry_run", 0))
    print(f"--- INICIANDO MIGRACAO (DRY RUN = {dry_run}) ---")
    
    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    
    # 1. Auditar Gateways
    gateways = frappe.get_all("Payment Gateway", fields=["name", "gateway_controller"])
    stripe_gateways = [g.name for g in gateways if "stripe" in g.gateway_controller.lower()]
    if not stripe_gateways:
        frappe.throw("Nenhum gateway Stripe valido encontrado!")
    master_gateway = stripe_gateways[0]
    
    # 2. Verificar se ha assinaturas ativas semestrais
    semestral_enrollments = frappe.get_all("LMS Enrollment", filters={"custom_billing_period": "semestral", "custom_vedium_status": ["in", ["Active", "Trial", "Pending Review"]]}, fields=["name", "member", "course"])
    if semestral_enrollments:
        print(f"ABORTANDO: Encontradas {len(semestral_enrollments)} assinaturas semestrais ativas!")
        for e in semestral_enrollments:
            print(e)
        return
        
    courses = frappe.get_all("LMS Course", filters={"paid_course": 1}, fields=["name", "title", "currency"])
    
    for course in courses:
        print(f"\nProcessando {course.title}...")
        
        # Recuperando via BD puro para garantir que pegamos a coluna antiga, mesmo que escondida
        old_semestral = frappe.db.get_value("LMS Course", course.name, "custom_stripe_semestral_plan")
        anual = frappe.db.get_value("LMS Course", course.name, "custom_stripe_annual_plan")
        
        new_monthly_name = f"{course.title} – Mensal"
        new_monthly_price = None
        
        if old_semestral:
            old_plan_doc = frappe.get_doc("Subscription Plan", old_semestral)
            print(f"  [SEMESTRAL] Encontrado: {old_plan_doc.name}")
            
            # Checar uso
            used = frappe.db.exists("LMS Enrollment", {"custom_stripe_price_id": old_plan_doc.product_price_id})
            
            if not dry_run:
                # Inativar price no stripe
                try:
                    stripe.Price.modify(old_plan_doc.product_price_id, active=False)
                    print(f"  [STRIPE] Price {old_plan_doc.product_price_id} inativado.")
                except Exception as e:
                    print(f"  [STRIPE ERRO] Não foi possivel inativar {old_plan_doc.product_price_id}: {e}")
                
                if used:
                    frappe.db.set_value("Subscription Plan", old_semestral, "enabled", 0)
                    frappe.rename_doc("Subscription Plan", old_semestral, f"[ARQUIVADO] {old_semestral}", force=True, ignore_if_exists=True)
                    print(f"  [FRAPPE] Plano arquivado.")
                else:
                    frappe.delete_doc("Subscription Plan", old_semestral, force=1)
                    print(f"  [FRAPPE] Plano deletado definitivamente (sem uso historico).")
            else:
                print(f"  (Dry Run) Inativaria Price {old_plan_doc.product_price_id} e {'arquivaria' if used else 'deletaria'} o plano Frappe.")
                
            # O valor mensal sera o mesmo valor que estava configurado no Semestral! (Ja que o semestral ja era 1 mes)
            monthly_cost = old_plan_doc.cost
            
            if not dry_run:
                # Criar o novo Price mensal real
                try:
                    old_price_stripe = stripe.Price.retrieve(old_plan_doc.product_price_id)
                    new_price_stripe = stripe.Price.create(
                        product=old_price_stripe.product,
                        unit_amount=int(monthly_cost * 100),
                        currency=course.currency.lower(),
                        recurring={"interval": "month", "interval_count": 1},
                        metadata={"vedium_plan_type": "monthly", "vedium_commitment_months": "0"}
                    )
                    new_monthly_price = new_price_stripe.id
                    print(f"  [STRIPE] Novo Price Mensal criado: {new_monthly_price}")
                except Exception as e:
                    print(f"  [STRIPE ERRO] Falha ao criar novo price mensal: {e}")
            else:
                print("  (Dry Run) Criaria novo Price mensal no Stripe.")
                new_monthly_price = "price_dry_run_monthly"
                
            if not dry_run:
                # Criar novo Subscription Plan Mensal
                if not frappe.db.exists("Subscription Plan", new_monthly_name):
                    new_plan = frappe.get_doc({
                        "doctype": "Subscription Plan",
                        "plan_name": new_monthly_name,
                        "payment_gateway": old_plan_doc.payment_gateway,
                        "product_price_id": new_monthly_price,
                        "billing_interval": "Month",
                        "billing_interval_count": 1,
                        "currency": course.currency,
                        "cost": monthly_cost
                    })
                    new_plan.insert(ignore_permissions=True)
                    print(f"  [FRAPPE] Plano {new_monthly_name} criado.")
                else:
                    frappe.db.set_value("Subscription Plan", new_monthly_name, "product_price_id", new_monthly_price)
                    
                frappe.db.set_value("LMS Course", course.name, "custom_stripe_monthly_plan", new_monthly_name)
                # Anula a coluna antiga
                frappe.db.set_value("LMS Course", course.name, "custom_stripe_semestral_plan", None)
            else:
                print(f"  (Dry Run) Criaria Subscription Plan '{new_monthly_name}' e associaria a custom_stripe_monthly_plan.")

        # Atualizar Metadados do Price Anual
        if anual:
            print(f"  [ANUAL] Encontrado: {anual}")
            anual_doc = frappe.get_doc("Subscription Plan", anual)
            if not dry_run:
                try:
                    stripe.Price.modify(
                        anual_doc.product_price_id, 
                        metadata={"vedium_plan_type": "annual", "vedium_commitment_months": "12"}
                    )
                    print(f"  [STRIPE] Metadata anual atualizado.")
                except Exception as e:
                    print(f"  [STRIPE ERRO] {e}")
            else:
                print("  (Dry Run) Atualizaria metadata no price Anual.")
                
    if not dry_run:
        frappe.db.commit()
        print("\n--- MIGRACAO CONCLUIDA COM SUCESSO ---")
    else:
        print("\n--- DRY RUN CONCLUIDO ---")
