import frappe

frappe.connect(site='vedium.local')

print("🔧 Alterando credenciais do Administrator...\n")

# Alterar email do Administrator
try:
    admin = frappe.get_doc("User", "Administrator")
    admin.email = "contato@ivonmatos.com.br"
    admin.first_name = "Ivon"
    admin.last_name = "Matos"
    admin.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"✓ Email do Administrator alterado para: {admin.email}")
except Exception as e:
    print(f"✗ Erro ao alterar email: {str(e)}")

# Alterar senha
try:
    frappe.set_user("Administrator")
    from frappe.utils.password import update_password
    update_password("Administrator", "***REDACTED-PASSWORD***")
    frappe.db.commit()
    print("✓ Senha do Administrator alterada com sucesso")
except Exception as e:
    print(f"✗ Erro ao alterar senha: {str(e)}")

print("\n✅ Configuração concluída!")
print("\n📝 Credenciais de acesso:")
print("   URL: http://localhost:8005")
print("   Usuário: Administrator")
print("   Email: contato@ivonmatos.com.br")
print("   Senha: ***REDACTED-PASSWORD***")
