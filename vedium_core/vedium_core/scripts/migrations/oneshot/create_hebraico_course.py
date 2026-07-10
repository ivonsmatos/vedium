# -*- coding: utf-8 -*-
"""Cria o curso-piloto de Hebraico na plataforma (doc "Proposta_Vedium_
Benchmark_Espanhol_Hebraico.pdf", 2026).

A proposta é explícita: NÃO abrir Hebraico em trilha completa
(Básico/Intermediário/Avançado) como o Espanhol. O piloto começa por
"Hebraico Moderno A1" com alfabetização incluída; níveis seguintes
(A2/B1) e a trilha de Hebraico Bíblico só entram depois de validar essa
primeira turma.

Este script cria APENAS o curso (título, descrição, preço-piloto) —
sem capítulos/lições, porque a grade curricular de Hebraico ainda não foi
entregue. Rode create_espanhol_courses/seed_espanhol_quizzes como
referência de como popular módulos quando a grade chegar.

Rodar (idempotente):
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.create_hebraico_course.run
"""

import frappe

CATEGORY = "Hebraico"
CURRENCY = "BRL"

SLUG = "hebraico-moderno-a1"
TITLE = "Hebraico Moderno — Nível A1 (com Alfabetização)"
SHORT_INTRODUCTION = (
    "Turma-piloto: saia do zero lendo as letras, reconhecendo sons e falando "
    "frases de uso real. Ao vivo, em turma pequena, com professor especialista."
)
DESCRIPTION = (
    "<p>O <strong>Hebraico Moderno A1</strong> é o piloto de lançamento do Hebraico "
    "na Vedium: alfabetização (leitura do alef-bet) incluída, para quem nunca teve "
    "contato com o idioma.</p>"
    "<p><strong>Ao final do curso você será capaz de:</strong></p><ul>"
    "<li>Ler e reconhecer as letras do alfabeto hebraico e seus sons</li>"
    "<li>Cumprimentar, se apresentar e formar frases simples do dia a dia</li>"
    "<li>Entender o básico de vocabulário e estrutura do hebraico moderno</li>"
    "</ul>"
    "<p>Turma pequena (4 a 8 alunos), 2 aulas ao vivo por semana. Este é um piloto: "
    "a continuidade em A2/B1 e a trilha de Hebraico Bíblico serão abertas depois da "
    "validação desta primeira turma.</p>"
)
PRICE = 397


def run():
    _ensure_category()
    cat_name = frappe.db.get_value("LMS Category", {"category": CATEGORY}, "name")

    existing_name = frappe.db.get_value("LMS Course", {"title": TITLE}, "name")
    if existing_name and existing_name != SLUG:
        print(f"  — Encontrado '{existing_name}' → renomeando para '{SLUG}'...")
        frappe.rename_doc("LMS Course", existing_name, SLUG, force=True)
        frappe.db.commit()
        print(f"\n✓ Curso '{SLUG}' já existia, apenas renomeado.")
        return

    if frappe.db.exists("LMS Course", SLUG):
        print(f"\n— Curso '{SLUG}' já existe, nada a fazer.")
        return

    instructor = _default_instructor()
    course = frappe.get_doc({
        "doctype": "LMS Course",
        "title": TITLE,
        "short_introduction": SHORT_INTRODUCTION,
        "description": DESCRIPTION,
        "paid_course": 1,
        "course_price": PRICE,
        "currency": CURRENCY,
        "published": 1,
        "category": cat_name,
        "instructors": [{"instructor": instructor}],
    })
    course.insert(ignore_permissions=True)
    if course.name != SLUG:
        print(f"    (auto-name '{course.name}' → renomeando para '{SLUG}')")
        frappe.rename_doc("LMS Course", course.name, SLUG, force=True)
    frappe.db.commit()

    print(f"\n✓ Curso '{SLUG}' criado (instrutor back-end: {instructor}).")
    print("  Sem módulos ainda — aguardando a grade curricular de Hebraico.")


def _ensure_category():
    if frappe.db.exists("LMS Category", {"category": CATEGORY}):
        return
    frappe.get_doc({"doctype": "LMS Category", "category": CATEGORY}).insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  ✓ Categoria '{CATEGORY}' criada.")


def _default_instructor():
    for candidate in ("Administrator", "contato@vediums.com"):
        if frappe.db.exists("User", candidate):
            return candidate
    user = frappe.db.get_value("User", {"enabled": 1, "user_type": "System User"}, "name")
    return user or "Administrator"
