import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# Campos customizados do Vedium em DocTypes oficiais.
# gamification.add_points depende de User.vedium_points — por isso esta
# função roda no after_migrate (install.py), idempotente.

CUSTOM_FIELDS = {
    "User": [
        {
            "fieldname": "vedium_points",
            "label": "Vedium Points",
            "fieldtype": "Int",
            "insert_after": "first_name",
            "default": "0",
            "read_only": 1,
        },
        {
            "fieldname": "preferred_language",
            "label": "Preferred Language",
            "fieldtype": "Link",
            "options": "Language",
            "insert_after": "vedium_points",
        },
        {
            "fieldname": "custom_preferred_language",
            "label": "Idioma de Interesse (Onboarding)",
            "fieldtype": "Data",
            "insert_after": "preferred_language",
        },
        {
            "fieldname": "custom_learning_goal",
            "label": "Objetivo de Aprendizado",
            "fieldtype": "Data",
            "insert_after": "custom_preferred_language",
        },
        {
            "fieldname": "custom_study_frequency",
            "label": "Frequência de Estudo",
            "fieldtype": "Data",
            "insert_after": "custom_learning_goal",
        },
        {
            "fieldname": "custom_onboarding_done",
            "label": "Onboarding Concluído",
            "fieldtype": "Check",
            "insert_after": "custom_study_frequency",
        },
    ],
    "System Settings": [
        {
            "fieldname": "custom_vedium_vapid_public_key",
            "label": "Vedium VAPID Public Key",
            "fieldtype": "Data",
        },
        {
            "fieldname": "custom_vedium_vapid_private_key",
            "label": "Vedium VAPID Private Key",
            "fieldtype": "Password",
            "insert_after": "custom_vedium_vapid_public_key",
        },
        {
            "fieldname": "custom_vedium_vapid_email",
            "label": "Vedium VAPID Contact E-mail",
            "fieldtype": "Data",
            "insert_after": "custom_vedium_vapid_private_key",
        },
    ],
    "LMS Certificate": [
        {
            "fieldname": "verification_code",
            "label": "Verification Code",
            "fieldtype": "Data",
            "insert_after": "member",
            "unique": 1,
            "read_only": 1,
        },
        {
            "fieldname": "enrollment",
            "label": "Enrollment",
            "fieldtype": "Link",
            "options": "LMS Enrollment",
            "insert_after": "verification_code",
        },
    ],
    "LMS Course": [
        {
            "fieldname": "custom_prerequisite_course",
            "label": "Curso pré-requisito (gate de nível)",
            "fieldtype": "Link",
            "options": "LMS Course",
            "insert_after": "category",
        },
        {
            "fieldname": "custom_stripe_monthly_plan",
            "label": "Plano Stripe mensal",
            "fieldtype": "Link",
            "options": "Subscription Plan",
            "insert_after": "custom_prerequisite_course",
        },
        {
            "fieldname": "custom_stripe_annual_plan",
            "label": "Plano Stripe anual",
            "fieldtype": "Link",
            "options": "Subscription Plan",
            "insert_after": "custom_stripe_monthly_plan",
        },
    ],
    "LMS Enrollment": [
        {
            "fieldname": "custom_vedium_status",
            "label": "Status Vedium",
            "fieldtype": "Select",
            "options": (
                "Active\nTrial\nCancellation Requested\nPending Review\n"
                "Suspended\nCancelled\nEnded\nExpired"
            ),
            "default": "Active",
            "insert_after": "role",
            "in_list_view": 1,
        },
        {
            "fieldname": "custom_vedium_status_changed_on",
            "label": "Status alterado em",
            "fieldtype": "Datetime",
            "insert_after": "custom_vedium_status",
            "read_only": 1,
        },
        {
            "fieldname": "custom_vedium_status_reason",
            "label": "Motivo do status",
            "fieldtype": "Small Text",
            "insert_after": "custom_vedium_status_changed_on",
        },
        {
            "fieldname": "custom_trial_start",
            "label": "Início do trial",
            "fieldtype": "Datetime",
            "insert_after": "custom_vedium_status_reason",
            "read_only": 1,
        },
        {
            "fieldname": "custom_trial_end",
            "label": "Fim do trial",
            "fieldtype": "Datetime",
            "insert_after": "custom_trial_start",
            "read_only": 1,
        },
        {
            "fieldname": "custom_stripe_customer_id",
            "label": "Stripe Customer ID",
            "fieldtype": "Data",
            "insert_after": "custom_trial_end",
            "read_only": 1,
        },
        {
            "fieldname": "custom_stripe_subscription_id",
            "label": "Stripe Subscription ID",
            "fieldtype": "Data",
            "insert_after": "custom_stripe_customer_id",
            "unique": 1,
            "read_only": 1,
        },
        {
            "fieldname": "custom_stripe_price_id",
            "label": "Stripe Price ID",
            "fieldtype": "Data",
            "insert_after": "custom_stripe_subscription_id",
            "read_only": 1,
        },
        {
            "fieldname": "custom_billing_period",
            "label": "Período contratual",
            "fieldtype": "Select",
            "options": "monthly\nannual",
            "insert_after": "custom_stripe_price_id",
            "read_only": 1,
        },
        {
            "fieldname": "custom_classes_per_week",
            "label": "Aulas por semana",
            "fieldtype": "Int",
            "insert_after": "custom_billing_period",
            "read_only": 1,
            "in_list_view": 1,
        },
        {
            "fieldname": "custom_frequency_discount_percent",
            "label": "Desconto por frequência (%)",
            "fieldtype": "Percent",
            "insert_after": "custom_classes_per_week",
            "read_only": 1,
        },
        {
            "fieldname": "custom_contract_monthly_amount",
            "label": "Valor mensal contratado",
            "fieldtype": "Currency",
            "insert_after": "custom_frequency_discount_percent",
            "read_only": 1,
        },
        {
            "fieldname": "custom_contract_currency",
            "label": "Moeda contratada",
            "fieldtype": "Data",
            "insert_after": "custom_contract_monthly_amount",
            "read_only": 1,
            "default": "BRL",
        },
        {
            "fieldname": "custom_minimum_term_ends_on",
            "label": "Fim da permanência mínima",
            "fieldtype": "Date",
            "insert_after": "custom_contract_monthly_amount",
            "read_only": 1,
        },
        {
            "fieldname": "custom_payment_failed_on",
            "label": "Primeira falha de pagamento",
            "fieldtype": "Datetime",
            "insert_after": "custom_minimum_term_ends_on",
            "read_only": 1,
        },
        {
            "fieldname": "custom_stripe_last_invoice_id",
            "label": "Última fatura Stripe",
            "fieldtype": "Data",
            "insert_after": "custom_payment_failed_on",
            "read_only": 1,
        },
        {
            "fieldname": "custom_cancellation_requested_on",
            "label": "Cancelamento solicitado em",
            "fieldtype": "Datetime",
            "insert_after": "custom_stripe_last_invoice_id",
            "read_only": 1,
        },
        {
            "fieldname": "custom_payment_gateway",
            "label": "Gateway do pagamento",
            "fieldtype": "Data",
            "insert_after": "custom_cancellation_requested_on",
            "read_only": 1,
        },
        {
            "fieldname": "custom_payment_reference",
            "label": "Referência do pagamento",
            "fieldtype": "Data",
            "insert_after": "custom_payment_gateway",
            "read_only": 1,
        },
        {
            "fieldname": "custom_payment_amount",
            "label": "Valor do pagamento",
            "fieldtype": "Currency",
            "insert_after": "custom_payment_reference",
            "read_only": 1,
        },
        {
            "fieldname": "custom_payment_currency",
            "label": "Moeda do pagamento",
            "fieldtype": "Link",
            "options": "Currency",
            "insert_after": "custom_payment_amount",
            "read_only": 1,
        },
        {
            # Marca quando o "nudge de ativação" já foi disparado para esta
            # matrícula (aluno matriculou mas ainda não começou o curso). Sem
            # isso, o job diário reenviaria o empurrão todo dia — ver
            # vedium_core/student_onboarding.py::detect_inactive_students.
            "fieldname": "custom_activation_nudged_on",
            "label": "Nudge de ativação enviado em",
            "fieldtype": "Datetime",
            "insert_after": "custom_payment_currency",
            "read_only": 1,
        },
        {
            # Maior marco de progresso (25/50/75/100%) já notificado ao Brevo
            # (fluxo A10). Anti-duplicidade: só emite quando cruza um marco novo.
            # Ver vedium_core/gamification.py::handle_course_progress_milestone.
            "fieldname": "custom_last_progress_milestone",
            "label": "Último marco de progresso notificado (%)",
            "fieldtype": "Int",
            "default": "0",
            "insert_after": "custom_activation_nudged_on",
            "read_only": 1,
        },
        {
            # Data da aula mais recente para a qual já disparamos o alerta de
            # faltas consecutivas (fluxo A09). Idempotência do detector de
            # ausência — ver vedium_core/attendance_events.py.
            "fieldname": "custom_absence_alerted_on",
            "label": "Alerta de ausência (última aula) em",
            "fieldtype": "Date",
            "insert_after": "custom_last_progress_milestone",
            "read_only": 1,
        },
    ],
    "Integration Request": [
        {
            "fieldname": "custom_vedium_attempts",
            "label": "Tentativas Vedium",
            "fieldtype": "Int",
            "default": "0",
            "read_only": 1,
        },
        {
            "fieldname": "custom_vedium_last_attempt_on",
            "label": "Última tentativa Vedium",
            "fieldtype": "Datetime",
            "insert_after": "custom_vedium_attempts",
            "read_only": 1,
        },
    ],
    "Employee": [
        {
            "fieldname": "custom_cpf",
            "label": "CPF",
            "fieldtype": "Data",
            "insert_after": "passport_number",
        },
        {
            "fieldname": "custom_rnm",
            "label": "RNM (Registro Nacional Migratório)",
            "fieldtype": "Data",
            "insert_after": "custom_cpf",
        },
    ],
}


def setup_custom_fields():
    # update=True: reaplica opções/propriedades em campos já existentes (não só
    # insere os ausentes). Sem isso, mudar `options` no source nunca chegava ao
    # campo vivo — foi o que barrou matrículas "monthly" quando o Select ainda
    # tinha as opções antigas ("semestral\nannual").
    create_custom_fields(CUSTOM_FIELDS, update=True)
    frappe.db.commit()


if __name__ == "__main__":
    setup_custom_fields()
