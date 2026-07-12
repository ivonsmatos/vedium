# -*- coding: utf-8 -*-
"""
Vedium — Tutor IA (RAG + Groq)

Pedido do usuário (2026-07-09): "chat tutor onde posso por dentro do servidor
uma rag conectado com o API do GROQ para responder os alunos, ou conectado
com toda a documentação do frapper para ajudar com duvidas da plataforma e
ajudar no desenvolvimento do aprendizado".

Este módulo SUBSTITUI vedium_core/controllers/ai_controller.py (nunca
chamado por nenhuma página, dependia de doctypes "AI Persona"/
"AI Interaction Log" que nunca existiram, e usava o modelo Groq
"llama3-70b-8192", removido do catálogo há muito tempo).

Arquitetura (deliberadamente simples — sem vector DB/embeddings, que
adicionaria dependência pesada num servidor que já teve outage por falta
de RAM, ver memória do projeto):

    1. RAG por palavra-chave (sem custo, sem dependência nova) sobre DUAS
       bases de conhecimento reais:
       - Conteúdo das lições do curso em que o aluno está matriculado
         (Course Lesson.content/body) -- ajuda pedagógica.
       - FAQ curado sobre a PRÓPRIA plataforma Vedium (progresso,
         certificado, indicação, prática diária...) -- dúvidas de uso.
       "Documentação do Frappe" genérica (frappe.io) NÃO entra aqui: o
       aluno pergunta sobre a Vedium, não sobre o framework por baixo.
    2. Persona: prompt de sistema com guardrails, por curso/família de
       curso (não precisa de doctype -- mesmo padrão de
       course_translations.py: dict em código, sem Custom Field).
    3. Groq com modelo configurável. O padrão histórico era
       openai/gpt-oss-120b, mas algumas organizações bloqueiam modelos por
       política interna; por isso o runtime tenta fallbacks disponíveis antes
       de desistir.
    4. Log: Vedium AI Chat Session + Vedium AI Chat Message (doctypes
       custom, criados em install.py -- ensure_ai_tutor_doctypes()).
    5. Fallback humano: escalate_to_human() cria HD Ticket via
       vedium_core.helpdesk.create_ticket(), anexando o histórico da
       conversa.
"""
import json
import time

import frappe
from frappe import _

CHAT_SESSION = "Vedium AI Chat Session"
CHAT_MESSAGE = "Vedium AI Chat Message"

# openai/gpt-oss-120b esta bloqueado a nivel de organizacao nesta conta Groq
# (confirmado 2026-07-11 via inspect_ai_tutor.py: 403 PermissionDeniedError).
# Mantido como ultimo fallback -- se o admin da org liberar o modelo, volta a
# ser tentado, so que sem custar a latencia dele em toda mensagem.
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_FALLBACK_MODELS = (
    "llama-3.1-8b-instant",
    "qwen/qwen3-32b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
)
RATE_LIMIT_QUOTA = 30
RATE_LIMIT_WINDOW = 3600
MAX_HISTORY_MESSAGES = 12  # últimas N mensagens mandadas de volta pro modelo como contexto

GUARDRAILS = """INSTRUÇÕES CRÍTICAS:
- Você é o Tutor IA da Vedium, uma escola de idiomas 100% online (aulas ao vivo).
- Responda SEMPRE em português do Brasil, a não ser que o aluno escreva em outro idioma.
- Seja conciso, didático e encorajador.
- Não invente preço, professor, data de aula ou informação que não esteja no CONTEXTO fornecido.
- Se a dúvida for sobre pagamento, cancelamento, acesso à conta ou problema técnico sério,
  recomende falar com o suporte humano (o aluno tem um botão "Falar com um humano" na tela).
- Não discuta política, religião ou temas polêmicos; recuse educadamente e volte ao assunto.
- Não gere conteúdo violento, odioso ou explícito.
"""

# Persona por família de curso -- mesmo racional de course_translations.py:
# dict em código, sem Custom Field/migração.
PERSONAS = {
    "default": (
        "Você ajuda alunos da Vedium com dúvidas gerais sobre a plataforma "
        "(progresso, certificado, matrícula, prática diária) e dúvidas de "
        "idiomas em geral."
    ),
    "english": (
        "Você é tutor de inglês. Ajude com gramática, vocabulário, pronúncia "
        "(descrita em texto) e prática de conversação em inglês."
    ),
    "yoruba": (
        "Você é tutor de iorubá. Ajude com gramática, vocabulário, tons e "
        "aspectos culturais do povo iorubá."
    ),
    "ple": (
        "Você é tutor de português para estrangeiros (PLE). Responda em "
        "português simples e claro, adequado ao nível do aluno, e ajude "
        "também em inglês quando o aluno tiver dificuldade de entender."
    ),
}

_FAMILY_BY_COURSE_PREFIX = (
    ("iorub", "yoruba"),
    ("ingl", "english"),
    ("portugues-para-estrangeiros", "ple"),
)

# FAQ curado da PLATAFORMA (não do Frappe genérico) -- grounded no código
# real já verificado nesta sessão. Cada entrada: (palavras-chave, resposta).
PLATFORM_FAQ = [
    (
        ["progresso", "andamento", "meu progresso"],
        "Seu progresso fica em /meu-progresso: nível CEFR estimado, pontos, "
        "nível de gamificação (Bronze/Prata/Ouro/Diamante), badges conquistados "
        "e status de cada curso matriculado.",
    ),
    (
        ["certificado", "certificate", "diploma"],
        "O certificado é emitido automaticamente quando você completa 100% das "
        "lições do curso. Você pode verificar a autenticidade de qualquer "
        "certificado Vedium em /certificado, informando o código impresso nele.",
    ),
    (
        ["indicação", "indicar", "indique", "referral", "convidar amigo"],
        "No programa de indicação (/programa-de-indicacao), você recebe um "
        "código único. Quando um amigo se matricula usando seu código, ele "
        "ganha desconto e você recebe um cupom de recompensa por e-mail.",
    ),
    (
        ["pontos", "nível", "gamificação", "badge", "conquista"],
        "Você ganha pontos completando lições (+10), passando em quizzes "
        "(+25), na prova final de nível (+100) e ao concluir um curso "
        "inteiro com certificado (+200). Os pontos definem seu nível "
        "(Bronze, Prata, Ouro, Diamante), visível em /meu-progresso.",
    ),
    (
        ["prática diária", "praticar", "exercício diário"],
        "A página /pratica-diaria tem exercícios rápidos de revisão para "
        "manter a consistência entre as aulas ao vivo.",
    ),
    (
        ["matrícula", "matricular", "comprar curso", "pagamento", "assinar"],
        "A matrícula é feita dentro da plataforma (app.vediums.com), com "
        "login e pagamento seguro via Stripe. A página /matricula te ajuda a "
        "escolher curso, plano e objetivo antes de seguir para o checkout.",
    ),
    (
        ["cancelar", "reembolso", "arrependimento"],
        "Você tem 7 dias corridos após a contratação para cancelar com "
        "reembolso integral (direito de arrependimento, CDC). Veja a "
        "Política de Cancelamento e Reembolso em /cancelamento-reembolso.",
    ),
    (
        ["prova", "quiz", "avaliação final", "tentativa"],
        "As provas de nível têm 40 questões sorteadas de um banco maior, "
        "embaralhadas a cada tentativa. Você precisa de 70% de acerto para "
        "passar e tem até 3 tentativas.",
    ),
    (
        ["próximo nível", "avançado", "intermediário", "desbloquear"],
        "Nos cursos de Português para Estrangeiros, passar na prova de um "
        "nível libera o conteúdo do próximo nível SE você já tiver "
        "comprado — senão, você fica apto e só falta concluir a compra.",
    ),
]


def _course_family(course_name):
    if not course_name:
        return "default"
    lower = course_name.lower()
    for prefix, family in _FAMILY_BY_COURSE_PREFIX:
        if lower.startswith(prefix):
            return family
    return "default"


def _search_lesson_context(course_name, query, limit=3):
    """RAG por palavra-chave sobre as lições do curso do aluno. Sem vector
    DB: conta quantas palavras da pergunta aparecem em cada lição e retorna
    as mais relevantes. Suficiente para um curso com dezenas de lições;
    não escala pra milhares, mas não é o caso aqui."""
    if not course_name:
        return []

    words = {w for w in query.lower().split() if len(w) > 3}
    if not words:
        return []

    lessons = frappe.get_all(
        "Course Lesson",
        filters={"course": course_name},
        fields=["title", "content", "body"],
    )

    scored = []
    for lesson in lessons:
        text = _lesson_plain_text(lesson)
        text_lower = text.lower()
        score = sum(1 for w in words if w in text_lower)
        if score:
            scored.append((score, lesson.title, text[:600]))

    scored.sort(key=lambda row: row[0], reverse=True)
    return [{"title": title, "excerpt": excerpt} for _, title, excerpt in scored[:limit]]


def _lesson_plain_text(lesson):
    if lesson.get("body"):
        return lesson["body"]
    raw = lesson.get("content")
    if not raw:
        return ""
    try:
        blocks = json.loads(raw).get("blocks", [])
        return "\n".join(
            b.get("data", {}).get("text", "") for b in blocks if b.get("data")
        )
    except (ValueError, AttributeError):
        return str(raw)


def _search_platform_faq(query, limit=2):
    words = {w for w in query.lower().split() if len(w) > 2}
    scored = []
    for keywords, answer in PLATFORM_FAQ:
        score = sum(1 for k in keywords if k in query.lower())
        if score:
            scored.append((score, answer))
    scored.sort(key=lambda row: row[0], reverse=True)
    return [answer for _, answer in scored[:limit]]


def _check_rate_limit(user):
    if user == "Administrator":
        return
    bucket = int(time.time() // RATE_LIMIT_WINDOW)
    cache_key = f"vedium_ai_tutor_rl:{user}:{bucket}"
    current = int(frappe.cache().get_value(cache_key) or 0)
    if current >= RATE_LIMIT_QUOTA:
        frappe.throw(
            _("Você atingiu o limite de {0} mensagens por hora. Tente novamente mais tarde.").format(
                RATE_LIMIT_QUOTA
            ),
            frappe.TooManyRequestsError if hasattr(frappe, "TooManyRequestsError") else frappe.ValidationError,
        )
    frappe.cache().set_value(cache_key, current + 1, expires_in_sec=RATE_LIMIT_WINDOW * 2)


def _get_groq_client():
    from groq import Groq

    api_key = frappe.conf.get("groq_api_key") or frappe.db.get_single_value(
        "System Settings", "custom_groq_api_key"
    )
    if not api_key:
        frappe.throw(_("Tutor IA não está configurado ainda (chave da Groq ausente)."))
    return Groq(api_key=api_key)


def _configured_groq_model():
    return (
        frappe.conf.get("vedium_ai_tutor_model")
        or frappe.db.get_single_value("System Settings", "custom_vedium_ai_tutor_model")
        or GROQ_MODEL
    )


def _groq_model_candidates():
    seen = set()
    for model in (_configured_groq_model(), *GROQ_FALLBACK_MODELS):
        if model and model not in seen:
            seen.add(model)
            yield model


def _create_groq_completion(client, messages):
    last_error = None
    for model in _groq_model_candidates():
        try:
            completion = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.6,
                max_tokens=500,
            )
            return completion, model
        except Exception as exc:
            last_error = exc
            message = str(exc).lower()
            # Só tenta fallback quando o problema é claramente o modelo.
            # Erros de rede, chave inválida, rate limit etc. devem falhar
            # rápido para não mascarar configuração real.
            if not any(
                marker in message
                for marker in (
                    "model",
                    "permission",
                    "blocked",
                    "deprecat",
                    "not found",
                    "does not exist",
                )
            ):
                raise
            frappe.logger("vedium.ai_tutor").warning(
                f"Groq model {model!r} failed, trying fallback: {exc}"
            )
    raise last_error


def _get_or_create_session(session_name, user, course_name):
    if session_name and frappe.db.exists(CHAT_SESSION, session_name):
        session = frappe.get_doc(CHAT_SESSION, session_name)
        if session.member != user:
            frappe.throw(_("Sessão de chat não encontrada."), frappe.PermissionError)
        return session

    ensure_ai_tutor_doctypes()
    session = frappe.get_doc(
        {
            "doctype": CHAT_SESSION,
            "member": user,
            "course": course_name or None,
            "started_on": frappe.utils.now_datetime(),
            "status": "Aberta",
        }
    )
    session.insert(ignore_permissions=True)
    return session


def _append_message(session, role, content):
    frappe.get_doc(
        {
            "doctype": CHAT_MESSAGE,
            "parent": session.name,
            "parenttype": CHAT_SESSION,
            "parentfield": "messages",
            "role": role,
            "content": content,
            "sent_on": frappe.utils.now_datetime(),
        }
    ).insert(ignore_permissions=True)


def _recent_history(session_name):
    if not frappe.db.exists("DocType", CHAT_MESSAGE):
        return []
    rows = frappe.get_all(
        CHAT_MESSAGE,
        filters={"parent": session_name},
        fields=["role", "content"],
        order_by="creation asc",
        limit_page_length=MAX_HISTORY_MESSAGES,
    )
    return [{"role": r.role, "content": r.content} for r in rows]


@frappe.whitelist()
def chat(message, course=None, session_name=None):
    """Endpoint principal do widget de chat (área autenticada do aluno)."""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para conversar com o Tutor IA."), frappe.PermissionError)

    message = (message or "").strip()
    if not message:
        frappe.throw(_("Mensagem vazia."))
    if len(message) > 2000:
        frappe.throw(_("Mensagem muito longa (máximo 2000 caracteres)."))

    _check_rate_limit(user)

    session = _get_or_create_session(session_name, user, course)
    course_name = session.course

    family = _course_family(course_name)
    persona_prompt = PERSONAS.get(family, PERSONAS["default"])

    lesson_hits = _search_lesson_context(course_name, message)
    faq_hits = _search_platform_faq(message)

    context_parts = []
    if lesson_hits:
        context_parts.append("Trechos relevantes do curso do aluno:")
        for hit in lesson_hits:
            context_parts.append(f"- ({hit['title']}) {hit['excerpt']}")
    if faq_hits:
        context_parts.append("Informações da plataforma Vedium:")
        context_parts.extend(f"- {a}" for a in faq_hits)
    context_text = "\n".join(context_parts)

    system_prompt = f"{GUARDRAILS}\n\n{persona_prompt}"
    if context_text:
        system_prompt += f"\n\nCONTEXTO (use só se for relevante pra pergunta):\n{context_text}"

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(_recent_history(session.name))
    messages.append({"role": "user", "content": message})

    _append_message(session, "user", message)

    client = _get_groq_client()
    start = time.time()
    try:
        completion, model_used = _create_groq_completion(client, messages)
        reply = completion.choices[0].message.content
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.ai_tutor.chat")
        frappe.throw(_("O Tutor IA está indisponível agora. Tente novamente em instantes ou fale com o suporte."))

    _append_message(session, "assistant", reply)
    frappe.db.commit()

    duration_ms = int((time.time() - start) * 1000)
    frappe.logger("vedium.ai_tutor").info(
        f"user={user} session={session.name} model={model_used} duration_ms={duration_ms} "
        f"lesson_hits={len(lesson_hits)} faq_hits={len(faq_hits)}"
    )

    return {"session_name": session.name, "reply": reply}


@frappe.whitelist()
def escalate_to_human(session_name, reason=None):
    """Cria um chamado no Helpdesk com o histórico da conversa, quando o
    Tutor IA não resolve a dúvida do aluno."""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Faça login para falar com o suporte."), frappe.PermissionError)

    if not frappe.db.exists(CHAT_SESSION, session_name):
        frappe.throw(_("Sessão de chat não encontrada."))
    session = frappe.get_doc(CHAT_SESSION, session_name)
    if session.member != user:
        frappe.throw(_("Sessão de chat não encontrada."), frappe.PermissionError)

    history = _recent_history(session_name)
    transcript = "\n\n".join(
        f"{'Aluno' if h['role'] == 'user' else 'Tutor IA'}: {h['content']}" for h in history
    )

    from vedium_core.helpdesk import create_ticket

    ticket = create_ticket(
        subject="Escalado do Tutor IA — " + (reason or "dúvida não resolvida pela IA"),
        description=transcript or "(sem histórico)",
        category="Tutor IA",
        raised_by=user,
    )

    session.status = "Escalada"
    session.save(ignore_permissions=True)
    frappe.db.commit()

    return {"ticket": ticket.name}


def ensure_ai_tutor_doctypes():
    """Cria os doctypes custom do Tutor IA (idempotente). Mesmo padrão de
    vedium_core.careers.ensure_candidatura_doctype."""
    if not frappe.db.exists("DocType", CHAT_MESSAGE):
        message_dt = frappe.new_doc("DocType")
        message_dt.name = CHAT_MESSAGE
        message_dt.module = "Vedium Core"
        message_dt.custom = 1
        message_dt.istable = 1
        for fn, label, ft, extra in [
            ("role", "Autor", "Select", {"options": "user\nassistant", "reqd": 1}),
            ("content", "Conteúdo", "Long Text", {"reqd": 1}),
            ("sent_on", "Enviado em", "Datetime", {}),
        ]:
            row = {"fieldname": fn, "label": label, "fieldtype": ft}
            row.update(extra)
            message_dt.append("fields", row)
        message_dt.insert(ignore_permissions=True)

    if not frappe.db.exists("DocType", CHAT_SESSION):
        session_dt = frappe.new_doc("DocType")
        session_dt.name = CHAT_SESSION
        session_dt.module = "Vedium Core"
        session_dt.custom = 1
        session_dt.autoname = "hash"
        session_dt.sort_field = "modified"
        session_dt.sort_order = "DESC"
        for fn, label, ft, extra in [
            ("member", "Aluno", "Link", {"options": "User", "reqd": 1, "in_list_view": 1}),
            ("course", "Curso", "Link", {"options": "LMS Course"}),
            ("started_on", "Iniciada em", "Datetime", {}),
            ("status", "Status", "Select", {"options": "Aberta\nEscalada\nEncerrada", "default": "Aberta"}),
            ("messages", "Mensagens", "Table", {"options": CHAT_MESSAGE}),
        ]:
            row = {"fieldname": fn, "label": label, "fieldtype": ft}
            row.update(extra)
            session_dt.append("fields", row)
        for role in ["System Manager"]:
            session_dt.append("permissions", {
                "role": role, "read": 1, "write": 1, "create": 1, "delete": 1,
                "email": 1, "export": 1, "report": 1, "share": 1, "print": 1,
            })
        session_dt.insert(ignore_permissions=True)

    frappe.db.commit()
