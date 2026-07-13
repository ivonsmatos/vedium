import frappe
from vedium_core.careers import set_careers_seo_context

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.positions = [
        "Преподаватель английского языка",
        "Преподаватель йоруба",
        "Преподаватель португальского как иностранного",
        "Преподаватель иврита",
        "Преподаватель испанского языка",
        "Преподаватель немецкого языка",
        "Преподаватель китайского языка",
        "Служба поддержки студентов",
        "Маркетинг / контент",
        "Продажи",
        "Другое (укажите в сообщении)",
    ]
    set_careers_seo_context(context, "ru")
