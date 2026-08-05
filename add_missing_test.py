import re

with open("vedium_core/vedium_core/tests/test_pure_ioruba_avancado_catalog_seeding.py", "r", encoding="utf-8") as f:
    content = f.read()

test_func = """
    @patch("vedium_core.scripts.migrations.oneshot.seed_ioruba_avancado_catalog.frappe")
    def test_missing_stripe_key_creates_with_enabled_0(self, mock_frappe):
        \"\"\"Testa se a ausência de STRIPE_SECRET_KEY cria registros desabilitados.\"\"\"
        mock_frappe.conf.get.return_value = None
        mock_frappe.get_all.return_value = []
        mock_frappe.db.get_value.return_value = None
        
        mock_doc = MagicMock()
        mock_frappe.get_doc.return_value = mock_doc

        seed_script.execute()

        created_docs = []
        for call in mock_frappe.get_doc.mock_calls:
            if call.args and isinstance(call.args[0], dict):
                created_docs.append(call.args[0])
            elif call.kwargs and "doctype" in call.kwargs:
                created_docs.append(call.kwargs)

        assert len(created_docs) > 0
        
        for doc_args in created_docs:
            expected_enabled = 1 if doc_args.get("stripe_price_id") else 0
            assert doc_args.get("enabled") == expected_enabled, f"Deveria ser enabled={expected_enabled} quando stripe_price_id for {doc_args.get('stripe_price_id')}."
            assert doc_args.get("stripe_validated") == expected_enabled, f"Deveria ser stripe_validated={expected_enabled} quando stripe_price_id for {doc_args.get('stripe_price_id')}."

"""

content = content.replace("class TestIorubaAvancadoCatalogSeeding:\n", "class TestIorubaAvancadoCatalogSeeding:\n" + test_func)

with open("vedium_core/vedium_core/tests/test_pure_ioruba_avancado_catalog_seeding.py", "w", encoding="utf-8") as f:
    f.write(content)
