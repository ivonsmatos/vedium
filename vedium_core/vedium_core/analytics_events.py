import frappe
import json

def track_course_view(course_name):
    """
    Rastreia visualização de curso
    """
    course = frappe.get_doc("LMS Course", course_name)
    
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
    course = frappe.get_doc("LMS Course", course_name)
    
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
    course = frappe.get_doc("LMS Course", course_name)
    
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
