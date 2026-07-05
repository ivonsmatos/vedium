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
    from werkzeug.test import EnvironBuilder
    from werkzeug.wrappers import Request as WerkzeugRequest
    from frappe.website.path_resolver import PathResolver

    for page in PAGES:
        print(f"\n=== {page} ===")
        try:
            frappe.set_user("Guest")
            builder = EnvironBuilder(path=f"/{page}", method="GET")
            frappe.local.request = WerkzeugRequest(builder.get_environ())
            # Chama o resolver + renderer diretamente, pulando o
            # get_response() de mais alto nivel que engole a excecao e
            # devolve so um 500 generico (nao chama frappe.log_error nem
            # propaga o traceback pro chamador).
            resolver = PathResolver(page)
            result = resolver.resolve()
            # resolve() pode devolver so o renderer OU uma tupla
            # (endpoint, renderer) dependendo da versao do frappe --
            # cobre os dois casos.
            renderer = result[-1] if isinstance(result, (tuple, list)) else result
            print("tipo do resolve():", type(result).__name__, "-> renderer:", type(renderer).__name__)
            html = renderer.render()
            if hasattr(html, "status_code"):
                print("status:", html.status_code)
            else:
                print("render retornou:", type(html).__name__, str(html)[:300])
        except Exception:
            print("EXCEPTION (traceback real, direto do renderer):")
            traceback.print_exc()
        finally:
            frappe.set_user("Administrator")
