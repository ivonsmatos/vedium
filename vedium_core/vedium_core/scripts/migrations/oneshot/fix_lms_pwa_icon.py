"""Corrige o ícone do app.vediums.com (PWA/splash mostrando o chapéu de
formatura padrão do Frappe LMS em vez da marca Vedium).

Causa raiz: `lms.lms.api.get_pwa_manifest` usa
`Website Settings.banner_image` como ícone do manifest; se estiver vazio,
cai no fallback `manifest-icon-192.maskable.png` do próprio app lms — o
chapéu de formatura azul que aparece na splash/ícone instalado.

⚠️ O ícone PRECISA ser o de 192x192: get_pwa_manifest declara
"sizes": "192x192" fixo no manifest, então arquivo de outra dimensão
(a 1ª versão deste fix usava o de 512x512) é rejeitado na validação do
navegador e o chapéu volta (achado do QA 2026-07-01).

Correção: aponta banner_image para o ícone oficial da Vedium em 192x192.
Idempotente.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.fix_lms_pwa_icon.run
"""
import frappe

VEDIUM_ICON = "/assets/vedium_core/images/icon-192x192.png"


def run():
    current = frappe.db.get_single_value("Website Settings", "banner_image")
    if current == VEDIUM_ICON:
        print(f"Já correto: banner_image = {current}")
        return

    frappe.db.set_single_value("Website Settings", "banner_image", VEDIUM_ICON)
    frappe.db.commit()
    print(f"banner_image: {current!r} -> {VEDIUM_ICON!r}")
    print("Ícone do PWA/app.vediums.com corrigido para a marca Vedium.")
