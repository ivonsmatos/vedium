"""
vedium_stripe_audit.py — Auditoria Stripe + Frappe para a Vedium.

Uso:
  STRIPE_SECRET_KEY=sk_live_... python3 vedium_stripe_audit.py \
      --frappe-json /tmp/frappe_stripe_config.json \
      [--output matrix.json]

Saída:
  - Tabela formatada no stdout com a MATRIZ DE PREÇOS
  - JSON completo em --output (padrão: stripe_audit_result.json)

NÃO escreve nada no Stripe nem no Frappe.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
NOT_COMMERCIAL_SLUGS = {"teste-validacao-de-pagamento", "teste-validacao"}
NOT_COMMERCIAL_TITLES = {"TESTE - Validacao de Pagamento", "TESTE"}

SUPPORTED_CURRENCIES = {"BRL", "USD"}

# Status codes
APPROVED = "APROVADO"
PENDING_VALUE = "PENDENTE DE VALOR"
PENDING_PRODUCT = "PENDENTE DE PRODUCT"
INCONSISTENT = "INCONSISTENTE"
NOT_COMMERCIAL = "NAO COMERCIAL"


# ---------------------------------------------------------------------------
# Stripe helpers (sem frappe)
# ---------------------------------------------------------------------------

def _stripe():
    try:
        import stripe as _s
        return _s
    except ImportError:
        sys.exit("Instale o SDK: pip install stripe")


def _list_all(stripe, resource, **kwargs):
    items = []
    for item in resource.list(limit=100, **kwargs).auto_paging_iter():
        items.append(dict(item))
    return items


def fetch_stripe_data(stripe) -> dict:
    """Lista todos os Products e Prices do Stripe."""
    print("  → Buscando Products do Stripe...")
    products = {p["id"]: p for p in _list_all(stripe, stripe.Product, active=None)}
    print(f"     {len(products)} Products encontrados")

    print("  → Buscando Prices ativos...")
    active_prices = {p["id"]: p for p in _list_all(stripe, stripe.Price, active=True)}
    print(f"     {len(active_prices)} Prices ativos")

    print("  → Buscando Prices inativos...")
    inactive_prices = {
        p["id"]: p
        for p in _list_all(stripe, stripe.Price, active=False)
        if p.get("type") == "recurring"
    }
    print(f"     {len(inactive_prices)} Prices inativos recorrentes")

    return {
        "products": products,
        "active_prices": active_prices,
        "inactive_prices": inactive_prices,
        "all_prices": {**active_prices, **inactive_prices},
    }


# ---------------------------------------------------------------------------
# Análise de cada curso
# ---------------------------------------------------------------------------

def _slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-")


def _is_test_course(course: dict) -> bool:
    name = course.get("name", "")
    title = course.get("title", "")
    return (
        _slug(name) in NOT_COMMERCIAL_SLUGS
        or any(t.lower() in title.lower() for t in NOT_COMMERCIAL_TITLES)
        or "teste" in name.lower()
    )


def _price_status(price_id: str | None, all_prices: dict) -> dict:
    """Retorna um resumo do Price ou erro se não encontrado."""
    if not price_id or not price_id.startswith("price_"):
        return {"found": False, "active": False, "error": "sem price_id válido"}
    p = all_prices.get(price_id)
    if not p:
        return {"found": False, "active": False, "error": "price_id não encontrado no Stripe"}
    recurring = p.get("recurring") or {}
    return {
        "found": True,
        "active": p.get("active", False),
        "type": p.get("type"),
        "currency": (p.get("currency") or "").upper(),
        "unit_amount": p.get("unit_amount"),
        "interval": recurring.get("interval"),
        "interval_count": recurring.get("interval_count"),
        "product_id": p.get("product"),
        "nickname": p.get("nickname"),
        "metadata": p.get("metadata") or {},
        "created": p.get("created"),
        "error": None,
    }


def _classify_plan(
    course: dict,
    period: str,
    plan_name: str | None,
    plans: dict,
    gateways: dict,
    all_prices: dict,
    products: dict,
) -> dict:
    """Classifica um curso/período e retorna a linha da matriz."""
    field = "custom_stripe_annual_plan" if period == "annual" else "custom_stripe_monthly_plan"

    row: dict[str, Any] = {
        "course_id": course.get("name"),
        "course_title": course.get("title"),
        "period": period,
        "published": course.get("published", False),
        "plan_name": plan_name,
        "plan_cost": None,
        "plan_currency": None,
        "plan_billing_interval": None,
        "plan_billing_interval_count": None,
        "plan_gateway": None,
        "plan_gateway_ok": False,
        "price_id": None,
        "price_active": False,
        "price_type": None,
        "price_currency": None,
        "price_unit_amount": None,
        "price_interval": None,
        "price_interval_count": None,
        "price_product_id": None,
        "price_product_name": None,
        "price_error": None,
        "status": PENDING_PRODUCT,
        "issues": [],
        "action": "INVESTIGAR",
    }

    if not plan_name:
        row["issues"].append(f"campo {field} vazio no LMS Course")
        row["status"] = PENDING_PRODUCT
        row["action"] = "CRIAR SUBSCRIPTION PLAN E VINCULAR"
        return row

    plan = plans.get(plan_name)
    if not plan:
        row["issues"].append(f"Subscription Plan '{plan_name}' não encontrado no Frappe")
        row["status"] = INCONSISTENT
        row["action"] = "RECRIAR SUBSCRIPTION PLAN"
        return row

    row["plan_cost"] = plan.get("cost")
    row["plan_currency"] = (plan.get("currency") or "").upper()
    row["plan_billing_interval"] = plan.get("billing_interval")
    row["plan_billing_interval_count"] = plan.get("billing_interval_count")

    gw = plan.get("payment_gateway")
    row["plan_gateway"] = gw
    ctrl = gateways.get(gw, "") or ""
    row["plan_gateway_ok"] = "stripe" in ctrl.lower()

    price_id = (plan.get("product_price_id") or "").strip()
    row["price_id"] = price_id

    ps = _price_status(price_id, all_prices)
    row["price_active"] = ps.get("active", False)
    row["price_type"] = ps.get("type")
    row["price_currency"] = ps.get("currency")
    row["price_unit_amount"] = ps.get("unit_amount")
    row["price_interval"] = ps.get("interval")
    row["price_interval_count"] = ps.get("interval_count")
    row["price_product_id"] = ps.get("product_id")
    row["price_error"] = ps.get("error")

    prod_id = ps.get("product_id")
    if prod_id and prod_id in products:
        row["price_product_name"] = products[prod_id].get("name")

    # Verificações
    issues = []

    if not row["plan_gateway_ok"]:
        issues.append(f"gateway '{gw}' não é Stripe (controller={ctrl!r})")

    if not ps.get("found"):
        issues.append(ps.get("error", "price não encontrado"))
    else:
        if not ps.get("active"):
            issues.append("Price INATIVO no Stripe")
        if ps.get("type") != "recurring":
            issues.append(f"Price type={ps.get('type')!r} (precisa ser 'recurring')")
        if (ps.get("interval") or "").lower() not in {"month", "monthly"}:
            issues.append(
                f"interval={ps.get('interval')!r} interval_count={ps.get('interval_count')} "
                "(Vedium usa month/1 para ambos os planos)"
            )
        if int(ps.get("interval_count") or 0) != 1:
            issues.append(f"interval_count={ps.get('interval_count')} (precisa ser 1)")
        unit = ps.get("unit_amount")
        if unit is None or unit == 0:
            issues.append("unit_amount ZERO ou ausente")
        if ps.get("currency") not in SUPPORTED_CURRENCIES:
            issues.append(f"moeda {ps.get('currency')!r} não suportada")

    row["issues"] = issues

    if not issues:
        row["status"] = APPROVED
        row["action"] = "NENHUMA (OK)"
    elif any("INATIVO" in i or "não encontrado" in i for i in issues):
        row["status"] = INCONSISTENT
        row["action"] = "CRIAR NOVO PRICE ATIVO + ATUALIZAR PLAN"
    elif any("interval" in i.lower() for i in issues):
        row["status"] = INCONSISTENT
        row["action"] = "CRIAR PRICE month/1 + ATUALIZAR PLAN"
    elif any("ZERO" in i for i in issues):
        row["status"] = PENDING_VALUE
        row["action"] = "AGUARDAR VALOR OFICIAL"
    else:
        row["status"] = INCONSISTENT
        row["action"] = "INVESTIGAR E CORRIGIR"

    return row


# ---------------------------------------------------------------------------
# Geração da matriz
# ---------------------------------------------------------------------------

def build_matrix(frappe_data: dict, stripe_data: dict) -> list[dict]:
    courses = frappe_data.get("courses") or []
    plans = frappe_data.get("plans") or {}
    gateways = frappe_data.get("gateways") or {}
    all_prices = stripe_data.get("all_prices") or {}
    products = stripe_data.get("products") or {}

    rows = []
    for course in sorted(courses, key=lambda c: c.get("title", "")):
        if _is_test_course(course):
            for period in ("monthly", "annual"):
                rows.append({
                    "course_id": course.get("name"),
                    "course_title": course.get("title"),
                    "period": period,
                    "published": course.get("published", False),
                    "plan_name": None,
                    "price_id": None,
                    "status": NOT_COMMERCIAL,
                    "issues": [],
                    "action": "EXCLUIR DO CATÁLOGO COMERCIAL",
                })
            continue

        for period in ("monthly", "annual"):
            field = "custom_stripe_annual_plan" if period == "annual" else "custom_stripe_monthly_plan"
            plan_name = course.get(field)
            row = _classify_plan(
                course, period, plan_name, plans, gateways, all_prices, products
            )
            rows.append(row)

    return rows


# ---------------------------------------------------------------------------
# Exibição
# ---------------------------------------------------------------------------

def _mask(s: str | None, keep: int = 8) -> str:
    if not s:
        return "—"
    return s[:keep] + "..." if len(s) > keep else s


def print_matrix(rows: list[dict]) -> None:
    print("\n" + "=" * 120)
    print("MATRIZ DE PREÇOS — VEDIUM LMS × STRIPE")
    print("=" * 120)
    print(f"{'Curso':<30} {'Per.':<8} {'Status':<22} {'Plano':<30} {'Price ID':<20} "
          f"{'Valor':>8} {'Moeda':<5} {'Int.':<6} {'Ativo':<6} {'Issues'}")
    print("-" * 120)

    status_counts: dict[str, int] = {}
    for r in rows:
        st = r.get("status", "?")
        status_counts[st] = status_counts.get(st, 0) + 1

        price_id = _mask(r.get("price_id"), 12)
        valor = r.get("price_unit_amount")
        valor_str = f"{valor / 100:.2f}" if valor else "—"
        moeda = r.get("price_currency") or "—"
        interval = r.get("price_interval") or "—"
        ativo = "SIM" if r.get("price_active") else "NÃO"
        issues = "; ".join(r.get("issues") or [])[:60]
        plan = (r.get("plan_name") or "—")[:28]
        curso = (r.get("course_title") or r.get("course_id") or "?")[:28]
        periodo = r.get("period", "?")[:7]

        marker = "✅" if st == APPROVED else ("🚫" if st == NOT_COMMERCIAL else "⚠️ ")
        print(f"{marker} {curso:<28} {periodo:<8} {st:<22} {plan:<30} {price_id:<20} "
              f"{valor_str:>8} {moeda:<5} {interval:<6} {ativo:<6} {issues}")

    print("-" * 120)
    print("\nRESUMO:")
    for st, count in sorted(status_counts.items()):
        print(f"  {st:<25}: {count}")
    print()


# ---------------------------------------------------------------------------
# Relatório de problemas do Stripe
# ---------------------------------------------------------------------------

def print_stripe_issues(stripe_data: dict) -> None:
    all_prices = stripe_data.get("all_prices") or {}
    products = stripe_data.get("products") or {}

    zero_prices = [p for p in all_prices.values() if (p.get("unit_amount") or 0) == 0]
    inactive = [p for p in stripe_data.get("inactive_prices", {}).values()]
    non_recurring = [
        p for p in stripe_data.get("active_prices", {}).values()
        if p.get("type") != "recurring"
    ]

    print(f"\n{'='*60}")
    print("PROBLEMAS DETECTADOS NO STRIPE")
    print(f"{'='*60}")
    print(f"  Products: {len(products)}")
    print(f"  Prices ativos recorrentes: {len([p for p in stripe_data.get('active_prices', {}).values() if p.get('type')=='recurring'])}")
    print(f"  Prices com valor ZERO: {len(zero_prices)}")
    print(f"  Prices inativos recorrentes: {len(inactive)}")
    print(f"  Prices ativos NÃO recorrentes: {len(non_recurring)}")

    if zero_prices:
        print("\n  Prices ZERO:")
        for p in zero_prices:
            print(f"    {p['id']} | product={p.get('product')} | active={p.get('active')}")

    if inactive:
        print(f"\n  Prices INATIVOS (total: {len(inactive)}) [primeiros 10]:")
        for p in inactive[:10]:
            prod = products.get(p.get("product", ""), {})
            print(f"    {p['id']} | {prod.get('name','?')} | {p.get('currency','?')} "
                  f"{(p.get('unit_amount') or 0)/100:.2f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Audita Stripe × Frappe para a Vedium")
    parser.add_argument("--frappe-json", required=True, help="JSON gerado pelo get_stripe_config.py")
    parser.add_argument("--output", default="stripe_audit_result.json")
    args = parser.parse_args()

    api_key = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
    if not api_key.startswith("sk_"):
        sys.exit("❌ STRIPE_SECRET_KEY ausente ou inválida.")
    if "test" in api_key:
        print("⚠️  Chave de TESTE detectada.")
    else:
        print("🔑 Chave LIVE detectada.")

    stripe = _stripe()
    stripe.api_key = api_key
    stripe.api_version = "2024-06-20"

    with open(args.frappe_json, encoding="utf-8") as f:
        frappe_data = json.load(f)

    print(f"\n  Cursos Frappe carregados: {len(frappe_data.get('courses', []))}")
    print(f"  Subscription Plans carregados: {len(frappe_data.get('plans', {}))}")

    print("\nBuscando dados do Stripe...")
    stripe_data = fetch_stripe_data(stripe)

    print("\nGerando matriz...")
    matrix = build_matrix(frappe_data, stripe_data)
    print_matrix(matrix)
    print_stripe_issues(stripe_data)

    # Salvar resultado
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "live" if "live" in api_key else "test",
        "frappe_courses": len(frappe_data.get("courses", [])),
        "stripe_products": len(stripe_data.get("products", {})),
        "stripe_active_prices": len(stripe_data.get("active_prices", {})),
        "matrix": matrix,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n  Matriz completa salva em: {args.output}")
    print("  ⚠️  Não versione — pode conter Price IDs e metadados de produção.")

    # Resumo de ações necessárias
    pending = [r for r in matrix if r.get("status") not in (APPROVED, NOT_COMMERCIAL)]
    approved = [r for r in matrix if r.get("status") == APPROVED]
    print(f"\n  APROVADOS: {len(approved)} / {len(matrix)}")
    print(f"  PENDENTES: {len(pending)}")
    if pending:
        print("\n  Cursos que precisam de ação:")
        seen = set()
        for r in pending:
            key = r["course_id"]
            if key not in seen:
                seen.add(key)
                print(f"    • {r['course_title']} [{r['status']}]")


if __name__ == "__main__":
    main()
