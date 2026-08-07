import frappe
from frappe import _

# NOTA: estas funções MONTAM o payload do evento (GTM dataLayer / GA4);
# o disparo é client-side. Nada é enviado ao GA4 daqui.


def _get_published_course(course_name):
    """Carrega curso garantindo que está publicado (evita vazar rascunhos)."""
    course = frappe.get_doc("LMS Course", course_name)
    if not course.published:
        frappe.throw(_("Curso não encontrado"), frappe.DoesNotExistError)
    return course


def track_course_view(course_name):
    """
    Rastreia visualização de curso
    """
    course = _get_published_course(course_name)
    
    event_data = {
        'event': 'view_course',
        'course_name': course.title,
        'course_category': course.category or "Geral",
        'course_price': float(course.course_price or 0),
        'currency': course.currency or 'BRL',
        'course_id': course.name
    }
    
    return event_data

def track_course_enrollment(course_name, user_email, payment_method=None):
    """
    Rastreia inscrição em curso
    """
    course = _get_published_course(course_name)
    
    event_data = {
        'event': 'enroll_course',
        'course_name': course.title,
        'course_price': float(course.course_price or 0),
        'currency': course.currency or 'BRL',
        'payment_method': payment_method or 'free',
        'user_email': user_email
    }
    
    return event_data

def track_purchase(transaction_id, course_name, amount, currency='BRL', payment_method='credit_card'):
    """
    Rastreia compra concluída
    """
    course = _get_published_course(course_name)

    event_data = {
        'event': 'purchase',
        'transaction_id': transaction_id,
        'value': float(amount),
        'currency': currency,
        'payment_method': payment_method,
        'items': [{
            'item_name': course.title,
            'item_category': course.category or "Curso",
            'price': float(amount),
            'quantity': 1
        }]
    }
    
    return event_data

def send_ga4_purchase_server_side(transaction_id, course_name, amount, currency='BRL', client_id=None):
    """Envia o evento `purchase` ao GA4 via Measurement Protocol (server-side),
    disparado pelo webhook Stripe após a matrícula — garante que a venda
    concluída vire conversão no GA4, independente do client-side.

    No-op se GA4_MEASUREMENT_ID / GA4_API_SECRET não estiverem no site_config.
    Roda em background (enqueue) e engole erros para nunca afetar a matrícula.
    """
    measurement_id = frappe.conf.get("GA4_MEASUREMENT_ID")
    api_secret = frappe.conf.get("GA4_API_SECRET")
    if not measurement_id or not api_secret:
        return  # GA4 server-side não configurado

    # client_id ideal = _ga do navegador (capturado no checkout p/ atribuição);
    # fallback determinístico por transação para não perder a conversão.
    if not client_id:
        client_id = f"vedium.{transaction_id}"

    payload = track_purchase(transaction_id, course_name, amount, currency)
    body = {
        "client_id": client_id,
        "non_personalized_ads": False,
        "events": [{
            "name": "purchase",
            "params": {
                "transaction_id": transaction_id,
                "value": float(amount),
                "currency": currency,
                "items": payload["items"],
            },
        }],
    }
    try:
        import requests
        requests.post(
            "https://www.google-analytics.com/mp/collect"
            f"?measurement_id={measurement_id}&api_secret={api_secret}",
            json=body,
            timeout=10,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "GA4 purchase (Measurement Protocol) falhou")


def track_lesson_completion(course_name, lesson_name, progress_percentage):
    """
    Rastreia conclusão de lição
    """
    event_data = {
        'event': 'complete_lesson',
        'course_name': course_name,
        'lesson_name': lesson_name,
        'progress_percentage': progress_percentage
    }
    
    return event_data

@frappe.whitelist()
def send_analytics_event(event_type, **kwargs):
    """
    API endpoint para enviar eventos de analytics
    
    Uso:
    frappe.call({
        method: 'vedium_core.analytics_events.send_analytics_event',
        args: {
            event_type: 'view_course',
            course_name: 'curso-ingles-basico'
        }
    })
    """
    if event_type == 'view_course':
        return track_course_view(kwargs.get('course_name'))
    elif event_type == 'enroll_course':
        return track_course_enrollment(
            kwargs.get('course_name'),
            kwargs.get('user_email'),
            kwargs.get('payment_method')
        )
    elif event_type == 'purchase':
        return track_purchase(
            kwargs.get('transaction_id'),
            kwargs.get('course_name'),
            kwargs.get('amount'),
            kwargs.get('currency', 'BRL'),
            kwargs.get('payment_method')
        )
    elif event_type == 'complete_lesson':
        return track_lesson_completion(
            kwargs.get('course_name'),
            kwargs.get('lesson_name'),
            kwargs.get('progress_percentage')
        )
    else:
        frappe.throw(
            _("Tipo de evento desconhecido: '{0}'. Tipos válidos: "
              "view_course, enroll_course, purchase, complete_lesson.").format(
                frappe.utils.escape_html(str(event_type))
            )
        )
