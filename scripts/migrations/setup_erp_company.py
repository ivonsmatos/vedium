"""
Configura empresa Vedium + plano de contas + CRM básico.
Execute: printf '%run /path/setup_erp_company.py\nexit\n' | bench --site app.vediums.com console
"""

import frappe
from frappe.utils import today, getdate
from datetime import date

# ─── 0. PRÉ-REQUISITOS: WAREHOUSE TYPES ──────────────────────────────────────

for wt in ["Transit", "Stores", "Finished Goods", "Raw Material"]:
    if not frappe.db.exists("Warehouse Type", wt):
        frappe.get_doc({"doctype": "Warehouse Type", "name": wt}).insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  ✓ Warehouse Type: {wt}")

# ─── 1. EMPRESA ──────────────────────────────────────────────────────────────

if not frappe.db.exists("Company", "Vedium"):
    company = frappe.get_doc(
        {
            "doctype": "Company",
            "company_name": "Vedium",
            "abbr": "VDM",
            "default_currency": "BRL",
            "country": "Brazil",
            "date_of_establishment": "2024-12-12",
            "domain": "Education",
            "tax_id": "58.434.869/0001-24",
            "email": "contato@vediums.com",
            "phone_no": "(11) 4190-6079",
            "website": "vediums.com",
        }
    )
    company.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✓ Empresa 'Vedium' criada")
else:
    # Atualiza campos com dados do CNPJ
    frappe.db.set_value("Company", "Vedium", {
        "tax_id": "58.434.869/0001-24",
        "date_of_establishment": "2024-12-12",
        "phone_no": "(11) 4190-6079",
        "email": "contato@vediums.com",
        "website": "vediums.com",
    })
    frappe.db.commit()
    print("✓ Empresa 'Vedium' atualizada com dados do CNPJ")

# ─── 2. MOEDA BRL ────────────────────────────────────────────────────────────

if not frappe.db.exists("Currency", "BRL"):
    cur = frappe.get_doc(
        {
            "doctype": "Currency",
            "currency_name": "BRL",
            "symbol": "R$",
            "fraction": "Centavo",
            "fraction_units": 100,
            "enabled": 1,
        }
    )
    cur.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✓ Moeda BRL criada")
else:
    frappe.db.set_value("Currency", "BRL", "enabled", 1)
    frappe.db.commit()
    print("✓ Moeda BRL habilitada")

# ─── 3. ANO FISCAL ───────────────────────────────────────────────────────────

fy_name = "2025-2026"
if not frappe.db.exists("Fiscal Year", fy_name):
    fy = frappe.get_doc(
        {
            "doctype": "Fiscal Year",
            "year": fy_name,
            "year_start_date": "2025-01-01",
            "year_end_date": "2025-12-31",
            "companies": [{"company": "Vedium"}],
        }
    )
    fy.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"✓ Ano fiscal {fy_name} criado")
else:
    print(f"✓ Ano fiscal {fy_name} já existe")

# Define o ano fiscal padrão
frappe.db.set_default("fiscal_year", fy_name)

# ─── 4. CONFIGURAÇÕES GLOBAIS ─────────────────────────────────────────────────

global_defaults = frappe.get_doc("Global Defaults")
global_defaults.default_company = "Vedium"
global_defaults.default_currency = "BRL"
global_defaults.current_fiscal_year = fy_name
global_defaults.country = "Brazil"
global_defaults.save(ignore_permissions=True)
frappe.db.commit()
print("✓ Global Defaults configurado")

# ─── 5. CRM — TERRITORY ──────────────────────────────────────────────────────

# Ensure root exists
if not frappe.db.exists("Territory", "All Territories"):
    frappe.get_doc({
        "doctype": "Territory",
        "territory_name": "All Territories",
        "is_group": 1,
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    print("  ✓ Territory root: All Territories")

territories = [
    "Brasil",
    "São Paulo",
    "Rio de Janeiro",
    "Minas Gerais",
    "Outros Estados",
]
for t in territories:
    if not frappe.db.exists("Territory", t):
        doc = frappe.get_doc(
            {
                "doctype": "Territory",
                "territory_name": t,
                "parent_territory": "All Territories" if t == "Brasil" else "Brasil",
            }
        )
        try:
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  ✓ Territory: {t}")
        except Exception as e:
            print(f"  ⚠ Territory {t}: {e}")

# ─── 6. CRM — CUSTOMER GROUP ─────────────────────────────────────────────────

# Ensure root exists
if not frappe.db.exists("Customer Group", "All Customer Groups"):
    frappe.get_doc({
        "doctype": "Customer Group",
        "customer_group_name": "All Customer Groups",
        "is_group": 1,
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    print("  ✓ Customer Group root: All Customer Groups")

customer_groups = [
    ("Aluno", "All Customer Groups"),
    ("Empresa Parceira", "All Customer Groups"),
    ("Escola", "All Customer Groups"),
]
for grp, parent in customer_groups:
    if not frappe.db.exists("Customer Group", grp):
        doc = frappe.get_doc(
            {
                "doctype": "Customer Group",
                "customer_group_name": grp,
                "parent_customer_group": parent,
            }
        )
        try:
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  ✓ Customer Group: {grp}")
        except Exception as e:
            print(f"  ⚠ Customer Group {grp}: {e}")

# ─── 7. CRM — LEAD SOURCES ───────────────────────────────────────────────────

lead_sources = [
    "Site Vediums.com",
    "Indicação",
    "Instagram",
    "Google Ads",
    "WhatsApp",
    "Evento",
]
for src in lead_sources:
    if not frappe.db.exists("Lead Source", src):
        doc = frappe.get_doc({"doctype": "Lead Source", "source_name": src})
        try:
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  ✓ Lead Source: {src}")
        except Exception as e:
            print(f"  ⚠ Lead Source {src}: {e}")

# ─── 8. SELLING SETTINGS ─────────────────────────────────────────────────────

try:
    selling_settings = frappe.get_doc("Selling Settings")
    if not selling_settings.customer_group and frappe.db.exists("Customer Group", "Aluno"):
        selling_settings.customer_group = "Aluno"
    if not selling_settings.territory and frappe.db.exists("Territory", "Brasil"):
        selling_settings.territory = "Brasil"
    selling_settings.save(ignore_permissions=True)
    frappe.db.commit()
    print("✓ Selling Settings configurado")
except Exception as e:
    print(f"  ⚠ Selling Settings: {e}")

# ─── RESUMO ───────────────────────────────────────────────────────────────────

print("")
print("=" * 50)
print("  Setup ERP Vedium concluído!")
print("=" * 50)
company = frappe.get_doc("Company", "Vedium")
print(f"  Empresa:    {company.company_name} ({company.abbr})")
print(f"  País:       {company.country}")
print(f"  Moeda:      {company.default_currency}")
print(f"  Ano Fiscal: {fy_name}")
coa_count = frappe.db.count("Account", {"company": "Vedium"})
print(f"  Contas:     {coa_count} no plano de contas")
print("=" * 50)
