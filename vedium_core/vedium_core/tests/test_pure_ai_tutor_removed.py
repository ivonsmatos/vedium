"""Guardas para manter o Tutor IA desativado.

O widget anterior travava a área do aluno. Estes testes evitam que endpoint,
frontend ou configuração Groq voltem sem uma decisão explícita de produto.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

INSTALL = (CORE / "install.py").read_text(encoding="utf-8")
CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")
PROGRESSO_HTML = (CORE / "www" / "meu-progresso.html").read_text(encoding="utf-8")
PYPROJECT = (ROOT / "vedium_core" / "pyproject.toml").read_text(encoding="utf-8")


def test_ai_tutor_backend_was_removed():
    assert not (CORE / "ai_tutor.py").exists()
    assert "vedium_core.ai_tutor" not in INSTALL
    assert "ensure_ai_tutor_doctypes" not in INSTALL


def test_ai_tutor_widget_was_removed_from_student_progress_page():
    forbidden = [
        "vd-tutor",
        "Tutor IA",
        "vedium_core.ai_tutor.chat",
        "vedium_core.ai_tutor.escalate_to_human",
    ]
    for token in forbidden:
        assert token not in PROGRESSO_HTML


def test_groq_config_and_dependency_were_removed():
    forbidden = [
        "groq",
        "custom_groq_api_key",
        "custom_vedium_ai_tutor_model",
    ]
    for token in forbidden:
        assert token not in CUSTOM_SETUP
        assert token not in PYPROJECT


def test_migrate_cleans_old_ai_tutor_artifacts():
    assert "def _remove_ai_tutor_artifacts" in INSTALL
    for token in [
        "System Settings-custom_groq_api_key",
        "System Settings-custom_vedium_ai_tutor_model",
        "AI Tutor Session",
        "AI Tutor Message",
    ]:
        assert token in INSTALL
