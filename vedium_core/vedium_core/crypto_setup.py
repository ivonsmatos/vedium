import frappe

def setup_currencies_and_gateways():
    # 1. Ensure Currencies exist
    currencies = [
        {"name": "USD", "currency_name": "United States Dollar", "symbol": "$", "fraction": "Cent"},
        {"name": "BRL", "currency_name": "Brazil Real", "symbol": "R$", "fraction": "Centavo"}
    ]

    for c in currencies:
        if not frappe.db.exists("Currency", c["name"]):
            doc = frappe.get_doc({
                "doctype": "Currency",
                "currency_name": c["currency_name"],
                "enabled": 1,
                "fraction": c["fraction"],
                "fraction_units": 100,
                "smallest_currency_fraction_value": 0.01,
                "symbol": c["symbol"],
                "name": c["name"]
            })
            doc.insert(ignore_permissions=True)
            print(f"Currency {c['name']} created.")
        else:
            frappe.db.set_value("Currency", c["name"], "enabled", 1)
            print(f"Currency {c['name']} enabled.")

    # 2. Setup Crypto Payment Gateway Placeholder (Custom Field/Linking)
    # We can use the 'Payment Gateway' doctype from the payments app
    if frappe.db.exists("DocType", "Payment Gateway"):
        if not frappe.db.exists("Payment Gateway", "Crypto - Coinbase"):
            gateway = frappe.get_doc({
                "doctype": "Payment Gateway",
                "gateway_name": "Crypto - Coinbase",
                "gateway_settings": "NowPayments Settings" # Generic or custom settings
            })
            # gateway.insert(ignore_permissions=True)
            pass

    frappe.db.commit()

if __name__ == "__main__":
    setup_currencies_and_gateways()
