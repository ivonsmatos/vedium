import frappe

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.positions = [
        "Professor(a) de Ingles",
        "Professor(a) de Ioruba",
        "Professor(a) de Portugues para Estrangeiros",
        "Atendimento / Suporte ao Aluno",
        "Marketing / Conteudo",
        "Vendas / Comercial",
        "Outra (especificar na mensagem)",
    ]
