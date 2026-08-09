"""Testes puros de P8 (métricas de funil) e P9 (clusters SEO), 2026-08-09."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

FUNNEL = (CORE / "funnel_metrics.py").read_text(encoding="utf-8")
CLUSTERS = (CORE / "content_clusters.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_modules_are_valid_python():
    ast.parse(FUNNEL)
    ast.parse(CLUSTERS)


# ---- P8 ----

def test_funnel_metrics_covers_the_funnel():
    assert "def funnel_metrics(" in FUNNEL
    assert "@frappe.whitelist()" in FUNNEL
    for token in ("leads_total", "enrollments_active", "mrr", "ticket_medio",
                  "churn_rate", "active_by_language", "referral"):
        assert token in FUNNEL, token
    # reusa a medição de indicação (P7)
    assert "referral_metrics" in FUNNEL


def test_funnel_metrics_is_staff_only():
    """Métrica de negócio (MRR/churn/leads) NÃO pode vazar pra aluno logado."""
    block = FUNNEL.split("def funnel_metrics(", 1)[1].split("since =", 1)[0]
    assert "frappe.get_roles()" in block
    assert "frappe.PermissionError" in block


# ---- P9 ----

def test_clusters_map_all_languages_to_pillars():
    from importlib import util
    spec = util.spec_from_file_location("content_clusters", CORE / "content_clusters.py")
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for cat in ("ingles", "ioruba", "hebraico", "espanhol", "ple"):
        c = mod.cluster_for_category(cat)
        assert c and c["pillar_url"].startswith("/")
        assert c["teste_url"].startswith("/")
    # aliases e desconhecido
    assert mod.cluster_for_category("português")["pillar_url"] == "/portugues-para-estrangeiros"
    assert mod.cluster_for_category("klingon") is None
    assert mod.cluster_for_category(None) is None


def test_cluster_helper_registered_in_jinja():
    assert "vedium_core.content_clusters.cluster_for_category" in HOOKS
