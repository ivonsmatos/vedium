# -*- coding: utf-8 -*-
"""
Hierarquia de exceções do Vedium.

Uso:
    from vedium_core.exceptions import PaymentError, EnrollmentError

    raise PaymentError("Falha ao processar pagamento", gateway="stripe")
    frappe.throw(_("Erro"), PaymentError)

Todas herdam de VediumError → frappe.ValidationError, garantindo:
- HTTP 417 automático pelo Frappe (não 500)
- Mensagem traduzível via _()
- Logging padronizado via frappe.log_error
"""

import frappe
from frappe import _


class VediumError(frappe.ValidationError):
    """Erro base de todas as exceções Vedium. Retorna HTTP 417."""


class PaymentError(VediumError):
    """
    Falha relacionada a pagamento (gateway, webhook, checkout).
    Exemplos: HMAC inválido, gateway não configurado, enrollment duplicado.
    """

    def __init__(self, message=None, gateway: str = ""):
        self.gateway = gateway
        super().__init__(message or _("Erro no processamento do pagamento"))


class EnrollmentError(VediumError):
    """
    Falha ao criar ou validar uma matrícula (LMS Enrollment).
    Exemplos: curso já adquirido, curso inativo, cota atingida.
    """


class CertificateError(VediumError):
    """
    Falha na emissão ou verificação de certificado.
    Exemplos: matrícula não concluída, certificado já emitido.
    """


class GatewayNotFoundError(PaymentError):
    """
    Gateway de pagamento desconhecido ou não configurado.
    Subclasse de PaymentError para filtros específicos de pagamento.
    """

    def __init__(self, gateway_name: str = ""):
        super().__init__(
            _("Gateway de pagamento não suportado: {0}").format(gateway_name),
            gateway=gateway_name,
        )


class RateLimitError(VediumError):
    """
    Limite de requisições atingido (rate limiting por IP).
    O Frappe mapeia ValidationError → HTTP 417; para 429 use frappe.TooManyRequestsError
    diretamente (quando disponível).
    """


class LGPDError(VediumError):
    """
    Operação LGPD/GDPR bloqueada (consentimento ausente, dados não encontrados).
    """
