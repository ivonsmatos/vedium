"""Testes puros da Home do Aluno (P4, 2026-08-08).

Página AGREGADORA server-rendered em /aluno — não duplica o LMS nativo (linka
pra ele); reúne próxima aula+Meet, presença (Registro de Aula), pagamento,
progresso e atalhos.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

ALUNO_PY = (CORE / "www" / "aluno.py").read_text(encoding="utf-8")
ALUNO_HTML = (CORE / "www" / "aluno.html").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_controller_is_valid_python():
    ast.parse(ALUNO_PY)


def test_requires_login():
    """Página logada: Guest é redirecionado para o login (com volta pra /aluno)."""
    assert 'frappe.session.user == "Guest"' in ALUNO_PY
    # 302 (temporário) — um 301 no gate de login seria cacheado e prenderia o
    # usuário fora da página depois de logar.
    assert "raise frappe.Redirect(302)" in ALUNO_PY
    assert "/login?redirect-to=/aluno" in ALUNO_PY
    assert "no_cache = 1" in ALUNO_PY


def test_aggregates_native_data_without_duplicating():
    """Agrega dos doctypes nativos: matrícula (progresso), aula ao vivo (join_url
    do Meet), presença (Aluno da Aula Vedium). Linka pro LMS, não recria."""
    assert 'frappe.get_all(\n        "LMS Enrollment"' in ALUNO_PY or '"LMS Enrollment"' in ALUNO_PY
    assert '"LMS Live Class"' in ALUNO_PY
    assert "join_url" in ALUNO_PY
    assert "tabAluno da Aula Vedium" in ALUNO_PY
    assert "LMS Batch Enrollment" in ALUNO_PY
    # linka pro LMS nativo (não reimplementa curso/lições)
    assert "app.vediums.com/lms" in ALUNO_PY


def test_sections_are_defensive():
    """Cada seção degrada sem quebrar a página (nunca 500)."""
    assert "def _safe(" in ALUNO_PY
    assert "frappe.log_error" in ALUNO_PY


def test_template_uses_theme_and_key_blocks():
    assert 'include "templates/includes/site_navbar.html"' in ALUNO_HTML
    assert 'include "templates/includes/site_footer.html"' in ALUNO_HTML
    assert "noindex" in ALUNO_HTML  # área logada não indexa
    # blocos-chave da jornada
    for token in ("Próxima aula", "Presença", "Pagamento", "Meus cursos", "Google Meet"):
        assert token in ALUNO_HTML


def test_aluno_redirect_removed_so_page_serves():
    """O antigo redirect /aluno -> /lms foi removido (senão interceptaria a página)."""
    assert '{"source": "/aluno", "target"' not in HOOKS
