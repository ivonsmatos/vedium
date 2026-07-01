"""Resolve a colisão do doctype 'LMS Certificate'.

Contexto: o `vedium_core` shipava um doctype custom com `name: "LMS Certificate"`
(módulo "Vedium Core"), idêntico em nome ao doctype NATIVO do Frappe LMS. Como
nome de doctype é único no Frappe e o `vedium_core` migra depois do `lms`, o
custom vencia o `bench migrate` e passava a "dono" da tabela — sequestrando o
certificado nativo (controller, form e definição de campos do LMS eram ignorados).

Correção (idempotente):
1. Reimporta o doctype NATIVO do app `lms` com force, restaurando module="LMS",
   os campos nativos e o controller oficial. Sem isso, remover o JSON custom não
   basta: se o `bench migrate` não detectar mudança no JSON do lms, o module fica
   preso em "Vedium Core" (órfão).
2. Recria os Custom Fields da Vedium (verification_code, enrollment) sobre o
   nativo, via setup_custom_fields — as colunas já existem na tabela, então é só
   registrar os Custom Fields.

Seguro em produção: há 0 registros de certificado (verificado em 2026-07-01).

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.fix_certificate_collision.run
"""
import frappe


def run():
    before = frappe.db.get_value("DocType", "LMS Certificate", "module")
    print(f"Antes: LMS Certificate.module = {before}")

    # 1. Restaura o doctype nativo do LMS (module, campos e controller).
    frappe.reload_doc("lms", "doctype", "lms_certificate", force=True)

    # 2. Reaplica os Custom Fields da Vedium sobre o nativo.
    from vedium_core.custom_setup import setup_custom_fields

    setup_custom_fields()
    frappe.db.commit()

    after = frappe.db.get_value("DocType", "LMS Certificate", "module")
    has_vcode = frappe.db.exists(
        "Custom Field", {"dt": "LMS Certificate", "fieldname": "verification_code"}
    )
    has_enrollment = frappe.db.exists(
        "Custom Field", {"dt": "LMS Certificate", "fieldname": "enrollment"}
    )
    print(f"Depois: LMS Certificate.module = {after}")
    print(f"Custom Field verification_code: {'OK' if has_vcode else 'FALTANDO'}")
    print(f"Custom Field enrollment: {'OK' if has_enrollment else 'FALTANDO'}")

    if after == "LMS" and has_vcode and has_enrollment:
        print("\n✅ Colisão resolvida: certificado nativo restaurado + extensões Vedium.")
    else:
        print("\n⚠️ Estado inesperado — revisar manualmente.")
