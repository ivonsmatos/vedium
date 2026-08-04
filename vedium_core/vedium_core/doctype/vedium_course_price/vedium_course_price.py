# Copyright (c) 2026, Vedium and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe import _

class VediumCoursePrice(Document):
    def before_insert(self):
        self.set_catalog_key()

    def validate(self):
        self.set_catalog_key()
        self.validate_business_rules()
        self.validate_stripe_data()

    def set_catalog_key(self):
        if not self.course or not self.billing_period or not self.classes_per_week or not self.stripe_environment or not self.catalog_version:
            return
        
        self.catalog_key = f"{self.course}:{self.billing_period}:{self.classes_per_week}x:{self.stripe_environment}:v{self.catalog_version}"

    def validate_business_rules(self):
        if not self.classes_per_week or self.classes_per_week < 1 or self.classes_per_week > 5:
            frappe.throw(_("Aulas por semana deve estar entre 1 e 5."))
        
        if self.billing_period not in ["monthly", "annual"]:
            frappe.throw(_("Período de cobrança deve ser 'monthly' ou 'annual'."))
            
        if self.currency not in ["BRL", "USD"]:
            frappe.throw(_("Moeda deve ser BRL ou USD."))
            
        if not self.amount or self.amount <= 0:
            frappe.throw(_("Valor deve ser maior que zero."))
            
        if not self.stripe_product_id or not self.stripe_product_id.startswith("prod_"):
            frappe.throw(_("Stripe Product ID deve começar com 'prod_'."))
            
        if not self.stripe_price_id or not self.stripe_price_id.startswith("price_"):
            frappe.throw(_("Stripe Price ID deve começar com 'price_'."))
            
        if not self.catalog_version or self.catalog_version < 1:
            frappe.throw(_("Versão do catálogo deve ser maior ou igual a 1."))

        # Verifica duplicidade da chave
        existing = frappe.db.exists("Vedium Course Price", {"catalog_key": self.catalog_key, "name": ["!=", self.name]})
        if existing:
            frappe.throw(_("Já existe um registro com a chave {0} ({1})").format(self.catalog_key, existing))

    def validate_stripe_data(self):
        if not self.enabled:
            return

        import stripe
        stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
        if not stripe.api_key:
            frappe.throw(_("STRIPE_SECRET_KEY não configurada."))

        try:
            price = stripe.Price.retrieve(self.stripe_price_id)
        except stripe.error.StripeError as e:
            frappe.throw(_("Erro ao consultar Stripe: {0}").format(str(e)))

        if not price.get("active"):
            self.stripe_validated = 0
            frappe.throw(_("Price não está ativo no Stripe."))

        if (price.get("livemode") and self.stripe_environment == "test") or (not price.get("livemode") and self.stripe_environment == "live"):
            self.stripe_validated = 0
            frappe.throw(_("O ambiente do Price no Stripe diverge do cadastrado."))

        if price.get("product") != self.stripe_product_id:
            self.stripe_validated = 0
            frappe.throw(_("Product ID diverge do cadastrado."))

        if (price.get("currency") or "").upper() != self.currency:
            self.stripe_validated = 0
            frappe.throw(_("Moeda diverge do cadastrado."))

        if price.get("type") != "recurring":
            self.stripe_validated = 0
            frappe.throw(_("Price não é recorrente no Stripe."))

        recurring = price.get("recurring") or {}
        if recurring.get("interval_count", 1) != 1:
            self.stripe_validated = 0
            frappe.throw(_("Recorrência não é mensal no Stripe (interval_count diferente de 1)."))
            
        # O anual cobra mensalmente
        if recurring.get("interval") != "month":
            self.stripe_validated = 0
            frappe.throw(_("Recorrência não é mensal no Stripe."))

        if self.unit_amount and price.get("unit_amount") is not None:
            if int(round(self.unit_amount * 100)) != int(price.get("unit_amount")):
                self.stripe_validated = 0
                frappe.throw(_("Valor unitário diverge do Stripe."))

        if self.stripe_lookup_key and price.get("lookup_key") != self.stripe_lookup_key:
            self.stripe_validated = 0
            frappe.throw(_("Lookup key diverge do Stripe."))

        metadata = price.get("metadata") or {}
        if self.billing_period == "annual":
            if metadata.get("interval") != "annual":
                self.stripe_validated = 0
                frappe.throw(_("Metadado 'interval' no Stripe deve ser 'annual' para planos anuais."))
            if int(metadata.get("minimum_term_months") or 0) != 12:
                self.stripe_validated = 0
                frappe.throw(_("Metadado 'minimum_term_months' no Stripe deve ser 12 para planos anuais."))
            if int(metadata.get("charge_count") or 0) != 12:
                self.stripe_validated = 0
                frappe.throw(_("Metadado 'charge_count' no Stripe deve ser 12 para planos anuais."))
        else:
            if metadata.get("interval") != "monthly":
                self.stripe_validated = 0
                frappe.throw(_("Metadado 'interval' no Stripe deve ser 'monthly' para planos mensais."))
            if int(metadata.get("minimum_term_months") or 0) != 0:
                self.stripe_validated = 0
                frappe.throw(_("Metadado 'minimum_term_months' no Stripe deve ser 0 para planos mensais."))

        self.stripe_validated = 1
        self.last_stripe_validation = now_datetime()
