import frappe

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
    context.lang = "ru"
    context.canonical_url = "https://vediums.com/ru/carreiras"
    context.alt_lang_url = "https://vediums.com/carreiras"
