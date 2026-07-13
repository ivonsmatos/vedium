import frappe
from vedium_core.careers import set_careers_seo_context

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.positions = [
        "English Teacher",
        "Yoruba Teacher",
        "Portuguese for Foreigners Teacher",
        "Hebrew Teacher",
        "Spanish Teacher",
        "German Teacher",
        "Mandarin Teacher",
        "Customer Service / Student Support",
        "Marketing / Content",
        "Sales",
        "Other (specify in the message)",
    ]
    set_careers_seo_context(context, "en")
