"""Testes puros da gamificação (fase 1, 2026-07-09).

Mesmo padrão dos outros test_pure_*: rodam sem Frappe/bench, validando o
texto-fonte (gamification.py importa frappe no topo, então não dá pra
importar o módulo aqui).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

GAMIFICATION = (CORE / "gamification.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")
BADGES_SEED = (
    CORE / "scripts" / "migrations" / "oneshot" / "setup_lms_badges.py"
).read_text(encoding="utf-8")


def test_quiz_and_certificate_events_are_wired_in_hooks():
    """Os dois doc_events novos de gamificação precisam estar registrados —
    sem isso os handlers nunca rodam (mesma classe de bug do scheduler
    duplicado corrigido em 2026-07-06)."""
    assert (
        '"LMS Quiz Submission": {\n        "after_insert": '
        '"vedium_core.gamification.handle_quiz_submission"' in HOOKS
    )
    assert (
        '"LMS Certificate": {\n        "after_insert": '
        '"vedium_core.gamification.handle_certificate_issued"' in HOOKS
    )
    assert "vedium_core.gamification.Gamification." not in HOOKS
    assert "def handle_lesson_completion(doc, method=None):" in GAMIFICATION
    assert "def handle_quiz_submission(doc, method=None):" in GAMIFICATION
    assert "def handle_certificate_issued(doc, method=None):" in GAMIFICATION


def test_quiz_points_only_on_first_pass():
    """Repetir a prova pra melhorar nota não pode pontuar de novo — o
    handler exclui a submissão atual e procura aprovação anterior."""
    assert "already_passed" in GAMIFICATION
    assert '"name": ["!=", doc.name]' in GAMIFICATION
    assert '"percentage": [">=", passing]' in GAMIFICATION
    # Prova final vale mais que exercício de fixação
    assert 'quiz_title.startswith("Prova Final")' in GAMIFICATION
    assert "100 if" in GAMIFICATION and "else 25" in GAMIFICATION


def test_milestone_coupon_is_deterministic_and_durable():
    """1 cupom por (aluno, curso concluído), com marcador DURÁVEL no banco:
    o código do cupom é derivado por hashlib de member:course (não
    frappe.generate_hash, que ignora o txt nas versões recentes e geraria
    código diferente a cada chamada), e a existência do cupom é o próprio
    anti-duplicidade — cache/Redis não serve (FLUSHALL apagaria o marcador,
    aconteceu de verdade em 2026-07-06)."""
    assert "hashlib.sha256" in GAMIFICATION
    assert "frappe.generate_hash(f" not in GAMIFICATION
    assert 'frappe.db.exists("Coupon", {"coupon_code": coupon_code})' in GAMIFICATION
    # Básico -> Intermediário -> Avançado (Avançado não tem próximo)
    assert '"portugues-para-estrangeiros-basico": "portugues-para-estrangeiros-intermediario"' in GAMIFICATION
    assert '"portugues-para-estrangeiros-intermediario": "portugues-para-estrangeiros-avancado"' in GAMIFICATION
    assert '"portugues-para-estrangeiros-avancado":' not in GAMIFICATION.split("MILESTONE_NEXT_COURSE = {")[1].split("}")[0]


def test_levels_are_monotonic_and_start_at_zero():
    levels_src = GAMIFICATION.split("LEVELS = [")[1].split("]")[0]
    thresholds = []
    for line in levels_src.strip().splitlines():
        line = line.strip().strip(",")
        if not line.startswith("("):
            continue
        thresholds.append(int(line.strip("()").split(",")[0]))
    assert thresholds[0] == 0, "primeiro nível precisa começar em 0 pontos"
    assert thresholds == sorted(thresholds), "faixas de nível precisam ser crescentes"


def test_custom_progress_page_was_removed_but_gamification_core_remains():
    assert not (CORE / "www" / "meu_progresso.py").exists()
    assert not (CORE / "www" / "meu-progresso.html").exists()
    assert "def get_level" in GAMIFICATION
    assert "def get_next_level" in GAMIFICATION
    assert "vedium_points" in GAMIFICATION


def test_badge_seed_matches_native_lms_badge_semantics():
    """Condições dos badges seguem a semântica REAL do LMS Badge nativo
    (confirmada no código-fonte oficial em 2026-07-09): expressão Python
    sobre o doc, user_field apontando o aluno, imagem obrigatória usando
    asset que existe no repo."""
    assert '"reference_doctype": "LMS Quiz Submission"' in BADGES_SEED
    assert '"condition": "doc.percentage == 100"' in BADGES_SEED
    assert '"user_field": "member"' in BADGES_SEED
    assert '"grant_only_once": 1' in BADGES_SEED

    # Toda imagem referenciada precisa existir fisicamente no repo
    icons_dir = CORE / "public" / "images" / "icones" / "SVG" / "SOLID"
    for line in BADGES_SEED.splitlines():
        if "ICON_BASE}/" in line and ".svg" in line:
            filename = line.split("ICON_BASE}/")[1].split('"')[0]
            assert (icons_dir / filename).exists(), f"ícone de badge não existe: {filename}"
