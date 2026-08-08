# -*- coding: utf-8 -*-
"""Health check E2E pós-deploy (Bloco 6 do Plano de Fechamento).

Substitui o smoke test baseado só em HTTP 200: verifica de fato as
integrações críticas e falha o deploy quando alguma delas está quebrada.

Rodar:
    bench --site app.vediums.com execute vedium_core.health.run

Semântica de saída:
  - `critical` falho  -> levanta SystemExit(1)  => o step do deploy falha.
  - `warning` falho   -> imprime AVISO, não derruba o deploy.

Cada check é isolado: exceção dentro de um check vira FAIL daquele check,
nunca aborta a bateria inteira (senão o primeiro erro esconderia o resto).
"""

import time

import frappe


# ---------------------------------------------------------------------------
# Infra de execução
# ---------------------------------------------------------------------------

class _Results:
    def __init__(self):
        self.rows = []

    def add(self, name, ok, detail="", critical=True):
        self.rows.append(
            {"name": name, "ok": bool(ok), "detail": detail, "critical": critical}
        )

    def check(self, name, fn, critical=True):
        try:
            ok, detail = fn()
        except Exception as exc:  # noqa: BLE001 - queremos o motivo, não o traceback
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        self.add(name, ok, detail, critical)


def run():
    results = _Results()

    results.check("db.connection", _check_db)
    results.check("db.write_rollback", _check_db_write_rollback)
    results.check("scheduler.enabled", _check_scheduler)
    results.check("queue.enqueue", _check_queue, critical=False)
    results.check("stripe.config", _check_stripe_config)
    results.check("stripe.catalog", _check_stripe_catalog, critical=False)
    results.check("lms.doctypes", _check_lms)
    results.check("crm.doctype", _check_crm, critical=False)
    results.check("raven.setup", _check_raven, critical=False)
    results.check("raven.realtime", _check_raven_realtime, critical=False)
    results.check("helpdesk.setup", _check_helpdesk, critical=False)
    results.check("brevo.config", _check_brevo, critical=False)
    results.check("email.outgoing", _check_email, critical=False)
    results.check("email.queue_backlog", _check_email_backlog, critical=False)

    return _report(results)


def _report(results):
    failed_critical = []
    failed_warning = []

    print("\n=== Vedium health check ===")
    for row in results.rows:
        if row["ok"]:
            status = "OK  "
        elif row["critical"]:
            status = "FAIL"
            failed_critical.append(row)
        else:
            status = "WARN"
            failed_warning.append(row)
        detail = f" | {row['detail']}" if row["detail"] else ""
        print(f"  [{status}] {row['name']}{detail}")

    print(
        f"\nResumo: {len(results.rows)} checks | "
        f"{len(failed_critical)} falha(s) crítica(s) | "
        f"{len(failed_warning)} aviso(s)"
    )

    if failed_critical:
        names = ", ".join(row["name"] for row in failed_critical)
        print(f"\nDEPLOY DEVE FALHAR — checks críticos quebrados: {names}")
        raise SystemExit(1)

    print("\nTudo crítico saudável.")
    return {"ok": True, "warnings": len(failed_warning)}


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def _check_db():
    value = frappe.db.sql("SELECT 1")[0][0]
    count = frappe.db.count("User")
    return value == 1, f"{count} usuários"


def _check_db_write_rollback():
    """Prova que o banco aceita escrita, sem deixar lixo: grava e desfaz."""
    key = f"vedium_health_probe_{int(time.time())}"
    frappe.db.savepoint("vedium_health")
    try:
        doc = frappe.get_doc({
            "doctype": "ToDo",
            "description": f"health check probe {key}",
            "status": "Cancelled",
        })
        doc.insert(ignore_permissions=True)
        wrote = bool(doc.name)
    finally:
        frappe.db.rollback(save_point="vedium_health")
    return wrote, "escrita + rollback ok"


def _check_scheduler():
    if frappe.utils.scheduler.is_scheduler_inactive():
        return False, "scheduler inativo"
    return True, "ativo"


def _check_queue():
    job = frappe.enqueue("frappe.ping", queue="short")
    return bool(job), f"job enfileirado ({getattr(job, 'id', '?')})"


def _check_stripe_config():
    key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not key:
        return False, "STRIPE_SECRET_KEY ausente"
    mode = "live" if str(key).startswith("sk_live") else (
        "test" if str(key).startswith("sk_test") else "desconhecido"
    )
    secret = frappe.conf.get("STRIPE_WEBHOOK_SECRET") or frappe.conf.get(
        "stripe_webhook_secret"
    )
    if not secret:
        return False, f"chave {mode}, mas STRIPE_WEBHOOK_SECRET ausente"
    return True, f"chave {mode} + webhook secret presentes"


def _check_stripe_catalog():
    """Conta preços cadastrados no Frappe. Não chama a API da Stripe (o
    health check roda em todo deploy; bater na Stripe toda vez é caro e
    sujeito a rate limit — a auditoria completa é feita pelo workflow
    dedicado de catálogo)."""
    if not frappe.db.exists("DocType", "Vedium Course Price"):
        return False, "DocType 'Vedium Course Price' ausente"
    total = frappe.db.count("Vedium Course Price")
    return total > 0, f"{total} preços cadastrados"


def _check_lms():
    missing = [
        dt for dt in ("LMS Course", "LMS Enrollment", "LMS Batch")
        if not frappe.db.exists("DocType", dt)
    ]
    if missing:
        return False, f"DocTypes ausentes: {missing}"
    courses = frappe.db.count("LMS Course", {"published": 1})
    enrollments = frappe.db.count("LMS Enrollment")
    return True, f"{courses} cursos publicados, {enrollments} matrículas"


def _check_crm():
    if not frappe.db.exists("DocType", "CRM Lead"):
        return False, "DocType 'CRM Lead' ausente"
    return True, f"{frappe.db.count('CRM Lead')} leads"


def _check_raven():
    required = ("Raven User", "Raven Workspace", "Raven Channel", "Raven Channel Member")
    missing = [dt for dt in required if not frappe.db.exists("DocType", dt)]
    if missing:
        return False, f"DocTypes ausentes: {missing}"
    if not frappe.db.exists("Raven Workspace", "Vedium"):
        return False, "workspace 'Vedium' ausente"
    channels = frappe.db.count("Raven Channel", {"workspace": "Vedium"})
    return channels > 0, f"{channels} canais no workspace Vedium"


def _check_raven_realtime():
    """O bundle do Raven precisa do patch 'força WebSocket' senão o chat em tempo
    real quebra atrás do Cloudflare. O after_migrate reaplica; aqui só detectamos
    regressão (ex.: se o patch falhou por permissão)."""
    from vedium_core.raven_realtime import is_realtime_patched

    if is_realtime_patched():
        return True, "patch websocket presente no bundle"
    return False, "bundle do Raven SEM patch websocket — realtime pode quebrar"


def _check_helpdesk():
    if not frappe.db.exists("DocType", "HD Ticket"):
        return False, "DocType 'HD Ticket' ausente"
    from vedium_core.helpdesk import DEFAULT_TEAM

    if frappe.db.exists("DocType", "HD Team") and not frappe.db.exists(
        "HD Team", DEFAULT_TEAM
    ):
        return False, f"time '{DEFAULT_TEAM}' ausente"
    return True, f"{frappe.db.count('HD Ticket')} tickets"


def _check_brevo():
    from vedium_core import brevo

    if not brevo.is_enabled():
        return False, "desabilitado ou BREVO_API_KEY ausente"
    result = brevo.test_connection()
    return bool(result), f"conexão ok ({str(result)[:80]})"


def _check_email():
    accounts = frappe.get_all(
        "Email Account",
        filters={"enable_outgoing": 1},
        fields=["name", "email_id"],
        limit_page_length=5,
    )
    if not accounts:
        return False, "nenhuma conta de saída habilitada"
    return True, f"{len(accounts)} conta(s): {[a.email_id for a in accounts]}"


def _check_email_backlog():
    """Fila acumulada indica envio travado (SMTP/OAuth quebrado)."""
    pending = frappe.db.count("Email Queue", {"status": "Not Sent"})
    errors = frappe.db.count("Email Queue", {"status": "Error"})
    ok = pending < 100 and errors < 20
    return ok, f"{pending} pendentes, {errors} com erro"
