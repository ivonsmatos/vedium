"""
Wrapper para executar a auditoria Stripe dentro do container Frappe.

Roda via:
  docker exec vedium-frappe python3 /tmp/run_audit_inside.py

A chave e lida do frappe.conf (site_config.json) — nunca sai do container.
O resultado e gravado em /tmp/stripe_audit_result.json sem a chave.
"""
import os
import sys
import json
import subprocess

# Inicializar Frappe
BENCH = "/home/frappe/frappe-bench"
SITE = "app.vediums.com"
sys.path.insert(0, f"{BENCH}/apps/frappe")

import frappe
frappe.init(site=SITE, sites_path=f"{BENCH}/sites")
frappe.connect()

# Ler chave do site_config
key = frappe.conf.get("STRIPE_SECRET_KEY") or ""
if not key:
    print("ERRO: STRIPE_SECRET_KEY nao encontrada no site_config", file=sys.stderr)
    sys.exit(1)

mode = "live" if key.startswith("sk_live") else "test"
print(f"Stripe key: presente ({mode})")

# Verificar que o audit script esta disponivel
AUDIT_SCRIPT = "/opt/vedium/scripts/vedium_stripe_audit.py"
if not os.path.exists(AUDIT_SCRIPT):
    print(f"ERRO: {AUDIT_SCRIPT} nao encontrado", file=sys.stderr)
    sys.exit(1)

FRAPPE_JSON = "/tmp/frappe_stripe_config.json"
OUTPUT = "/tmp/stripe_audit_result.json"

# Rodar o audit como subprocesso (para isolar o ambiente)
result = subprocess.run(
    [sys.executable, AUDIT_SCRIPT, "--frappe-json", FRAPPE_JSON, "--output", OUTPUT],
    env={**os.environ, "STRIPE_SECRET_KEY": key},
    capture_output=False,  # deixar stdout/stderr passar para o terminal
    timeout=300,
)
sys.exit(result.returncode)
