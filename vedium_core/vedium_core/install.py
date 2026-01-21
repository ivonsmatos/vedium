# Vedium Installation Script

import frappe

def before_install():
    pass

def after_install():
    frappe.msgprint("Vedium Core Installed Successfully!")

def after_migrate():
    pass
