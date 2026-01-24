# Copyright (c) 2024, Vedium and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from vedium_core.vedium_core.api import get_published_courses, get_course_categories

class TestVediumAPI(FrappeTestCase):
	def test_get_categories(self):
		# Create a dummy category if none exists
		if not frappe.db.exists("LMS Category", "Test Category"):
			doc = frappe.new_doc("LMS Category")
			doc.category_name = "Test Category"
			doc.description = "Test Description"
			doc.insert()

		categories = get_course_categories()
		self.assertTrue(len(categories) > 0)
		self.assertTrue("Test Category" in [c.category_name for c in categories])

	def test_get_published_courses(self):
		# Ensure we have a published course
		course_name = "Test Course 101"
		if not frappe.db.exists("LMS Course", {"title": course_name}):
			doc = frappe.new_doc("LMS Course")
			doc.title = course_name
			doc.published = 1
			doc.save()
		
		courses = get_published_courses()
		found = False
		for c in courses:
			if c.title == course_name:
				found = True
				break
		
		self.assertTrue(found)
