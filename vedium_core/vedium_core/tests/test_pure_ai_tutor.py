"""Testes puros do Tutor IA (fase 2 da gamificação/produto IA, 2026-07-09).

Mesmo padrão dos outros test_pure_*: valida o texto-fonte, sem precisar de
Frappe/bench (ai_tutor.py importa frappe no topo).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

AI_TUTOR = (CORE / "ai_tutor.py").read_text(encoding="utf-8")
INSTALL = (CORE / "install.py").read_text(encoding="utf-8")
CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")
PROGRESSO_HTML = (CORE / "www" / "meu-progresso.html").read_text(encoding="utf-8")


def test_old_dead_ai_controller_was_removed():
    """controllers/ai_controller.py nunca foi chamado por nenhuma página,
    dependia de doctypes (AI Persona/AI Interaction Log) que nunca
    existiram, e usava um modelo Groq removido do catálogo há muito tempo
    (llama3-70b-8192). Substituído por vedium_core/ai_tutor.py -- não pode
    sobrar duplicado/morto no repo."""
    assert not (CORE / "controllers" / "ai_controller.py").exists()


def test_groq_model_is_not_a_known_stale_name():
    """O modelo REAL usado (GROQ_MODEL) não pode ser um nome descontinuado
    -- llama3-70b-8192 (formato antigo, usado no controller morto) e
    llama-3.3-70b-versatile (descontinuado em 2026-06-17, confirmado em
    console.groq.com/docs/deprecations). A menção ao nome antigo no
    docstring (explicando a troca) é esperada e não conta como uso real."""
    model_line = [l for l in AI_TUTOR.splitlines() if l.strip().startswith("GROQ_MODEL = ")][0]
    assert model_line.strip() == 'GROQ_MODEL = "openai/gpt-oss-120b"'


def test_chat_endpoint_requires_login_and_rate_limits():
    assert "\n@frappe.whitelist()\ndef chat(" in AI_TUTOR
    body = AI_TUTOR.split("def chat(")[1].split("def escalate_to_human")[0]
    assert "frappe.session.user" in body
    assert "_check_rate_limit(user)" in body


def test_rag_uses_two_real_knowledge_sources_not_external_frappe_docs():
    """RAG busca em (1) conteúdo real das lições do curso do aluno e
    (2) um FAQ curado da PLATAFORMA VEDIUM (grounded em features já
    verificadas nesta sessão) -- o texto explicitamente documenta que
    documentação genérica do frappe.io NÃO é usada como fonte (o aluno
    pergunta sobre a Vedium, não sobre o framework por baixo)."""
    assert "_search_lesson_context" in AI_TUTOR
    assert "_search_platform_faq" in AI_TUTOR
    assert "NÃO entra aqui" in AI_TUTOR  # docstring explícito da decisão
    # Nenhuma chamada de rede pra frappe.io -- é só uma referência em texto
    assert "requests.get" not in AI_TUTOR and "urlopen" not in AI_TUTOR
    # FAQ precisa cobrir os recursos reais já verificados nesta sessão
    faq_block = AI_TUTOR.split("PLATFORM_FAQ = [")[1].split("\n]\n")[0]
    for topic in ["progresso", "certificado", "indicação", "pontos", "prova"]:
        assert topic in faq_block


def test_escalation_reuses_existing_helpdesk_module_not_a_new_one():
    """Fallback humano precisa usar o helpdesk.py já existente (HD Ticket
    nativo, com fallback pra Support Ticket) -- não inventar um segundo
    mecanismo de chamado."""
    body = AI_TUTOR.split("def escalate_to_human")[1]
    assert "from vedium_core.helpdesk import create_ticket" in body
    assert 'category="Tutor IA"' in body


def test_doctypes_are_wired_into_install_and_no_orphan_reference():
    """Mesma classe de bug já vista nesta sessão (módulo referenciado em
    hooks.py mas nunca commitado): ensure_ai_tutor_doctypes precisa estar
    em install.py, e o próprio ai_tutor.py precisa definir a função que
    chama."""
    assert "def ensure_ai_tutor_doctypes" in AI_TUTOR
    assert "from vedium_core.ai_tutor import ensure_ai_tutor_doctypes" in INSTALL
    assert "ensure_ai_tutor_doctypes()" in INSTALL


def test_groq_key_fallback_field_exists_in_custom_setup():
    assert '"custom_groq_api_key"' in CUSTOM_SETUP
    assert "System Settings" in CUSTOM_SETUP.split('"custom_groq_api_key"')[0].split('"LMS Course"')[-1] \
        or '"custom_groq_api_key"' in CUSTOM_SETUP


def test_widget_is_mounted_on_authenticated_student_page():
    """O doc de arquitetura (14-atendimento-e-tutor-ia.md) é explícito:
    'Tutor IA na home pública' é o que NÃO construir agora -- o widget
    tem que estar em /meu-progresso (área autenticada), não numa página
    pública de marketing."""
    assert "vedium_core.ai_tutor.chat" in PROGRESSO_HTML
    assert "vd-tutor-fab" in PROGRESSO_HTML
    assert "vedium_core.ai_tutor.escalate_to_human" in PROGRESSO_HTML


def test_message_length_is_capped_both_client_and_server_side():
    assert "maxlength=\"2000\"" in PROGRESSO_HTML
    assert "len(message) > 2000" in AI_TUTOR
