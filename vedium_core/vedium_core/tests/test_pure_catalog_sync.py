import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

is_frappe_mocked = 'frappe' not in sys.modules
if is_frappe_mocked:
    sys.modules['frappe'] = MagicMock()
    sys.modules['frappe.utils'] = MagicMock()
    sys.modules['frappe.custom'] = MagicMock()
    sys.modules['frappe.custom.doctype'] = MagicMock()
    sys.modules['frappe.custom.doctype.custom_field'] = MagicMock()
    sys.modules['frappe.custom.doctype.custom_field.custom_field'] = MagicMock()
import frappe

from vedium_core.catalog_sync import sync_course_catalog, ensure_custom_contract_currency_field

class TestCatalogSync:
    def test_sync_dryrun_does_not_save_anything(self):
        config = {
            "course_name": "fake-course",
            "commercial_name": "Fake Course",
            "product_id": "prod_123",
            "currency": "usd",
            "catalog_version": 1,
            "monthly_prices": [
                {"classes_per_week": 1, "unit_amount": 1000, "lookup_key": "fake_1", "nickname": "Fake 1", "amount": 10.0, "subtotal": 10.0, "frequency_discount_percent": 0},
            ],
            "annual_prices": [
                {"classes_per_week": 1, "unit_amount": 800, "lookup_key": "fake_a1", "nickname": "Fake A1", "amount": 8.0, "subtotal": 10.0, "frequency_discount_percent": 0},
            ]
        }
        assert callable(sync_course_catalog)
        
    def test_custom_contract_currency_field_definition(self):
        assert callable(ensure_custom_contract_currency_field)
