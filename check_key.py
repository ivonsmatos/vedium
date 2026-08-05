import json
from pathlib import Path

path = Path("/home/frappe/frappe-bench/sites/app.vediums.com/site_config.json")
try:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    key = config.get("STRIPE_SECRET_KEY") or ""
    print(f"Key present: {bool(key)}")
    if key.startswith("sk_live_"):
        print("Ambiente Stripe: live")
except Exception as e:
    print(f"Error: {e}")
