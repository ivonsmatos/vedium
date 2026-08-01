# -*- coding: utf-8 -*-
"""
Vedium — Trial de 7 dias para cursos pagos

Como funciona:
    1. Aluno solicita trial via API (start_trial):
       - Cria LMS Enrollment com custom_vedium_status="Trial"
       - Registra data de início em Vedium Trial (se DocType existir) ou
         via User Permission custom
       - Trial expira automaticamente via scheduler diário

    2. Scheduler (expire_trials) roda 1x/dia:
       - Busca enrollments Trial com mais de 7 dias
       - Move para "Expired" ou remove acesso

    3. Conversão: aluno faz checkout → enrollment vira "Active"

Integração no hooks.py:
    scheduler_events = {
        "daily": ["vedium_core.trial.expire_trials"]
    }
"""

from datetime import datetime, timedelta

import frappe
from frappe import _

from vedium_core.exceptions import EnrollmentError, PaymentError

TRIAL_DAYS = 7
TRIAL_STATUS = "Trial"
ENROLLED_STATUS = "Active"
EXPIRED_STATUS = "Expired"
STATUS_FIELD = "custom_vedium_status"


# ──────────────────────────────────────────────
# API pública
# ──────────────────────────────────────────────

@frappe.whitelist()
def start_trial(course: str):
    """
    Inicia um trial de 7 dias para o curso especificado.

    Regras:
    - Usuário deve estar logado
    - Curso deve existir e ser publicado
    - Usuário não pode ter matrícula ativa nem trial em andamento
    - Só um trial por curso por usuário (para sempre)
    """
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para iniciar o período de avaliação"), EnrollmentError)

    # Valida o curso
    if not frappe.db.exists("LMS Course", {"name": course, "published": 1}):
        frappe.throw(_("Curso não encontrado ou não disponível"), EnrollmentError)

    # Verifica se já tem matrícula (qualquer status)
    existing = frappe.db.get_value(
        "LMS Enrollment",
        {"member": user, "course": course},
        ["name", STATUS_FIELD],
        as_dict=True,
    )
    if existing:
        existing_status = existing.get(STATUS_FIELD) or ENROLLED_STATUS
        if existing_status in (ENROLLED_STATUS, TRIAL_STATUS):
            frappe.throw(
                _("Você já possui acesso ativo a este curso"),
                EnrollmentError,
            )
        if existing_status == EXPIRED_STATUS:
            frappe.throw(
                _("Seu período de avaliação deste curso já foi utilizado"),
                EnrollmentError,
            )

    # Verifica se o curso permite trial
    allows_trial = frappe.db.get_value("LMS Course", course, "custom_allow_trial")
    if allows_trial is not None and not allows_trial:
        frappe.throw(_("Este curso não possui período de avaliação gratuito"), EnrollmentError)

    # Cria a matrícula trial
    trial_start = datetime.now()
    trial_end = trial_start + timedelta(days=TRIAL_DAYS)

    enrollment = frappe.get_doc({
        "doctype": "LMS Enrollment",
        "member": user,
        "course": course,
        STATUS_FIELD: TRIAL_STATUS,
        "custom_vedium_status_changed_on": trial_start,
        "custom_vedium_status_reason": "Trial iniciado pelo aluno",
        "custom_trial_start": trial_start,
        "custom_trial_end": trial_end,
        "member_type": "Student",
    })
    enrollment.insert(ignore_permissions=True)
    frappe.db.commit()

    # Notifica o aluno
    _send_trial_welcome(user, course, trial_end)

    return {
        "status": "trial_started",
        "enrollment": enrollment.name,
        "trial_end": trial_end.strftime("%d/%m/%Y"),
        "days": TRIAL_DAYS,
        "message": _(
            "Seu período de avaliação de {0} dias foi iniciado. "
            "Experimente à vontade até {1}."
        ).format(TRIAL_DAYS, trial_end.strftime("%d/%m/%Y")),
    }


@frappe.whitelist()
def get_trial_status(course: str):
    """Retorna o status do trial do usuário para o curso dado."""
    user = frappe.session.user
    if user == "Guest":
        return {"has_trial": False, "can_start": False}

    enrollment = frappe.db.get_value(
        "LMS Enrollment",
        {"member": user, "course": course},
        ["name", STATUS_FIELD, "custom_trial_start", "custom_trial_end"],
        as_dict=True,
    )

    if not enrollment:
        # Verifica quantos trials o usuário já usou (limite: 1 trial ativo por vez)
        active_trials = frappe.db.count(
            "LMS Enrollment",
            {"member": user, STATUS_FIELD: TRIAL_STATUS},
        )
        return {
            "has_trial": False,
            "can_start": True,
            "active_trials": active_trials,
        }

    days_left = None
    if enrollment.custom_trial_end:
        delta = enrollment.custom_trial_end - datetime.now()
        days_left = max(0, delta.days)

    return {
        "has_trial": enrollment.get(STATUS_FIELD) == TRIAL_STATUS,
        "status": enrollment.get(STATUS_FIELD) or ENROLLED_STATUS,
        "enrollment": enrollment.name,
        "days_left": days_left,
        "trial_end": enrollment.custom_trial_end.strftime("%d/%m/%Y") if enrollment.custom_trial_end else None,
        "can_start": False,
    }


# ──────────────────────────────────────────────
# Scheduler — roda 1x/dia via hooks.py
# ──────────────────────────────────────────────

def expire_trials():
    """
    Expira enrollments Trial com mais de TRIAL_DAYS dias.
    Chamado pelo scheduler diário do Frappe.

    Adicionar em hooks.py:
        scheduler_events = {
            "daily": ["vedium_core.trial.expire_trials"]
        }
    """
    now = datetime.now()
    expired_cutoff = now - timedelta(days=TRIAL_DAYS)

    # Busca trials vencidos (usa campo custom_trial_start ou fallback em creation)
    expired = frappe.get_all(
        "LMS Enrollment",
        filters={STATUS_FIELD: TRIAL_STATUS},
        fields=["name", "member", "course", "custom_trial_start", "creation"],
    )

    count = 0
    for e in expired:
        trial_start = e.custom_trial_start or e.creation
        if not trial_start:
            continue

        # Normaliza para datetime
        if not isinstance(trial_start, datetime):
            try:
                trial_start = datetime.fromisoformat(str(trial_start))
            except (ValueError, TypeError):
                continue

        if trial_start <= expired_cutoff:
            try:
                # Document.save é intencional: dispara os hooks de LMS
                # Enrollment, mantendo Raven e Brevo sincronizados com a
                # expiração do trial. db.set_value ignorava esses hooks.
                enrollment = frappe.get_doc("LMS Enrollment", e.name)
                enrollment.update(
                    {
                        STATUS_FIELD: EXPIRED_STATUS,
                        "custom_vedium_status_changed_on": now,
                        "custom_vedium_status_reason": "Trial expirado automaticamente",
                    }
                )
                enrollment.save(ignore_permissions=True)
                count += 1
                _send_trial_expiry_notice(e.member, e.course)
            except Exception as ex:
                frappe.log_error(
                    f"Erro ao expirar trial {e.name}: {ex}",
                    "Vedium.Trial.expire",
                )

    if count:
        frappe.db.commit()
        frappe.log_error(  # usa log_error como auditoria (não é um erro)
            f"expire_trials: {count} trial(s) expirado(s) em {now.strftime('%Y-%m-%d')}",
            "Vedium.Trial.audit",
        )

    return count


# ──────────────────────────────────────────────
# Helpers internos
# ──────────────────────────────────────────────

def _send_trial_welcome(user: str, course: str, trial_end: datetime):
    """Envia e-mail de boas-vindas ao trial."""
    try:
        course_title = frappe.db.get_value("LMS Course", course, "title") or course
        frappe.sendmail(
            recipients=[user],
            subject=_("🎓 Seu período de avaliação foi iniciado — {0}").format(course_title),
            message=_(
                "<p>Olá!</p>"
                "<p>Seu período de avaliação gratuito de <strong>{0} dias</strong> "
                "para o curso <strong>{1}</strong> foi iniciado.</p>"
                "<p>Você tem acesso completo até <strong>{2}</strong>. "
                "Aproveite ao máximo!</p>"
                "<p>Se gostar da experiência, assine o plano e continue aprendendo sem interrupções.</p>"
                "<p>Bons estudos! 🌍<br>Equipe Vedium</p>"
            ).format(TRIAL_DAYS, course_title, trial_end.strftime("%d/%m/%Y")),
            now=frappe.flags.in_test,
        )
    except Exception as ex:
        frappe.log_error(f"Erro ao enviar e-mail de trial para {user}: {ex}", "Vedium.Trial.welcome")


def _send_trial_expiry_notice(user: str, course: str):
    """Notifica o aluno que o trial expirou."""
    try:
        course_title = frappe.db.get_value("LMS Course", course, "title") or course
        frappe.sendmail(
            recipients=[user],
            subject=_("⏰ Seu período de avaliação de {0} expirou").format(course_title),
            message=_(
                "<p>Olá!</p>"
                "<p>Seu período de avaliação gratuito do curso <strong>{0}</strong> chegou ao fim.</p>"
                "<p>Para continuar aprendendo, <a href='https://vediums.com/planos'>assine um plano</a> "
                "e retome de onde parou.</p>"
                "<p>Qualquer dúvida, fale com a gente: "
                "<a href='mailto:contato@vediums.com'>contato@vediums.com</a></p>"
                "<p>Equipe Vedium 🌍</p>"
            ).format(course_title),
            now=frappe.flags.in_test,
        )
    except Exception as ex:
        frappe.log_error(f"Erro ao enviar e-mail de expiração de trial para {user}: {ex}", "Vedium.Trial.expiry")
