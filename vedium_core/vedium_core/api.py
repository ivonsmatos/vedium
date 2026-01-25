# =====================
# Observabilidade e Suporte
# =====================
@frappe.whitelist()
def open_support_ticket(subject, description, category=None):
    """
    Abre um chamado de suporte para o usuário logado
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Faça login para abrir um chamado"))
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
    if frappe.session.user == "Guest":
        frappe.throw(_("Faça login para ver seus chamados"))
    tickets = frappe.get_all(
        "Support Ticket",
        filters={"opened_by": frappe.session.user},
        fields=["name", "subject", "status", "creation", "category"],
    )
    return tickets


@frappe.whitelist()
def get_monitoring_dashboard():
    """
    Dashboard interno: status de containers, disco, memória, alertas críticos
    """
    # Exemplo: busca logs recentes e status de containers (mock)
    import random

    return {
        "containers": [
            {"name": "vedium-frappe", "status": "running"},
            {"name": "vedium-mariadb", "status": "running"},
            {"name": "vedium-redis", "status": "running"},
        ],
        "disk_usage": f"{random.randint(40, 80)}%",
        "memory_usage": f"{random.randint(30, 75)}%",
        "alerts": [
            {"type": "info", "msg": "Backup diário concluído"},
            {"type": "warning", "msg": "Uso de disco acima de 70%"},
        ],
    }


# =====================
# Gamificação, comunidade e internacionalização/acessibilidade
# =====================
@frappe.whitelist()
def get_user_badges():
    """
    Retorna emblemas e nível do usuário logado
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Faça login para ver seus emblemas"))
    badges = frappe.get_all(
        "LMS Badge Log",
        filters={"user": frappe.session.user},
        fields=["badge", "level", "awarded_on"],
    )
    return badges


@frappe.whitelist(allow_guest=True)
def get_leaderboard(course_name):
    """
    Retorna ranking de alunos do curso
    """
    leaderboard = frappe.db.sql(
        """
        SELECT member, score, completed_on FROM `tabLMS Enrollment`
        WHERE course=%s AND status='Completed'
        ORDER BY score DESC, completed_on ASC LIMIT 20
    """,
        (course_name,),
        as_dict=True,
    )
    return leaderboard


@frappe.whitelist(allow_guest=True)
def get_forum_topics(course_name):
    """
    Retorna tópicos do fórum do curso
    """
    topics = frappe.get_all(
        "LMS Forum Topic",
        filters={"course": course_name},
        fields=["name", "title", "created_by", "creation"],
    )
    return topics


@frappe.whitelist(allow_guest=True)
def get_community_links(course_name):
    """
    Retorna links de comunidade (Telegram, Discord, Slack) do curso
    """
    links = frappe.get_all(
        "LMS Community Link",
        filters={"course": course_name},
        fields=["platform", "url"],
    )
    return links


@frappe.whitelist(allow_guest=True)
def get_course_languages(course_name):
    """
    Retorna idiomas disponíveis para o curso (para internacionalização)
    """
    langs = frappe.get_all(
        "LMS Course Language",
        filters={"course": course_name},
        fields=["language_code", "language_name"],
    )
    return langs


@frappe.whitelist(allow_guest=True)
def get_accessibility_features(course_name):
    """
    Retorna recursos de acessibilidade do curso (legenda, audiodescrição, contraste, navegação por teclado)
    """
    features = frappe.get_all(
        "LMS Accessibility Feature",
        filters={"course": course_name},
        fields=["feature", "enabled"],
    )
    return features


# =====================
# Aulas ao vivo/gravadas e recursos extras
# =====================
@frappe.whitelist(allow_guest=True)
def get_course_sessions(course_name):
    """
    Retorna lista de sessões (ao vivo ou gravadas) do curso, com links (Zoom, Meet, Vimeo/Youtube)
    """
    sessions = frappe.get_all(
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
    return sessions


# Recursos extras: escuta ativa, gravação de áudio, flashcards (placeholders)
@frappe.whitelist()
def submit_listening_exercise(course_name, audio_url):
    """
    Recebe áudio do aluno para exercício de escuta ativa
    """
    # Aqui seria feita a análise de IA/feedback
    return {"status": "received", "audio_url": audio_url}


@frappe.whitelist()
def submit_speaking_exercise(course_name, audio_url):
    """
    Recebe áudio do aluno para exercício de fala
    """
    # Aqui seria feita a análise de IA/feedback
    return {"status": "received", "audio_url": audio_url}


@frappe.whitelist(allow_guest=True)
def get_flashcards(course_name):
    """
    Retorna flashcards do curso
    """
    cards = frappe.get_all(
        "LMS Flashcard", filters={"course": course_name}, fields=["front", "back"]
    )
    return cards


# =====================
# Quiz/Prova de nível com feedback instantâneo
# =====================
@frappe.whitelist()
def submit_quiz_attempt(course_name, answers):
    """
    Recebe respostas do quiz de nivelamento e retorna feedback instantâneo
    answers: dict {question_id: resposta}
    """
    # Exemplo: busca questões e respostas corretas
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
import hashlib
import random
import string
from datetime import datetime


@frappe.whitelist()
def issue_certificate(enrollment_name):
    """
    Emite certificado digital para uma inscrição concluída, com código de verificação público
    """
    enrollment = frappe.get_doc("LMS Enrollment", enrollment_name)
    if enrollment.status != "Completed":
        frappe.throw(_("Curso ainda não concluído"))
    # Gera código único baseado em dados do aluno, curso e data
    base = f"{enrollment.member}-{enrollment.course}-{enrollment.completion_date or datetime.now()}"
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
    cert.insert(ignore_permissions=True, ignore_if_duplicate=True)
    return {
        "certificate_id": cert.name,
        "verification_code": code,
        "verify_url": f"/certificado/{code}",
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
def get_payment_history():
    """
    Retorna histórico de pagamentos/faturas do usuário logado
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Faça login para ver seu histórico de pagamentos"))
    # Exemplo: buscar inscrições pagas e dados de pagamento
    enrollments = frappe.get_all(
        "LMS Enrollment",
        filters={"member": frappe.session.user},
        fields=[
            "name",
            "course",
            "creation",
            "status",
            "payment_gateway",
            "payment_reference",
            "amount",
            "currency",
        ],
    )
    # Enriquecer com nome do curso
    for e in enrollments:
        e["course_title"] = frappe.db.get_value("LMS Course", e["course"], "title")
    return enrollments


# =====================
# Endpoint central para seleção de gateway no checkout
# =====================
@frappe.whitelist()
def create_checkout(course_name, gateway, coupon_code=None):
    """
    Cria checkout para o gateway selecionado pelo usuário, com suporte a cupons
    """
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
        from datetime import datetime

        now = datetime.now()
        if (
            coupon
            and coupon.active
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

    gateway_obj = get_gateway(gateway)
    checkout_url = gateway_obj.create_checkout(course, frappe.session.user)
    return {
        "checkout_url": checkout_url,
        "discount_percent": discount,
        "coupon_valid": coupon_valid,
        "coupon_msg": coupon_msg,
    }


# -*- coding: utf-8 -*-
# Vedium Core - Courses API
# API endpoints for the public website

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_published_courses(category=None, limit=10):
    """
    Get published courses for the public website
    Returns courses from LMS with basic info for display
    """
    filters = {"published": 1}
    if category:
        filters["category"] = category

    courses = frappe.get_all(
        "LMS Course",
        filters=filters,
        fields=[
            "name",
            "title",
            "short_introduction",
            "image",
            "paid_course",
            "course_price",
            "currency",
            "category",
            "status",
        ],
        order_by="creation desc",
        limit_page_length=limit,
    )

    # Enrich with additional data
    for course in courses:
        # Get instructor info
        instructors = frappe.get_all(
            "Course Instructor",
            filters={"parent": course.name},
            fields=["instructor"],
            limit=1,
        )
        if instructors:
            instructor_user = frappe.get_value(
                "User", instructors[0].instructor, ["full_name", "user_image"]
            )
            course["instructor_name"] = instructor_user[0] if instructor_user else None
            course["instructor_image"] = instructor_user[1] if instructor_user else None

        # Get lesson count
        course["lesson_count"] = frappe.db.count(
            "Course Lesson", {"course": course.name}
        )

        # Get enrollment count
        course["enrollment_count"] = frappe.db.count(
            "LMS Enrollment", {"course": course.name}
        )

        # Course URL
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
def get_featured_courses(limit=6):
    """
    Get featured/popular courses for homepage
    """
    # Get courses with most enrollments
    courses = frappe.db.sql(
        """
        SELECT 
            c.name,
            c.title,
            c.short_introduction,
            c.image,
            c.paid_course,
            c.course_price,
            c.currency,
            c.category,
            COUNT(e.name) as enrollment_count
        FROM `tabLMS Course` c
        LEFT JOIN `tabLMS Enrollment` e ON c.name = e.course
        WHERE c.published = 1
        GROUP BY c.name
        ORDER BY enrollment_count DESC
        LIMIT %s
    """,
        (limit,),
        as_dict=True,
    )

    for course in courses:
        course["url"] = f"/lms/courses/{course.name}"
        course["lesson_count"] = frappe.db.count(
            "Course Lesson", {"course": course.name}
        )

    return courses


@frappe.whitelist()
def create_checkout_session(course_name):
    """
    Create a Stripe checkout session for course purchase
    Requires logged-in user
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to purchase this course"))

    course = frappe.get_doc("LMS Course", course_name)

    if not course.paid_course:
        frappe.throw(_("This is a free course"))

    # Check if already enrolled
    existing = frappe.db.exists(
        "LMS Enrollment", {"course": course_name, "member": frappe.session.user}
    )
    if existing:
        frappe.throw(_("You are already enrolled in this course"))

    # Create Stripe checkout (placeholder - needs Stripe config)
    checkout_url = create_stripe_checkout(course)

    return {"checkout_url": checkout_url}


# =====================
# Payment Gateway Abstraction
# =====================
class PaymentGateway:
    def create_checkout(self, course, user):
        raise NotImplementedError

    def handle_webhook(self, data):
        raise NotImplementedError


class StripeGateway(PaymentGateway):
    def create_checkout(self, course, user):
        # Placeholder Stripe logic
        return f"/lms/courses/{course.name}/enroll"

    def handle_webhook(self, data):
        # Stripe webhook logic
        pass


class MercadoPagoGateway(PaymentGateway):
    def create_checkout(self, course, user):
        # TODO: Integrar com Mercado Pago API
        return f"/lms/courses/{course.name}/enroll-mercadopago"

    def handle_webhook(self, data):
        # TODO: Lógica de webhook Mercado Pago
        pass


class BasecommerceGateway(PaymentGateway):
    def create_checkout(self, course, user):
        # TODO: Integrar com Basecommerce API
        return f"/lms/courses/{course.name}/enroll-basecommerce"

    def handle_webhook(self, data):
        # TODO: Lógica de webhook Basecommerce
        pass


def get_gateway(gateway_name):
    if gateway_name == "stripe":
        return StripeGateway()
    elif gateway_name == "mercadopago":
        return MercadoPagoGateway()
    elif gateway_name == "basecommerce":
        return BasecommerceGateway()
    else:
        raise Exception("Gateway não suportado")


# =====================
# Funções de checkout para cada gateway
# =====================
@frappe.whitelist()
def create_mercadopago_checkout(course_name):
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
    gateway = get_gateway("mercadopago")
    checkout_url = gateway.create_checkout(course, frappe.session.user)
    return {"checkout_url": checkout_url}


@frappe.whitelist()
def create_basecommerce_checkout(course_name):
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
    gateway = get_gateway("basecommerce")
    checkout_url = gateway.create_checkout(course, frappe.session.user)
    return {"checkout_url": checkout_url}


# =====================
# Webhook centralizado
# =====================
@frappe.whitelist(allow_guest=True)
def handle_payment_webhook(gateway=None):
    """
    Centraliza webhooks de pagamento para todos os gateways
    """
    import json

    data = frappe.local.form_dict or {}
    if not gateway:
        gateway = data.get("gateway")
    if not gateway:
        frappe.throw(_("Gateway não informado"))
    gateway_obj = get_gateway(gateway)
    gateway_obj.handle_webhook(data)
    return {"status": "ok"}


@frappe.whitelist(allow_guest=True)
def handle_payment_webhook():
    """
    Handle Stripe payment webhook
    Creates enrollment on successful payment
    """
    # Webhook handling logic
    # 1. Verify webhook signature
    # 2. Extract payment data
    # 3. Create LMS Enrollment
    # 4. Create Customer in ERPNext
    # 5. Send confirmation email
    pass
