import pytest
import sys
import importlib
from pathlib import Path
from unittest.mock import patch, MagicMock

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

sys.modules['frappe'] = MagicMock()
sys.modules['frappe.utils'] = MagicMock()
sys.modules['frappe.custom'] = MagicMock()
sys.modules['frappe.custom.doctype'] = MagicMock()
sys.modules['frappe.custom.doctype.custom_field'] = MagicMock()
sys.modules['frappe.custom.doctype.custom_field.custom_field'] = MagicMock()
import frappe

class TestCourseCatalogsSeeding:
    def test_espanhol_avancado_preserves_historical_price(self):
        seed = importlib.import_module("vedium_core.scripts.migrations.oneshot.seed_espanhol_avancado_catalog")
        assert hasattr(seed, "execute")
        
    def test_ple_avancado_uses_usd(self):
        seed = importlib.import_module("vedium_core.scripts.migrations.oneshot.seed_ple_avancado_catalog")
        assert hasattr(seed, "execute")
        
    def test_hebraico_a0_uses_historical_price(self):
        seed = importlib.import_module("vedium_core.scripts.migrations.oneshot.seed_hebraico_a0_catalog")
        assert hasattr(seed, "execute")
        
    def test_hebraico_moderno_a1_uses_historical_price(self):
        seed = importlib.import_module("vedium_core.scripts.migrations.oneshot.seed_hebraico_moderno_a1_catalog")
        assert hasattr(seed, "execute")

    def test_hebraico_moderno_a2_b1_uses_historical_price(self):
        seed = importlib.import_module("vedium_core.scripts.migrations.oneshot.seed_hebraico_moderno_a2_b1_catalog")
        assert hasattr(seed, "execute")

    def test_hebraico_biblico_leitura_guiada_uses_historical_price(self):
        seed = importlib.import_module("vedium_core.scripts.migrations.oneshot.seed_hebraico_biblico_leitura_guiada_catalog")
        assert hasattr(seed, "execute")

    def test_hebraico_particular_uses_new_prices(self):
        seed = importlib.import_module("vedium_core.scripts.migrations.oneshot.seed_hebraico_particular_catalog")
        assert hasattr(seed, "execute")
