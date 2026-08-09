"""Testes puros do pipeline comercial (P3, 2026-08-08).

Foco: os formulários do site criam o lead no estágio/origem CORRETOS e o insert
não falha mais por link quebrado (bug: source = "Website <intent>" inexistente).
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

PIPELINE = (CORE / "crm_pipeline.py").read_text(encoding="utf-8")
FUNNEL = (CORE / "public_funnel.py").read_text(encoding="utf-8")
BREVO = (CORE / "brevo.py").read_text(encoding="utf-8")
INSTALL = (CORE / "install.py").read_text(encoding="utf-8")
CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_pipeline_module_is_valid_python():
    ast.parse(PIPELINE)


def test_source_is_validated_not_a_broken_link():
    """O bug antigo era source = f\"Website {intent_label}\" (registro
    inexistente) → LinkValidationError → lead perdido. Agora resolve para uma
    origem VÁLIDA com fallback garantido."""
    assert 'f"Website {intent_label}"' not in FUNNEL
    assert "resolve_lead_source(intent)" in FUNNEL
    assert "resolve_lead_status(intent)" in FUNNEL
    assert 'FALLBACK_LEAD_SOURCE = "Website"' in PIPELINE
    # ensure cria a origem pelo campo de autoname correto (field:source_name)
    assert '"source_name"' in PIPELINE


def test_form_lead_enters_at_new_stage():
    assert 'DEFAULT_LEAD_STATUS = "New"' in PIPELINE
    assert "lead.status = status" in FUNNEL


def test_course_interest_is_structured_and_synced_to_brevo():
    """Curso de interesse vira campo estruturado (custom_curso_interesse) e
    alimenta o atributo COURSE do Brevo na nutrição de lead."""
    assert "custom_curso_interesse" in CUSTOM_SETUP
    assert "lead.custom_curso_interesse = course" in FUNNEL
    lead_attrs = BREVO.split("def process_lead_snapshot", 1)[1].split("def ", 1)[0]
    assert '"COURSE": snapshot.get("course")' in lead_attrs


def test_pipeline_seed_is_wired_in_after_migrate():
    assert "_ensure_crm_pipeline()" in INSTALL
    assert "from vedium_core.crm_pipeline import ensure_crm_pipeline" in INSTALL


def test_new_lead_creates_commercial_task():
    """Lead novo → tarefa (ToDo) de primeiro contato. O e-mail ao lead é do
    Brevo (A01); aqui é o trabalho interno do time."""
    assert "def on_lead_created(doc, method=None)" in PIPELINE
    block = PIPELINE.split("def on_lead_created", 1)[1].split("def alert_stale_leads", 1)[0]
    assert '"doctype": "ToDo"' in block
    assert '"reference_type": "CRM Lead"' in block
    # destino configurável, com fallback pra coordenação
    assert 'DEFAULT_COMMERCIAL_EMAIL = "contato@vediums.com"' in PIPELINE
    assert "VEDIUM_COMMERCIAL_EMAIL" in PIPELINE
    # wired no after_insert (junto do brevo, não no lugar dele)
    assert '"vedium_core.crm_pipeline.on_lead_created"' in HOOKS
    assert '"vedium_core.brevo.on_crm_lead"' in HOOKS


def test_stale_lead_alert_is_idempotent_and_scheduled():
    """Lead em 'New' há +24h sem contato → alerta a coordenação uma vez."""
    assert "def alert_stale_leads(" in PIPELINE
    block = PIPELINE.split("def alert_stale_leads", 1)[1]
    assert '"status": "New"' in block
    assert '"custom_stale_alerted_on": ["is", "not set"]' in block
    assert "custom_stale_alerted_on" in CUSTOM_SETUP
    assert "vedium_core.crm_pipeline.alert_stale_leads" in HOOKS
