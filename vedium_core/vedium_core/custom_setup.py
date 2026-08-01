import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

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
        # Onboarding wizard (/onboarding) — ver vedium_core/onboarding.py
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
    # Chaves VAPID pra Web Push — ver vedium_core/push_notifications.py
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
    # Extensões Vedium ao certificado NATIVO do LMS (LMS Certificate).
    # Antes existia um doctype custom homônimo que sequestrava o nativo; foi
    # removido. Estas duas colunas dão suporte à verificação pública em
    # /certificado (api.issue_certificate / verify_certificate).
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
    # Gate entre níveis do curso PLE (Básico -> Intermediário -> Avançado):
    # se setado, o aluno só enxerga o conteúdo deste curso depois de ter um
    # LMS Certificate emitido pro curso pré-requisito. Ver vedium_core/ple_gating.py.
    "LMS Course": [
        {
            "fieldname": "custom_prerequisite_course",
            "label": "Curso pré-requisito (gate de nível)",
            "fieldtype": "Link",
            "options": "LMS Course",
            "insert_after": "category",
        },
        # IDs de preço Stripe para assinaturas recorrentes.
        # Cadastre os Price IDs em app.vediums.com/desk para cada curso.
        # Formato: price_XXXXXXXXXXXXXXXXXXXX (ID do Stripe)
        {
            "fieldname": "custom_stripe_price_id_semestral",
            "label": "Stripe Price ID — Semestral (6 meses)",
            "fieldtype": "Data",
            "insert_after": "custom_prerequisite_course",
            "description": "Price ID do Stripe para o plano semestral (mode=subscription). Ex: price_1AbCdEfGhIjK",
        },
        {
            "fieldname": "custom_stripe_price_id_anual",
            "label": "Stripe Price ID — Anual (12 meses)",
            "fieldtype": "Data",
            "insert_after": "custom_stripe_price_id_semestral",
            "description": "Price ID do Stripe para o plano anual (mode=subscription). Ex: price_1AbCdEfGhIjK",
        },
    ],
    # Fonte da verdade Vedium para acesso do aluno.
    # O DocType nativo "LMS Enrollment" do LMS não possui um campo status
    # canônico. Estes campos são usados por trial, cancelamento e pela futura
    # sincronização de membros em canais de comunicação (Raven/Vedium).
    "LMS Enrollment": [
        {
            "fieldname": "custom_vedium_status",
            "label": "Status Vedium",
            "fieldtype": "Select",
            "options": "Active\nTrial\nSuspended\nCancelled\nEnded\nExpired",
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
        # Rastreamento de assinatura recorrente Stripe
        {
            "fieldname": "custom_stripe_subscription_id",
            "label": "Stripe Subscription ID",
            "fieldtype": "Data",
            "insert_after": "custom_trial_end",
            "read_only": 1,
            "description": "ID da assinatura no Stripe (sub_XXXX). Preenchido automaticamente pelo webhook.",
        },
        {
            "fieldname": "custom_billing_period",
            "label": "Plano contratado",
            "fieldtype": "Select",
            "options": "monthly\nsemestral\nanual",
            "insert_after": "custom_stripe_subscription_id",
            "read_only": 1,
        },
        {
            "fieldname": "custom_contract_start",
            "label": "Início do contrato",
            "fieldtype": "Datetime",
            "insert_after": "custom_billing_period",
            "read_only": 1,
        },
        {
            "fieldname": "custom_contract_end",
            "label": "Fim da permanência mínima",
            "fieldtype": "Datetime",
            "insert_after": "custom_contract_start",
            "read_only": 1,
            "description": "Data calculada automaticamente: semestral = +6 meses, anual = +12 meses.",
        },
        {
            "fieldname": "custom_payment_failure_since",
            "label": "Falha de pagamento desde",
            "fieldtype": "Datetime",
            "insert_after": "custom_contract_end",
            "read_only": 1,
            "description": "Preenchido no primeiro invoice.payment_failed. Limpo quando invoice.paid.",
        },
        {
            "fieldname": "custom_cancellation_requested_on",
            "label": "Cancelamento solicitado em",
            "fieldtype": "Datetime",
            "insert_after": "custom_payment_failure_since",
            "read_only": 1,
            "description": "Se solicitado antes da permanência mínima, cancela ao fim do contrato.",
        },
        {
            "fieldname": "custom_last_invoice_id",
            "label": "Último invoice Stripe",
            "fieldtype": "Data",
            "insert_after": "custom_cancellation_requested_on",
            "read_only": 1,
            "description": "ID do último invoice processado — usado para idempotência de webhooks.",
        },
    ],
    # Documentos brasileiros do professor/funcionário — o Employee nativo do
    # Frappe HR não tem CPF nem RNM (só "Passport Number", que não é o
    # documento correto pra estrangeiro com registro migratório). Ver
    # scripts/migrations/oneshot/hire_guadalupe_hr_record.py.
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
    for doctype, field_list in CUSTOM_FIELDS.items():
        for field in field_list:
            if frappe.db.exists(
                "Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}
            ):
                continue
            create_custom_field(doctype, field)

    frappe.db.commit()


if __name__ == "__main__":
    setup_custom_fields()
