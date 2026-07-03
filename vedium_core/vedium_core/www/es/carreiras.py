import frappe

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.positions = [
        "Profesor de Inglés",
        "Profesor de Yoruba",
        "Profesor de Portugués para Extranjeros",
        "Atención al Cliente / Soporte al Estudiante",
        "Marketing / Contenido",
        "Ventas",
        "Otro (especifica en el mensaje)",
    ]
    context.lang = "es"
    context.canonical_url = "https://vediums.com/es/carreiras"
    context.alt_lang_url = "https://vediums.com/carreiras"
