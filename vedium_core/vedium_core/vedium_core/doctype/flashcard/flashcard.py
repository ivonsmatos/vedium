import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today

class Flashcard(Document):
	def on_update(self):
		pass

	@frappe.whitelist()
	def update_srs(self, quality):
		"""
		Simple SM-2 implementation.
		quality: 0-5 (0 = forgot, 5 = perfect)
		"""
		# quality: 0: Total blackout, 1: Incorrect, 2: Correct (hard), 3: Correct (medium), 4: Correct (easy), 5: Perfect
		if quality < 3:
			self.repetition_count = 0
			self.interval = 1
		else:
			if self.repetition_count == 0:
				self.interval = 1
			elif self.repetition_count == 1:
				self.interval = 6
			else:
				self.interval = int(self.interval * self.ease_factor)
			
			self.repetition_count += 1
		
		# Ease factor calculation: EF' = EF + (0.1 - (5-q)*(0.08 + (5-q)*0.02))
		self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
		
		self.next_review = add_days(today(), self.interval)
		self.save()
		return self.next_review
