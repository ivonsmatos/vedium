"""Testes puros de P5 (relatório de evolução) e P6 (retenção), 2026-08-09."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

REPORT = (CORE / "pedagogical_report.py").read_text(encoding="utf-8")
RETENTION = (CORE / "retention_events.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_modules_are_valid_python():
    ast.parse(REPORT)
    ast.parse(RETENTION)


# ---- P5 ----

def test_evolution_summary_uses_native_capture():
    assert "tabAluno da Aula Vedium" in REPORT
    assert "!= 'Rascunho'" in REPORT
    for skill in ("participacao", "compreensao", "producao_oral", "producao_escrita", "pronuncia"):
        assert skill in REPORT


def test_monthly_evolution_emits_event_and_is_scheduled():
    assert "def emit_monthly_evolution(" in REPORT
    assert '"monthly_evolution"' in REPORT
    # feeds A08-05 params
    assert "attendance_rate" in REPORT and "monthly_report_url" in REPORT
    # gate anti-duplicação com o Brevo p/ o e-mail interino
    assert "lifecycle_owned_by_brevo" in REPORT
    # cron mensal (dia 1)
    assert '"0 11 1 * *": ["vedium_core.pedagogical_report.emit_monthly_evolution"]' in HOOKS


# ---- P6 ----

def test_dormant_detection_is_field_free_and_scheduled():
    """Aluno começou e sumiu ~10d (janela sobre last_active), distinto do caso de
    ativação (quem nunca começou)."""
    assert "INACTIVE_DAYS = 10" in RETENTION
    assert "last_active" in RETENTION
    assert '"student_inactive"' in RETENTION
    assert "_has_started" in RETENTION  # exige ter começado
    assert "vedium_core.retention_events.detect_dormant_students" in HOOKS


def test_at_risk_digest_is_weekly_internal():
    assert "def weekly_at_risk_digest(" in RETENTION
    assert "RISK_MAX_PROGRESS" in RETENTION
    assert "frappe.sendmail" in RETENTION  # digest interno pra coordenação
    assert "vedium_core.retention_events.weekly_at_risk_digest" in HOOKS


def test_engaged_reuses_existing_milestone_not_duplicated():
    """Engajado→indicação (A12) reusa o progress_milestone(=100) do gamification,
    não recria um detector."""
    assert "progress_milestone" in RETENTION  # documentado no módulo
