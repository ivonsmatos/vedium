# -*- coding: utf-8 -*-
# Vedium Core — API pública e endpoints internos
# Imports pesados (mercadopago, stripe, services.*) ficam lazy dentro das
# funções que os usam, para o módulo carregar mesmo sem essas dependências
# instaladas (ex.: workers que só processam fila).

import hashlib
from datetime import datetime

import frappe
from frappe import _


def _safe_get_all(doctype, **kwargs):
    """
    Versão defensiva de frappe.get_all que devolve [] se o DocType não
    existe ainda (caso de funcionalidades opcionais como fórum, comunidade,
    flashcards). Evita 500 silencioso até criarmos os DocTypes.
    """
    if not frappe.db.exists("DocType", doctype):
        return []
    try:
        return frappe.get_all(doctype, **kwargs)
    except Exception as e:
        frappe.log_error(
            f"Erro consultando {doctype}: {e}",
            f"Vedium.api._safe_get_all.{doctype}",
        )
        return []


def rate_limit_by_ip(action: str, limit: int, window_sec: int = 3600):
    """
    Rate-limit simples por IP para endpoints públicos (anti-spam).
    Janela FIXA por bucket de tempo: a chave inclui o número da janela
    atual, então expira sozinha e nunca fica órfã sem TTL (o que
    bloquearia o IP para sempre).
    """
    import time

    ip = getattr(frappe.local, "request_ip", None) or "unknown"
    bucket = int(time.time() // window_sec)
    cache_key = f"vedium_rl:{action}:{ip}:{bucket}"
    current = int(frappe.cache().get_value(cache_key) or 0)
    if current >= limit:
        frappe.throw(
            _("Muitas tentativas. Aguarde alguns minutos e tente novamente."),
            frappe.TooManyRequestsError
            if hasattr(frappe, "TooManyRequestsError")
            else frappe.ValidationError,
        )
    frappe.cache().set_value(cache_key, current + 1, expires_in_sec=window_sec * 2)


# =====================
# Contato público (sem login)
# =====================
@frappe.whitelist(allow_guest=True)
def send_contact_message(
    sender_name, sender_email, phone=None, subject=None, message=None
):
    """
    Recebe mensagem do formulário de contato e envia por e-mail
    """
    import re

    rate_limit_by_ip("contact", limit=5, window_sec=3600)

    if not sender_name or not sender_email:
        frappe.throw(_("Nome e e-mail são obrigatórios"))
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", sender_email):
        frappe.throw(_("E-mail inválido"))

    email_body = f"""
        <h3>Nova mensagem via site Vedium</h3>
        <p><strong>Nome:</strong> {frappe.utils.escape_html(sender_name)}</p>
        <p><strong>E-mail:</strong> {frappe.utils.escape_html(sender_email)}</p>
        <p><strong>Telefone:</strong> {frappe.utils.escape_html(phone or 'Não informado')}</p>
        <p><strong>Assunto:</strong> {frappe.utils.escape_html(subject or 'Sem assunto')}</p>
        <hr>
        <p><strong>Mensagem:</strong></p>
        <p>{frappe.utils.escape_html(message or '').replace(chr(10), '<br>')}</p>
    """

    frappe.sendmail(
        recipients=["contato@vediums.com"],
        subject=f"[Site Vedium] {frappe.utils.escape_html(subject or 'Contato')}",
        message=email_body,
        reply_to=sender_email,
        now=True,
    )

    # Alimenta o topo do funil: todo contato vira lead no CRM (com o
    # histórico da mensagem). Defensivo — nunca quebra o envio do e-mail.
    try:
        _upsert_crm_lead_from_contact(sender_name, sender_email, phone, subject, message)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.crm.contact_lead")

    return {"success": True}


def _upsert_crm_lead_from_contact(sender_name, sender_email, phone, subject, message):
    """Cria (ou comenta em) um CRM Lead a partir do formulário de contato."""
    if not frappe.db.exists("DocType", "CRM Lead"):
        return

    note = (
        f"Mensagem via site — assunto: {subject or 'sem assunto'}\n\n"
        f"{(message or '').strip()}"
    )

    from vedium_core.integrations import ensure_contact

    parts = (sender_name or "").strip().split(" ", 1)
    ensure_contact(
        sender_email,
        first_name=parts[0],
        last_name=parts[1] if len(parts) > 1 else None,
        mobile=phone,
    )

    existing = frappe.db.get_value("CRM Lead", {"email": sender_email}, "name")
    if existing:
        # Lead já existe (novo interesse) — registra a mensagem no histórico
        frappe.get_doc("CRM Lead", existing).add_comment("Comment", note)
    else:
        lead = frappe.new_doc("CRM Lead")
        lead.first_name = parts[0]
        if len(parts) > 1:
            lead.last_name = parts[1]
        lead.lead_name = (sender_name or "").strip()
        lead.email = sender_email
        if phone:
            lead.mobile_no = phone
        lead.source = "Website"
        lead.insert(ignore_permissions=True)
        lead.add_comment("Comment", note)


@frappe.whitelist()
def open_support_ticket(subject, description, category=None):
    """
    Abre um chamado de suporte para o usuário logado.
    Rate limit: 10 chamados/hora por IP.
    """
    rate_limit_by_ip("support_ticket", limit=10, window_sec=3600)
    ticket = frappe.get_doc(
        {
            "doctype": "Support Ticket",
            "subject": subject,
            "description": description,
            "category": category or "Geral",
            "opened_by": frappe.session.user,
        }
    )
    ticket.insert(ignore_permissions=True)
    return {"ticket_id": ticket.name}


@frappe.whitelist()
def get_my_tickets():
    """
    Lista chamados abertos pelo usuário logado
    """
    tickets = frappe.get_all(
        "Support Ticket",
        filters={"opened_by": frappe.session.user},
        fields=["name", "subject", "status", "creation", "category"],
    )
    return tickets


@frappe.whitelist()
def get_monitoring_dashboard():
    """
    Dashboard interno com dados REAIS do site: erros recentes, scheduler,
    último backup e tamanho do banco. Restrito a operadores.
    """
    roles = set(frappe.get_roles(frappe.session.user))
    if not roles & {"System Manager", "Administrator", "Vedium Ops"}:
        frappe.throw(_("Permissão negada"), frappe.PermissionError)

    import os

    alerts = []

    # Erros das últimas 24h (Error Log do próprio Frappe)
    error_count_24h = frappe.db.count(
        "Error Log",
        {"creation": [">", frappe.utils.add_to_date(None, hours=-24)]},
    )
    if error_count_24h > 50:
        alerts.append(
            {"type": "warning", "msg": f"{error_count_24h} erros nas últimas 24h"}
        )

    # Scheduler ativo?
    scheduler_disabled = bool(
        frappe.utils.cint(frappe.db.get_default("disable_scheduler") or 0)
    )
    if scheduler_disabled:
        alerts.append({"type": "critical", "msg": "Scheduler DESATIVADO"})

    # Último backup local (sites/<site>/private/backups)
    last_backup = None
    try:
        backup_dir = frappe.utils.get_backups_path()
        files = [
            os.path.join(backup_dir, f)
            for f in os.listdir(backup_dir)
            if f.endswith(".sql.gz")
        ]
        if files:
            newest = max(files, key=os.path.getmtime)
            last_backup = datetime.fromtimestamp(
                os.path.getmtime(newest)
            ).isoformat()
            age_hours = (
                datetime.now() - datetime.fromtimestamp(os.path.getmtime(newest))
            ).total_seconds() / 3600
            if age_hours > 36:
                alerts.append(
                    {
                        "type": "warning",
                        "msg": f"Último backup local tem {age_hours:.0f}h",
                    }
                )
    except Exception:
        pass

    # Tamanho do banco
    db_size_mb = None
    try:
        row = frappe.db.sql(
            """SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 1)
               FROM information_schema.tables WHERE table_schema = DATABASE()"""
        )
        db_size_mb = float(row[0][0]) if row and row[0][0] else None
    except Exception:
        pass

    return {
        "error_count_24h": error_count_24h,
        "scheduler_enabled": not scheduler_disabled,
        "last_backup": last_backup,
        "db_size_mb": db_size_mb,
        "alerts": alerts,
    }


# =====================
# Gamificação, comunidade e internacionalização/acessibilidade
# =====================
@frappe.whitelist()
def get_user_badges():
    """
    Retorna emblemas e nível do usuário logado.
    Se o DocType ainda não existe (feature opcional), retorna [].
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Faça login para ver seus emblemas"))
    return _safe_get_all(
        "LMS Badge Log",
        filters={"user": frappe.session.user},
        fields=["badge", "level", "awarded_on"],
    )


@frappe.whitelist(allow_guest=True)
def get_leaderboard(course_name, limit=20, start=0):
    """
    Retorna ranking de alunos do curso. Suporta paginação via `start`.
    """
    leaderboard = frappe.db.sql(
        """
        SELECT member, score, completed_on FROM `tabLMS Enrollment`
        WHERE course=%s AND status='Completed'
        ORDER BY score DESC, completed_on ASC
        LIMIT %s OFFSET %s
    """,
        (course_name, int(limit), int(start)),
        as_dict=True,
    )
    return leaderboard


@frappe.whitelist(allow_guest=True)
def get_forum_topics(course_name):
    """Tópicos do fórum do curso. [] se DocType não existe ainda."""
    return _safe_get_all(
        "LMS Forum Topic",
        filters={"course": course_name},
        fields=["name", "title", "created_by", "creation"],
    )


@frappe.whitelist(allow_guest=True)
def get_community_links(course_name):
    """Links de comunidade (Telegram, Discord, Slack). [] se DocType não existe."""
    return _safe_get_all(
        "LMS Community Link",
        filters={"course": course_name},
        fields=["platform", "url"],
    )


@frappe.whitelist(allow_guest=True)
def get_course_languages(course_name):
    """Idiomas do curso para i18n. [] se DocType não existe."""
    return _safe_get_all(
        "LMS Course Language",
        filters={"course": course_name},
        fields=["language_code", "language_name"],
    )


@frappe.whitelist(allow_guest=True)
def get_accessibility_features(course_name):
    """Recursos de acessibilidade. [] se DocType não existe."""
    return _safe_get_all(
        "LMS Accessibility Feature",
        filters={"course": course_name},
        fields=["feature", "enabled"],
    )


# =====================
# Aulas ao vivo/gravadas e recursos extras
# =====================
@frappe.whitelist(allow_guest=True)
def get_course_sessions(course_name):
    """Sessões (ao vivo/gravadas) do curso. [] se DocType não existe."""
    return _safe_get_all(
        "LMS Session",
        filters={"course": course_name},
        fields=[
            "name",
            "title",
            "type",
            "start_time",
            "end_time",
            "video_url",
            "live_url",
            "platform",
        ],
    )


# Recursos extras: escuta ativa, gravação de áudio, flashcards (placeholders)
@frappe.whitelist()
def submit_listening_exercise(course_name, audio_url):
    """
    Recebe áudio do aluno para exercício de escuta ativa
    """
    from vedium_core.services.ai_service import AIService

    ai = AIService()
    result = ai.analyze_audio(audio_url, context="listening")
    return {"status": "analyzed", "result": result}


@frappe.whitelist()
def submit_speaking_exercise(course_name, audio_url):
    """
    Recebe áudio do aluno para exercício de fala
    """
    from vedium_core.services.ai_service import AIService

    ai = AIService()
    result = ai.analyze_audio(audio_url, context="speaking")
    return {"status": "analyzed", "result": result}


@frappe.whitelist(allow_guest=True)
def get_flashcards(course_name):
    """Flashcards do curso. [] se DocType não existe."""
    return _safe_get_all(
        "LMS Flashcard",
        filters={"course": course_name},
        fields=["front", "back"],
    )


# =====================
# Quiz/Prova de nível com feedback instantâneo
# =====================
@frappe.whitelist()
def submit_quiz_attempt(course_name, answers):
    """
    Recebe respostas do quiz de nivelamento e retorna feedback instantâneo.
    answers: dict {question_id: resposta} — Frappe envia como string JSON, parseado aqui.
    Rate limit: 10 tentativas/hora por IP (anti-bruteforce).
    """
    import json

    rate_limit_by_ip("quiz_attempt", limit=10, window_sec=3600)

    # M-07 fix: Frappe passes whitelisted dict params as JSON strings
    if isinstance(answers, str):
        try:
            answers = json.loads(answers)
        except (ValueError, TypeError):
            frappe.throw(_("Formato de respostas inválido"))

    if not frappe.db.exists("DocType", "LMS Quiz Question"):
        frappe.throw(_("Quiz não disponível para este curso ainda"))

    questions = frappe.get_all(
        "LMS Quiz Question",
        filters={"course": course_name},
        fields=["name", "correct_answer", "feedback"],
    )
    correct = 0
    total = len(questions)
    feedbacks = []
    for q in questions:
        user_answer = answers.get(q["name"])
        if user_answer == q["correct_answer"]:
            correct += 1
        else:
            feedbacks.append({"question": q["name"], "feedback": q["feedback"]})
    score = int((correct / total) * 100) if total else 0
    return {"score": score, "total": total, "correct": correct, "feedbacks": feedbacks}


# =====================
# Emissão automática de certificado digital
# =====================


@frappe.whitelist()
def issue_certificate(enrollment_name):
    """
    Emite certificado digital para uma inscrição concluída, com código de verificação público.
    Rate limit: 5 emissões/hora por IP (evita geração massiva).
    """
    rate_limit_by_ip("issue_certificate", limit=5, window_sec=3600)
    enrollment = frappe.get_doc("LMS Enrollment", enrollment_name)
    # Bug real encontrado em 2026-07-07: esta função checava
    # `enrollment.status != "Completed"`, mas LMS Enrollment não tem (e nunca
    # teve) um campo "status" -- nada no código jamais setava esse valor, e a
    # emissão de certificado sempre falhava silenciosamente antes de chegar
    # aqui (Frappe retorna None num atributo inexistente, então a comparação
    # nunca batia). `progress` é o campo real e nativo (Float 0-100),
    # mantido pelo próprio LMS conforme o aluno completa as lições.
    if (enrollment.progress or 0) < 100:
        frappe.throw(_("Curso ainda não concluído"))
    # Gera código único baseado em dados do aluno, curso e data
    base = f"{enrollment.member}-{enrollment.course}-{datetime.now()}"
    code = hashlib.sha256(base.encode()).hexdigest()[:12].upper()
    # Cria registro de certificado (ou atualiza)
    cert = frappe.get_doc(
        {
            "doctype": "LMS Certificate",
            "enrollment": enrollment.name,
            "member": enrollment.member,
            "course": enrollment.course,
            "issue_date": datetime.now(),
            "verification_code": code,
        }
    )
    # ignore_mandatory: o certificado NATIVO do LMS marca `template` como
    # obrigatório; a emissão da Vedium usa código de verificação próprio e não
    # depende de template, então dispensamos essa obrigatoriedade.
    cert.insert(
        ignore_permissions=True, ignore_if_duplicate=True, ignore_mandatory=True
    )
    return {
        "certificate_id": cert.name,
        "verification_code": code,
        "verify_url": f"/certificado?code={code}",
    }


# Endpoint público para verificação de certificado
@frappe.whitelist(allow_guest=True)
def verify_certificate(code):
    cert = frappe.get_all(
        "LMS Certificate",
        filters={"verification_code": code},
        fields=["member", "course", "issue_date", "enrollment"],
    )
    if not cert:
        frappe.throw(_("Certificado não encontrado"))
    return cert[0]


# =====================
# Histórico de pagamentos/faturas do usuário
# =====================
@frappe.whitelist()
def get_payment_history(limit=50, start=0):
    """
    Retorna histórico de pagamentos/faturas do usuário logado. Suporta paginação.
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Faça login para ver seu histórico de pagamentos"))
    # Busca matrículas + título do curso em um único JOIN (evita N+1)
    enrollments = frappe.db.sql(
        """
        SELECT
            e.name, e.course, e.creation, e.status,
            e.payment_gateway, e.payment_reference,
            e.amount, e.currency,
            c.title AS course_title
        FROM `tabLMS Enrollment` e
        LEFT JOIN `tabLMS Course` c ON c.name = e.course
        WHERE e.member = %s
        ORDER BY e.creation DESC
        LIMIT %s OFFSET %s
        """,
        (frappe.session.user, int(limit), int(start)),
        as_dict=True,
    )
    return enrollments


# =====================
# Endpoint central para seleção de gateway no checkout
# =====================
@frappe.whitelist()
def create_checkout(course_name, gateway, coupon_code=None):
    """
    Cria checkout para o gateway selecionado pelo usuário, com suporte a cupons.
    Rate limit: 20 tentativas/hora por IP (anti-flooding de sessões de pagamento).
    """
    rate_limit_by_ip("checkout", limit=20, window_sec=3600)
    if frappe.session.user == "Guest":
        frappe.throw(_("Por favor, faça login para comprar este curso"))
    course = frappe.get_doc("LMS Course", course_name)
    if not course.paid_course:
        frappe.throw(_("Este curso é gratuito"))
    existing = frappe.db.exists(
        "LMS Enrollment", {"course": course_name, "member": frappe.session.user}
    )
    if existing:
        frappe.throw(_("Você já está inscrito neste curso"))

    discount = 0
    coupon_valid = False
    coupon_msg = None
    if coupon_code:
        # Exemplo: buscar cupom válido
        coupon = frappe.db.get_value(
            "Coupon",
            coupon_code,
            [
                "name",
                "discount_percent",
                "active",
                "max_uses",
                "used_count",
                "valid_from",
                "valid_to",
            ],
            as_dict=True,
        )

        now = datetime.now()
        if coupon:
            if (
                coupon.active
                and (not coupon.valid_from or coupon.valid_from <= now)
                and (not coupon.valid_to or coupon.valid_to >= now)
            ):
                if not coupon.max_uses or (coupon.used_count or 0) < coupon.max_uses:
                    discount = float(coupon.discount_percent or 0)
                    coupon_valid = True
                else:
                    coupon_msg = _("Cupom já atingiu o limite de uso")
            else:
                coupon_msg = _("Cupom inválido ou expirado")
        else:
            # Não é um Coupon — tenta como código de indicação (programa de
            # indicação). Mesmo parâmetro coupon_code, mesmo contrato de
            # retorno: nenhuma mudança necessária nos gateways de pagamento.
            from vedium_core.referrals import validate_referral_code

            referral = validate_referral_code(coupon_code, referee=frappe.session.user)
            if referral:
                discount = float(referral.discount_percent or 0)
                coupon_valid = True
            else:
                coupon_msg = _("Cupom inválido ou expirado")

    # M-03 fix: apply the discount to the course price before creating checkout
    # We pass the discounted price to the gateway instead of the full price
    final_price = float(course.course_price or 0)
    if coupon_valid and discount > 0:
        final_price = round(final_price * (1 - discount / 100), 2)
        # Temporarily override course_price so gateway uses discounted value
        course.course_price = final_price

    gateway_obj = get_gateway(gateway)
    checkout_url = gateway_obj.create_checkout(
        course,
        frappe.session.user,
        coupon_code=coupon_code if coupon_valid else None,
    )
    return {
        "checkout_url": checkout_url,
        "discount_percent": discount,
        "final_price": final_price,
        "coupon_valid": coupon_valid,
        "coupon_msg": coupon_msg,
    }


# =====================
# Cursos públicos e enrollment
# =====================


def create_enrollment_if_paid(
    course_name, user, gateway, payment_id, amount=None, currency=None,
    coupon_code=None,
):
    """
    Helper to create enrollment after successful payment.
    Consome 1 uso do cupom (se houver) — incremento atômico, só após
    pagamento confirmado, garantindo que max_uses seja respeitado.
    """
    if frappe.db.exists("LMS Enrollment", {"course": course_name, "member": user}):
        return

    enrollment = frappe.get_doc(
        {
            "doctype": "LMS Enrollment",
            "course": course_name,
            "member": user,
            "status": "Active",  # Or whatever status means 'Enrolled'
            "payment_gateway": gateway,
            "payment_reference": payment_id,
            "amount": amount,
            "currency": currency,
            "enrollment_date": frappe.utils.now_datetime(),
            # O preço do Stripe ja inclui o certificado/avaliacao -- sem isso,
            # o botao nativo "Get Certified" do LMS manda o aluno pra uma tela
            # de cobranca separada do proprio LMS (paid_certificate), cobrando
            # de novo por algo ja pago aqui. Ver docs/plataforma/04.
            "purchased_certificate": 1,
        }
    )
    enrollment.insert(ignore_permissions=True)

    if coupon_code and frappe.db.exists("Coupon", coupon_code):
        frappe.db.sql(
            """UPDATE `tabCoupon`
               SET used_count = COALESCE(used_count, 0) + 1
               WHERE name = %s""",
            (coupon_code,),
        )
    elif coupon_code and frappe.db.exists("Referral", coupon_code):
        from vedium_core.referrals import record_referral_conversion

        record_referral_conversion(coupon_code, user, course_name, enrollment.name)

    # E-mail de boas-vindas (na fila, nunca bloqueia/aborta a matrícula)
    try:
        course_title = (
            frappe.db.get_value("LMS Course", course_name, "title") or course_name
        )
        user_email = frappe.db.get_value("User", user, "email") or user
        first_name = frappe.db.get_value("User", user, "first_name") or ""
        frappe.sendmail(
            recipients=[user_email],
            subject=f"Matrícula confirmada — {course_title} | Vedium",
            message=f"""
                <h3>Bem-vindo(a){', ' + frappe.utils.escape_html(first_name) if first_name else ''}!</h3>
                <p>Seu pagamento foi confirmado e sua matrícula no curso
                <strong>{frappe.utils.escape_html(course_title)}</strong> está ativa.</p>
                <p><a href="https://app.vediums.com/lms/courses/{course_name}">
                Acessar o curso agora</a></p>
                <p>Qualquer dúvida, responda este e-mail ou escreva para
                contato@vediums.com.</p>
                <p>— Equipe Vedium</p>
            """,
        )
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.payments.enrollment_email"
        )

    frappe.msgprint(_("Inscrição realizada com sucesso!"))


@frappe.whitelist(allow_guest=True)
def get_published_courses(category=None, limit=10, start=0):
    """
    Retorna cursos publicados para o site público.
    Suporta paginação via `start` (offset). Usa JOIN único para evitar N+1.
    """
    category_filter = "AND c.category = %(category)s" if category else ""
    courses = frappe.db.sql(
        f"""
        SELECT
            c.name, c.title, c.short_introduction, c.image,
            c.paid_course, c.course_price, c.currency,
            c.category, c.status,
            u.full_name AS instructor_name,
            u.user_image AS instructor_image,
            COUNT(DISTINCT cl.name) AS lesson_count,
            COUNT(DISTINCT e.name)  AS enrollment_count
        FROM `tabLMS Course` c
        LEFT JOIN `tabCourse Instructor` ci ON ci.parent = c.name
        LEFT JOIN `tabUser` u ON u.name = ci.instructor
        LEFT JOIN `tabCourse Lesson` cl ON cl.course = c.name
        LEFT JOIN `tabLMS Enrollment` e ON e.course  = c.name
        WHERE c.published = 1
        {category_filter}
        GROUP BY c.name
        ORDER BY c.creation DESC
        LIMIT %(limit)s OFFSET %(start)s
        """,
        {"category": category, "limit": int(limit), "start": int(start)},
        as_dict=True,
    )
    for course in courses:
        course["url"] = f"/lms/courses/{course.name}"
    return courses


@frappe.whitelist(allow_guest=True)
def get_course_categories():
    """
    Get all course categories
    """
    categories = frappe.get_all(
        "LMS Category", filters={}, fields=["name", "category"], order_by="category"
    )
    return categories


@frappe.whitelist(allow_guest=True)
def get_featured_courses(limit=6, start=0):
    """
    Retorna cursos em destaque para a homepage.
    Ordena por matrículas DESC. Suporta paginação via `start`.
    """
    courses = frappe.db.sql(
        """
        SELECT
            c.name, c.title, c.short_introduction, c.image,
            c.paid_course, c.course_price, c.currency, c.category,
            COUNT(DISTINCT e.name) AS enrollment_count,
            COUNT(DISTINCT cl.name) AS lesson_count
        FROM `tabLMS Course` c
        LEFT JOIN `tabLMS Enrollment` e  ON e.course = c.name
        LEFT JOIN `tabCourse Lesson`   cl ON cl.course = c.name
        WHERE c.published = 1
        GROUP BY c.name
        ORDER BY enrollment_count DESC
        LIMIT %s OFFSET %s
        """,
        (int(limit), int(start)),
        as_dict=True,
    )
    for course in courses:
        course["url"] = f"/lms/courses/{course.name}"
    return courses


@frappe.whitelist()
def create_checkout_session(course_name):
    """
    Create a Stripe checkout session for course purchase.
    Requires logged-in user. Uses the gateway factory pattern.
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Por favor, faça login para comprar este curso"))

    course = frappe.get_doc("LMS Course", course_name)

    if not course.paid_course:
        frappe.throw(_("Este curso é gratuito"))

    # Check if already enrolled
    existing = frappe.db.exists(
        "LMS Enrollment", {"course": course_name, "member": frappe.session.user}
    )
    if existing:
        frappe.throw(_("Você já está inscrito neste curso"))

    # C-01 fix: use the gateway factory instead of the non-existent create_stripe_checkout()
    gateway_obj = get_gateway("stripe")
    checkout_url = gateway_obj.create_checkout(course, frappe.session.user)

    return {"checkout_url": checkout_url}


# =====================
# Payment Gateway Abstraction
# =====================
class PaymentGateway:
    def create_checkout(self, course, user, coupon_code=None):
        raise NotImplementedError

    def handle_webhook(self, data):
        raise NotImplementedError


class StripeGateway(PaymentGateway):
    def _get_api_key(self):
        key = frappe.conf.get("STRIPE_SECRET_KEY")
        if not key:
            frappe.throw(
                _("STRIPE_SECRET_KEY n\u00e3o configurado no site_config.json")
            )
        return key

    def create_checkout(self, course, user, coupon_code=None):
        import stripe

        stripe.api_key = self._get_api_key()

        user_email = frappe.get_value("User", user, "email") or user
        base_url = frappe.utils.get_url()
        currency = (getattr(course, "currency", None) or "BRL").lower()
        unit_amount = int(float(course.course_price or 0) * 100)  # centavos/cents

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {"name": course.title},
                        "unit_amount": unit_amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            customer_email=user_email,
            client_reference_id=f"{course.name}|{user}",
            success_url=(
                f"{base_url}/lms/courses/{course.name}"
                "?payment=success&session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=f"{base_url}/lms/courses/{course.name}?payment=cancelled",
            metadata={
                "course_name": course.name,
                "user": user,
                "site": frappe.local.site,
                "coupon_code": coupon_code or "",
            },
        )
        return session.url

    def handle_webhook(self, event):
        if event.get("type") == "checkout.session.completed":
            session = event.get("data", {}).get("object", {})
            ref = session.get("client_reference_id", "")
            coupon_code = (session.get("metadata") or {}).get("coupon_code") or None
            try:
                course_name, user = ref.split("|", 1)
                create_enrollment_if_paid(
                    course_name,
                    user,
                    "stripe",
                    session.get("payment_intent", ""),
                    amount=(session.get("amount_total") or 0) / 100,
                    currency=(session.get("currency") or "brl").upper(),
                    coupon_code=coupon_code,
                )
            except ValueError:
                frappe.log_error(
                    f"Stripe webhook: client_reference_id inv\u00e1lido: {ref}"
                )


class MercadoPagoGateway(PaymentGateway):
    def get_sdk(self):
        import mercadopago

        access_token = frappe.conf.get("MERCADOPAGO_ACCESS_TOKEN")
        if not access_token:
            frappe.throw(_("MERCADOPAGO_ACCESS_TOKEN não configurado"))
        return mercadopago.SDK(access_token)

    def create_checkout(self, course, user, coupon_code=None):
        sdk = self.get_sdk()

        preference_data = {
            "items": [
                {
                    "title": course.title,
                    "quantity": 1,
                    "unit_price": float(course.course_price),
                    "currency_id": course.currency or "BRL",
                }
            ],
            "payer": {"email": user},
            "back_urls": {
                "success": f"{frappe.utils.get_url()}/lms/enrollment/success",
                "failure": f"{frappe.utils.get_url()}/lms/enrollment/failure",
                "pending": f"{frappe.utils.get_url()}/lms/enrollment/pending",
            },
            "auto_return": "approved",
            # Formato: course|user[|coupon] — webhook aceita 2 ou 3 segmentos
            "external_reference": f"{course.name}|{user}|{coupon_code or ''}",
        }

        preference_response = sdk.preference().create(preference_data)
        response = preference_response.get("response", {})

        # Prefer sandbox for testing if configured, else init_point
        return (
            response.get("sandbox_init_point")
            if frappe.conf.get("DEVELOPER_MODE")
            else response.get("init_point")
        )

    def handle_webhook(self, data):
        # Mercado Pago sends topic/type and id
        topic = data.get("topic") or data.get("type")
        resource_id = data.get("id") or data.get("data", {}).get("id")

        if topic == "payment" and resource_id:
            sdk = self.get_sdk()
            payment_info = sdk.payment().get(resource_id)
            if payment_info["status"] == 200:
                payment = payment_info["response"]
                status = payment.get("status")
                external_ref = payment.get("external_reference")

                if status == "approved" and external_ref:
                    try:
                        # 2 segmentos (legado) ou 3 (com cupom)
                        parts = external_ref.split("|")
                        if len(parts) < 2:
                            raise ValueError(external_ref)
                        course_name, user = parts[0], parts[1]
                        coupon_code = parts[2] if len(parts) > 2 and parts[2] else None
                        create_enrollment_if_paid(
                            course_name,
                            user,
                            "mercadopago",
                            str(resource_id),
                            amount=payment.get("transaction_amount"),
                            currency=payment.get("currency_id"),
                            coupon_code=coupon_code,
                        )
                    except ValueError:
                        frappe.log_error(
                            "Invalid external_reference in MercadoPago Webhook"
                        )


class BasecommerceGateway(PaymentGateway):
    def create_checkout(self, course, user, coupon_code=None):
        # TODO: Integrar com Basecommerce API
        return f"/lms/courses/{course.name}/enroll-basecommerce"

    def handle_webhook(self, data):
        # TODO: Lógica de webhook Basecommerce
        pass


class CryptoGateway(PaymentGateway):
    def create_checkout(self, course, user, coupon_code=None):
        from vedium_core.services.crypto_service import CryptoService

        service = CryptoService()
        charge = service.create_charge(
            course.course_price, course.currency or "USD", user
        )
        url = charge.get("hosted_url")
        if not url:
            frappe.throw(
                _("Pagamento em criptomoeda indisponível no momento"),
            )
        return url

    def handle_webhook(self, data):
        # M-08: Explicitly raise NotImplementedError — crypto webhooks are not yet handled.
        # Prevents enrollments from being silently skipped.
        # TODO: Implement Coinbase Commerce HMAC verification and enrollment creation.
        raise NotImplementedError(
            "CryptoGateway.handle_webhook is not yet implemented. "
            "Implement Coinbase Commerce HMAC verification before enabling crypto webhooks."
        )


def get_gateway(gateway_name):
    if gateway_name == "stripe":
        return StripeGateway()
    elif gateway_name == "mercadopago":
        return MercadoPagoGateway()
    elif gateway_name == "basecommerce":
        return BasecommerceGateway()
    elif gateway_name == "crypto":
        # Coinbase Commerce ainda não está integrado de verdade (mock).
        # Só habilita com flag explícita + API key — evita URL falsa em prod.
        if not (
            frappe.conf.get("CRYPTO_ENABLED") and frappe.conf.get("CRYPTO_API_KEY")
        ):
            frappe.throw(_("Gateway de pagamento não configurado"), frappe.ValidationError)
        return CryptoGateway()
    else:
        frappe.throw(
            _("Gateway de pagamento não suportado: {0}").format(gateway_name),
            frappe.ValidationError,
        )


# =====================
# Webhook dedicado Stripe (processa raw JSON body com verificação de assinatura)
# =====================
@frappe.whitelist(allow_guest=True)
def stripe_webhook():
    """
    Endpoint exclusivo para webhooks do Stripe.
    URL: /api/method/vedium_core.api.stripe_webhook
    Registrar no Stripe Dashboard → Developers → Webhooks.
    Eventos: checkout.session.completed

    Segurança: em produção (DEVELOPER_MODE=0), STRIPE_WEBHOOK_SECRET é
    obrigatório. Sem segredo configurado em produção → 401.
    """
    import stripe

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY", "")
    payload = frappe.request.get_data(as_text=True)
    sig_header = frappe.request.headers.get("Stripe-Signature")
    webhook_secret = frappe.conf.get("STRIPE_WEBHOOK_SECRET")
    is_dev = bool(frappe.conf.get("developer_mode") or frappe.conf.get("DEVELOPER_MODE"))

    if not webhook_secret:
        # Em produção, segredo ausente é falha de configuração crítica
        if not is_dev:
            frappe.log_error(
                "STRIPE_WEBHOOK_SECRET ausente em produção — webhook rejeitado",
                "Vedium.payments.stripe_webhook",
            )
            frappe.throw(
                _("Webhook não configurado corretamente"),
                frappe.AuthenticationError,
            )
        # Em dev: aceita sem verificar, mas loga
        frappe.log_error(
            "STRIPE_WEBHOOK_SECRET ausente (DEV) — webhook não verificado",
            "Vedium.payments.stripe_webhook",
        )

    if webhook_secret and not sig_header:
        frappe.throw(
            _("Stripe-Signature header obrigatório"),
            frappe.AuthenticationError,
        )

    try:
        if webhook_secret and sig_header:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            event = stripe.Event.construct_from(
                frappe.parse_json(payload), stripe.api_key
            )
    except stripe.error.SignatureVerificationError as e:
        frappe.log_error(
            f"Stripe webhook signature inválida: {e}",
            "Vedium.payments.stripe_webhook",
        )
        frappe.throw(_("Webhook signature inválida"), frappe.AuthenticationError)
    except Exception as e:
        frappe.log_error(
            f"Stripe webhook parse error: {e}",
            "Vedium.payments.stripe_webhook",
        )
        frappe.throw(_("Webhook inválido"), frappe.AuthenticationError)

    gateway_obj = StripeGateway()
    gateway_obj.handle_webhook(event)
    return {"status": "ok"}


# =====================
# Funções de checkout para cada gateway
# =====================
@frappe.whitelist()
def create_mercadopago_checkout(course_name):
    """
    [DEPRECATED] Use `create_checkout(course_name, gateway='mercadopago')` em vez disto.
    Mantido por compatibilidade com clientes antigos. Será removido na v2.
    """
    frappe.log_error(
        f"create_mercadopago_checkout chamado para {course_name} — migrar para create_checkout",
        "Vedium.api.deprecated",
    )
    return create_checkout(course_name, gateway="mercadopago")


@frappe.whitelist()
def create_basecommerce_checkout(course_name):
    """
    [DEPRECATED] Use `create_checkout(course_name, gateway='basecommerce')` em vez disto.
    Mantido por compatibilidade com clientes antigos. Será removido na v2.
    """
    frappe.log_error(
        f"create_basecommerce_checkout chamado para {course_name} — migrar para create_checkout",
        "Vedium.api.deprecated",
    )
    return create_checkout(course_name, gateway="basecommerce")


# =====================
# Webhook centralizado
# =====================
def _is_dev_mode() -> bool:
    return bool(
        frappe.conf.get("developer_mode") or frappe.conf.get("DEVELOPER_MODE")
    )


def _require_webhook_secret(secret_name: str, gateway: str) -> str:
    """Em produção, exige o segredo configurado. Em dev, permite ausente."""
    secret = frappe.conf.get(secret_name)
    if not secret:
        if not _is_dev_mode():
            frappe.log_error(
                f"{secret_name} ausente em produção — webhook rejeitado",
                f"Vedium.payments.{gateway}_webhook",
            )
            frappe.throw(
                _("Webhook não configurado corretamente"),
                frappe.AuthenticationError,
            )
        frappe.log_error(
            f"{secret_name} ausente (DEV) — webhook não verificado",
            f"Vedium.payments.{gateway}_webhook",
        )
    return secret or ""


@frappe.whitelist(allow_guest=True)
def handle_payment_webhook(gateway=None):
    """
    Centraliza webhooks de pagamento para todos os gateways.
    Verifica assinatura HMAC antes de processar qualquer evento.

    Em produção (DEVELOPER_MODE=0), segredo HMAC do gateway é obrigatório.
    """
    import hashlib
    import hmac

    data = frappe.local.form_dict or {}
    if not gateway:
        gateway = data.get("gateway")
    if not gateway:
        frappe.throw(_("Gateway não informado"))

    if gateway == "mercadopago":
        sig_header = frappe.request.headers.get("X-Signature", "")
        webhook_secret = _require_webhook_secret(
            "MERCADOPAGO_WEBHOOK_SECRET", "mercadopago"
        )
        if webhook_secret:
            if not sig_header:
                frappe.throw(
                    _("X-Signature header obrigatório"),
                    frappe.AuthenticationError,
                )
            try:
                parts = {
                    k: v
                    for k, v in (p.split("=", 1) for p in sig_header.split(","))
                }
                ts = parts.get("ts", "")
                v1 = parts.get("v1", "")
                data_id = data.get("data", {}).get("id", data.get("id", ""))
                request_id = frappe.request.headers.get("X-Request-Id", "")
                manifest = f"id:{data_id};request-id:{request_id};ts:{ts}"
                expected = hmac.new(
                    webhook_secret.encode(), manifest.encode(), hashlib.sha256
                ).hexdigest()
                if not hmac.compare_digest(expected, v1):
                    frappe.throw(
                        _("Webhook signature inválida"),
                        frappe.AuthenticationError,
                    )
            except frappe.AuthenticationError:
                raise
            except Exception as e:
                frappe.log_error(
                    f"MercadoPago webhook signature check failed: {e}",
                    "Vedium.payments.mercadopago_webhook",
                )
                frappe.throw(
                    _("Webhook signature inválida"),
                    frappe.AuthenticationError,
                )

    elif gateway == "stripe":
        sig_header = frappe.request.headers.get("Stripe-Signature")
        stripe_secret = _require_webhook_secret("STRIPE_WEBHOOK_SECRET", "stripe")
        if stripe_secret:
            if not sig_header:
                frappe.throw(
                    _("Stripe-Signature header obrigatório"),
                    frappe.AuthenticationError,
                )
            try:
                import stripe

                payload = frappe.request.get_data(as_text=True)
                stripe.Webhook.construct_event(payload, sig_header, stripe_secret)
            except frappe.AuthenticationError:
                raise
            except Exception as e:
                frappe.log_error(
                    f"Stripe webhook signature check failed: {e}",
                    "Vedium.payments.stripe_webhook",
                )
                frappe.throw(
                    _("Webhook signature inválida"),
                    frappe.AuthenticationError,
                )

    elif gateway == "crypto":
        # CryptoGateway.handle_webhook ainda não implementa verificação HMAC
        # do Coinbase Commerce. Em produção, falhamos cedo para não criar
        # matrículas baseadas em payload não verificado.
        if not _is_dev_mode():
            frappe.log_error(
                "Webhook crypto recebido mas handler ainda não implementa "
                "verificação HMAC do Coinbase Commerce",
                "Vedium.payments.crypto_webhook",
            )
            frappe.throw(
                _("Gateway crypto não habilitado para webhooks em produção"),
                frappe.AuthenticationError,
            )

    gateway_obj = get_gateway(gateway)
    gateway_obj.handle_webhook(data)
    return {"status": "ok"}


@frappe.whitelist()
def create_crypto_checkout(course_name):
    if frappe.session.user == "Guest":
        frappe.throw(_("Por favor, faça login para comprar este curso"))
    course = frappe.get_doc("LMS Course", course_name)
    if not course.paid_course:
        frappe.throw(_("Este curso é gratuito"))
    existing = frappe.db.exists(
        "LMS Enrollment", {"course": course_name, "member": frappe.session.user}
    )
    if existing:
        frappe.throw(_("Você já está inscrito neste curso"))
    gateway = get_gateway("crypto")
    checkout_url = gateway.create_checkout(course, frappe.session.user)
    return {"checkout_url": checkout_url}
