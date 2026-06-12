import frappe

def create_sample_test():
	if frappe.db.exists("Placement Test", "Inglês Inicial"):
		return
	
	test = frappe.get_doc({
		"doctype": "Placement Test",
		"title": "Inglês Inicial",
		"description": "Teste rápido para iniciantes. Avalie seu nível de A1.",
		"target_course": "Inglês Iniciante", # Assumes this course exists
		"min_score": 70,
		"max_time": 15,
		"questions": [
			{
				"question": "What is the correct form: 'I ____ a student'?",
				"option_a": "am",
				"option_b": "is",
				"option_c": "are",
				"option_d": "be",
				"correct_answer": "A",
				"points": 1,
				"difficulty": "Beginner"
			},
			{
				"question": "How do you say 'Livro' in English?",
				"option_a": "Pen",
				"option_b": "Book",
				"option_c": "Table",
				"option_d": "Chair",
				"correct_answer": "B",
				"points": 1,
				"difficulty": "Beginner"
			}
		]
	})
	test.insert()
	frappe.db.commit()

if __name__ == "__main__":
	create_sample_test()
