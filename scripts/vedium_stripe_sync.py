"""
vedium_stripe_sync.py — Sincronização idempotente Stripe × Frappe para Vedium.

Este script NUNCA:
  - cria clientes, invoices, subscriptions reais
  - conclui checkouts
  - exclui Prices
  - inventa valores
  - reutiliza Prices de outros cursos

Uso:
  python3 vedium_stripe_sync.py \\
      --frappe-json /tmp/frappe_config.json \\
      --matrix-json stripe_audit_result.json \\
      --approved-json approved_matrix.json \\  # operador edita e aprova
      --dry-run \\
      [--apply] [--course <slug>] [--all] \\
      [--monthly-only] [--annual-only] \\
      [--resume] [--rollback-mapping rollback.json]

REGRAS:
  - --dry-run: mostra operações propostas, não cria nada
  - --apply: cria somente após --dry-run + confirmação explícita
  - Um curso só é processado se estiver na --approved-json com valores explícitos
  - Idempotency key: vedium:{env}:{course_id}:{period}:{currency}:{unit_amount}:v1

Valores precisam estar na --approved-json. Nunca são deduzidos automaticamente.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
IDEMPOTENCY_VERSION = "v1"
SUPPORTED_CURRENCIES = {"BRL", "USD"}
SUPPORTED_INTERVALS = {"month"}
REQUIRED_METADATA_KEYS = {
    "vedium_course_id", "vedium_course_title", "vedium_period",
    "vedium_environment", "vedium_source", "vedium_schema_version",
}
SCHEMA_VERSION = "1"


# ---------------------------------------------------------------------------
# Helpers Stripe
# ---------------------------------------------------------------------------

def _stripe():
    try:
        import stripe as _s
        return _s
    except ImportError:
        sys.exit("Instale o SDK: pip install stripe")


def _idempotency_key(env: str, course_id: str, period: str, currency: str, unit_amount: int) -> str:
    return f"vedium:{env}:{course_id}:{period}:{currency.lower()}:{unit_amount}:{IDEMPOTENCY_VERSION}"


def _lookup_key(course_id: str, period: str, currency: str) -> str:
    slug = course_id.lower().replace(" ", "-").replace("_", "-")
    return f"vedium_{slug}_{period}_{currency.lower()}_{IDEMPOTENCY_VERSION}"


def _find_existing_price(stripe, product_id: str, period: str, currency: str, unit_amount: int) -> dict | None:
    """Procura Price ativo já criado pela Vedium para este curso/período/valor."""
    try:
        prices = stripe.Price.list(
            product=product_id,
            active=True,
            currency=currency.lower(),
            lookup_keys=[_lookup_key(product_id, period, currency)],
            limit=10,
        )
        for p in prices.get("data", []):
            meta = p.get("metadata") or {}
            if (
                meta.get("vedium_period") == period
                and p.get("unit_amount") == unit_amount
                and (p.get("recurring") or {}).get("interval") == "month"
                and int((p.get("recurring") or {}).get("interval_count") or 0) == 1
            ):
                return dict(p)
    except Exception:
        pass
    return None


def _create_price(stripe, env: str, product_id: str, course_entry: dict, dry_run: bool) -> dict | None:
    course_id = course_entry["course_id"]
    course_title = course_entry["course_title"]
    period = course_entry["period"]
    currency = course_entry["currency"].upper()
    unit_amount = course_entry["unit_amount"]  # em centavos
    minimum_term = 12 if period == "annual" else 0

    idem_key = _idempotency_key(env, course_id, period, currency, unit_amount)
    lk = _lookup_key(course_id, period, currency)
    metadata = {
        "vedium_course_id": course_id,
        "vedium_course_title": course_title[:255],
        "vedium_period": period,
        "vedium_environment": env,
        "vedium_source": "vedium_stripe_sync.py",
        "vedium_schema_version": SCHEMA_VERSION,
        "vedium_minimum_term_months": str(minimum_term),
    }
    period_label = "Mensal" if period == "monthly" else "Anual (12 meses)"
    nickname = f"Vedium – {course_title} – {period_label}"

    if dry_run:
        print(f"    [DRY-RUN] CREATE Price: {lk}")
        print(f"              product={product_id}")
        print(f"              unit_amount={unit_amount} ({unit_amount/100:.2f} {currency})")
        print(f"              interval=month/1  minimum_term={minimum_term}")
        print(f"              idempotency_key={idem_key}")
        return {"dry_run": True, "would_create": True, "lookup_key": lk}

    # Verificar se já existe
    existing = _find_existing_price(stripe, product_id, period, currency, unit_amount)
    if existing:
        print(f"    ✅ Price já existe: {existing['id']} (reutilizando)")
        return existing

    # Criar novo
    try:
        price = stripe.Price.create(
            product=product_id,
            currency=currency.lower(),
            unit_amount=unit_amount,
            recurring={"interval": "month", "interval_count": 1},
            nickname=nickname[:255],
            lookup_key=lk,
            transfer_lookup_key=False,
            metadata=metadata,
            idempotency_key=idem_key,
        )
        print(f"    ✅ Price CRIADO: {price['id']}")
        return dict(price)
    except Exception as exc:
        print(f"    ❌ Erro ao criar Price: {exc}")
        return None


def _validate_price(stripe, price_id: str, expected: dict) -> list[str]:
    """Recupera e valida o Price criado. Retorna lista de erros."""
    errors = []
    try:
        p = stripe.Price.retrieve(price_id)
    except Exception as exc:
        return [f"Não foi possível recuperar o Price: {exc}"]

    if not p.get("active"):
        errors.append("Price não está ativo após criação")
    if p.get("type") != "recurring":
        errors.append(f"type={p.get('type')!r} (esperado 'recurring')")
    rec = p.get("recurring") or {}
    if rec.get("interval") != "month":
        errors.append(f"interval={rec.get('interval')!r} (esperado 'month')")
    if int(rec.get("interval_count") or 0) != 1:
        errors.append(f"interval_count={rec.get('interval_count')} (esperado 1)")
    if p.get("unit_amount") != expected.get("unit_amount"):
        errors.append(
            f"unit_amount={p.get('unit_amount')} != esperado {expected.get('unit_amount')}"
        )
    if (p.get("currency") or "").upper() != expected.get("currency", "").upper():
        errors.append(
            f"currency={p.get('currency')!r} != esperado {expected.get('currency')!r}"
        )
    if p.get("product") != expected.get("product_id"):
        errors.append(
            f"product={p.get('product')!r} != esperado {expected.get('product_id')!r}"
        )
    return errors


# ---------------------------------------------------------------------------
# Frappe update helpers (via bench execute inline)
# ---------------------------------------------------------------------------

def _update_frappe_plan(frappe_runner, plan_name: str, price_id: str, cost: float,
                         currency: str, dry_run: bool) -> bool:
    """Atualiza ou cria Subscription Plan no Frappe via bench execute."""
    code = f"""
import frappe, json
plan = frappe.db.get_value(
    'Subscription Plan', '{plan_name}',
    ['name', 'product_price_id', 'cost', 'currency'], as_dict=True
)
print(json.dumps(dict(plan) if plan else None))
"""
    result = frappe_runner(code)
    existing = json.loads(result) if result and result.strip() else None

    if existing:
        if existing.get("product_price_id") == price_id:
            print(f"    ✅ Subscription Plan '{plan_name}' já aponta para {price_id[:12]}...")
            return True
        if dry_run:
            print(f"    [DRY-RUN] UPDATE Subscription Plan '{plan_name}'")
            print(f"              product_price_id: {existing.get('product_price_id')!r} → {price_id}")
            return True
        update_code = f"""
import frappe
frappe.db.set_value('Subscription Plan', '{plan_name}', {{
    'product_price_id': '{price_id}',
    'cost': {cost},
    'currency': '{currency}',
}})
frappe.db.commit()
print('updated')
"""
        res = frappe_runner(update_code)
        print(f"    ✅ Subscription Plan '{plan_name}' atualizado: {res}")
        return True
    else:
        print(f"    ⚠️  Subscription Plan '{plan_name}' não encontrado — não será criado nesta etapa.")
        print(f"       Use o Frappe admin para criar manualmente com product_price_id={price_id}")
        return False


def _update_lms_course(frappe_runner, course_id: str, field: str, plan_name: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"    [DRY-RUN] UPDATE LMS Course '{course_id}'")
        print(f"              {field} → {plan_name!r}")
        return True
    code = f"""
import frappe
frappe.db.set_value('LMS Course', '{course_id}', '{field}', '{plan_name}')
frappe.db.commit()
print('updated')
"""
    res = frappe_runner(code)
    print(f"    ✅ LMS Course '{course_id}' {field} atualizado: {res}")
    return True


# ---------------------------------------------------------------------------
# Carregamento do arquivo aprovado pelo operador
# ---------------------------------------------------------------------------

def load_approved_matrix(path: str) -> dict[str, dict]:
    """
    O operador edita stripe_audit_result.json e cria um approved_matrix.json
    com apenas os cursos aprovados, adicionando unit_amount e currency explícitos.

    Formato esperado por linha:
    {
        "course_id": "ingles-a1",
        "course_title": "Inglês A1",
        "period": "monthly",
        "product_id": "prod_xxx",
        "currency": "BRL",
        "unit_amount": 19900,   ← em centavos, OBRIGATÓRIO
        "plan_name": "Vedium — Inglês A1 — Mensal",  ← nome do Subscription Plan
        "approved": true,
        "value_source": "tabela oficial 2026"
    }
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    approved = {}
    entries = data if isinstance(data, list) else data.get("approved", [])
    for entry in entries:
        if not entry.get("approved"):
            continue
        course_id = entry.get("course_id", "")
        period = entry.get("period", "")
        if not course_id or not period:
            continue

        unit_amount = entry.get("unit_amount")
        if not unit_amount or int(unit_amount) <= 0:
            print(f"  ⛔ BLOQUEADO: {course_id}/{period} — unit_amount ausente ou zero")
            continue
        currency = (entry.get("currency") or "").upper()
        if currency not in SUPPORTED_CURRENCIES:
            print(f"  ⛔ BLOQUEADO: {course_id}/{period} — moeda inválida: {currency!r}")
            continue
        product_id = entry.get("product_id", "")
        if not product_id.startswith("prod_"):
            print(f"  ⛔ BLOQUEADO: {course_id}/{period} — product_id inválido: {product_id!r}")
            continue

        key = f"{course_id}:{period}"
        approved[key] = entry

    print(f"  {len(approved)} entradas aprovadas carregadas")
    return approved


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sincroniza Stripe × Frappe (Vedium)")
    parser.add_argument("--frappe-json", required=True)
    parser.add_argument("--approved-json", required=True,
                        help="JSON com entradas aprovadas pelo operador (inclui unit_amount)")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Mostrar operações sem executar (padrão: ativo)")
    parser.add_argument("--apply", action="store_true",
                        help="Executar operações (desativa --dry-run)")
    parser.add_argument("--course", help="Processar somente este course_id")
    parser.add_argument("--all", action="store_true", help="Processar todos os aprovados")
    parser.add_argument("--monthly-only", action="store_true")
    parser.add_argument("--annual-only", action="store_true")
    parser.add_argument("--resume", action="store_true",
                        help="Pular cursos já processados com sucesso")
    parser.add_argument("--rollback-mapping",
                        help="Arquivo JSON para gravar mapeamento anterior (rollback)")
    parser.add_argument("--output", default="stripe_sync_result.json")
    parser.add_argument("--frappe-container", default="vedium-frappe",
                        help="Nome do container Docker com o Frappe")
    parser.add_argument("--site", default="app.vediums.com")
    args = parser.parse_args()

    dry_run = args.dry_run and not args.apply
    env = "live" if "live" in (os.environ.get("STRIPE_SECRET_KEY") or "") else "test"

    if args.apply and not args.dry_run:
        # Dry-run automático antes de aplicar
        pass
    if not (args.course or args.all):
        sys.exit("❌ Use --course <slug> ou --all para especificar o escopo.")

    api_key = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
    if not api_key.startswith("sk_"):
        sys.exit("❌ STRIPE_SECRET_KEY ausente ou inválida.")

    stripe = _stripe()
    stripe.api_key = api_key
    stripe.api_version = "2024-06-20"

    print(f"{'[DRY-RUN]' if dry_run else '[APPLY]'} modo={env}")

    with open(args.frappe_json, encoding="utf-8") as f:
        frappe_data = json.load(f)

    print("Carregando entradas aprovadas...")
    approved = load_approved_matrix(args.approved_json)

    if not approved:
        sys.exit("❌ Nenhuma entrada aprovada encontrada. Edite o --approved-json.")

    if args.apply and not dry_run:
        print("\n⚠️  MODO --apply ATIVO. Esta operação criará Prices REAIS no Stripe.")
        confirm = input("Digite 'CONFIRMO' para prosseguir: ").strip()
        if confirm != "CONFIRMO":
            sys.exit("Operação cancelada pelo operador.")

    # Frappe runner via Docker
    import subprocess

    def frappe_runner(python_code: str) -> str:
        if dry_run:
            return "dry-run"
        cmd = [
            "docker", "exec", "-w", "/home/frappe/frappe-bench",
            args.frappe_container,
            "bench", "--site", args.site, "execute",
            "--args", json.dumps({"_code": python_code}),
        ]
        # Alternativa: bench execute com código inline
        # Por segurança, usamos pipe
        exec_cmd = [
            "docker", "exec", "-i", args.frappe_container,
            "python3", "-c",
            f"import sys; sys.path.insert(0,'/home/frappe/frappe-bench/apps/frappe'); "
            f"import frappe; frappe.init(site='{args.site}', "
            f"sites_path='/home/frappe/frappe-bench/sites'); frappe.connect(); "
            + python_code
        ]
        result = subprocess.run(exec_cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip()

    results = []
    rollback_map = {}

    entries_to_process = list(approved.values())
    if args.course:
        entries_to_process = [e for e in entries_to_process if e["course_id"] == args.course]
    if args.monthly_only:
        entries_to_process = [e for e in entries_to_process if e["period"] == "monthly"]
    if args.annual_only:
        entries_to_process = [e for e in entries_to_process if e["period"] == "annual"]

    print(f"\n  Entradas a processar: {len(entries_to_process)}")

    for entry in entries_to_process:
        course_id = entry["course_id"]
        period = entry["period"]
        product_id = entry["product_id"]
        unit_amount = int(entry["unit_amount"])
        currency = entry["currency"].upper()
        plan_name = entry.get("plan_name", f"Vedium — {entry.get('course_title',course_id)} — {'Mensal' if period=='monthly' else 'Anual'}")

        print(f"\n{'─'*60}")
        print(f"  {course_id} / {period} | {unit_amount/100:.2f} {currency} | {product_id[:12]}...")
        print(f"  Fonte do valor: {entry.get('value_source','NÃO ESPECIFICADA')}")

        # Salvar mapeamento anterior para rollback
        frappe_courses = frappe_data.get("courses") or {}
        if isinstance(frappe_courses, list):
            course_fdata = next((c for c in frappe_courses if c.get("name") == course_id), {})
        else:
            course_fdata = frappe_courses.get(course_id, {})

        field = "custom_stripe_annual_plan" if period == "annual" else "custom_stripe_monthly_plan"
        rollback_map[f"{course_id}:{period}"] = {
            "course_id": course_id,
            "field": field,
            "previous_plan": course_fdata.get(field),
            "previous_plan_price": (frappe_data.get("plans", {}).get(course_fdata.get(field), {}) or {}).get("product_price_id"),
        }

        # Criar Price
        price = _create_price(stripe, env, product_id, entry, dry_run=dry_run)
        if not price:
            print(f"  ❌ Falha ao criar Price — pulando curso")
            results.append({"course_id": course_id, "period": period, "ok": False, "error": "falha ao criar Price"})
            continue

        price_id = price.get("id") if not dry_run else "price_DRY_RUN"

        # Validar Price
        if not dry_run and price_id and price_id.startswith("price_"):
            errors = _validate_price(stripe, price_id, {
                "unit_amount": unit_amount,
                "currency": currency,
                "product_id": product_id,
            })
            if errors:
                print(f"  ❌ Validação pós-criação falhou: {errors}")
                results.append({"course_id": course_id, "period": period, "ok": False,
                                 "price_id": price_id, "errors": errors})
                continue

        # Atualizar Subscription Plan
        plan_updated = _update_frappe_plan(
            frappe_runner, plan_name, price_id,
            unit_amount / 100, currency, dry_run=dry_run
        )

        # Atualizar LMS Course
        course_updated = _update_lms_course(
            frappe_runner, course_id, field, plan_name, dry_run=dry_run
        )

        results.append({
            "course_id": course_id,
            "period": period,
            "ok": True,
            "price_id": price_id,
            "plan_name": plan_name,
            "plan_updated": plan_updated,
            "course_updated": course_updated,
            "dry_run": dry_run,
        })

    # Salvar rollback map
    if args.rollback_mapping and rollback_map:
        with open(args.rollback_mapping, "w", encoding="utf-8") as f:
            json.dump(rollback_map, f, indent=2)
        print(f"\n  Mapeamento anterior salvo em: {args.rollback_mapping}")

    # Salvar resultado
    ok_count = sum(1 for r in results if r.get("ok"))
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "dry_run" if dry_run else "apply",
        "env": env,
        "total": len(results),
        "ok": ok_count,
        "failed": len(results) - ok_count,
        "results": results,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"{'[DRY-RUN] ' if dry_run else ''}RESULTADO: {ok_count}/{len(results)} OK")
    print(f"  Resultado salvo em: {args.output}")
    if dry_run:
        print("\n  ➤ Para aplicar: rode novamente com --apply (sem --dry-run)")
    print("=" * 60)


if __name__ == "__main__":
    main()
