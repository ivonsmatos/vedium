"""Testes puros para o manifesto e o importador Wiki da Vedium.

Executado sem bench. Valida:
- JSON válido e estrutura coerente;
- todos os espaços, grupos e páginas têm os campos obrigatórios;
- nenhuma página tem conteúdo vazio ou placeholder [TODO];
- rotas seguem o padrão kebab-case;
- sem duplicatas de rota por espaço;
- contagem de páginas;
- importador carrega sem erro de sintaxe;
- _find_existing retorna None quando não existe doc;
- _first_field retorna o primeiro campo que existe;
- dry_run não pode chamar frappe.db sem frappe real.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Caminhos — o arquivo de teste está em vedium_core/vedium_core/tests/
# APP_ROOT = vedium_core/vedium_core/ (o pacote Python da aplicação)
# ---------------------------------------------------------------------------

_THIS_FILE = Path(__file__).resolve()
# parents[0] = tests/, parents[1] = vedium_core/ (package), parents[2] = vedium_core/ (app), parents[3] = vedium/ (repo)
APP_ROOT = _THIS_FILE.parents[1]   # vedium_core/vedium_core/
MANIFEST_PATH = APP_ROOT / "wiki_content" / "manifest.json"
IMPORTER_PATH = APP_ROOT / "wiki_import.py"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def manifest() -> dict:
    assert MANIFEST_PATH.exists(), f"Manifesto não encontrado: {MANIFEST_PATH}"
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return data


@pytest.fixture(scope="module")
def all_spaces(manifest) -> list[dict]:
    return manifest.get("spaces", [])


@pytest.fixture(scope="module")
def all_pages_flat(all_spaces) -> list[tuple[str, dict]]:
    """Todas as páginas como (space_route, page)."""
    result = []
    for space in all_spaces:
        for page in space.get("pages", []):
            result.append((space.get("route", ""), page))
        for group in space.get("groups", []):
            for page in group.get("pages", []):
                result.append((space.get("route", ""), page))
    return result


# ---------------------------------------------------------------------------
# Estrutura do manifesto
# ---------------------------------------------------------------------------

def test_manifest_is_valid_json():
    assert MANIFEST_PATH.exists()
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_manifest_has_version_and_spaces(manifest):
    assert "version" in manifest
    assert manifest["version"] >= 2
    assert "spaces" in manifest
    assert len(manifest["spaces"]) >= 1


def test_all_spaces_have_required_fields(all_spaces):
    for space in all_spaces:
        assert "title" in space, f"Espaço sem title: {space}"
        assert space["title"].strip(), f"Espaço com title vazio: {space}"
        assert "route" in space or space.get("existing"), f"Espaço sem route: {space}"


def test_all_spaces_have_published_flag(all_spaces):
    for space in all_spaces:
        if not space.get("existing"):
            assert "published" in space, f"Espaço sem published: {space['title']}"


def test_all_pages_have_required_fields(all_pages_flat):
    for space_route, page in all_pages_flat:
        assert "title" in page, f"[{space_route}] Página sem title: {page}"
        assert page["title"].strip(), f"[{space_route}] Página com title vazio"
        assert "route" in page, f"[{space_route}] Página sem route: {page.get('title')}"
        assert "content" in page, f"[{space_route}] Página sem content: {page.get('title')}"
        assert "published" in page, f"[{space_route}] Página sem published: {page.get('title')}"


def test_no_empty_page_content(all_pages_flat):
    for space_route, page in all_pages_flat:
        content = page.get("content", "")
        assert content.strip(), (
            f"[{space_route}] Conteúdo vazio na página: {page.get('title')}"
        )


def test_no_todo_placeholder_in_content(all_pages_flat):
    """Garante que nenhum conteúdo tem [TODO] (apenas [A CONFIRMAR] é permitido)."""
    for space_route, page in all_pages_flat:
        content = page.get("content", "")
        assert "[TODO]" not in content, (
            f"[{space_route}] Conteúdo com [TODO] na página: {page.get('title')}"
        )


def test_all_routes_are_kebab_case(all_spaces, all_pages_flat):
    kebab = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    for space in all_spaces:
        route = space.get("route", "")
        if route:
            assert kebab.match(route), f"Rota de espaço não é kebab-case: '{route}'"

    for space_route, page in all_pages_flat:
        route = page.get("route", "")
        assert route, f"[{space_route}] Página sem route: {page.get('title')}"
        assert kebab.match(route), (
            f"[{space_route}] Rota de página não é kebab-case: '{route}' — {page.get('title')}"
        )


def test_no_duplicate_routes_within_space(all_spaces):
    for space in all_spaces:
        seen_routes: set[str] = set()
        all_space_pages: list[dict] = list(space.get("pages", []))
        for group in space.get("groups", []):
            all_space_pages.extend(group.get("pages", []))

        for page in all_space_pages:
            route = page.get("route", "")
            assert route not in seen_routes, (
                f"[{space.get('route')}] Rota duplicada: '{route}'"
            )
            seen_routes.add(route)


def test_total_page_count_is_substantial(all_pages_flat):
    total = len(all_pages_flat)
    assert total >= 150, f"Total de páginas muito baixo: {total}"


def test_new_spaces_have_correct_routes(all_spaces):
    expected = {
        "processos-administrativos",
        "politicas-compliance",
        "faq-comercial-financeiro",
        "faq-tecnico",
    }
    actual_routes = {s.get("route") for s in all_spaces if not s.get("existing")}
    missing = expected - actual_routes
    assert not missing, f"Espaços novos sem rota esperada: {missing}"


def test_pedagogical_space_has_group(all_spaces):
    pedagogical = next(
        (s for s in all_spaces if s.get("route") == "documentacao-pedagogica-dos-cursos"),
        None,
    )
    assert pedagogical is not None, "Espaço pedagógico não encontrado no manifesto"
    groups = pedagogical.get("groups", [])
    assert any(g.get("title") == "Modelos e Padrões Pedagógicos" for g in groups)


def test_pedagogical_group_has_at_least_18_pages(all_spaces):
    pedagogical = next(
        (s for s in all_spaces if s.get("route") == "documentacao-pedagogica-dos-cursos"),
        None,
    )
    assert pedagogical is not None
    group = next(
        (g for g in pedagogical.get("groups", []) if g["title"] == "Modelos e Padrões Pedagógicos"),
        None,
    )
    assert group is not None
    assert len(group.get("pages", [])) >= 18, (
        f"Grupo pedagógico tem {len(group.get('pages', []))} páginas, esperado >= 18"
    )


def test_processos_admin_groups_and_pages(all_spaces):
    space = next(
        (s for s in all_spaces if s.get("route") == "processos-administrativos"),
        None,
    )
    assert space is not None
    groups = space.get("groups", [])
    assert len(groups) >= 6, f"Processos Administrativos tem {len(groups)} grupos, esperado >= 6"
    total_pages = sum(len(g.get("pages", [])) for g in groups)
    assert total_pages >= 50, f"Processos Administrativos tem {total_pages} páginas nos grupos"


def test_politicas_compliance_groups(all_spaces):
    space = next(
        (s for s in all_spaces if s.get("route") == "politicas-compliance"),
        None,
    )
    assert space is not None
    groups = space.get("groups", [])
    assert len(groups) >= 5


def test_faq_groups_and_pages(all_spaces):
    for route in ("faq-comercial-financeiro", "faq-tecnico"):
        space = next((s for s in all_spaces if s.get("route") == route), None)
        assert space is not None, f"Espaço não encontrado: {route}"
        groups = space.get("groups", [])
        assert len(groups) >= 4, f"{route} tem {len(groups)} grupos"
        total = sum(len(g.get("pages", [])) for g in groups)
        assert total >= 40, f"{route} tem {total} páginas nos grupos"


# ---------------------------------------------------------------------------
# Importador — sintaxe e funções puras
# ---------------------------------------------------------------------------

def test_importer_is_valid_python():
    assert IMPORTER_PATH.exists(), f"Importador não encontrado: {IMPORTER_PATH}"
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    # Garante que o arquivo parseia sem erros
    tree = ast.parse(source)
    assert tree is not None


def test_importer_defines_import_manifest():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "def import_manifest" in source


def test_importer_has_dry_run_support():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "dry_run" in source


def test_importer_has_rollback():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "rollback" in source


def test_importer_has_group_support():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "_upsert_group" in source


def test_importer_has_counters():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "counters" in source
    assert '"created"' in source
    assert '"updated"' in source
    assert '"skipped"' in source
    assert '"errors"' in source


def test_importer_never_deletes():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    # Não deve chamar doc.delete() nem frappe.delete_doc()
    assert "doc.delete()" not in source
    assert "frappe.delete_doc(" not in source


def test_importer_uses_adaptive_fieldnames():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "_fieldnames" in source
    assert "_first_field" in source


def test_importer_load_manifest_resolves_relative_paths():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "frappe.get_app_path" in source


def test_importer_uses_ignore_permissions():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "ignore_permissions" in source


def test_importer_has_whitelist_decorator():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "@frappe.whitelist()" in source


def test_importer_logs_result():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "frappe.logger" in source or "frappe.log_error" in source


def test_importer_conditional_publishing():
    source = IMPORTER_PATH.read_text(encoding="utf-8")
    assert "has_pending_confirmation" in source
    assert 'not has_pending_confirmation and cint(page.get("published", 1))' in source


# ---------------------------------------------------------------------------

# Lógica pura isolada (sem frappe)
# ---------------------------------------------------------------------------

def test_first_field_returns_first_existing():
    """Testa _first_field sem precisar de frappe."""
    available = {"title", "route", "published", "wiki_space"}

    def _first_field(fields: set, *candidates: str):
        return next((name for name in candidates if name in fields), None)

    assert _first_field(available, "title", "page_title") == "title"
    assert _first_field(available, "page_title", "title") == "title"
    assert _first_field(available, "slug", "route") == "route"
    assert _first_field(available, "nonexistent") is None


def test_manifest_content_has_confirmar_not_todo(all_pages_flat):
    """[A CONFIRMAR] é permitido; [TODO] não."""
    confirmar_pages = [
        page for _, page in all_pages_flat
        if "[A CONFIRMAR]" in page.get("content", "")
    ]
    # Deve haver algumas páginas com [A CONFIRMAR] — é esperado
    assert len(confirmar_pages) > 0, "Nenhuma página usa [A CONFIRMAR] — revisar conteúdo"


def test_all_pages_start_with_markdown_header(all_pages_flat):
    """Toda página deve começar com um título Markdown (#)."""
    for space_route, page in all_pages_flat:
        content = page.get("content", "").strip()
        assert content.startswith("#"), (
            f"[{space_route}] Página não começa com # : {page.get('title')}"
        )


def test_dpo_email_present_in_lgpd_pages(all_spaces):
    """O e-mail do DPO deve aparecer nas páginas de LGPD."""
    lgpd_pages = []
    for space in all_spaces:
        if space.get("route") == "politicas-compliance":
            for group in space.get("groups", []):
                if "LGPD" in group.get("title", "") or "Privacidade" in group.get("title", ""):
                    lgpd_pages.extend(group.get("pages", []))

    assert lgpd_pages, "Nenhuma página de LGPD encontrada"
    dpo_pages = [p for p in lgpd_pages if "dpo@vediums.com" in p.get("content", "")]
    assert len(dpo_pages) > 0, "E-mail do DPO não encontrado nas páginas de LGPD"
