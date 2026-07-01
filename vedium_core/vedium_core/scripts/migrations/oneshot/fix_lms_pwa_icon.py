"""Corrige o ícone do app.vediums.com (PWA/splash mostrando o chapéu de
formatura padrão do Frappe LMS em vez da marca Vedium).

Causa raiz: `lms.lms.api.get_pwa_manifest` usa
`Website Settings.banner_image` como ícone do manifest; se estiver vazio,
cai no fallback `manifest-icon-192.maskable.png` do próprio app lms — o
chapéu de formatura azul que aparece na splash/ícone instalado.

Correção: aponta banner_image para o ícone oficial da Vedium (já usado no
manifest do site institucional). Idempotente.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.fix_lms_pwa_icon.run
"""
import frappe

VEDIUM_ICON = "/assets/vedium_core/images/icon-512x512.png"


def run():
    current = frappe.db.get_single_value("Website Settings", "banner_image")
    if current == VEDIUM_ICON:
        print(f"Já correto: banner_image = {current}")
        return

    frappe.db.set_single_value("Website Settings", "banner_image", VEDIUM_ICON)
    frappe.db.commit()
    print(f"banner_image: {current!r} -> {VEDIUM_ICON!r}")
    print("Ícone do PWA/app.vediums.com corrigido para a marca Vedium.")
