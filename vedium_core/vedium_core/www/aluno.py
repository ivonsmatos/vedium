"""Home do Aluno Vedium (P4 — Experiência do aluno).

Página AGREGADORA (não duplica o LMS nativo): reúne numa só tela a próxima aula
ao vivo + Meet, progresso, presença (do Registro de Aula), status de pagamento e
atalhos (LMS/Raven/suporte/materiais). O curso/lições em si continuam no LMS
nativo — esta página LINKA pra ele. Server-rendered, logada.

Cada seção é defensiva: se um dado faltar, a seção some, mas a página nunca 500.
"""

import frappe
from frappe.utils import today

no_cache = 1

RAVEN_URL = "https://app.vediums.com/raven"
SUPPORT_URL = "https://vediums.com/contato"
LMS_COURSES_URL = "https://app.vediums.com/lms/courses"
BILLING_PORTAL_URL = (
    "https://app.vediums.com/api/method/"
    "vedium_core.stripe_billing.billing_portal_redirect"
)
# Status de presença que contam como "compareceu".
_ATTENDED = ("Presente", "Atrasado", "Saida antecipada")


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/aluno"
        raise frappe.Redirect

    user = frappe.session.user
    context.no_cache = 1
    context.title = "Minha Jornada | Vedium"
    context.description = "Sua jornada de aprendizado na Vedium."
    context.canonical_url = "https://app.vediums.com/aluno"
    context.student_name = (
        frappe.db.get_value("User", user, "first_name")
        or frappe.db.get_value("User", user, "full_name")
        or ""
    )
    context.enrollments = _safe(_enrollments, user, default=[])
    context.next_class = _safe(_next_live_class, user)
    context.attendance = _safe(_attendance, user)
    context.payment = _safe(_payment_status, user, default={"ok": True, "failed": False})
    context.raven_url = RAVEN_URL
    context.support_url = SUPPORT_URL
    context.lms_url = LMS_COURSES_URL
    context.billing_url = BILLING_PORTAL_URL
    return context


def _safe(fn, user, default=None):
    try:
        return fn(user)
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Vedium.aluno.{fn.__name__}")
        return default


def _enrollments(user):
    rows = frappe.get_all(
        "LMS Enrollment",
        filters={"member": user},
        fields=["course", "progress", "custom_vedium_status"],
        limit_page_length=0,
    )
    out = []
    for r in rows:
        title = frappe.db.get_value("LMS Course", r.course, "title") or r.course
        out.append(
            {
                "course": r.course,
                "title": title,
                "progress": int(r.progress or 0),
                "status": r.custom_vedium_status or "Active",
            }
        )
    return out


def _student_batches(user):
    return frappe.get_all(
        "LMS Batch Enrollment", filters={"member": user}, pluck="batch"
    )


def _next_live_class(user):
    batches = _student_batches(user)
    if not batches:
        return None
    rows = frappe.get_all(
        "LMS Live Class",
        filters={"batch_name": ["in", batches], "date": [">=", today()]},
        fields=["title", "date", "time", "join_url", "duration"],
        order_by="date asc, time asc",
        limit_page_length=1,
    )
    if not rows:
        return None
    c = rows[0]
    try:
        weekday = frappe.utils.format_datetime(c.date, "EEEE")
    except Exception:
        weekday = ""
    return {
        "title": c.title,
        "date": frappe.utils.formatdate(c.date, "dd/MM"),
        "weekday": weekday,
        "time": str(c.time)[:5] if c.time else "",
        "join_url": c.join_url,
        "duration": c.duration,
    }


def _attendance(user):
    rows = frappe.db.sql(
        """
        SELECT c.status_presenca AS status, COUNT(*) AS n
        FROM `tabAluno da Aula Vedium` c
        JOIN `tabRegistro de Aula Vedium` r ON r.name = c.parent
        WHERE c.aluno = %s AND COALESCE(r.status_registro, '') != 'Rascunho'
        GROUP BY c.status_presenca
        """,
        (user,),
        as_dict=True,
    )
    total = sum(x.n for x in rows)
    if not total:
        return None
    attended = sum(x.n for x in rows if x.status in _ATTENDED)
    return {"pct": int(round(attended * 100 / total)), "attended": attended, "total": total}


def _payment_status(user):
    failed = frappe.db.exists(
        "LMS Enrollment", {"member": user, "custom_payment_failed_on": ["is", "set"]}
    )
    return {"ok": not failed, "failed": bool(failed)}
