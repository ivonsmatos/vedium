import frappe

frappe.connect(site='vedium.local')

print("🔧 Configurando Payment Gateways e Terms and Conditions...\n")

# =====================================================
# 1. Criar Payment Gateway - MercadoPago
# =====================================================
try:
    if not frappe.db.exists("Payment Gateway", "MercadoPago"):
        mp_gateway = frappe.get_doc({
            "doctype": "Payment Gateway",
            "gateway": "MercadoPago",
            "gateway_settings": "MercadoPago Settings"
        })
        mp_gateway.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✓ Payment Gateway 'MercadoPago' criado")
    else:
        print("⚠ Payment Gateway 'MercadoPago' já existe")
except Exception as e:
    print(f"✗ Erro ao criar MercadoPago: {str(e)}")

# =====================================================
# 2. Criar Payment Gateway - Stripe
# =====================================================
try:
    if not frappe.db.exists("Payment Gateway", "Stripe"):
        stripe_gateway = frappe.get_doc({
            "doctype": "Payment Gateway",
            "gateway": "Stripe",
            "gateway_settings": "Stripe Settings"
        })
        stripe_gateway.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✓ Payment Gateway 'Stripe' criado")
    else:
        print("⚠ Payment Gateway 'Stripe' já existe")
except Exception as e:
    print(f"✗ Erro ao criar Stripe: {str(e)}")

# =====================================================
# 3. Criar Terms and Conditions - Vedium
# =====================================================
terms_content = """
<h2>Termos e Condições de Uso - Vedium Global Education</h2>

<h3>1. Aceitação dos Termos</h3>
<p>Ao se inscrever em nossos cursos, você concorda com estes termos e condições.</p>

<h3>2. Acesso aos Cursos</h3>
<p>O acesso aos cursos é concedido mediante pagamento integral do valor do curso. O acesso é válido por 12 meses a partir da data de matrícula.</p>

<h3>3. Política de Reembolso</h3>
<p>Oferecemos garantia de reembolso de 7 dias. Após este período, não serão aceitos pedidos de reembolso.</p>

<h3>4. Propriedade Intelectual</h3>
<p>Todo o conteúdo dos cursos é propriedade da Vedium Global Education e protegido por direitos autorais. É proibida a reprodução, distribuição ou compartilhamento do conteúdo.</p>

<h3>5. Certificados</h3>
<p>Certificados são emitidos apenas para alunos que completarem 100% do curso e obtiverem nota mínima de 70% nas avaliações.</p>

<h3>6. Privacidade</h3>
<p>Seus dados pessoais são protegidos conforme nossa Política de Privacidade e a LGPD (Lei Geral de Proteção de Dados).</p>

<h3>7. Suporte</h3>
<p>Oferecemos suporte via email em até 48 horas úteis. Contato: contato@vediums.com</p>

<h3>8. Modificações</h3>
<p>Reservamo-nos o direito de modificar estes termos a qualquer momento. Alterações serão comunicadas por email.</p>

<p><strong>Última atualização:</strong> 08/02/2026</p>
"""

try:
    if not frappe.db.exists("Terms and Conditions", "Vedium - Termos de Uso"):
        terms = frappe.get_doc({
            "doctype": "Terms and Conditions",
            "title": "Vedium - Termos de Uso",
            "terms": terms_content,
            "disabled": 0
        })
        terms.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✓ Terms and Conditions 'Vedium - Termos de Uso' criado")
    else:
        print("⚠ Terms and Conditions já existe")
except Exception as e:
    print(f"✗ Erro ao criar Terms: {str(e)}")

# =====================================================
# 4. Criar Item Group para Cursos (se não existir)
# =====================================================
try:
    if not frappe.db.exists("Item Group", "Cursos Online"):
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "Cursos Online",
            "parent_item_group": "All Item Groups",
            "is_group": 0
        })
        item_group.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✓ Item Group 'Cursos Online' criado")
    else:
        print("⚠ Item Group 'Cursos Online' já existe")
except Exception as e:
    print(f"✗ Erro ao criar Item Group: {str(e)}")

# =====================================================
# 5. Verificar configuração da Company
# =====================================================
company = frappe.get_doc("Company", "Vedium")
print(f"\n📊 Company: {company.name}")
print(f"   Moeda padrão: {company.default_currency}")
print(f"   Abbr: {company.abbr}")

print("\n✅ Configuração do ERPNext concluída!")
print("\n📝 Próximos passos:")
print("   1. Configurar credenciais do MercadoPago no Payment Gateway")
print("   2. Cadastrar primeiro curso")
print("   3. Testar fluxo de pagamento")
