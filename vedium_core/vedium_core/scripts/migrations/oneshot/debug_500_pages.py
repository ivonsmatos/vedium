"""Diagnostico temporario: renderiza algumas paginas publicas diretamente
no servidor (sem passar por gunicorn/nginx) e imprime o traceback real de
qualquer excecao, ja que a producao esconde o traceback do navegador
(developer_mode=0) e o erro nao estava aparecendo no Error Log nem no
stdout do gunicorn pras rotas que davam 500/403.

So leitura -- nao muda nada no banco. Apagar depois de usar.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.debug_500_pages.run
"""
import traceback

import frappe

PAGES = ["sobre", "catalogo", "empresas", "diferenciais", "blog"]


def run():
    from frappe.website.serve import get_response

    for page in PAGES:
        print(f"\n=== {page} ===")
        try:
            frappe.set_user("Guest")
            resp = get_response(page)
            print("status:", resp.status_code)
        except Exception:
            print("EXCEPTION:")
            traceback.print_exc()
        finally:
            frappe.set_user("Administrator")
