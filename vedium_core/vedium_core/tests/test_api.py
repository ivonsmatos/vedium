from vedium_core.api import create_checkout, get_payment_history


class TestPaymentAPI(FrappeTestCase):
    def setUp(self):
        # Garante categoria, curso e usuário de teste
        if not frappe.db.exists("LMS Category", "TestPayCat"):
            cat = frappe.new_doc("LMS Category")
            cat.category = "TestPayCat"
            cat.insert()
        if not frappe.db.exists("LMS Course", {"title": "TestPayCourse"}):
            doc = frappe.new_doc("LMS Course")
            doc.title = "TestPayCourse"
            doc.category = "TestPayCat"
            doc.short_introduction = "Intro"
            doc.status = "Approved"
            doc.paid_course = 1
            doc.course_price = 100
            doc.currency = "BRL"
            doc.published = 1
            doc.insert()
        self.course_name = frappe.get_value(
            "LMS Course", {"title": "TestPayCourse"}, "name"
        )
        self.user = "testuser@vedium.com"
        if not frappe.db.exists("User", self.user):
            u = frappe.new_doc("User")
            u.email = self.user
            u.first_name = "Test"
            u.last_name = "User"
            u.insert()
        frappe.set_user(self.user)

    def tearDown(self):
        frappe.set_user("Administrator")

    def test_checkout_success(self):
        # Remove inscrição anterior
        frappe.db.delete(
            "LMS Enrollment", {"course": self.course_name, "member": self.user}
        )
        resp = create_checkout(self.course_name, "stripe")
        self.assertIn("checkout_url", resp)

    def test_checkout_duplicate(self):
        # Cria inscrição manual
        frappe.get_doc(
            {
                "doctype": "LMS Enrollment",
                "course": self.course_name,
                "member": self.user,
                "status": "Active",
            }
        ).insert()
        with self.assertRaises(Exception):
            create_checkout(self.course_name, "stripe")
        frappe.db.delete(
            "LMS Enrollment", {"course": self.course_name, "member": self.user}
        )

    def test_checkout_invalid_gateway(self):
        with self.assertRaises(Exception):
            create_checkout(self.course_name, "inexistente")

    def test_checkout_with_coupon(self):
        # Cria cupom válido
        code = "CUPOM10"
        if not frappe.db.exists("Coupon", code):
            c = frappe.new_doc("Coupon")
            c.name = code
            c.discount_percent = 10
            c.active = 1
            c.insert()
        frappe.db.delete(
            "LMS Enrollment", {"course": self.course_name, "member": self.user}
        )
        resp = create_checkout(self.course_name, "stripe", coupon_code=code)
        self.assertTrue(resp["coupon_valid"])
        self.assertEqual(resp["discount_percent"], 10)

    def test_payment_history(self):
        # Cria inscrição paga
        frappe.get_doc(
            {
                "doctype": "LMS Enrollment",
                "course": self.course_name,
                "member": self.user,
                "status": "Active",
                "payment_gateway": "stripe",
                "payment_reference": "ref123",
                "amount": 100,
                "currency": "BRL",
            }
        ).insert()
        history = get_payment_history()
        self.assertTrue(any(e["course_title"] == "TestPayCourse" for e in history))


# Copyright (c) 2024, Vedium and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from vedium_core.api import get_published_courses, get_course_categories


class TestVediumAPI(FrappeTestCase):
    def test_get_categories(self):
        # Create a dummy category if none exists
        if not frappe.db.exists("LMS Category", "Test Category"):
            doc = frappe.new_doc("LMS Category")
            doc.category = "Test Category"
            # doc.description = "Test Description" # description might not be in the minimal json I saw? It was in standard fields? checking json... no description field in json excerpt.
            # But api.py queries it. Assume keeping it doesn't hurt or it's standard.
            doc.insert()

        categories = get_course_categories()
        self.assertTrue(len(categories) > 0)
        self.assertTrue("Test Category" in [c.category for c in categories])

    def test_get_published_courses(self):
        # Ensure category exists
        if not frappe.db.exists("LMS Category", "Test Category"):
            cat = frappe.new_doc("LMS Category")
            cat.category = "Test Category"
            cat.insert()

        # Ensure we have a published course
        course_name = "Test Course 101"
        if not frappe.db.exists("LMS Course", {"title": course_name}):
            doc = frappe.new_doc("LMS Course")
            doc.title = course_name
            doc.category = "Test Category"
            doc.short_introduction = "Test Short Intro"
            doc.description = "Test Full Description"
            doc.status = "Approved"  # or equivalent
            doc.append("instructors", {"instructor": "Administrator"})
            doc.published = 1
            doc.save()

        courses = get_published_courses()
        found = False
        for c in courses:
            if c.title == course_name:
                found = True
                break

        self.assertTrue(found)
