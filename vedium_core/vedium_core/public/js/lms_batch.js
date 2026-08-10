// Botão "Gerar aulas ao vivo" no formulário da turma (LMS Batch) — tira o
// gerador da linha de comando (P2). Chama o método whitelisted (staff-only)
// vedium_core.live_class_scheduler.generate_live_classes_for_batch.
frappe.ui.form.on("LMS Batch", {
	refresh(frm) {
		if (frm.is_new()) {
			return;
		}
		frm.add_custom_button("Gerar aulas ao vivo", () => {
			const dialog = new frappe.ui.Dialog({
				title: "Gerar aulas ao vivo recorrentes",
				fields: [
					{
						fieldname: "weekdays",
						fieldtype: "MultiCheck",
						label: "Dias da semana",
						reqd: 1,
						columns: 2,
						options: [
							{ label: "Segunda", value: "segunda" },
							{ label: "Terça", value: "terca" },
							{ label: "Quarta", value: "quarta" },
							{ label: "Quinta", value: "quinta" },
							{ label: "Sexta", value: "sexta" },
							{ label: "Sábado", value: "sabado" },
							{ label: "Domingo", value: "domingo" },
						],
					},
					{
						fieldname: "host",
						fieldtype: "Link",
						options: "User",
						label: "Professor (host)",
						description: "Vazio = usa o 1º instrutor da turma.",
					},
					{
						fieldname: "duration",
						fieldtype: "Int",
						label: "Duração (min)",
						description: "Opcional; default = janela da turma ou 60.",
					},
				],
				primary_action_label: "Gerar",
				primary_action: (values) => {
					if (!values.weekdays || !values.weekdays.length) {
						frappe.msgprint("Escolha ao menos um dia da semana.");
						return;
					}
					frappe.call({
						method: "vedium_core.live_class_scheduler.generate_live_classes_for_batch",
						args: {
							batch_name: frm.doc.name,
							weekdays: values.weekdays,
							host: values.host || null,
							duration: values.duration || null,
						},
						freeze: true,
						freeze_message: "Gerando aulas...",
						callback: (r) => {
							dialog.hide();
							if (r.message) {
								frappe.msgprint(
									`Aulas criadas: <b>${r.message.created}</b>. ` +
										`Já existiam: ${r.message.skipped}. Host: ${r.message.host}.`
								);
							}
						},
					});
				},
			});
			dialog.show();
		});
	},
});
