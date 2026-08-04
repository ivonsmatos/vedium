"""Service for querying pre-configured course prices (Stripe catalog)."""

from __future__ import annotations

import frappe
from frappe import _


def get_course_price(course_name, billing_period, classes_per_week, environment="live"):
    """
    Localiza exatamente um registro ativo e validado no catálogo.
    Falha se não encontrar ou se houver múltiplos ativos de forma inconsistente.
    """
    if not course_name:
        frappe.throw(_("Curso não informado."))
    if billing_period not in ["monthly", "annual"]:
        frappe.throw(_("Período de cobrança inválido (deve ser 'monthly' ou 'annual')."))
    if not classes_per_week or int(classes_per_week) < 1 or int(classes_per_week) > 5:
        frappe.throw(_("Aulas por semana deve estar entre 1 e 5."))

    filters = {
        "course": course_name,
        "billing_period": billing_period,
        "classes_per_week": int(classes_per_week),
        "stripe_environment": environment,
        "enabled": 1,
        "stripe_validated": 1,
    }

    records = frappe.get_all("Vedium Course Price", filters=filters, pluck="name")

    if not records:
        frappe.throw(_("Preço não encontrado no catálogo para as opções selecionadas."))
    
    if len(records) > 1:
        # Se houver mais de um, pegar o de maior versão ou falhar
        # Por segurança, vamos falhar, exigindo que o admin desative os antigos
        frappe.throw(_("Múltiplos preços ativos encontrados. Contate o suporte administrativo."))

    return frappe.get_doc("Vedium Course Price", records[0])


def is_catalog_complete(course_name, environment="live"):
    """
    Verifica se o curso possui os 10 registros necessários (5 mensais + 5 anuais)
    ativos e validados.
    """
    if not course_name:
        return False
        
    counts = frappe.db.count("Vedium Course Price", filters={
        "course": course_name,
        "stripe_environment": environment,
        "enabled": 1,
        "stripe_validated": 1
    }, group_by="billing_period", debug=False)
    
    # O group_by retorna algo como: [(5, 'annual'), (5, 'monthly')] se fetch_as_dict=False
    # Mas no get_all/count pode ser complicado. Vamos fazer manual.
    
    monthly_count = frappe.db.count("Vedium Course Price", filters={
        "course": course_name,
        "stripe_environment": environment,
        "enabled": 1,
        "stripe_validated": 1,
        "billing_period": "monthly"
    })
    
    annual_count = frappe.db.count("Vedium Course Price", filters={
        "course": course_name,
        "stripe_environment": environment,
        "enabled": 1,
        "stripe_validated": 1,
        "billing_period": "annual"
    })
    
    # Se tem algum incompleto mas tem pelo menos 1, retornamos ValueError
    # O requisito: "Se houver apenas parte dos registros, bloquear o Checkout administrativo e registrar erro de configuração."
    total = monthly_count + annual_count
    
    if total == 10 and monthly_count == 5 and annual_count == 5:
        return True
        
    if total > 0:
        frappe.log_error(
            f"Catálogo incompleto para o curso {course_name}. Mensal: {monthly_count}, Anual: {annual_count}.",
            "Vedium Course Price Error"
        )
        return "incomplete"
        
    return False
