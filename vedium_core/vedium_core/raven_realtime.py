"""Robustez do realtime do Raven (chat) — patch idempotente do bundle.

Contexto: `frappe-react-sdk` (usado pelo Raven) NÃO expõe `transports` como opção
ao instanciar o `socket.io-client`, então cai no default (`polling` + upgrade). O
handshake de long-polling do Engine.IO fica instável atravessando a rede anycast
do Cloudflare (requests da mesma sessão chegando por nós de borda diferentes, fora
de ordem) → o realtime do chat quebra ("Realtime events are not working"; mensagens
só aparecem após refresh). O fix força `transports:["websocket"]` direto no bundle
JS já compilado/minificado servido em produção.

O problema do fix manual: o hash do bundle muda a cada rebuild do Raven
(`index-<hash>.js`), então um `bench update raven` sobrescreve e desfaz o patch sem
aviso. Este módulo reaplica o patch de forma IDEMPOTENTE e roda no `after_migrate`
(todo deploy) + pode ser chamado à mão após atualizar o Raven:

    bench --site <site> execute vedium_core.raven_realtime.ensure_websocket_patch

Fix definitivo (upstream) seria expor `transports` como prop do `FrappeProvider`
no `frappe-react-sdk`; enquanto isso não existe, este re-patch é a rede de proteção.
"""

import os

import frappe

# O socket.io-client é instanciado com estas opções no bundle minificado. O patch
# insere `transports:["websocket"],` entre `secure:...` e `extraHeaders:`. Os nomes
# das PROPRIEDADES não são minificados (fazem parte da API do socket.io), então o
# anchor é estável entre rebuilds mesmo que variáveis locais mudem de nome.
_ANCHOR = 'secure:this.protocol==="https",extraHeaders:'
_PATCHED = 'secure:this.protocol==="https",transports:["websocket"],extraHeaders:'
_MARKER = 'transports:["websocket"]'


def _assets_dir():
    return frappe.get_app_path("raven", "public", "raven", "assets")


def ensure_websocket_patch():
    """Reaplica (idempotente) o patch 'força WebSocket' nos bundles do Raven.

    Retorna dict: {"patched": [arquivos alterados], "already": [já ok], ...}.
    Nunca levanta — realtime é user-facing, mas não pode quebrar o migrate/deploy.
    """
    try:
        assets = _assets_dir()
    except Exception:
        return {"patched": [], "skipped": "raven não instalado"}
    if not os.path.isdir(assets):
        return {"patched": [], "skipped": "diretório de assets do raven ausente"}

    patched, already = [], []
    for fname in sorted(os.listdir(assets)):
        if not (fname.startswith("index-") and fname.endswith(".js")):
            continue
        path = os.path.join(assets, fname)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        if _MARKER in content:
            already.append(fname)
            continue
        if _ANCHOR not in content:
            continue  # chunk/vendor sem a instanciação do socket
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content.replace(_ANCHOR, _PATCHED))
            patched.append(fname)
        except OSError:
            frappe.log_error(
                f"Falha ao escrever patch websocket em {fname}",
                "Vedium.raven_realtime",
            )

    if patched:
        frappe.logger().info(f"Raven websocket patch aplicado: {patched}")
    return {"patched": patched, "already": already}


def is_realtime_patched():
    """True se o bundle principal do Raven (o que tem o socket) está patchado.

    Usado pelo health check. Se nenhum bundle tem o anchor, considera N/A (True)
    para não gerar falso-alarme quando o Raven muda de estrutura.
    """
    try:
        assets = _assets_dir()
    except Exception:
        return True
    if not os.path.isdir(assets):
        return True
    saw_socket_bundle = False
    for fname in os.listdir(assets):
        if not (fname.startswith("index-") and fname.endswith(".js")):
            continue
        path = os.path.join(assets, fname)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        if _MARKER in content:
            return True
        if _ANCHOR in content:
            saw_socket_bundle = True
    # Achou o bundle do socket mas sem o marcador => não patchado.
    return not saw_socket_bundle
