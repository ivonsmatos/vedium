# -*- coding: utf-8 -*-
# Vedium Core — API pública e endpoints internos
# Imports pesados (prometheus_client, mercadopago, services.*) ficam lazy
# dentro das funções que os usam, para o módulo carregar mesmo sem essas
# dependências instaladas.

import hashlib
from datetime import datetime

import frappe
from frappe import _


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
    return {"success": True}


@frappe.whitelist()
def open_support_ticket(subject, description, category=None):
    """
    Abre um chamado de suporte para o usuário logado
    """
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


@frappe.whitelist()
def get_metrics():
    """
    Expõe métricas do Prometheus.
    Requer autenticação. Em produção, adicionalmente proteger via nginx
    (auth_basic) ou liberar apenas para IPs internos do scraper.
    """
    if not _user_can_view_metrics():
        frappe.throw(_("Permissão negada"), frappe.PermissionError)

    from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

    frappe.response["result"] = generate_latest()
    frappe.response["type"] = "binary"
    frappe.response["content_type"] = CONTENT_TYPE_LATEST


def _user_can_view_metrics() -> bool:
    if frappe.session.user == "Guest":
        return False
    roles = set(frappe.get_roles(frappe.session.user))
    return bool(roles & {"System Manager", "Administrator", "Vedium Ops"})


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
    Recebe respostas do quiz de nivelamento e retorna feedback instantâneo.
    answers: dict {question_id: resposta} — Frappe envia como string JSON, parseado aqui.
    """
    import json

    # M-07 fix: Frappe passes whitelisted dict params as JSON strings
    if isinstance(answers, str):
        try:
            answers = json.loads(answers)
        except (ValueError, TypeError):
            frappe.throw(_("Formato de respostas inválido"))

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

    # M-03 fix: apply the discount to the course price before creating checkout
    # We pass the discounted price to the gateway instead of the full price
    final_price = float(course.course_price or 0)
    if coupon_valid and discount > 0:
        final_price = round(final_price * (1 - discount / 100), 2)
        # Temporarily override course_price so gateway uses discounted value
        course.course_price = final_price

    gateway_obj = get_gateway(gateway)
    checkout_url = gateway_obj.create_checkout(course, frappe.session.user)
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
    course_name, user, gateway, payment_id, amount=None, currency=None
):
    """
    Helper to create enrollment after successful payment
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
        }
    )
    enrollment.insert(ignore_permissions=True)
    frappe.msgprint(_("Inscrição realizada com sucesso!"))


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
    def create_checkout(self, course, user):
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

    def create_checkout(self, course, user):
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
            },
        )
        return session.url

    def handle_webhook(self, event):
        if event.get("type") == "checkout.session.completed":
            session = event.get("data", {}).get("object", {})
            ref = session.get("client_reference_id", "")
            try:
                course_name, user = ref.split("|", 1)
                create_enrollment_if_paid(
                    course_name,
                    user,
                    "stripe",
                    session.get("payment_intent", ""),
                    amount=(session.get("amount_total") or 0) / 100,
                    currency=(session.get("currency") or "brl").upper(),
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

    def create_checkout(self, course, user):
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
            "external_reference": f"{course.name}|{user}",
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
                        course_name, user = external_ref.split("|")
                        create_enrollment_if_paid(
                            course_name,
                            user,
                            "mercadopago",
                            str(resource_id),
                            amount=payment.get("transaction_amount"),
                            currency=payment.get("currency_id"),
                        )
                    except ValueError:
                        frappe.log_error(
                            "Invalid external_reference in MercadoPago Webhook"
                        )


class BasecommerceGateway(PaymentGateway):
    def create_checkout(self, course, user):
        # TODO: Integrar com Basecommerce API
        return f"/lms/courses/{course.name}/enroll-basecommerce"

    def handle_webhook(self, data):
        # TODO: Lógica de webhook Basecommerce
        pass


class CryptoGateway(PaymentGateway):
    def create_checkout(self, course, user):
        from vedium_core.services.crypto_service import CryptoService

        service = CryptoService()
        charge = service.create_charge(
            course.course_price, course.currency or "USD", user
        )
        return charge.get("hosted_url")

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
        return CryptoGateway()
    else:
        raise Exception("Gateway não suportado")


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
    """
    import stripe

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY", "")
    payload = frappe.request.get_data(as_text=True)
    sig_header = frappe.request.headers.get("Stripe-Signature")
    webhook_secret = frappe.conf.get("STRIPE_WEBHOOK_SECRET")

    if webhook_secret and not sig_header:
        frappe.throw(_("Stripe-Signature header obrigatório"), frappe.AuthenticationError)

    try:
        if webhook_secret and sig_header:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            # Sem segredo configurado: aceita em modo desenvolvimento (log de aviso)
            frappe.log_error(
                "STRIPE_WEBHOOK_SECRET não configurado — webhook não verificado",
                "Stripe Webhook Warning",
            )
            event = stripe.Event.construct_from(
                frappe.parse_json(payload), stripe.api_key
            )
    except stripe.error.SignatureVerificationError as e:
        frappe.log_error(f"Stripe webhook signature inválida: {e}")
        frappe.throw(_("Webhook signature inválida"), frappe.AuthenticationError)
    except Exception as e:
        frappe.log_error(f"Stripe webhook parse error: {e}")
        frappe.throw(_("Webhook inválido"), frappe.AuthenticationError)

    gateway_obj = StripeGateway()
    gateway_obj.handle_webhook(event)
    return {"status": "ok"}


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
    Centraliza webhooks de pagamento para todos os gateways.
    C-03 fix: verifica assinatura HMAC antes de processar qualquer evento.
    """
    import hashlib
    import hmac

    data = frappe.local.form_dict or {}
    if not gateway:
        gateway = data.get("gateway")
    if not gateway:
        frappe.throw(_("Gateway não informado"))

    # --- C-03: HMAC signature verification ---
    if gateway == "mercadopago":
        # MercadoPago sends X-Signature header: "ts=<timestamp>,v1=<hmac_sha256>"
        sig_header = frappe.request.headers.get("X-Signature", "")
        webhook_secret = frappe.conf.get("MERCADOPAGO_WEBHOOK_SECRET")
        if webhook_secret and sig_header:
            try:
                parts = {
                    k: v for k, v in (p.split("=", 1) for p in sig_header.split(","))
                }
                ts = parts.get("ts", "")
                v1 = parts.get("v1", "")
                # MercadoPago manifest: HMAC of "id:<payment_id>;request-id:<req_id>;ts:<ts>"
                data_id = data.get("data", {}).get("id", data.get("id", ""))
                request_id = frappe.request.headers.get("X-Request-Id", "")
                manifest = f"id:{data_id};request-id:{request_id};ts:{ts}"
                expected = hmac.new(
                    webhook_secret.encode(), manifest.encode(), hashlib.sha256
                ).hexdigest()
                if not hmac.compare_digest(expected, v1):
                    frappe.throw(
                        _("Webhook signature inválida"), frappe.AuthenticationError
                    )
            except Exception as e:
                frappe.log_error(f"MercadoPago webhook signature check failed: {e}")
                frappe.throw(
                    _("Webhook signature inválida"), frappe.AuthenticationError
                )

    elif gateway == "stripe":
        # Stripe sends Stripe-Signature header for HMAC verification
        sig_header = frappe.request.headers.get("Stripe-Signature")
        stripe_secret = frappe.conf.get("STRIPE_WEBHOOK_SECRET")
        if stripe_secret and sig_header:
            try:
                import stripe

                payload = frappe.request.get_data(as_text=True)
                stripe.Webhook.construct_event(payload, sig_header, stripe_secret)
            except Exception as e:
                frappe.log_error(f"Stripe webhook signature check failed: {e}")
                frappe.throw(
                    _("Webhook signature inválida"), frappe.AuthenticationError
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


# =====================
# PWA Analytics Tracking
# =====================
@frappe.whitelist()
def track_pwa_install():
    """
    A-04 fix: Track PWA installation event.
    Called by pwa-register.js when the user installs the app.
    """
    if frappe.session.user == "Guest":
        return {"status": "ok", "tracked": False}

    try:
        frappe.log(f"Vedium: PWA installed by user {frappe.session.user}")
        # Optionally store in a custom log or fire a server-side analytics event
        return {"status": "ok", "tracked": True, "user": frappe.session.user}
    except Exception as e:
        frappe.log_error(f"track_pwa_install error: {e}")
        return {"status": "error"}
