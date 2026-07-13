import frappe
from vedium_core.careers import set_careers_seo_context

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.positions = [
        "Englischlehrer(in)",
        "Yoruba-Lehrer(in)",
        "Lehrer(in) für Portugiesisch als Fremdsprache",
        "Hebräischlehrer(in)",
        "Spanischlehrer(in)",
        "Deutschlehrer(in)",
        "Mandarin-Lehrer(in)",
        "Kundenservice / Studierendenbetreuung",
        "Marketing / Content",
        "Vertrieb",
        "Andere (bitte in der Nachricht angeben)",
    ]
    set_careers_seo_context(context, "de")
