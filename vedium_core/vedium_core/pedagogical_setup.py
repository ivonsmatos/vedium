import json

import frappe


PROFESSOR_ROLE = "Vedium Professor"
COORDINATION_ROLE = "Vedium Coordenacao Pedagogica"
DOCTYPE = "Registro de Aula Vedium"
WORKSPACE_TITLE = "Pedagogia"


def ensure_pedagogical_setup():
    ensure_roles()
    ensure_workflow()
    ensure_reports()
    ensure_workspace()


def ensure_roles():
    for role in (PROFESSOR_ROLE, COORDINATION_ROLE):
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1,
            }).insert(ignore_permissions=True)


def ensure_workflow():
    if not frappe.db.exists("DocType", DOCTYPE):
        return

    for state in (
        "Rascunho",
        "Enviado",
        "Revisado pela coordenação",
        "Pendente de ajuste",
        "Concluído",
    ):
        _ensure_workflow_state(state)

    for action in (
        "Enviar para coordenação",
        "Marcar como revisado",
        "Solicitar ajuste",
        "Reenviar",
        "Concluir",
    ):
        _ensure_workflow_action(action)

    workflow_name = "Fluxo Registro de Aula Vedium"
    if frappe.db.exists("Workflow", workflow_name):
        workflow = frappe.get_doc("Workflow", workflow_name)
        workflow.states = []
        workflow.transitions = []
    else:
        workflow = frappe.new_doc("Workflow")
        workflow.workflow_name = workflow_name

    workflow.document_type = DOCTYPE
    workflow.workflow_state_field = "status_registro"
    workflow.is_active = 1
    workflow.override_status = 0
    workflow.send_email_alert = 0

    for state, doc_status, allow_edit in (
        ("Rascunho", "0", PROFESSOR_ROLE),
        ("Enviado", "0", COORDINATION_ROLE),
        ("Revisado pela coordenação", "0", COORDINATION_ROLE),
        ("Pendente de ajuste", "0", PROFESSOR_ROLE),
        ("Concluído", "0", COORDINATION_ROLE),
    ):
        workflow.append("states", {
            "state": state,
            "doc_status": doc_status,
            "allow_edit": allow_edit,
        })

    for state, action, next_state, allowed in (
        ("Rascunho", "Enviar para coordenação", "Enviado", PROFESSOR_ROLE),
        ("Enviado", "Marcar como revisado", "Revisado pela coordenação", COORDINATION_ROLE),
        ("Enviado", "Solicitar ajuste", "Pendente de ajuste", COORDINATION_ROLE),
        ("Pendente de ajuste", "Reenviar", "Enviado", PROFESSOR_ROLE),
        ("Revisado pela coordenação", "Concluir", "Concluído", COORDINATION_ROLE),
    ):
        workflow.append("transitions", {
            "state": state,
            "action": action,
            "next_state": next_state,
            "allowed": allowed,
            "allow_self_approval": 1,
        })

    workflow.save(ignore_permissions=True)


def _ensure_workflow_state(state):
    if frappe.db.exists("Workflow State", state):
        return
    frappe.get_doc({
        "doctype": "Workflow State",
        "workflow_state_name": state,
    }).insert(ignore_permissions=True)


def _ensure_workflow_action(action):
    if frappe.db.exists("Workflow Action Master", action):
        return
    frappe.get_doc({
        "doctype": "Workflow Action Master",
        "workflow_action_name": action,
    }).insert(ignore_permissions=True)


def ensure_reports():
    if not frappe.db.exists("DocType", DOCTYPE):
        return

    reports = {
        "Vedium - Frequencia por aluno": """
            SELECT
                a.aluno AS "Aluno:Link/User:220",
                COUNT(*) AS "Aulas:Int:90",
                SUM(CASE WHEN a.status_presenca IN ('Presente','Atrasado','Saida antecipada') THEN 1 ELSE 0 END) AS "Presencas:Int:100",
                SUM(CASE WHEN a.status_presenca IN ('Ausente','Falta justificada','Falta nao justificada') THEN 1 ELSE 0 END) AS "Faltas:Int:90"
            FROM `tabAluno da Aula Vedium` a
            INNER JOIN `tabRegistro de Aula Vedium` r ON r.name = a.parent
            WHERE r.status_registro != 'Rascunho'
            GROUP BY a.aluno
            ORDER BY 4 DESC, 2 DESC
        """,
        "Vedium - Frequencia por turma": """
            SELECT
                r.turma AS "Turma:Link/LMS Batch:220",
                COUNT(a.name) AS "Marcacoes:Int:100",
                SUM(CASE WHEN a.status_presenca IN ('Presente','Atrasado','Saida antecipada') THEN 1 ELSE 0 END) AS "Presencas:Int:100",
                SUM(CASE WHEN a.status_presenca IN ('Ausente','Falta justificada','Falta nao justificada') THEN 1 ELSE 0 END) AS "Faltas:Int:90"
            FROM `tabRegistro de Aula Vedium` r
            LEFT JOIN `tabAluno da Aula Vedium` a ON a.parent = r.name
            WHERE r.status_registro != 'Rascunho'
            GROUP BY r.turma
            ORDER BY 4 DESC
        """,
        "Vedium - Aulas por professor": """
            SELECT
                professor AS "Professor:Link/User:220",
                COUNT(*) AS "Aulas registradas:Int:130",
                SUM(CASE WHEN status_registro = 'Enviado' THEN 1 ELSE 0 END) AS "Pendentes de revisão:Int:150",
                SUM(CASE WHEN status_registro = 'Concluído' THEN 1 ELSE 0 END) AS "Concluidas:Int:100"
            FROM `tabRegistro de Aula Vedium`
            GROUP BY professor
            ORDER BY 2 DESC
        """,
        "Vedium - Alertas de coordenacao": """
            SELECT
                r.name AS "Registro:Link/Registro de Aula Vedium:180",
                r.data_aula AS "Data:Date:100",
                r.curso AS "Curso:Link/LMS Course:220",
                r.turma AS "Turma:Link/LMS Batch:220",
                r.professor AS "Professor:Link/User:220",
                a.aluno AS "Aluno:Link/User:220",
                a.tipo_alerta AS "Tipo:Data:120",
                a.prioridade AS "Prioridade:Data:100",
                a.observacao_individual AS "Observação:Text:260"
            FROM `tabRegistro de Aula Vedium` r
            INNER JOIN `tabAluno da Aula Vedium` a ON a.parent = r.name
            WHERE a.criar_alerta_coordenacao = 1 OR a.encaminhar_para_coordenacao = 1
            ORDER BY r.data_aula DESC, a.prioridade DESC
        """,
        "Vedium - Alunos que precisam de reforco": """
            SELECT
                a.aluno AS "Aluno:Link/User:220",
                r.curso AS "Curso:Link/LMS Course:220",
                r.turma AS "Turma:Link/LMS Batch:220",
                COUNT(*) AS "Ocorrencias:Int:110",
                MAX(r.data_aula) AS "Última aula:Date:110"
            FROM `tabAluno da Aula Vedium` a
            INNER JOIN `tabRegistro de Aula Vedium` r ON r.name = a.parent
            WHERE a.precisa_reforco = 1
            GROUP BY a.aluno, r.curso, r.turma
            ORDER BY 4 DESC
        """,
        "Vedium - Registros pendentes de revisao": """
            SELECT
                name AS "Registro:Link/Registro de Aula Vedium:180",
                data_aula AS "Data:Date:100",
                curso AS "Curso:Link/LMS Course:220",
                turma AS "Turma:Link/LMS Batch:220",
                professor AS "Professor:Link/User:220",
                status_registro AS "Status:Data:180",
                modified AS "Última alteração:Datetime:160"
            FROM `tabRegistro de Aula Vedium`
            WHERE status_registro IN ('Enviado','Pendente de ajuste','Rascunho')
            ORDER BY modified DESC
        """,
    }

    for report_name, query in reports.items():
        if frappe.db.exists("Report", report_name):
            report = frappe.get_doc("Report", report_name)
            report.query = _clean_query(query)
        else:
            report = frappe.get_doc({
                "doctype": "Report",
                "report_name": report_name,
                "ref_doctype": DOCTYPE,
                "report_type": "Query Report",
                "is_standard": "No",
                "module": "Vedium Core",
                "query": _clean_query(query),
                "roles": [
                    {"role": "System Manager"},
                    {"role": COORDINATION_ROLE},
                ],
            })
        report.save(ignore_permissions=True)


def ensure_workspace():
    if not frappe.db.exists("DocType", DOCTYPE) or not frappe.db.exists("DocType", "Workspace"):
        return

    report_names = [
        "Vedium - Frequencia por aluno",
        "Vedium - Frequencia por turma",
        "Vedium - Aulas por professor",
        "Vedium - Alertas de coordenacao",
        "Vedium - Alunos que precisam de reforco",
        "Vedium - Registros pendentes de revisao",
    ]
    reports_card = "Relatórios pedagógicos"

    content = [
        {"id": "header-pedagogia", "type": "header",
         "data": {"text": "<span class=\"h4\"><b>Pedagogia</b></span>", "col": 12}},
        {"id": "shortcut-novo-registro", "type": "shortcut",
         "data": {"shortcut_name": "Novo Registro de Aula", "col": 3}},
        {"id": "shortcut-lista-registros", "type": "shortcut",
         "data": {"shortcut_name": "Registros de Aula", "col": 3}},
        {"id": "card-relatorios", "type": "card",
         "data": {"card_name": reports_card, "col": 4}},
    ]

    if frappe.db.exists("Workspace", WORKSPACE_TITLE):
        workspace = frappe.get_doc("Workspace", WORKSPACE_TITLE)
    else:
        workspace = frappe.new_doc("Workspace")
        workspace.title = WORKSPACE_TITLE
        workspace.label = WORKSPACE_TITLE

    workspace.icon = "education"
    workspace.module = "Vedium Core"
    workspace.public = 1
    workspace.is_hidden = 0
    workspace.content = json.dumps(content)

    workspace.shortcuts = []
    for shortcut in (
        {
            "label": "Novo Registro de Aula",
            "type": "DocType",
            "link_to": DOCTYPE,
            "doc_view": "New",
            "icon": "small-file",
            "color": "Green",
        },
        {
            "label": "Registros de Aula",
            "type": "DocType",
            "link_to": DOCTYPE,
            "doc_view": "List",
            "icon": "list",
            "color": "Blue",
        },
    ):
        workspace.append("shortcuts", shortcut)

    workspace.links = []
    workspace.append("links", {"label": reports_card, "type": "Card Break"})
    for report_name in report_names:
        workspace.append("links", {
            "label": report_name,
            "type": "Link",
            "link_type": "Report",
            "link_to": report_name,
            "is_query_report": 1,
        })

    workspace.save(ignore_permissions=True)


def _clean_query(query):
    return "\n".join(line.strip() for line in query.strip().splitlines())
