import frappe
from vedium_core.careers import set_careers_seo_context

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.positions = [
        "Profesor de Inglés",
        "Profesor de Yoruba",
        "Profesor de Portugués para Extranjeros",
        "Profesor de Hebreo",
        "Profesor de Español",
        "Profesor de Alemán",
        "Profesor de Mandarín",
        "Atención al Cliente / Soporte al Estudiante",
        "Marketing / Contenido",
        "Ventas",
        "Otro (especifica en el mensaje)",
    ]
    set_careers_seo_context(context, "es")
