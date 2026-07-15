import frappe
from vedium_core.careers import set_careers_seo_context

no_cache = 1


def get_context(context):
    context.no_cache = 1
    set_careers_seo_context(context, "fr")
    context.title = "Travaillez avec Nous - Vedium"
    context.description = (
        "Travaillez chez Vedium : postes de professeur d'anglais, yoruba, "
        "portugais pour étrangers, hébreu, espagnol et plus, ainsi que "
        "service client, marketing et ventes. Envoyez votre candidature."
    )
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
