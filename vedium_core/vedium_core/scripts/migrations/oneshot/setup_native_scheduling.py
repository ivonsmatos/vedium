"""Habilita o agendamento NATIVO do Frappe LMS (Course Evaluator + Google
Meet para aulas 1-a-1; a Live Class/Zoom é configurada à parte no Desk).

O que faz, de forma idempotente:
1. Para cada curso publicado, descobre o professor a partir do child table
   `Course Instructor` (fonte da verdade já existente) e, se houver um
   `Course Evaluator` para esse professor, vincula o curso a ele
   (campo LMS Course.evaluator). Sem esse vínculo, o aluno não vê o botão
   de agendar avaliação dentro do LMS.
2. Liga `enable_certification` nos cursos que têm evaluator mas ainda estão
   com a certificação desligada (caso dos 3 cursos de PLE).

NÃO mexe em: horários de disponibilidade do professor (Evaluator Schedule),
conexão do Google Calendar de cada professor, nem credenciais do Zoom —
essas etapas são ações manuais/OAuth de cada usuário, impossíveis por script.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.setup_native_scheduling.run
"""
import frappe


def _instructor_of(course_name):
    rows = frappe.get_all(
        "Course Instructor",
        filters={"parent": course_name},
        fields=["instructor"],
        order_by="idx asc",
        limit_page_length=1,
    )
    return rows[0].instructor if rows else None


def run():
    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "title", "evaluator", "enable_certification"],
    )

    linked, cert_enabled, skipped = [], [], []
    for course in courses:
        instructor = _instructor_of(course.name)
        if not instructor:
            skipped.append(f"{course.name} (sem Course Instructor)")
            continue
        if not frappe.db.exists("Course Evaluator", instructor):
            skipped.append(f"{course.name} (instrutor {instructor} não é Course Evaluator)")
            continue

        changed = False
        if not course.evaluator:
            frappe.db.set_value("LMS Course", course.name, "evaluator", instructor)
            linked.append(f"{course.name} -> {instructor}")
            changed = True

        # Só ligamos certificação em cursos que agora têm avaliador — é o
        # que destrava o agendamento da avaliação para o aluno.
        if not course.enable_certification:
            frappe.db.set_value("LMS Course", course.name, "enable_certification", 1)
            cert_enabled.append(course.name)
            changed = True

        if not changed:
            skipped.append(f"{course.name} (já configurado)")

    frappe.db.commit()

    print("=== Cursos vinculados a evaluator ===")
    for x in linked:
        print("  +", x)
    print("=== Certificação ligada ===")
    for x in cert_enabled:
        print("  +", x)
    print("=== Ignorados/sem mudança ===")
    for x in skipped:
        print("  -", x)
    print(f"\nResumo: {len(linked)} vínculos, {len(cert_enabled)} certificações ligadas.")
    print(
        "\nFalta (ação manual de cada professor no LMS):\n"
        "  1. Conectar o Google Calendar (perfil do avaliador).\n"
        "  2. Cadastrar os horários disponíveis (Evaluator Schedule).\n"
        "Para aula em grupo (Zoom): preencher Zoom Settings + criar Batches."
    )
