"""Testes puros da automação de ausência (P2, 2026-08-08).

A captura de presença é NATIVA (Registro de Aula Vedium); aqui só validamos o
detector de faltas consecutivas que alimenta o fluxo A09 do kit Brevo.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

ATTENDANCE = (CORE / "attendance_events.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")
CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")


def test_module_is_valid_python():
    ast.parse(ATTENDANCE)


def test_reuses_native_attendance_not_a_new_one():
    """Lê os doctypes NATIVOS de presença (Registro de Aula Vedium / Aluno da
    Aula Vedium) — não cria um sistema de presença paralelo."""
    assert "tabRegistro de Aula Vedium" in ATTENDANCE
    assert "tabAluno da Aula Vedium" in ATTENDANCE
    assert "status_presenca" in ATTENDANCE


def test_absence_definition_and_threshold():
    assert '"Ausente"' in ATTENDANCE and '"Falta nao justificada"' in ATTENDANCE
    assert "ABSENCE_THRESHOLD = 3" in ATTENDANCE
    # Só conta registros finalizados (não Rascunho)
    assert "!= 'Rascunho'" in ATTENDANCE


def test_alert_is_idempotent_by_enrollment_marker():
    """Alerta UMA vez por sequência: dispara no limite exato e grava a data da
    aula em custom_absence_alerted_on (não repete em aulas já processadas)."""
    assert "custom_absence_alerted_on" in ATTENDANCE
    assert "streak != ABSENCE_THRESHOLD" in ATTENDANCE
    assert 'custom_absence_alerted_on' in CUSTOM_SETUP
    # respeita o gate de dono do ciclo de vida (Brevo) para o e-mail interino
    assert "lifecycle_owned_by_brevo" in ATTENDANCE
    assert 'student_absent' in ATTENDANCE


def test_scheduled_daily():
    assert "vedium_core.attendance_events.detect_absent_students" in HOOKS
