"""Liga o botão nativo "Get Certified" do LMS (que leva direto pro
agendamento de aula com o professor) sem cobrar o aluno de novo.

Contexto: o componente nativo do LMS (`CertificationLinks.vue`) só mostra
esse botão quando `LMS Course.paid_certificate = 1` — um conceito nativo de
"certificado vendido separado, com preço próprio dentro do LMS". Não é o
modelo da Vedium: o certificado/avaliação já está incluso no preço pago
via Stripe no checkout. Se ligássemos só `paid_certificate` sem também
marcar `purchased_certificate=1` na matrícula, o botão mandaria o aluno
pra uma tela de cobrança DENTRO do LMS, cobrando de novo.

O que este script faz, de forma idempotente:
1. Liga `paid_certificate=1` em todo curso publicado que já tem `evaluator`
   vinculado (mesmo critério do setup_native_scheduling.py).
2. Liga `purchased_certificate=1` em toda matrícula (LMS Enrollment) já
   existente — o aluno já pagou pelo curso completo, isso só reflete isso
   pro LMS não pedir de novo.
3. Matrículas NOVAS já vêm com isso ligado via api.create_enrollment_if_paid
   (alterado nesta mesma mudança) — este script cobre só o histórico.

Seguro em produção: só liga booleanos existentes, não mexe em preço, cupom,
ou qualquer dado financeiro.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.enable_native_scheduling_button.run
"""
import frappe


def run():
    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "evaluator", "paid_certificate"],
    )
    courses_updated = []
    for course in courses:
        if course.evaluator and not course.paid_certificate:
            frappe.db.set_value("LMS Course", course.name, "paid_certificate", 1)
            courses_updated.append(course.name)

    enrollments = frappe.get_all(
        "LMS Enrollment",
        filters={"purchased_certificate": ["!=", 1]},
        fields=["name"],
    )
    for enrollment in enrollments:
        frappe.db.set_value(
            "LMS Enrollment", enrollment.name, "purchased_certificate", 1
        )

    frappe.db.commit()

    print(f"Cursos com paid_certificate ligado agora: {len(courses_updated)}")
    for c in courses_updated:
        print("  +", c)
    print(f"Matrículas com purchased_certificate ligado agora: {len(enrollments)}")
