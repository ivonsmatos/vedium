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
			frappe.db.get_value("User", user, "vedium_points") + points)
		
		# In production, we'd also create a 'Point Transaction' log entry.
		frappe.msgprint(f"You earned {points} points for {reason}!")

	@staticmethod
	def handle_lesson_completion(user, course, lesson):
		"""
		Standard reward for completing a lesson.
		"""
		Gamification.add_points(user, 10, f"completing lesson {lesson}")
