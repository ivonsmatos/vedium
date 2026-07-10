import frappe

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.positions = [
        "Professeur d'Anglais",
        "Professeur de Yoruba",
        "Professeur de Portugais pour Étrangers",
        "Professeur d'Hébreu",
        "Professeur d'Espagnol",
        "Professeur d'Allemand",
        "Professeur de Mandarin",
        "Service Client / Support Étudiant",
        "Marketing / Contenu",
        "Ventes",
        "Autre (précisez dans le message)",
    ]
    context.lang = "fr"
    context.canonical_url = "https://vediums.com/fr/carreiras"
    context.alt_lang_url = "https://vediums.com/carreiras"
