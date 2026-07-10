import frappe

no_cache = 1


def get_context(context):
    context.no_cache = 1
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
