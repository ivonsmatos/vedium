import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

# Mocks para que os testes pure (sem bench) não quebrem no import
if 'frappe' not in sys.modules:
    sys.modules['frappe'] = MagicMock()
if 'stripe' not in sys.modules:
    sys.modules['stripe'] = MagicMock()
    
# Precisamos do script de seeding C1
import vedium_core.scripts.migrations.oneshot.seed_ioruba_intermediario_catalog as seed_script
import stripe

class TestIorubaIntermediarioCatalogSeeding:
    
    @patch('vedium_core.scripts.migrations.oneshot.seed_ioruba_intermediario_catalog.frappe')
    @patch('vedium_core.scripts.migrations.oneshot.seed_ioruba_intermediario_catalog.stripe')
    def test_seeding_creates_prices_if_not_exist(self, mock_stripe, mock_frappe):
        mock_frappe.db.exists.return_value = True
        mock_frappe.conf.get.return_value = "sk_test_123"
        
        # Simula que o Frappe não tem nenhum registro ainda
        mock_frappe.db.get_value.return_value = None
        
        # Simula que o Stripe NÃO encontra os preços (list retorna vazio)
        mock_stripe_list = MagicMock()
        mock_stripe_list.data = []
        mock_stripe.Price.list.return_value = mock_stripe_list
        
        # Simula a criação de um novo price no Stripe
        mock_new_price = MagicMock()
        mock_new_price.id = "price_mocked_123"
        mock_stripe.Price.create.return_value = mock_new_price
        
        seed_script.execute()
        
        # Deve ter chamado stripe.Price.create para os 8 preços que faltam
        assert mock_stripe.Price.create.call_count == 8
        
        # Verifica se frappe.get_doc foi chamado 10 vezes (2 reutilizados + 8 criados)
        assert mock_frappe.get_doc.call_count == 10
        
    @patch('vedium_core.scripts.migrations.oneshot.seed_ioruba_intermediario_catalog.frappe')
    @patch('vedium_core.scripts.migrations.oneshot.seed_ioruba_intermediario_catalog.stripe')
    def test_seeding_reuses_stripe_prices_if_exist(self, mock_stripe, mock_frappe):
        mock_frappe.db.exists.return_value = True
        mock_frappe.conf.get.return_value = "sk_test_123"
        
        # Simula que o Frappe não tem nenhum registro ainda
        mock_frappe.db.get_value.return_value = None
        
        # Simula que o Stripe JÁ TEM os preços!
        mock_existing_price = MagicMock()
        mock_existing_price.id = "price_already_exists_123"
        mock_existing_price.product = "prod_UznR5eXanIPt8H"
        mock_existing_price.currency = "brl"
        mock_existing_price.recurring.interval = "month"
        # O valor unit_amount depende do teste, vamos mockar a validação pra passar
        
        def mock_price_list(*args, **kwargs):
            # Adapta o unit_amount do mock baseado na lookup key que está sendo buscada
            lookup_key = kwargs.get('lookup_keys')[0]
            amount = 0
            if "monthly_2x" in lookup_key: amount = 43200
            elif "monthly_3x" in lookup_key: amount = 64800
            elif "monthly_4x" in lookup_key: amount = 86400
            elif "monthly_5x" in lookup_key: amount = 108000
            elif "annual_2x" in lookup_key: amount = 36000
            elif "annual_3x" in lookup_key: amount = 54000
            elif "annual_4x" in lookup_key: amount = 72000
            elif "annual_5x" in lookup_key: amount = 90000
            
            mock_existing_price.unit_amount = amount
            mock_list = MagicMock()
            mock_list.data = [mock_existing_price]
            return mock_list
            
        mock_stripe.Price.list.side_effect = mock_price_list
        
        seed_script.execute()
        
        # NENHUM price deve ser criado no stripe, pois todos já existem!
        assert mock_stripe.Price.create.call_count == 0
        
        # Verifica se frappe.get_doc foi chamado 10 vezes (2 existentes + 8 reaproveitados)
        assert mock_frappe.get_doc.call_count == 10

    @patch('vedium_core.scripts.migrations.oneshot.seed_ioruba_intermediario_catalog.frappe')
    @patch('vedium_core.scripts.migrations.oneshot.seed_ioruba_intermediario_catalog.stripe')
    def test_seeding_throws_on_divergent_stripe_data(self, mock_stripe, mock_frappe):
        mock_frappe.db.exists.return_value = True
        mock_frappe.conf.get.return_value = "sk_test_123"
        
        # Simula que o Frappe não tem nenhum registro ainda
        mock_frappe.db.get_value.return_value = None
        
        # Simula que o Stripe encontra um price, mas ele é de OUTRO produto!
        mock_existing_price = MagicMock()
        mock_existing_price.id = "price_wrong_product"
        mock_existing_price.product = "prod_OUTRO_PRODUTO"
        mock_existing_price.currency = "brl"
        mock_existing_price.unit_amount = 43200
        mock_existing_price.recurring.interval = "month"
        
        mock_list = MagicMock()
        mock_list.data = [mock_existing_price]
        mock_stripe.Price.list.return_value = mock_list
        
        # Usamos uma classe customizada pro Exception para bater com o mock do Frappe
        class FrappeThrow(Exception):
            pass
        mock_frappe.throw.side_effect = FrappeThrow
        
        with pytest.raises(FrappeThrow):
            seed_script.execute()
