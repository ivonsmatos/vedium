"""
Vedium – Script de operações Stripe em produção
Uso: python scripts/stripe_ops.py

Operações:
  1. Expirar 6 Checkout Sessions inválidas listadas explicitamente
  2. Listar todas as sessões open e validar que nenhuma usa price inválido
  3. Corrigir configuração do Customer Portal
  4. Gerar test-checkouts para todos os cursos (mensal + anual) sem pagamento

AVISO DE SEGURANÇA:
  - A chave Stripe é lida de forma silenciosa (getpass).
  - Nunca a cole em texto aberto, chat ou arquivo versionado.
  - Revogue imediatamente se suspeitar de exposição.
"""
from __future__ import annotations

import getpass
import json
import sys
from datetime import datetime
from typing import Any


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def _require_stripe():
    try:
        import stripe as _stripe
        return _stripe
    except ImportError:
        sys.exit("Instale o SDK: pip install stripe")


def _get_key() -> str:
    key = getpass.getpass("\nCole a Stripe SECRET Key (sk_live_...): ").strip()
    if not key.startswith("sk_"):
        sys.exit("❌ A chave deve começar com 'sk_'. Abortando.")
    if "live" not in key:
        print("⚠️  ATENÇÃO: Esta não parece ser uma chave de PRODUÇÃO (sk_live_).")
        if input("   Continuar mesmo assim? (s/N): ").strip().lower() != "s":
            sys.exit("Abortado pelo operador.")
    return key


# ---------------------------------------------------------------------------
# Etapa 1 – Expirar sessões inválidas
# ---------------------------------------------------------------------------

SESSIONS_TO_EXPIRE = [
    "cs_live_a1D8QLhiILDXUvUg7Kywy1cS27fDP9LaZ6MmOsV799dQHP2pFO9QyUQVHH",
    "cs_live_a1rOHgmGxflJTpaJKWDvvgATCbJqLdATHKsW89sHxqVPELnZyImfZuZcSj",
    "cs_live_a1LuzLWb4bwIHhtIzfdNS1ebxsj9kAkWmhTe95rm08tShzEdlZjklN4wss",
    "cs_live_a1XK6ZFWwIZNfmdDdLxb24doXoO4F3KEv1Jk2hOhQDE6PJPYBkfWhMB7IL",
    "cs_live_a1KhOtoixSiqvBYim9zP9q9ZyO0zuA9eC6NI7gayutSHwgUMSCXj6MUy0c",
    "cs_live_a1e91OTHrDSoul6I2DD8xiuHyxrnlaOPVMDPyL4HNsMF7X42drNf43ilUT",
]


def expire_invalid_sessions(stripe) -> list[dict]:
    print("\n" + "=" * 60)
    print("ETAPA 1 – Expirar sessões inválidas")
    print("=" * 60)
    results = []
    for session_id in SESSIONS_TO_EXPIRE:
        try:
            sess = stripe.checkout.Session.retrieve(session_id)
            status = sess.get("status") or "unknown"
            if status == "open":
                stripe.checkout.Session.expire(session_id)
                print(f"  ✅ Expirada: {session_id[:30]}...  (era: {status})")
                results.append({"id": session_id, "action": "expired", "prev_status": status})
            else:
                print(f"  ℹ️  Já {status}: {session_id[:30]}...")
                results.append({"id": session_id, "action": "skipped", "status": status})
        except Exception as exc:
            print(f"  ❌ Erro em {session_id[:30]}...: {exc}")
            results.append({"id": session_id, "action": "error", "error": str(exc)})
    return results


# ---------------------------------------------------------------------------
# Etapa 2 – Auditar sessões open restantes
# ---------------------------------------------------------------------------

SUSPICIOUS_MULTIPLIERS = {6, 10, 12}


def _price_issues(stripe, price_id: str, session_amount: int | None) -> list[str]:
    issues = []
    try:
        price = stripe.Price.retrieve(price_id)
    except Exception as exc:
        return [f"Não foi possível recuperar o price: {exc}"]

    if not price.get("active"):
        issues.append("PRICE INATIVO")

    unit = price.get("unit_amount") or 0
    if unit == 0:
        issues.append("PRICE ZERADO")

    recurring = price.get("recurring") or {}
    interval = recurring.get("interval", "")
    interval_count = int(recurring.get("interval_count") or 1)
    if interval not in ("month",) or interval_count != 1:
        issues.append(f"RECORRÊNCIA INVÁLIDA: {interval}/{interval_count}")

    # Detectar multiplied values (sinal de plano semestral/anual embutido no price)
    if unit and session_amount:
        for mult in SUSPICIOUS_MULTIPLIERS:
            if session_amount == unit * mult:
                issues.append(f"VALOR MULTIPLICADO POR {mult} (possível plano semestral/anual embutido)")

    # Nome do price pode revelar "semestral"
    nickname = (price.get("nickname") or "").lower()
    if "semestral" in nickname or "semiannual" in nickname:
        issues.append(f"PRICE SEMESTRAL: nickname='{price.get('nickname')}'")

    return issues


def audit_open_sessions(stripe) -> list[dict]:
    print("\n" + "=" * 60)
    print("ETAPA 2 – Auditar todas as sessões open restantes")
    print("=" * 60)

    sessions = stripe.checkout.Session.list(status="open", limit=100)
    rows = []
    for sess in sessions.auto_paging_iter():
        sess_id = sess.get("id", "")
        amount_total = sess.get("amount_total")
        line_items = stripe.checkout.Session.list_line_items(sess_id, limit=5)
        price_ids = [li["price"]["id"] for li in line_items.get("data", []) if li.get("price")]
        issues: list[str] = []
        for pid in price_ids:
            issues.extend(_price_issues(stripe, pid, amount_total))
        metadata = sess.get("metadata") or {}
        bp = metadata.get("billing_period", "")
        if "semestral" in bp.lower():
            issues.append(f"METADATA billing_period=semestral")
        rows.append({
            "id": sess_id,
            "amount_total": amount_total,
            "currency": sess.get("currency", "").upper(),
            "price_ids": price_ids,
            "billing_period": bp,
            "issues": issues,
            "ok": len(issues) == 0,
        })

    ok = [r for r in rows if r["ok"]]
    bad = [r for r in rows if not r["ok"]]
    print(f"\n  Total open: {len(rows)} | OK: {len(ok)} | Com problemas: {len(bad)}")
    if bad:
        print("\n  ⚠️  Sessões com problemas:")
        for r in bad:
            print(f"    {r['id'][:40]}... issues: {r['issues']}")
    else:
        print("  ✅ Nenhuma sessão com problemas.")
    return rows


# ---------------------------------------------------------------------------
# Etapa 3 – Corrigir Customer Portal
# ---------------------------------------------------------------------------

PORTAL_CONFIG = {
    "business_profile": {
        "privacy_policy_url": "https://vediums.com/privacidade",
        "terms_of_service_url": "https://vediums.com/termos",
    },
    "default_return_url": "https://vediums.com",
    "features": {
        "customer_update": {
            "enabled": True,
            "allowed_updates": ["email", "address", "phone", "name"],
        },
        "invoice_history": {"enabled": True},
        "payment_method_update": {"enabled": True},
        # O cancelamento é gerenciado pelo Frappe (verifica plano mensal vs.
        # compromisso anual). O Portal não pode cancelar diretamente.
        "subscription_cancel": {"enabled": False},
        "subscription_update": {"enabled": False},
    },
}


def fix_customer_portal(stripe) -> dict:
    print("\n" + "=" * 60)
    print("ETAPA 3 – Corrigir Customer Portal")
    print("=" * 60)

    configs = stripe.billing_portal.Configuration.list(limit=10)
    active_configs = [c for c in configs.get("data", []) if c.get("active")]

    if active_configs:
        config = active_configs[0]
        config_id = config["id"]
        print(f"  Atualizando configuração existente: {config_id}")
        updated = stripe.billing_portal.Configuration.modify(config_id, **PORTAL_CONFIG)
    else:
        print("  Criando nova configuração de portal...")
        updated = stripe.billing_portal.Configuration.create(**PORTAL_CONFIG)
        config_id = updated["id"]

    bp = updated.get("business_profile") or {}
    feats = updated.get("features") or {}
    sub_cancel = (feats.get("subscription_cancel") or {}).get("enabled", "?")
    print(f"  ✅ Portal {config_id}")
    print(f"     privacy_policy_url : {bp.get('privacy_policy_url')}")
    print(f"     terms_of_service_url: {bp.get('terms_of_service_url')}")
    print(f"     default_return_url : {updated.get('default_return_url')}")
    print(f"     subscription_cancel.enabled: {sub_cancel}")
    return {"config_id": config_id, "subscription_cancel_enabled": sub_cancel}


# ---------------------------------------------------------------------------
# Etapa 4 – Test-checkouts para todos os cursos
# ---------------------------------------------------------------------------

TEST_EMAIL = "operador+checkout-test@vediums.com"
BASE_URL = "https://app.vediums.com"

# Períodos para teste
PERIODS = [
    ("monthly", "Mensal", 0),
    ("annual", "Anual", 12),
]


def _get_all_active_prices(stripe) -> dict[str, dict]:
    """Retorna {price_id: price_object} para todos os prices recorrentes ativos."""
    prices: dict[str, dict] = {}
    for p in stripe.Price.list(active=True, type="recurring", limit=100).auto_paging_iter():
        prices[p["id"]] = p
    return prices


def _get_all_products(stripe) -> dict[str, dict]:
    """Retorna {product_id: product_object}."""
    products: dict[str, dict] = {}
    for prod in stripe.Product.list(active=True, limit=100).auto_paging_iter():
        products[prod["id"]] = prod
    return products


def _detect_plan_type(price: dict) -> str:
    """Inferir se o price é mensal ou anual com base nos metadados ou nickname."""
    recurring = price.get("recurring") or {}
    interval = recurring.get("interval", "")
    interval_count = int(recurring.get("interval_count") or 1)
    nickname = (price.get("nickname") or "").lower()
    metadata_period = (price.get("metadata") or {}).get("billing_period", "").lower()

    if "annual" in metadata_period or "anual" in metadata_period:
        return "annual"
    if "monthly" in metadata_period or "mensal" in metadata_period:
        return "monthly"
    if "anual" in nickname or "annual" in nickname or "yearly" in nickname:
        return "annual"
    if "mensal" in nickname or "monthly" in nickname:
        return "monthly"
    # Fallback: interval mensal = mensal
    if interval == "month" and interval_count == 1:
        return "monthly"
    return "unknown"


def run_test_checkouts(stripe) -> list[dict]:
    print("\n" + "=" * 60)
    print("ETAPA 4 – Test-checkouts (sem pagamento)")
    print("=" * 60)

    prices = _get_all_active_prices(stripe)
    products = _get_all_products(stripe)

    print(f"  Prices ativos recorrentes encontrados: {len(prices)}")
    print(f"  Produtos ativos encontrados: {len(products)}")

    # Agrupar prices por produto
    by_product: dict[str, list[dict]] = {}
    for pid, p in prices.items():
        prod_id = p.get("product", "")
        by_product.setdefault(prod_id, []).append(p)

    rows = []
    session_count = 0

    for prod_id, prod_prices in sorted(by_product.items()):
        prod = products.get(prod_id) or {}
        prod_name = prod.get("name") or prod_id

        monthly_prices = [p for p in prod_prices if _detect_plan_type(p) == "monthly"]
        annual_prices = [p for p in prod_prices if _detect_plan_type(p) == "annual"]

        for plan_label, plan_prices, min_term in [
            ("Mensal", monthly_prices, 0),
            ("Anual", annual_prices, 12),
        ]:
            if not plan_prices:
                rows.append({
                    "produto": prod_name,
                    "product_id": prod_id,
                    "plano": plan_label,
                    "price_id": "—",
                    "valor": "—",
                    "moeda": "—",
                    "interval": "—",
                    "interval_count": "—",
                    "billing_period_metadata": "—",
                    "minimum_term_months": "—",
                    "url": "—",
                    "status": "SEM PRICE",
                    "ok": False,
                })
                continue

            price = plan_prices[0]  # tomar o primeiro (pode haver múltiplos)
            price_id = price["id"]
            recurring = price.get("recurring") or {}
            unit_amount = price.get("unit_amount") or 0
            currency = (price.get("currency") or "").upper()
            interval = recurring.get("interval", "")
            interval_count = int(recurring.get("interval_count") or 1)

            metadata = {
                "course_name": prod_name,
                "user": TEST_EMAIL,
                "site": "app.vediums.com",
                "coupon_code": "",
                "billing_period": "annual" if min_term == 12 else "monthly",
                "minimum_term_months": str(min_term),
                "price_id": price_id,
            }
            params = {
                "mode": "subscription",
                "line_items": [{"price": price_id, "quantity": 1}],
                "customer_email": TEST_EMAIL,
                "client_reference_id": f"{prod_name}|{TEST_EMAIL}",
                "success_url": f"{BASE_URL}/lms/courses/{prod_id}?payment=success&session_id={{CHECKOUT_SESSION_ID}}",
                "cancel_url": f"{BASE_URL}/lms/courses/{prod_id}?payment=cancelled",
                "metadata": metadata,
                "subscription_data": {"metadata": metadata},
            }

            try:
                session = stripe.checkout.Session.create(**params)
                session_count += 1
                url = session.get("url") or "—"
                status = session.get("status") or "created"
                ok = True
            except Exception as exc:
                url = "—"
                status = f"ERRO: {exc}"
                ok = False

            rows.append({
                "produto": prod_name,
                "product_id": prod_id,
                "plano": plan_label,
                "price_id": price_id,
                "valor": f"{unit_amount / 100:.2f}" if unit_amount else "0",
                "moeda": currency,
                "interval": interval,
                "interval_count": interval_count,
                "billing_period_metadata": metadata["billing_period"],
                "minimum_term_months": min_term,
                "url": url[:80] + "..." if len(url) > 80 else url,
                "status": status,
                "ok": ok,
            })

    print(f"\n  Sessões criadas com sucesso: {session_count}")
    return rows


# ---------------------------------------------------------------------------
# Relatório final
# ---------------------------------------------------------------------------

def _print_table(rows: list[dict]) -> None:
    if not rows:
        print("  (nenhum resultado)")
        return
    cols = list(rows[0].keys())
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    widths = {c: min(w, 50) for c, w in widths.items()}  # truncar colunas largas
    header = " | ".join(c.ljust(widths[c]) for c in cols)
    sep = "-+-".join("-" * widths[c] for c in cols)
    print(f"\n  {header}")
    print(f"  {sep}")
    for r in rows:
        row_str = " | ".join(str(r.get(c, "")).ljust(widths[c])[:widths[c]] for c in cols)
        prefix = "  ✅" if r.get("ok") else "  ❌"
        print(f"{prefix} {row_str}")


def main():
    stripe = _require_stripe()
    api_key = _get_key()
    stripe.api_key = api_key
    stripe.api_version = "2024-06-20"  # versão estável

    print("\n🔑 Chave configurada. Iniciando operações...\n")

    # 1. Expirar sessões inválidas
    expire_results = expire_invalid_sessions(stripe)

    # 2. Auditar sessões open
    open_sessions = audit_open_sessions(stripe)

    # 3. Corrigir Customer Portal
    portal_result = fix_customer_portal(stripe)

    # 4. Test-checkouts
    checkout_rows = run_test_checkouts(stripe)

    # Sumário
    print("\n" + "=" * 60)
    print("SUMÁRIO DOS TEST-CHECKOUTS")
    print("=" * 60)
    display_cols = [
        "produto", "plano", "price_id", "valor", "moeda",
        "interval", "interval_count", "billing_period_metadata",
        "minimum_term_months", "status",
    ]
    display_rows = [{k: r[k] for k in display_cols if k in r} for r in checkout_rows]
    _print_table(display_rows)

    total = len(checkout_rows)
    ok_count = sum(1 for r in checkout_rows if r.get("ok"))
    bad_count = total - ok_count

    print(f"\n  Total de testes: {total}")
    print(f"  ✅ OK: {ok_count}")
    print(f"  ❌ Com problema: {bad_count}")

    # Sessões open com problema
    bad_open = [r for r in open_sessions if not r.get("ok")]
    print(f"\n  Sessões open com price inválido após expiração: {len(bad_open)}")

    print("\n" + "=" * 60)
    if bad_count == 0 and len(bad_open) == 0:
        print("✅ READY FOR CONTROLLED PAYMENT TEST")
    else:
        print("❌ NO-GO — inconsistências encontradas:")
        for r in checkout_rows:
            if not r.get("ok"):
                print(f"   • {r['produto']} [{r['plano']}]: {r['status']}")
        for r in bad_open:
            print(f"   • Sessão open inválida: {r['id'][:40]}... → {r['issues']}")
    print("=" * 60)

    # Salvar resultado em JSON (sem a chave)
    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "expired_sessions": expire_results,
        "open_sessions_audited": len(open_sessions),
        "open_sessions_with_issues": len(bad_open),
        "portal": portal_result,
        "checkout_tests": checkout_rows,
        "verdict": "READY" if (bad_count == 0 and len(bad_open) == 0) else "NO-GO",
    }
    out_path = "scripts/stripe_ops_result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Resultado completo salvo em: {out_path}")
    print("  ⚠️  Não versione este arquivo — pode conter URLs de checkout.")


if __name__ == "__main__":
    main()
