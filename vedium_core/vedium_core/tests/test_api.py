# Copyright (c) 2026, Vedium and Contributors
# See license.txt
#
# Testes de integração — exigem ambiente Frappe bench.
# Para rodar:  bench --site test_site run-tests --app vedium_core
#
# CI roda apenas testes "pure" (sem bench) por padrão; estes ficam reservados
# para o ambiente de homologação.

import unittest
from unittest import mock
import pytest

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
except ImportError:
    pytest.skip("Skipping Frappe integration tests (pure mode)", allow_module_level=True)

from vedium_core.api import (
    create_checkout,
    get_course_categories,
    get_published_courses,
    get_payment_history,
)


TEST_USER = "testuser@vediums.com"
TEST_CATEGORY = "TestPayCat"
TEST_COURSE_TITLE = "TestPayCourse"


class _SeedMixin:
    @classmethod
    def _seed(cls):
        if not frappe.db.exists("LMS Category", TEST_CATEGORY):
            cat = frappe.new_doc("LMS Category")
            cat.category = TEST_CATEGORY
            cat.insert(ignore_permissions=True)

        if not frappe.db.exists("LMS Course", {"title": TEST_COURSE_TITLE}):
            doc = frappe.new_doc("LMS Course")
            doc.title = TEST_COURSE_TITLE
            doc.category = TEST_CATEGORY
            doc.short_introduction = "Intro"
            doc.status = "Approved"
            doc.paid_course = 1
            doc.course_price = 100
            doc.currency = "BRL"
            doc.published = 1
            doc.insert(ignore_permissions=True)

        cls.course_name = frappe.get_value(
            "LMS Course", {"title": TEST_COURSE_TITLE}, "name"
        )

        if not frappe.db.exists("User", TEST_USER):
            u = frappe.new_doc("User")
            u.email = TEST_USER
            u.first_name = "Test"
            u.last_name = "User"
            u.insert(ignore_permissions=True)


class TestPaymentAPI(FrappeTestCase, _SeedMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._seed()

    def setUp(self):
        frappe.set_user(TEST_USER)
        frappe.db.delete(
            "LMS Enrollment",
            {"course": self.course_name, "member": TEST_USER},
        )

    def tearDown(self):
        frappe.set_user("Administrator")

    def test_checkout_success(self):
        resp = create_checkout(self.course_name, "stripe")
        self.assertIn("checkout_url", resp)

    def test_checkout_duplicate_raises(self):
        frappe.get_doc(
            {
                "doctype": "LMS Enrollment",
                "course": self.course_name,
                "member": TEST_USER,
                "status": "Active",
            }
        ).insert(ignore_permissions=True)
        with self.assertRaises(Exception):
            create_checkout(self.course_name, "stripe")

    def test_checkout_invalid_gateway(self):
        with self.assertRaises(Exception):
            create_checkout(self.course_name, "inexistente")

    def test_payment_history_includes_enrollment(self):
        frappe.get_doc(
            {
                "doctype": "LMS Enrollment",
                "course": self.course_name,
                "member": TEST_USER,
                "status": "Active",
                "payment_gateway": "stripe",
                "payment_reference": "ref123",
                "amount": 100,
                "currency": "BRL",
            }
        ).insert(ignore_permissions=True)
        history = get_payment_history()
        self.assertTrue(
            any(e.get("course_title") == TEST_COURSE_TITLE for e in history)
        )


class TestCoursesAPI(FrappeTestCase, _SeedMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._seed()

    def test_get_categories(self):
        categories = get_course_categories()
        self.assertTrue(any(c.get("category") == TEST_CATEGORY for c in categories))

    def test_get_published_courses(self):
        courses = get_published_courses()
        self.assertTrue(any(c.get("title") == TEST_COURSE_TITLE for c in courses))


class TestMercadoPagoCheckout(FrappeTestCase, _SeedMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._seed()

    def setUp(self):
        frappe.set_user(TEST_USER)
        frappe.db.delete(
            "LMS Enrollment",
            {"course": self.course_name, "member": TEST_USER},
        )

    def test_mercadopago_checkout_returns_init_point(self):
        with mock.patch("mercadopago.SDK") as MockSDK:
            instance = MockSDK.return_value
            instance.preference.return_value.create.return_value = {
                "response": {"init_point": "https://mp.com/checkout"}
            }
            from vedium_core.api import create_mercadopago_checkout

            with mock.patch.object(
                frappe.conf, "get", return_value="TEST-TOKEN", create=True
            ):
                resp = create_mercadopago_checkout(self.course_name)

            self.assertEqual(resp["checkout_url"], "https://mp.com/checkout")


if __name__ == "__main__":
    unittest.main()
