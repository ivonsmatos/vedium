import re

import frappe
from frappe.model.document import Document


class VediumBlogPost(Document):
	def validate(self):
		if not self.slug:
			self.slug = re.sub(r"[^a-z0-9]+", "-", (self.title or "").lower()).strip("-")
		self.slug = re.sub(r"[^a-z0-9]+", "-", self.slug.lower()).strip("-")
