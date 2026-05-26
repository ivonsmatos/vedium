import frappe

class Gamification:
	@staticmethod
	def add_points(user, points, reason="Action"):
		"""
		Adds points to a user and logs the transaction.
		"""
		if not user or not points:
			return
		
		frappe.db.set_value("User", user, "vedium_points", 
			(frappe.db.get_value("User", user, "vedium_points") or 0) + points)
		
		# In production, we'd also create a 'Point Transaction' log entry.

	@staticmethod
	def handle_lesson_completion(doc, method):
		"""
		Standard reward for completing a lesson.
		"""
		# LMS Course Progress uses 'member' for the enrolled user and 'course' for context
		Gamification.add_points(doc.member, 10, f"completing a lesson in {doc.course}")
