"""
Versão do stripe_ops.py para execução no servidor via variável de ambiente.
A chave é lida de STRIPE_SECRET_KEY (já presente no /opt/vedium/deploy/.env).

Nunca execute este script com a chave exposta em logs ou terminal.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Reusar toda a lógica do stripe_ops.py
# ---------------------------------------------------------------------------
_HERE = __file__
sys.path.insert(0, os.path.dirname(_HERE))

# Importar as funções do stripe_ops
from stripe_ops import (  # noqa: E402
    expire_invalid_sessions,
    audit_open_sessions,
    fix_customer_portal,
    run_test_checkouts,
    _print_table,
    _require_stripe,
)


def main():
    stripe = _require_stripe()

    api_key = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
    if not api_key.startswith("sk_"):
        sys.exit("❌ STRIPE_SECRET_KEY ausente ou inválida. Abortando.")
    if "live" not in api_key:
        print("⚠️  AVISO: Chave não parece ser de produção (sk_live_).")

    stripe.api_key = api_key
    stripe.api_version = "2024-06-20"

    print("🔑 Chave configurada via variável de ambiente. Iniciando operações...\n")

    expire_results = expire_invalid_sessions(stripe)
    open_sessions = audit_open_sessions(stripe)
    portal_result = fix_customer_portal(stripe)
    checkout_rows = run_test_checkouts(stripe)

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
    bad_open = [r for r in open_sessions if not r.get("ok")]

    print(f"\n  Total testes: {total} | OK: {ok_count} | NO-GO: {bad_count}")
    print(f"  Sessões open com problema após expiração: {len(bad_open)}")

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

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "expired_sessions": expire_results,
        "open_sessions_audited": len(open_sessions),
        "open_sessions_with_issues": len(bad_open),
        "portal": portal_result,
        "checkout_tests": checkout_rows,
        "verdict": "READY" if (bad_count == 0 and len(bad_open) == 0) else "NO-GO",
    }
    out_path = os.path.join(os.path.dirname(_HERE), "stripe_ops_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  Resultado completo salvo em: {out_path}")


if __name__ == "__main__":
    main()
