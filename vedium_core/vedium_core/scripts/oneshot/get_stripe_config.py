"""Exporta dados de LMS Courses e Subscription Plans para JSON.

Uso via bench execute:
  bench --site app.vediums.com execute \
      vedium_core.scripts.oneshot.get_stripe_config.run \
      > /tmp/frappe_stripe_config.json
"""
from __future__ import annotations
import json
import frappe


def run(**kwargs):
    courses = frappe.get_all(
        "LMS Course",
        fields=[
            "name", "title", "published",
            "custom_stripe_monthly_plan",
            "custom_stripe_annual_plan",
        ],
        limit=100,
    )

    plan_names = set()
    for c in courses:
        if c.get("custom_stripe_monthly_plan"):
            plan_names.add(c["custom_stripe_monthly_plan"])
        if c.get("custom_stripe_annual_plan"):
            plan_names.add(c["custom_stripe_annual_plan"])

    plans = {}
    if plan_names:
        rows = frappe.get_all(
            "Subscription Plan",
            filters=[["name", "in", list(plan_names)]],
            fields=[
                "name", "plan_name", "cost", "currency",
                "billing_interval", "billing_interval_count",
                "payment_gateway", "product_price_id",
            ],
        )
        for r in rows:
            plans[r["name"]] = r

    # Payment gateway controllers
    gateways = {}
    for row in frappe.get_all("Payment Gateway", fields=["name", "gateway_controller"]):
        gateways[row["name"]] = row["gateway_controller"]

    result = {"courses": courses, "plans": plans, "gateways": gateways}
    print(json.dumps(result, default=str, indent=2))
