import sys
from pathlib import Path
from unittest.mock import MagicMock

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

sys.modules["frappe"] = MagicMock()
sys.modules["frappe.utils"] = MagicMock()
sys.modules["frappe.custom"] = MagicMock()
sys.modules["frappe.custom.doctype"] = MagicMock()
sys.modules["frappe.custom.doctype.custom_field"] = MagicMock()
sys.modules["frappe.custom.doctype.custom_field.custom_field"] = MagicMock()

from vedium_core.catalog_definitions import get_catalog_configs
from vedium_core.catalog_sync import (
    build_expected_metadata,
    ensure_custom_contract_currency_field,
    is_complete_catalog,
    sync_course_catalog,
    validate_price_snapshot,
)


class TestCatalogDefinitions:
    def test_catalog_contains_twenty_courses_and_two_hundred_prices(self):
        configs = get_catalog_configs()
        assert len(configs) == 20
        assert sum(len(config["monthly_prices"]) + len(config["annual_prices"]) for config in configs) == 200
        assert len({config["product_id"] for config in configs}) == 20
        assert len({config["course_name"] for config in configs}) == 20

    def test_every_course_has_distinct_frequencies(self):
        for config in get_catalog_configs():
            for period in ("monthly_prices", "annual_prices"):
                assert {row["classes_per_week"] for row in config[period]} == {1, 2, 3, 4, 5}
                assert len({row["lookup_key"] for row in config[period]}) == 5

    def test_private_hebrew_uses_explicit_one_x_and_preserves_legacy(self):
        config = next(row for row in get_catalog_configs() if row["course_name"] == "hebraico-particular")
        assert config["monthly_prices"][0]["lookup_key"] == "hebraico-particular_monthly_1x"
        assert config["annual_prices"][0]["lookup_key"] == "hebraico-particular_annual_1x"
        assert config["monthly_prices"][1]["unit_amount"] == 100800
        assert config["annual_prices"][1]["unit_amount"] == 84000
        assert len(config["legacy_price_ids"]) == 2


class TestCatalogSyncPureRules:
    def test_public_functions_exist(self):
        assert callable(sync_course_catalog)
        assert callable(ensure_custom_contract_currency_field)

    def test_expected_metadata_for_annual_price(self):
        config = get_catalog_configs()[0]
        price_def = config["annual_prices"][1]
        metadata = build_expected_metadata(config, "annual", price_def)
        assert metadata["classes_per_week"] == "2"
        assert metadata["frequency_discount_percent"] == "10"
        assert metadata["minimum_term_months"] == "12"
        assert metadata["charge_count"] == "12"
        assert metadata["catalog_version"] == "1"

    def test_valid_price_snapshot(self):
        config = get_catalog_configs()[0]
        price_def = config["monthly_prices"][1]
        metadata = build_expected_metadata(config, "monthly", price_def)
        price = {
            "active": True,
            "livemode": True,
            "product": config["product_id"],
            "currency": "brl",
            "unit_amount": price_def["unit_amount"],
            "lookup_key": price_def["lookup_key"],
            "type": "recurring",
            "billing_scheme": "per_unit",
            "recurring": {"interval": "month", "interval_count": 1, "usage_type": "licensed"},
            "metadata": metadata,
        }
        assert validate_price_snapshot(
            price,
            product_id=config["product_id"],
            currency=config["currency"],
            unit_amount=price_def["unit_amount"],
            lookup_key=price_def["lookup_key"],
            expected_metadata=metadata,
        ) == []

    def test_rejects_wrong_product_quantity_price_or_metadata(self):
        errors = validate_price_snapshot(
            {
                "active": True,
                "livemode": True,
                "product": "prod_wrong",
                "currency": "brl",
                "unit_amount": 999,
                "lookup_key": "wrong",
                "type": "recurring",
                "billing_scheme": "per_unit",
                "recurring": {"interval": "month", "interval_count": 1, "usage_type": "licensed"},
                "metadata": {},
            },
            product_id="prod_expected",
            currency="brl",
            unit_amount=1000,
            lookup_key="expected",
            expected_metadata={"classes_per_week": "2"},
        )
        assert "Product ID divergente" in errors
        assert "Valor divergente" in errors
        assert "Lookup key divergente" in errors
        assert "Metadata classes_per_week divergente" in errors

    def test_catalog_requires_distinct_one_to_five_for_both_periods(self):
        complete = [
            {
                "billing_period": period,
                "classes_per_week": frequency,
                "stripe_validated": 1,
            }
            for period in ("monthly", "annual")
            for frequency in range(1, 6)
        ]
        assert is_complete_catalog(complete) is True
        incomplete = complete[:-1] + [complete[-2]]
        assert is_complete_catalog(incomplete) is False
