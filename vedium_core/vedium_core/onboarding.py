# -*- coding: utf-8 -*-
"""
Vedium — Módulo de Onboarding

Salva as preferências coletadas no wizard /onboarding:
    - Idioma de interesse (lang)
    - Objetivo do aluno (goal)
    - Frequência de estudo (freq)

Persiste em User Permission e/ou DocType custom 'Vedium User Preference'.
"""

import frappe
from frappe import _

_VALID_LANGS = {"en", "es", "fr", "de", "yo", "pt"}
_VALID_GOALS = {"work", "travel", "culture", "tech"}
_VALID_FREQS = {"1", "2", "5"}


@frappe.whitelist()
def save_onboarding(lang: str = "", goal: str = "", freq: str = ""):
    """
    Salva as preferências coletadas no wizard de onboarding.
    Chamado silenciosamente pelo JavaScript do wizard na última etapa.
    """
    user = frappe.session.user
    if user == "Guest":
        return {"status": "skip"}

    # Valida entradas
    lang  = lang.strip()  if lang  in _VALID_LANGS else ""
    goal  = goal.strip()  if goal  in _VALID_GOALS else ""
    freq  = freq.strip()  if freq  in _VALID_FREQS else ""

    # Salva em User (campos custom) — fallback resiliente
    updates = {}
    if lang:  updates["custom_preferred_language"] = lang
    if goal:  updates["custom_learning_goal"]      = goal
    if freq:  updates["custom_study_frequency"]    = freq
    if updates:
        try:
            frappe.db.set_value("User", user, updates)
            frappe.db.commit()
        except Exception as ex:
            # Campos custom podem não existir — log e segue
            frappe.log_error(f"Onboarding set_value falhou: {ex}", "Vedium.Onboarding")

    # Marca que o onboarding foi concluído
    try:
        frappe.db.set_value("User", user, "custom_onboarding_done", 1)
        frappe.db.commit()
    except Exception:
        pass

    return {"status": "ok", "lang": lang, "goal": goal, "freq": freq}


@frappe.whitelist()
def get_onboarding_status():
    """Retorna se o usuário já concluiu o onboarding (para redirecionamento automático)."""
    user = frappe.session.user
    if user == "Guest":
        return {"done": False}

    try:
        done = bool(frappe.db.get_value("User", user, "custom_onboarding_done"))
    except Exception:
        done = True  # Em caso de falha, não forçar o wizard

    return {"done": done}
