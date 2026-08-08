import unittest
from vedium_core.catalog_registry import generate_config_for_course, CATALOG


class TestFullCatalogRegistry(unittest.TestCase):

    def test_all_generic_courses_have_canonical_prices(self):
        self.assertEqual(len(CATALOG), 20, "O catálogo deve ter 20 cursos")

        for course_id, c in CATALOG.items():
            # Hebraico Particular é uma exceção comercial fixa (R$450/mês, 1x)
            # e permanece bloqueado no catálogo genérico 1–5x.
            if course_id == "hebraico-particular":
                self.assertEqual(c.get("blocked_status"), "BLOCKED_COMMERCIAL_DECISION")
                continue

            config = generate_config_for_course(course_id)
            self.assertEqual(len(config["monthly_prices"]), 5, f"{course_id} deve ter 5 prices mensais")
            self.assertEqual(len(config["annual_prices"]), 5, f"{course_id} deve ter 5 prices anuais")

            for i, p in enumerate(config["monthly_prices"]):
                classes = i + 1
                self.assertEqual(p["classes_per_week"], classes)

                if classes >= 2:
                    self.assertEqual(p["frequency_discount_percent"], 10)
                else:
                    self.assertEqual(p["frequency_discount_percent"], 0)

            for i, p in enumerate(config["annual_prices"]):
                classes = i + 1
                self.assertEqual(p["classes_per_week"], classes)

    def test_ingles_a1_values(self):
        config = generate_config_for_course("ingl-s-beginner")

        # Monthly 1x
        m1 = config["monthly_prices"][0]
        self.assertEqual(m1["amount"], 240.0)
        self.assertEqual(m1["unit_amount"], 24000)
        self.assertEqual(m1["lookup_key"], "ingles-a1_monthly")

        # Monthly 2x
        m2 = config["monthly_prices"][1]
        self.assertEqual(m2["amount"], 432.0)
        self.assertEqual(m2["unit_amount"], 43200)
        self.assertEqual(m2["lookup_key"], "ingles-a1_monthly_2x")

        # Annual 1x
        a1 = config["annual_prices"][0]
        self.assertEqual(a1["amount"], 200.0)
        self.assertEqual(a1["unit_amount"], 20000)
        self.assertEqual(a1["lookup_key"], "ingles-a1_annual")

        # Annual 2x
        a2 = config["annual_prices"][1]
        self.assertEqual(a2["amount"], 360.0)
        self.assertEqual(a2["unit_amount"], 36000)
        self.assertEqual(a2["lookup_key"], "ingles-a1_annual_2x")

    def test_ioruba_custom_annual(self):
        config = generate_config_for_course("iorub-b-sico")
        m1 = config["monthly_prices"][0]
        self.assertEqual(m1["amount"], 320.0)

        a1 = config["annual_prices"][0]
        self.assertEqual(a1["amount"], 266.66)

        a5 = config["annual_prices"][4]
        self.assertEqual(a5["amount"], 1199.97)

    def test_hebraico_particular_is_not_generic_catalog_offer(self):
        course = CATALOG["hebraico-particular"]
        self.assertEqual(course["product_id"], "prod_UznRzhBCmMC5y8")
        self.assertEqual(course["currency"], "BRL")
        self.assertEqual(course.get("blocked_status"), "BLOCKED_COMMERCIAL_DECISION")


if __name__ == "__main__":
    unittest.main()
