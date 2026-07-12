frappe.ui.form.on("Candidatura", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Aprovada") {
			return;
		}
		frm.add_custom_button("Aprovar como Professor", () => {
			const dialog = new frappe.ui.Dialog({
				title: "Aprovar candidatura como professor",
				fields: [
					{
						fieldname: "funcao",
						fieldtype: "Select",
						label: "Função",
						reqd: 1,
						options: [
							"Inglês",
							"Espanhol",
							"Português para Estrangeiros (PLE)",
							"Hebraico",
							"Iorubá",
							"Coordenação Pedagógica",
						].join("\n"),
					},
				],
				primary_action_label: "Aprovar",
				primary_action: (values) => {
					frappe.call({
						method: "vedium_core.careers.approve_candidatura_as_professor",
						args: { candidatura_name: frm.doc.name, funcao: values.funcao },
						freeze: true,
						freeze_message: "Aprovando...",
						callback: (r) => {
							dialog.hide();
							if (r.message && r.message.ok) {
								frappe.msgprint(
									`Professor aprovado (${r.message.funcao}). Usuário: ${r.message.user}.`
								);
								frm.reload_doc();
							}
						},
					});
				},
			});
			dialog.show();
		}).addClass("btn-primary");
	},
});
