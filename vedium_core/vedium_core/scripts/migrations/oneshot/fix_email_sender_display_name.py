"""Corrige o nome de exibição do remetente dos e-mails da Vedium.

Causa raiz: o Frappe usa o NOME DO DOCUMENTO "Email Account" (não um campo
separado) como parte do cabeçalho From — ver
`EmailAccount.default_sender` em apps/frappe/frappe/email/doctype/
email_account/email_account.py:
    email.utils.formataddr((self.name, self.get("email_id")))

A conta de envio da Vedium foi criada com o nome "Vedium Resend" (provável
referência ao provedor SMTP usado, Resend), então todo e-mail enviado pela
plataforma chega como "Vedium Resend <contato@vediums.com>" — nome estranho
para quem recebe (menciona um provedor terceiro, não a marca).

Fix: renomeia o documento para "Vedium" via frappe.rename_doc (operação
nativa do Frappe, atualiza automaticamente qualquer referência Link em
outros doctypes). Nenhum código do vedium_core referencia "Vedium Resend"
como string fixa (confirmado via grep antes deste commit), então não há
nada mais a ajustar no repo.

Idempotente: se o documento já se chama "Vedium" (ou "Vedium Resend" não
existir mais), não faz nada.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.fix_email_sender_display_name.run
"""
import frappe

OLD_NAME = "Vedium Resend"
NEW_NAME = "Vedium"


def run():
    if frappe.db.exists("Email Account", NEW_NAME):
        print(f"Já correto: Email Account '{NEW_NAME}' existe.")
        return

    if not frappe.db.exists("Email Account", OLD_NAME):
        print(f"Nada a fazer: Email Account '{OLD_NAME}' não existe.")
        return

    frappe.rename_doc("Email Account", OLD_NAME, NEW_NAME, force=True)
    frappe.db.commit()
    print(f"Email Account renomeado: '{OLD_NAME}' -> '{NEW_NAME}'.")
    print("E-mails da plataforma agora chegam como 'Vedium <contato@vediums.com>'.")
