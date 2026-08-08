"""Preços USD fixos (premium internacional) + planos USD por curso.

Decisão 2026-08-08: o público internacional (páginas EN/ES) paga em **USD com
preço FIXO e redondo por curso**, acima da conversão por câmbio (o mercado
internacional de aula ao vivo suporta — concorrentes cobram US$79-129/mês). NÃO é
câmbio. Cobrança escolhida pela LÍNGUA da página (EN/ES → USD, PT → BRL).

Mecânica (a mesma do Hebraico Particular, caminho base+quantidade): 1 preço Stripe
USD **mensal** + 1 **anual** por curso, num Subscription Plan USD. A escala 1–5x
sai por `quantity` + cupom de frequência no checkout. Assim são ~34 preços USD (17
cursos × 2), não 190 — e reusa o caminho legado (`_plan_payload`) já provado.

Fonte de verdade dos valores = `USD_MONTHLY_1X` abaixo. PLE fica de fora (já é USD
nativo, US$90/120 — não reconverter).
"""

from __future__ import annotations

import frappe

from vedium_core.catalog_registry import CATALOG

USD_GATEWAY = "Stripe-Stripe - USD - VDM"
ANNUAL_FACTOR = 0.78  # anual ~-22%/mês, como o doméstico

# Preço USD/mês (1x/semana) por curso — aprovado pelo usuário em 2026-08-08.
USD_MONTHLY_1X = {
    "hebraico-a0-alfabetizacao": 59,
    "ingl-s-beginner": 79,
    "ingl-s-elementary": 79,
    "ingl-s-pr-intermedi-rio": 79,
    "ingl-s-intermedi-rio": 79,
    "ingl-s-upper-intermedi-rio": 79,
    "ingl-s-avan-ado": 79,
    "espanhol-basico": 79,
    "iorub-b-sico": 99,
    "iorub-intermedi-rio": 99,
    "iorub-avan-ado": 99,
    "espanhol-intermediario": 109,
    "hebraico-moderno-a1": 109,
    "hebraico-moderno-a2-b1": 119,
    "espanhol-avancado": 139,
    "hebraico-biblico-leitura-guiada": 139,
    "hebraico-particular": 149,
}


def usd_monthly_amount(course_name: str):
    """Preço USD/mês (1x) do curso, ou None se o curso não vende em USD."""
    return USD_MONTHLY_1X.get(course_name)


def usd_annual_amount(course_name: str):
    monthly = USD_MONTHLY_1X.get(course_name)
    return round(monthly * ANNUAL_FACTOR) if monthly else None


def usd_plan_name(course_name: str, period: str) -> str:
    label = "Anual" if period == "annual" else "Mensal"
    return f"Vedium USD — {course_name} — {label}"


def ensure_usd_plans():
    """Cria/atualiza (idempotente) os preços Stripe USD + Subscription Plans USD.

    Otimizado: se o Subscription Plan já existe com o `cost` certo e um
    product_price_id, PULA a Stripe (não bate na API a cada deploy). Só cria/ajusta
    quando falta ou o valor mudou. Nunca levanta — roda no after_migrate."""
    created = []
    errors = []
    skipped = {"no_cfg": [], "already": []}
    for course_name, monthly in USD_MONTHLY_1X.items():
        cfg = CATALOG.get(course_name)
        if not cfg or not cfg.get("product_id"):
            skipped["no_cfg"].append(course_name)
            continue
        product_id = cfg["product_id"]
        for period, amount in (
            ("monthly", monthly),
            ("annual", round(monthly * ANNUAL_FACTOR)),
        ):
            plan_name = usd_plan_name(course_name, period)
            existing = frappe.db.get_value(
                "Subscription Plan", plan_name, ["cost", "product_price_id"], as_dict=True
            )
            if existing and float(existing.cost) == float(amount) and existing.product_price_id:
                skipped["already"].append(plan_name)
                continue
            try:
                price_id = _ensure_usd_price(course_name, period, product_id, amount)
                _ensure_usd_subscription_plan(plan_name, price_id, amount, course_name)
                created.append(plan_name)
            except Exception as exc:
                frappe.db.rollback()
                errors.append(f"{course_name}:{period}: {type(exc).__name__}: {exc}")
    frappe.db.commit()
    return {"created_or_updated": created, "skipped": skipped, "errors": errors}


def _ensure_usd_price(course_name, period, product_id, amount) -> str:
    """Preço Stripe USD recorrente mensal (base 1x), idempotente via lookup_key."""
    import stripe

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        raise RuntimeError("STRIPE_SECRET_KEY ausente")

    lookup_key = f"vedium-usd-{course_name}-{period}"
    unit_amount = int(round(float(amount) * 100))

    found = stripe.Price.list(lookup_keys=[lookup_key], limit=1).data
    if found and found[0].unit_amount == unit_amount and found[0].active:
        return found[0].id

    price = stripe.Price.create(
        product=product_id,
        currency="usd",
        unit_amount=unit_amount,
        recurring={"interval": "month", "interval_count": 1},
        lookup_key=lookup_key,
        transfer_lookup_key=True,
        nickname=usd_plan_name(course_name, period),
    )
    return price.id


def _ensure_usd_subscription_plan(plan_name, price_id, amount, course_name=None):
    if frappe.db.exists("Subscription Plan", plan_name):
        plan = frappe.get_doc("Subscription Plan", plan_name)
    else:
        plan = frappe.new_doc("Subscription Plan")
        plan.plan_name = plan_name
    plan.currency = "USD"
    plan.price_determination = "Fixed Rate"
    plan.cost = float(amount)
    plan.billing_interval = "Month"
    plan.billing_interval_count = 1
    plan.payment_gateway = USD_GATEWAY
    plan.product_price_id = price_id
    if course_name:
        item = _ensure_course_item(course_name)
        if item:
            plan.item = item
    plan.save(ignore_permissions=True)


def _ensure_course_item(course_name):
    """Item ERPNext exigido pelo Subscription Plan. Reusa o Item do plano BRL do
    mesmo curso se existir; senão cria um item de serviço mínimo."""
    # Reusa o item de um Subscription Plan BRL já existente do mesmo curso.
    title = frappe.db.get_value("LMS Course", course_name, "title") or course_name
    existing_brl = frappe.db.get_value(
        "Subscription Plan", f"Vedium — {title} — Mensal", "item"
    )
    if existing_brl:
        return existing_brl

    if not frappe.db.exists("DocType", "Item"):
        return None

    item_code = f"CURSO-{course_name.upper()}"
    if frappe.db.exists("Item", item_code):
        return item_code

    group = frappe.db.get_value("Item Group", {"is_group": 0}, "name") or frappe.db.get_value(
        "Item Group", {}, "name"
    )
    uom = frappe.db.get_value("UOM", {"name": "Unit"}, "name") or frappe.db.get_value("UOM", {}, "name")
    item = frappe.get_doc({
        "doctype": "Item",
        "item_code": item_code,
        "item_name": (title or course_name)[:140],
        "item_group": group,
        "stock_uom": uom,
        "is_stock_item": 0,
        "is_sales_item": 1,
    })
    item.insert(ignore_permissions=True)
    return item.name
