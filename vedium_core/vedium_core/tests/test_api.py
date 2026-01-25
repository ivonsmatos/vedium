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
			doc.status = "Approved" # or equivalent
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
