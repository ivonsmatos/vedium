# -*- coding: utf-8 -*-
"""Diagnóstico do Tutor IA (somente leitura, não expõe a chave da Groq).

O widget de chat em /meu-progresso não respondeu (nem mensagem do assistente
nem erro visível) para o usuário. Este script checa, na ordem mais provável
de causa:

  1. Se a GROQ_API_KEY está configurada (só imprime presença/tamanho, nunca
     o valor).
  2. Se a lib 'groq' está instalada no ambiente do container.
  3. Faz uma chamada real e mínima à Groq com os mesmos modelos/fallbacks do
     ai_tutor.py, pra ver a mensagem de erro exata se falhar.
  4. Confirma se os doctypes "Vedium AI Chat Session"/"Vedium AI Chat
     Message" existem (ensure_ai_tutor_doctypes já deveria ter criado).
  5. Lista os últimos Error Log com "ai_tutor" no título/traceback.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_ai_tutor.run
"""

import frappe


def run():
    key = frappe.conf.get("groq_api_key") or frappe.db.get_single_value(
        "System Settings", "custom_groq_api_key"
    )
    print("groq_api_key presente:", bool(key), "| tamanho:", len(key) if key else 0)

    model = (
        frappe.conf.get("vedium_ai_tutor_model")
        or frappe.db.get_single_value("System Settings", "custom_vedium_ai_tutor_model")
        or "openai/gpt-oss-120b"
    )
    print("Modelo configurado:", model)

    for doctype in ("Vedium AI Chat Session", "Vedium AI Chat Message"):
        print(f"DocType {doctype!r} existe:", bool(frappe.db.exists("DocType", doctype)))

    if not key:
        print("\n=> Sem chave configurada. Esse é o motivo do chat não responder.")
    else:
        try:
            from groq import Groq
        except Exception as e:
            print("FALHA ao importar 'groq':", type(e).__name__, "|", str(e)[:200])
            return

        client = Groq(api_key=key)
        from vedium_core.ai_tutor import _create_groq_completion

        try:
            completion, used_model = _create_groq_completion(
                client,
                [
                    {"role": "system", "content": "Responda só 'ok'."},
                    {"role": "user", "content": "teste de diagnostico"},
                ],
            )
            reply = completion.choices[0].message.content
            print(f"\n=> Chamada Groq OK (modelo {used_model!r}). Resposta:", reply[:200])
        except Exception as e:
            print("\n=> Chamada Groq FALHOU ->", type(e).__name__, "|", str(e)[:400])

    print("\nÚltimos Error Log com 'ai_tutor':")
    logs = frappe.get_all(
        "Error Log",
        filters=[["error", "like", "%ai_tutor%"]],
        fields=["name", "creation", "error"],
        order_by="creation desc",
        limit_page_length=5,
    )
    if not logs:
        print("  (nenhum)")
    for log in logs:
        first_line = (log.error or "").strip().splitlines()[-1][:200] if log.error else ""
        print(f"  {log.creation} [{log.name}] {first_line}")
