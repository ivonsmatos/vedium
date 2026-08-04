import pytest
import frappe
from unittest.mock import patch, MagicMock
from vedium_core.catalog_pricing import get_course_price, is_catalog_complete
from vedium_core.checkout_options import get_course_purchase_options
from vedium_core.stripe_billing import create_subscription_checkout, _checkout_completed
from vedium_core.scripts.migrations.oneshot.seed_ingls_beginner_catalog import _create_price_if_not_exists


class TestCatalogPricing:
    def test_catalog_pricing_service_throws_if_not_found(self):
        with pytest.raises(frappe.ValidationError, match="Preço não encontrado"):
            get_course_price("course_that_doesnt_exist", "monthly", 1)
            
    @patch("frappe.db.count")
    def test_is_catalog_complete(self, mock_count):
        # 1. Total incompleto
        mock_count.side_effect = [1, 0] # first call is monthly, second is annual
        assert is_catalog_complete("test-course") == "incomplete"
        
        # 2. Total completo
        mock_count.side_effect = [5, 5]
        assert is_catalog_complete("test-course") == True
        
        # 3. Vazio
        mock_count.side_effect = [0, 0]
        assert is_catalog_complete("test-course") == False

    @patch("vedium_core.checkout_options.is_catalog_complete")
    @patch("vedium_core.checkout_options.get_course_price")
    @patch("frappe.db.exists")
    @patch("frappe.get_doc")
    def test_get_course_purchase_options_with_catalog(self, mock_get_doc, mock_exists, mock_get_course_price, mock_is_catalog_complete):
        mock_exists.return_value = True
        
        course_mock = MagicMock()
        course_mock.paid_course = True
        course_mock.name = "ingl-s-beginner"
        course_mock.title = "Inglês Online ao Vivo A1"
        mock_get_doc.return_value = course_mock
        
        mock_is_catalog_complete.return_value = True
        
        price_mock = MagicMock()
        price_mock.currency = "BRL"
        price_mock.amount = 240.0
        price_mock.subtotal = 240.0
        price_mock.frequency_discount_percent = 0.0
        price_mock.minimum_term_months = 12
        mock_get_course_price.return_value = price_mock
        
        res = get_course_purchase_options("ingl-s-beginner")
        
        assert res["is_paid"] == True
        assert len(res["plans"]) == 2
        assert res["plans"][0]["title"] == "Plano mensal"
        assert res["plans"][1]["title"] == "Plano anual"
        assert res["plans"][0]["frequency_options"][0]["stripe_catalog"] == True
        assert res["plans"][0]["frequency_options"][0]["amount"] == 240.0
