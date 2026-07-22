# -*- coding: utf-8 -*-
"""Cria o registro formal de RH (Employee) de Guadalupe Samayoa de Trindade.

Complementa hire_guadalupe_espanhol.py (que só cria o User/acesso ao LMS e
não guarda dado sensível de contrato). Este script grava os dados do
contrato de prestação de serviço no Employee nativo do Frappe HR
(`hrms`), que já tem controle de permissão por role (HR Manager/HR User) --
não precisa de tela custom nem doctype novo.

Requer os Custom Fields custom_cpf/custom_rnm (vedium_core.custom_setup) já
aplicados via after_migrate.

⚠️ date_of_birth: não veio no contrato e é campo obrigatório do Employee.
Gravado com placeholder 1900-01-01 -- CORRIGIR manualmente em Frappe HR >
Employee > Guadalupe assim que a data real for informada.

Idempotente.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.hire_guadalupe_hr_record.run
"""

import frappe

EMAIL = "lupitasamayoa3@gmail.com"
FIRST_NAME = "Guadalupe"
LAST_NAME = "Samayoa de Trindade"
CELL_NUMBER = "+55 11 94446-5427"
ADDRESS = (
    "Rua Gato Cinzento, Bloco 2, apartamento 401, Vila Urupês, "
    "Suzano/SP, CEP 08615-070"
)
CPF = "236.034.328-94"
RNM = "V875570 W"
DESIGNATION = "Professor(a) de Espanhol"
DOB_PLACEHOLDER = "1900-01-01"


def run():
    from vedium_core.custom_setup import setup_custom_fields

    setup_custom_fields()

    employee = frappe.db.get_value("Employee", {"personal_email": EMAIL}, "name")
    if employee:
        doc = frappe.get_doc("Employee", employee)
        print(f"Employee já existia: {employee}")
    else:
        doc = frappe.new_doc("Employee")
        doc.date_of_joining = frappe.utils.nowdate()
        doc.date_of_birth = DOB_PLACEHOLDER
        doc.gender = "Female"

    doc.first_name = FIRST_NAME
    doc.last_name = LAST_NAME
    doc.company = "Vedium"
    doc.status = "Active"
    doc.designation = DESIGNATION
    doc.employment_type = "Contract"
    doc.cell_number = CELL_NUMBER
    doc.personal_email = EMAIL
    doc.user_id = EMAIL
    doc.current_address = ADDRESS
    doc.permanent_address = ADDRESS
    doc.marital_status = "Married"
    doc.custom_cpf = CPF
    doc.custom_rnm = RNM

    if doc.is_new():
        doc.insert(ignore_permissions=True)
        print(f"Employee criado: {doc.name}")
    else:
        doc.save(ignore_permissions=True)
        print(f"Employee atualizado: {doc.name}")

    frappe.db.commit()

    if doc.date_of_birth == DOB_PLACEHOLDER:
        print(
            "\n⚠️ date_of_birth ainda é PLACEHOLDER (1900-01-01) -- "
            "corrigir manualmente em Frappe HR > Employee assim que a "
            "data real for informada."
        )
