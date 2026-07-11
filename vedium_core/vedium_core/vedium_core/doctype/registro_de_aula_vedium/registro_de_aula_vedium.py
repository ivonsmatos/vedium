import frappe
from frappe import _
from frappe.model.document import Document


class RegistrodeAulaVedium(Document):
    def validate(self):
        if self.horario_inicio and self.horario_termino:
            if str(self.horario_termino) <= str(self.horario_inicio):
                frappe.throw(_("Horario de termino deve ser posterior ao horario de inicio."))

        if not self.professor:
            self.professor = frappe.session.user

    def before_save(self):
        self._set_alert_flags()

    def on_update(self):
        self._notify_pedagogical_alerts()
        self._notify_pending_adjustment()

    def _set_alert_flags(self):
        self.total_alunos = len(self.alunos or [])
        self.total_presentes = len([
            row for row in self.alunos or []
            if row.status_presenca in ("Presente", "Atrasado", "Saida antecipada")
        ])
        self.total_ausentes = len([
            row for row in self.alunos or []
            if row.status_presenca in ("Ausente", "Falta justificada", "Falta nao justificada")
        ])
        self.tem_alerta_coordenacao = any(
            row.criar_alerta_coordenacao or row.encaminhar_para_coordenacao
            for row in self.alunos or []
        )

    def _notify_pedagogical_alerts(self):
        if not self.tem_alerta_coordenacao:
            return
        if getattr(self.flags, "_pedagogical_alert_notified", False):
            return

        for user in _users_with_role("Vedium Coordenacao Pedagogica"):
            _create_todo_once(
                user=user,
                reference_type=self.doctype,
                reference_name=self.name,
                description=(
                    f"Registro de aula com alerta para coordenacao: {self.name} "
                    f"({self.tema_aula or self.curso})"
                ),
                priority="High",
            )
        self.flags._pedagogical_alert_notified = True

    def _notify_pending_adjustment(self):
        if self.status_registro != "Pendente de ajuste" or not self.professor:
            return
        _create_todo_once(
            user=self.professor,
            reference_type=self.doctype,
            reference_name=self.name,
            description=f"Registro de aula devolvido para ajuste: {self.name}",
            priority="Medium",
        )


def has_permission(doc, ptype, user):
    if not user or user == "Guest":
        return False
    if "System Manager" in frappe.get_roles(user):
        return True
    if "Vedium Coordenacao Pedagogica" in frappe.get_roles(user):
        return True
    if "Vedium Professor" not in frappe.get_roles(user):
        return False

    is_owner_or_teacher = doc.owner == user or doc.professor == user
    if ptype == "create":
        return True
    if ptype in ("read", "print", "email"):
        return is_owner_or_teacher
    if ptype == "write":
        return is_owner_or_teacher and doc.status_registro in ("Rascunho", "Pendente de ajuste")
    if ptype == "delete":
        return is_owner_or_teacher and doc.status_registro == "Rascunho"
    return False


def remind_draft_records():
    records = frappe.get_all(
        "Registro de Aula Vedium",
        filters={
            "status_registro": "Rascunho",
            "modified": ("<", frappe.utils.add_to_date(frappe.utils.now_datetime(), hours=-24)),
        },
        fields=["name", "professor", "tema_aula"],
        limit=200,
    )
    for record in records:
        if not record.professor:
            continue
        _create_todo_once(
            user=record.professor,
            reference_type="Registro de Aula Vedium",
            reference_name=record.name,
            description=f"Registro de aula ainda em rascunho ha mais de 24h: {record.tema_aula or record.name}",
            priority="Medium",
        )


def _users_with_role(role):
    return frappe.get_all(
        "Has Role",
        filters={"role": role, "parenttype": "User"},
        pluck="parent",
        distinct=True,
    )


def _create_todo_once(user, reference_type, reference_name, description, priority):
    existing = frappe.db.exists(
        "ToDo",
        {
            "allocated_to": user,
            "reference_type": reference_type,
            "reference_name": reference_name,
            "description": description,
            "status": ("!=", "Closed"),
        },
    )
    if existing:
        return
    todo = frappe.get_doc({
        "doctype": "ToDo",
        "allocated_to": user,
        "reference_type": reference_type,
        "reference_name": reference_name,
        "description": description,
        "priority": priority,
    })
    todo.insert(ignore_permissions=True)
