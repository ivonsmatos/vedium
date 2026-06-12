import frappe
from frappe.utils.user import add_role

def set_full_permissions(user_email):
    if not frappe.db.exists("User", user_email):
        print(f"User {user_email} not found.")
        return

    roles = ["System Manager", "Administrator", "CRM Manager", "LMS Manager"]
    for role in roles:
        if frappe.db.exists("Role", role):
            add_role(user_email, role)
            print(f"Role {role} added to {user_email}.")
    
    frappe.db.commit()
    print("Permissions updated successfully.")

if __name__ == "__main__":
    set_full_permissions("contato@ivonmatos.com.br")
