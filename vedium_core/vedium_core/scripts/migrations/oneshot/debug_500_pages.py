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
    # frappe.log_error() parece estar engolindo a excecao original (nenhum
    # Error Log novo aparece apesar dos 500 confirmados) -- monkeypatch pra
    # imprimir o traceback ORIGINAL antes de qualquer coisa que log_error
    # tente fazer (e capturar se o proprio log_error tambem falhar).
    original_log_error = frappe.log_error

    def patched_log_error(*args, **kwargs):
        print(">>> frappe.log_error foi chamado, traceback original:")
        print(frappe.get_traceback())
        try:
            return original_log_error(*args, **kwargs)
        except Exception:
            print(">>> frappe.log_error EM SI lancou excecao:")
            traceback.print_exc()

    frappe.log_error = patched_log_error

    from werkzeug.test import EnvironBuilder
    from werkzeug.wrappers import Request as WerkzeugRequest
    from frappe.website.serve import get_response

    for page in PAGES:
        print(f"\n=== {page} ===")
        try:
            frappe.set_user("Guest")
            # fake request context minimo -- get_response/NotPermittedPage
            # acessam frappe.request.path, que so existe dentro de uma
            # request WSGI real.
            builder = EnvironBuilder(path=f"/{page}", method="GET")
            frappe.local.request = WerkzeugRequest(builder.get_environ())
            resp = get_response(page)
            print("status:", resp.status_code)
            if resp.status_code >= 400:
                try:
                    body = resp.get_data(as_text=True)
                    print("body (primeiros 2000 chars):")
                    print(body[:2000])
                except Exception:
                    pass
        except Exception:
            print("EXCEPTION (nao capturada pelo get_response):")
            traceback.print_exc()
        finally:
            frappe.set_user("Administrator")

    frappe.log_error = original_log_error
