import frappe

# Faixas de nível por pontos acumulados (User.vedium_points).
# Usado para pontos/badges do aluno; os pontos vêm de lição concluída (+10),
# quiz aprovado (+25), prova final aprovada (+100) e certificado (+200).
LEVELS = [
    (0, "Bronze"),
    (300, "Prata"),
    (900, "Ouro"),
    (2000, "Diamante"),
]

# Marco -> cupom: ao emitir o certificado de um nível PLE, o aluno ganha
# um cupom de desconto pro próximo nível (gamificação que vira receita —
# mesmo doctype/fluxo de cupom do programa de indicação, ver referrals.py).
MILESTONE_NEXT_COURSE = {
    "portugues-para-estrangeiros-basico": "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-intermediario": "portugues-para-estrangeiros-avancado",
}
MILESTONE_DISCOUNT_PERCENT = 10
MILESTONE_COUPON_VALID_DAYS = 90

# Marcos de progresso do curso (%). Ao cruzar cada um pela 1ª vez, emitimos o
# evento Brevo `progress_milestone` que dispara o fluxo A10 do kit de e-mail
# (ver Cliente/Vedium/emailmkt e [[project_email_lifecycle_brevo]]). Só evento —
# o Brevo é o dono do corpo/entrega; nada de sendmail aqui.
PROGRESS_MILESTONES = (25, 50, 75, 100)


def get_level(points):
    """Nome do nível para uma quantidade de pontos."""
    points = points or 0
    current = LEVELS[0][1]
    for threshold, name in LEVELS:
        if points >= threshold:
            current = name
    return current


def get_next_level(points):
    """(nome, pontos_faltantes) do próximo nível, ou (None, 0) no topo."""
    points = points or 0
    for threshold, name in LEVELS:
        if points < threshold:
            return name, threshold - points
    return None, 0


class Gamification:
    @staticmethod
    def add_points(user, points, reason="Action"):
        """
        Soma pontos ao usuário usando UPDATE atômico.

        Original usava get_value + set_value, o que perdia atualizações
        concorrentes (race condition quando 2 lições terminam no mesmo
        instante — última escrita sobrescreve a outra).
        """
        if not user or not points:
            return

        try:
            frappe.db.sql(
                """
                UPDATE `tabUser`
                SET vedium_points = COALESCE(vedium_points, 0) + %s
                WHERE name = %s
                """,
                (points, user),
            )
        except Exception as e:
            # Campo customizado vedium_points pode não existir ainda — não
            # quebra o fluxo de conclusão de lição.
            frappe.log_error(
                f"add_points falhou para {user} (+{points}): {e}",
                "Vedium.gamification.add_points",
            )

    @staticmethod
    def handle_lesson_completion(doc, method):
        """Recompensa padrão para conclusão de uma lição + verificação de marco
        de progresso (evento Brevo A10). Nenhum dos dois pode quebrar o salvar
        do progresso do aluno."""
        Gamification.add_points(
            doc.member, 10, f"completing a lesson in {doc.course}"
        )
        try:
            handle_course_progress_milestone(doc)
        except Exception:
            frappe.log_error(
                frappe.get_traceback(), "Vedium.gamification.progress_milestone"
            )

    @staticmethod
    def handle_quiz_submission(doc, method):
        """Recompensa por passar num quiz (doc_event after_insert de LMS
        Quiz Submission). Só a PRIMEIRA aprovação de cada quiz pontua —
        repetir a prova pra melhorar a nota não gera pontos de novo."""
        try:
            passing = frappe.db.get_value("LMS Quiz", doc.quiz, "passing_percentage") or 70
            if (doc.percentage or 0) < passing:
                return

            already_passed = frappe.db.exists(
                "LMS Quiz Submission",
                {
                    "member": doc.member,
                    "quiz": doc.quiz,
                    "percentage": [">=", passing],
                    "name": ["!=", doc.name],
                },
            )
            if already_passed:
                return

            quiz_title = frappe.db.get_value("LMS Quiz", doc.quiz, "title") or ""
            points = 100 if quiz_title.startswith("Prova Final") else 25
            Gamification.add_points(doc.member, points, f"passing quiz {doc.quiz}")
        except Exception:
            frappe.log_error(
                frappe.get_traceback(), "Vedium.gamification.handle_quiz_submission"
            )

    @staticmethod
    def handle_certificate_issued(doc, method):
        """Recompensa por concluir um nível (doc_event after_insert de LMS
        Certificate): +200 pontos e, se o curso tiver um próximo nível
        mapeado (PLE), gera um cupom de desconto e avisa o aluno por
        e-mail. Nunca lança exceção — falha aqui não pode derrubar a
        emissão do certificado."""
        try:
            Gamification.add_points(doc.member, 200, f"completing course {doc.course}")
            _grant_milestone_coupon(doc.member, doc.course)
        except Exception:
            frappe.log_error(
                frappe.get_traceback(), "Vedium.gamification.handle_certificate_issued"
            )


def handle_lesson_completion(doc, method=None):
    """Hook importavel pelo Frappe para conclusao de licao."""
    return Gamification.handle_lesson_completion(doc, method)


def handle_quiz_submission(doc, method=None):
    """Hook importavel pelo Frappe para submissao de quiz."""
    return Gamification.handle_quiz_submission(doc, method)


def handle_certificate_issued(doc, method=None):
    """Hook importavel pelo Frappe para emissao de certificado."""
    return Gamification.handle_certificate_issued(doc, method)


def _course_progress_percent(member, course):
    """% de progresso do aluno no curso = lições concluídas / total de lições.
    Robusto: 0 se o curso não tem lições (evita divisão por zero)."""
    total = frappe.db.count("Course Lesson", {"course": course})
    if not total:
        return 0
    completed = frappe.db.count(
        "LMS Course Progress",
        {"member": member, "course": course, "status": "Complete"},
    )
    return int(round(completed * 100 / total))


def handle_course_progress_milestone(doc):
    """Ao concluir uma lição, se o aluno cruzou um marco novo (25/50/75/100%),
    emite o evento Brevo `progress_milestone` (fluxo A10). Idempotente via
    LMS Enrollment.custom_last_progress_milestone — cada marco dispara uma vez.
    Só emite evento (Brevo é dono do e-mail); no-op se Brevo desligado."""
    member = getattr(doc, "member", None)
    course = getattr(doc, "course", None)
    if not member or not course or member in ("Administrator", "Guest"):
        return

    enr = frappe.db.get_value(
        "LMS Enrollment",
        {"member": member, "course": course},
        ["name", "custom_last_progress_milestone"],
        as_dict=True,
    )
    if not enr:
        return

    pct = _course_progress_percent(member, course)
    reached = 0
    for m in PROGRESS_MILESTONES:
        if pct >= m:
            reached = m
    last = int(enr.custom_last_progress_milestone or 0)
    if not reached or reached <= last:
        return

    from vedium_core import brevo

    course_title = frappe.db.get_value("LMS Course", course, "title") or course
    email = frappe.db.get_value("User", member, "email") or member
    brevo.emit_contact_event(
        email,
        "progress_milestone",
        event_properties={
            "enrollment_id": enr.name,
            "course": course_title,
            "course_level": course_title,
            "milestone": reached,
            "progress_percent": pct,
            "progress_url": brevo.STUDENT_PORTAL_URL,
            "student_portal_url": brevo.STUDENT_PORTAL_URL,
        },
        contact_properties={"COURSE": course_title},
    )
    frappe.db.set_value(
        "LMS Enrollment", enr.name, "custom_last_progress_milestone", reached
    )


def _grant_milestone_coupon(member, course_name):
    next_course = MILESTONE_NEXT_COURSE.get(course_name)
    if not next_course:
        return

    # Anti-duplicidade durável: o código do cupom é determinístico por
    # (aluno, curso concluído) — reemitir o certificado não gera um segundo
    # cupom. Cache não serve de marcador aqui: Redis pode ser limpo
    # (FLUSHALL) e o marcador sumiria.
    # (hashlib, não frappe.generate_hash: este ignora o txt nas versões
    # recentes do Frappe e geraria um código diferente a cada chamada)
    import hashlib

    suffix = hashlib.sha256(f"{member}:{course_name}".encode()).hexdigest()[:8].upper()
    coupon_code = f"NIVEL-{suffix}"
    if frappe.db.exists("Coupon", {"coupon_code": coupon_code}):
        return
    frappe.get_doc(
        {
            "doctype": "Coupon",
            "coupon_code": coupon_code,
            "discount_percent": MILESTONE_DISCOUNT_PERCENT,
            "active": 1,
            "max_uses": 1,
            "valid_to": frappe.utils.add_days(
                frappe.utils.now_datetime(), MILESTONE_COUPON_VALID_DAYS
            ),
        }
    ).insert(ignore_permissions=True)

    try:
        email = frappe.db.get_value("User", member, "email") or member
        first_name = frappe.db.get_value("User", member, "first_name") or ""
        done_title = frappe.db.get_value("LMS Course", course_name, "title") or course_name
        next_title = frappe.db.get_value("LMS Course", next_course, "title") or next_course
        frappe.sendmail(
            recipients=[email],
            subject="Parabéns pelo certificado! Ganhe desconto no próximo nível 🎓 | Vedium",
            message=f"""
                <h3>Parabéns{', ' + frappe.utils.escape_html(first_name) if first_name else ''}!</h3>
                <p>Você concluiu <strong>{frappe.utils.escape_html(done_title)}</strong> e
                conquistou seu certificado.</p>
                <p>Como recompensa, aqui está um cupom de
                <strong>{MILESTONE_DISCOUNT_PERCENT}% de desconto</strong> para continuar sua
                jornada em <strong>{frappe.utils.escape_html(next_title)}</strong>:</p>
                <p style="font-size:20px;font-weight:700;">{coupon_code}</p>
                <p>Válido por {MILESTONE_COUPON_VALID_DAYS} dias.</p>
                <p>— Equipe Vedium</p>
            """,
            delayed=False,
        )
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.gamification.milestone_coupon_email"
        )
