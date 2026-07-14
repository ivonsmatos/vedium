import frappe
from vedium_core.careers import set_careers_seo_context

no_cache = 1


def get_context(context):
    context.no_cache = 1
    set_careers_seo_context(context)
    context.title = "Trabalhe Conosco - Vedium"
    context.description = (
        "Trabalhe na Vedium: vagas para professores de inglês, iorubá, "
        "português para estrangeiros, hebraico, espanhol e mais, além de "
        "atendimento, marketing e vendas. Envie sua candidatura."
    )
    context.positions = [
        "Professor(a) de Ingles",
        "Professor(a) de Ioruba",
        "Professor(a) de Portugues para Estrangeiros",
        "Professor(a) de Hebraico",
        "Professor(a) de Espanhol",
        "Professor(a) de Alemao",
        "Professor(a) de Mandarim",
        "Atendimento / Suporte ao Aluno",
        "Marketing / Conteudo",
        "Vendas / Comercial",
        "Outra (especificar na mensagem)",
    ]
