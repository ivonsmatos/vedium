import frappe


class Gamification:
    @staticmethod
    def add_points(user, points, reason="Action"):
        """
        Soma pontos ao usuário usando UPDATE atômico.

        Original usava get_value + set_value, o que perdia atualizações
        concorrentes (race condition quando 2 lições terminam no mesmo
        instante — última escrita sobrescreve a outra).
        """
        if not user or not points:
            return

        try:
            frappe.db.sql(
                """
                UPDATE `tabUser`
                SET vedium_points = COALESCE(vedium_points, 0) + %s
                WHERE name = %s
                """,
                (points, user),
            )
        except Exception as e:
            # Campo customizado vedium_points pode não existir ainda — não
            # quebra o fluxo de conclusão de lição.
            frappe.log_error(
                f"add_points falhou para {user} (+{points}): {e}",
                "Vedium.gamification.add_points",
            )

    @staticmethod
    def handle_lesson_completion(doc, method):
        """Recompensa padrão para conclusão de uma lição."""
        Gamification.add_points(
            doc.member, 10, f"completing a lesson in {doc.course}"
        )
