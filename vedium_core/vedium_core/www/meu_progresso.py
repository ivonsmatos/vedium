import frappe


no_cache = 1
APP_URL = "https://app.vediums.com"
PUBLIC_HOSTS = {"vediums.com", "www.vediums.com"}


def _redirect_public_host(path):
    host = (getattr(frappe.local, "request", None) and frappe.local.request.host) or ""
    host = host.split(":")[0].lower()
    if host in PUBLIC_HOSTS:
        frappe.local.flags.redirect_location = f"{APP_URL}{path}"
        raise frappe.Redirect


def _cefr_from_title(title):
    title = (title or "").lower()
    levels = [
        ("c1", "C1"),
        ("b2", "B2"),
        ("upper", "B2"),
        ("pré", "B1-"),
        ("pre", "B1-"),
        ("intermedi", "B1"),
        ("a2", "A2"),
        ("elementary", "A2"),
        ("a1", "A1"),
        ("beginner", "A1"),
        ("básico", "A1"),
        ("basico", "A1"),
    ]
    for needle, level in levels:
        if needle in title:
            return level
    return "Em diagnóstico"


def get_context(context):
    context.no_cache = 1
    context.title = "Meu progresso — Vedium"
    context.description = "Painel do aluno com progresso CEFR, revisão e próximos passos."
    _redirect_public_host("/meu-progresso")

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = (
            "https://app.vediums.com/login?redirect-to=/meu-progresso"
        )
        raise frappe.Redirect

    user = frappe.session.user
    enrollments = frappe.get_all(
        "LMS Enrollment",
        filters={"member": user},
        fields=["name", "course", "progress", "creation"],
        order_by="creation desc",
    )

    courses = []
    for enrollment in enrollments:
        title = frappe.db.get_value("LMS Course", enrollment.course, "title") or enrollment.course
        progress = enrollment.progress or 0
        status = "Concluído" if progress >= 100 else "Em andamento"
        courses.append(
            {
                "name": enrollment.name,
                "course": enrollment.course,
                "title": title,
                "status": status,
                "cefr": _cefr_from_title(title),
                "date": frappe.utils.format_datetime(enrollment.creation, "dd/MM/yyyy"),
            }
        )

    flashcards = frappe.get_all(
        "LMS Flashcard",
        filters={"user": user},
        fields=["front", "back", "course"],
        order_by="modified desc",
        limit_page_length=8,
    )
    badges = frappe.get_all(
        "LMS Badge Log",
        filters={"user": user},
        fields=["badge", "level", "awarded_on"],
        order_by="awarded_on desc",
        limit_page_length=8,
    )

    # Badges automáticos NATIVOS do LMS (LMS Badge Assignment — criados
    # sozinhos pelo LMS quando a condição do LMS Badge bate; ver
    # scripts/migrations/oneshot/setup_lms_badges.py). Mesclados na mesma
    # lista de conquistas do template.
    if frappe.db.exists("DocType", "LMS Badge Assignment"):
        for assignment in frappe.get_all(
            "LMS Badge Assignment",
            filters={"member": user},
            fields=["badge", "issued_on"],
            order_by="issued_on desc",
            limit_page_length=8,
        ):
            badges.append(
                frappe._dict(
                    badge=frappe.db.get_value("LMS Badge", assignment.badge, "title")
                    or assignment.badge,
                    level=None,
                    awarded_on=assignment.issued_on,
                )
            )

    # Pontos e nível de gamificação (User.vedium_points — lição +10,
    # quiz aprovado +25, prova final +100, certificado +200).
    from vedium_core.gamification import get_level, get_next_level

    points = frappe.db.get_value("User", user, "vedium_points") or 0
    context.points = points
    context.level = get_level(points)
    next_level, points_to_next = get_next_level(points)
    context.next_level = next_level
    context.points_to_next = points_to_next

    # Removido 2026-07-01: a seção "Aulas e tarefas" lia o doctype legado
    # Lesson Slot, substituído pelo agendamento NATIVO do Frappe LMS (Course
    # Evaluator + Google Meet). Lesson Slot está permanentemente vazio em
    # produção (0 registros) desde a migração — a query nunca retornava nada,
    # era código morto rodando a cada carregamento da página. Ver
    # docs/plataforma/01-mapa-nativo-vs-custom.md.

    context.courses = courses
    context.flashcards = flashcards
    context.badges = badges
    context.streak_hint = min(len(badges) + len(flashcards), 30)
    return context
