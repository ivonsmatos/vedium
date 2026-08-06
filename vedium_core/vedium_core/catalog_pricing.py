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


def is_catalog_complete(course_name: str, environment: str = "live") -> dict:
    """
    Verifica se o curso possui os 10 registros necessários (5 mensais + 5 anuais)
    ativos, validados, na versão 1 e no modo Live.
    Retorna o status em um dicionário completo e detalhado.
    """
    result = {
        "complete": False,
        "expected": 10,
        "valid": 0,
        "missing": [],
        "duplicated": [],
        "invalid": []
    }
    
    if not course_name:
        return result

    # Buscar todos os preços deste curso e ambiente (qualquer status, para relatar invalidez)
    prices = frappe.get_all(
        "Vedium Course Price",
        filters={"course": course_name, "stripe_environment": environment},
        fields=["name", "billing_period", "classes_per_week", "enabled", "stripe_validated", "catalog_version", "stripe_price_id"]
    )
    
    expected_combinations = {
        f"{period}:{classes}": 0
        for period in ["monthly", "annual"]
        for classes in [1, 2, 3, 4, 5]
    }
    
    for p in prices:
        key = f"{p.billing_period}:{p.classes_per_week}"
        is_valid = bool(
            p.enabled and 
            p.stripe_validated and 
            p.catalog_version == 1 and 
            p.stripe_price_id
        )
        
        if not is_valid:
            result["invalid"].append(p.name)
            continue
            
        if key in expected_combinations:
            expected_combinations[key] += 1
        else:
            # Caso não esperado
            result["invalid"].append(p.name)
            
    for key, count in expected_combinations.items():
        if count == 0:
            result["missing"].append(key)
        elif count == 1:
            result["valid"] += 1
        else:
            result["duplicated"].append(key)
            result["valid"] += 1 # Contamos apenas um como válido
            
    if result["valid"] == 10 and not result["missing"] and not result["duplicated"]:
        result["complete"] = True
        
    return result
