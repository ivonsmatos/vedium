import frappe

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
    context.lang = "en"
    context.canonical_url = "https://vediums.com/en/carreiras"
    context.alt_lang_url = "https://vediums.com/carreiras"
