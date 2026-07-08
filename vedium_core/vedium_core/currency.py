# -*- coding: utf-8 -*-
"""
Vedium — Conversão de moeda pra exibição de preço e checkout

Cada curso (LMS Course) tem um preço "de verdade" numa moeda fixa
(course.currency + course.course_price -- hoje BRL na maioria, USD no PLE).
Este módulo converte esse valor pra outras moedas EM TEMPO REAL, pra alunos
de fora do Brasil verem e pagarem no catálogo/checkout na moeda deles
(pedido explícito do usuário, 2026-07-07: "aluno precisa pagar em libras").

Fonte de câmbio: open.er-api.com (gratuita, sem chave, base configurável).
As taxas são cacheadas por 6h (frappe.cache()) -- não é preciso (nem
correto) chamar a API a cada carregamento de página.

Isto é conversão de EXIBIÇÃO/CHECKOUT, não uma tabela contábil de preços
fixos por moeda -- a margem em BRL do curso varia com o câmbio do dia,
igual qualquer venda internacional via cartão.
"""

import frappe

SUPPORTED_CURRENCIES = ["BRL", "USD", "EUR", "GBP"]
_CACHE_KEY = "vedium_fx_rates_brl"
_CACHE_TTL_SECONDS = 6 * 60 * 60  # 6h

_SYMBOLS = {"BRL": "R$", "USD": "US$", "EUR": "€", "GBP": "£"}


def _fetch_rates_from_api():
    """Busca as taxas de câmbio (base BRL) na API externa. Levanta exceção
    se a chamada falhar -- quem chama decide o fallback."""
    import requests

    resp = requests.get("https://open.er-api.com/v6/latest/BRL", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("result") != "success":
        raise ValueError(f"API de câmbio retornou erro: {data}")
    rates = data.get("rates") or {}
    rates["BRL"] = 1.0
    return {code: rates[code] for code in SUPPORTED_CURRENCIES if code in rates}


def get_rates():
    """Taxas de câmbio (quantas unidades de cada moeda por 1 BRL), com
    cache de 6h. Se a API estiver fora do ar e não houver cache, cai pra um
    fallback fixo (taxas aproximadas, atualizadas manualmente de vez em
    quando) -- nunca quebra o catálogo/checkout por causa de uma API
    externa instável."""
    cached = frappe.cache().get_value(_CACHE_KEY)
    if cached:
        return cached

    try:
        rates = _fetch_rates_from_api()
        frappe.cache().set_value(_CACHE_KEY, rates, expires_in_sec=_CACHE_TTL_SECONDS)
        return rates
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.currency.get_rates (fallback usado)"
        )
        # Fallback fixo -- só usado se a API externa cair E não houver
        # nada em cache ainda. Atualizar de vez em quando (câmbio aprox.).
        return {"BRL": 1.0, "USD": 0.18, "EUR": 0.16, "GBP": 0.14}


def convert_amount(amount, from_currency, to_currency):
    from_currency = (from_currency or "BRL").upper()
    to_currency = (to_currency or "BRL").upper()
    if from_currency == to_currency:
        return float(amount)

    rates = get_rates()
    rate_from = rates.get(from_currency)
    rate_to = rates.get(to_currency)
    if not rate_from or not rate_to:
        # Moeda não suportada -- devolve o valor original sem converter,
        # em vez de quebrar a página.
        return float(amount)

    amount_in_brl = float(amount) / rate_from
    return amount_in_brl * rate_to


def format_amount(amount, currency):
    currency = (currency or "BRL").upper()
    symbol = _SYMBOLS.get(currency, currency + " ")
    if currency == "BRL":
        return f"{symbol} {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{symbol} {amount:,.2f}"


@frappe.whitelist(allow_guest=True)
def get_supported_currencies():
    return SUPPORTED_CURRENCIES


@frappe.whitelist(allow_guest=True)
def get_catalog_prices(currency):
    """Retorna, pra TODOS os cursos pagos publicados, o preço convertido e
    formatado na moeda pedida. Usado pelo seletor de moeda no /catalogo e
    nas páginas de curso pra atualizar os preços exibidos sem recarregar
    a página."""
    currency = (currency or "BRL").upper()
    if currency not in SUPPORTED_CURRENCIES:
        frappe.throw(frappe._("Moeda não suportada: {0}").format(currency))

    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1, "paid_course": 1},
        fields=["name", "course_price", "currency"],
    )
    result = {}
    for course in courses:
        if not course.course_price:
            continue
        converted = convert_amount(course.course_price, course.currency, currency)
        result[course.name] = format_amount(converted, currency)
    return result


@frappe.whitelist(allow_guest=True)
def get_course_price_in_currency(course_name, currency):
    """Preço convertido de UM curso específico -- usado na página de
    detalhe do curso (/curso/<slug>) e antes de abrir o checkout."""
    currency = (currency or "BRL").upper()
    if currency not in SUPPORTED_CURRENCIES:
        frappe.throw(frappe._("Moeda não suportada: {0}").format(currency))

    course = frappe.db.get_value(
        "LMS Course", course_name, ["course_price", "currency"], as_dict=True
    )
    if not course or not course.course_price:
        frappe.throw(frappe._("Curso não encontrado ou gratuito"))

    converted = convert_amount(course.course_price, course.currency, currency)
    return {
        "currency": currency,
        "amount": round(converted, 2),
        "formatted": format_amount(converted, currency),
    }
