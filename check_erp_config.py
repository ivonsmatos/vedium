import frappe

frappe.connect(site='vedium.local')

# Verificar se Company existe
companies = frappe.get_all("Company", fields=["name", "abbr", "default_currency"])
print(f"\n📊 Companies cadastradas: {len(companies)}")
for c in companies:
    print(f"  - {c.name} ({c.abbr}) - {c.default_currency}")

# Verificar se há Payment Gateway configurado
gateways = frappe.get_all("Payment Gateway", fields=["name", "gateway"])
print(f"\n💳 Payment Gateways: {len(gateways)}")
for g in gateways:
    print(f"  - {g.name}: {g.gateway}")

# Verificar Currency
currencies = frappe.get_all("Currency", filters={"enabled": 1}, fields=["name", "symbol"])
print(f"\n💰 Moedas habilitadas: {len(currencies)}")
for curr in currencies[:5]:
    print(f"  - {curr.name} ({curr.symbol})")

# Verificar se há Item Group para cursos
item_groups = frappe.get_all("Item Group", fields=["name"])
print(f"\n📦 Item Groups: {len(item_groups)}")

# Verificar Terms and Conditions
terms = frappe.get_all("Terms and Conditions", fields=["name", "title"])
print(f"\n📜 Terms and Conditions: {len(terms)}")
for t in terms:
    print(f"  - {t.name}: {t.title}")

print("\n✅ Verificação concluída!")
