"""Programa de indicação — código pessoal, desconto automático no checkout
do indicado e recompensa (cupom) automática para quem indicou, com painel
e notificação por e-mail.

Reaproveita o mecanismo de Coupon já existente para a aplicação do desconto
(api.create_checkout / create_enrollment_if_paid) e para a recompensa do
indicador (geramos um Coupon de uso único para ele resgatar). Nenhuma
mudança é necessária nos gateways de pagamento: o código de indicação
trafega pelo mesmo parâmetro coupon_code que já existe no checkout.
"""

from urllib.parse import quote

import frappe
from frappe import _


def _generate_referral_code(user):
    """Gera um código curto e único, ex.: IND-AB12CD."""
    prefix = "IND"
    for _attempt in range(10):
        suffix = frappe.generate_hash(length=6).upper()
        code = f"{prefix}-{suffix}"
        if not frappe.db.exists("Referral", code):
            return code
    # Extremamente improvável de cair aqui (colisão 10x em hash de 6 chars).
    frappe.throw(_("Não foi possível gerar um código de indicação. Tente novamente."))


@frappe.whitelist()
def get_my_referral():
    """Retorna (e cria se necessário) o código de indicação do usuário logado."""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Por favor, faça login para acessar seu código de indicação"))

    referral = frappe.db.get_value(
        "Referral",
        {"referrer": user},
        [
            "referral_code",
            "active",
            "discount_percent",
            "reward_percent",
            "total_conversions",
        ],
        as_dict=True,
    )

    if not referral:
        code = _generate_referral_code(user)
        doc = frappe.get_doc(
            {
                "doctype": "Referral",
                "referral_code": code,
                "referrer": user,
                "active": 1,
            }
        )
        doc.insert(ignore_permissions=True)
        referral = frappe._dict({
            "referral_code": doc.referral_code,
            "active": 1,
            "discount_percent": doc.discount_percent,
            "reward_percent": doc.reward_percent,
            "total_conversions": 0,
        })

    base_url = frappe.utils.get_url()
    share_link = f"{base_url}/cursos-de-idiomas-online?ref={referral.referral_code}"
    whatsapp_text = quote(
        f"Oi! Quero te indicar a Vedium pra aprender idiomas. "
        f"Use meu código {referral.referral_code} e ganhe "
        f"{int(referral.discount_percent or 0)}% de desconto na matrícula: {share_link}"
    )
    return {
        "referral_code": referral.referral_code,
        "active": bool(referral.active),
        "discount_percent": referral.discount_percent,
        "reward_percent": referral.reward_percent,
        "total_conversions": referral.total_conversions or 0,
        "share_link": share_link,
        "whatsapp_link": f"https://wa.me/?text={whatsapp_text}",
    }


@frappe.whitelist()
def get_my_referral_conversions():
    """Lista as conversões (amigos que se matricularam) do usuário logado."""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Por favor, faça login"))

    rows = frappe.get_all(
        "Referral Conversion",
        filters={"referrer": user},
        fields=["referee", "course", "reward_coupon", "reward_percent", "converted_on"],
        order_by="converted_on desc",
        ignore_permissions=True,
    )
    for row in rows:
        full_name = frappe.db.get_value("User", row.referee, "full_name")
        row["referee_name"] = full_name or row.referee
        if row.course:
            row["course_title"] = frappe.db.get_value("LMS Course", row.course, "title") or row.course
    return rows


def validate_referral_code(code, referee=None):
    """
    Espelha a validação de cupom em api.create_checkout, mas para Referral.
    Retorna dict {referral_code, referrer, discount_percent, reward_percent} ou None.
    """
    if not code:
        return None
    referral = frappe.db.get_value(
        "Referral",
        code,
        ["referral_code", "referrer", "active", "discount_percent", "reward_percent"],
        as_dict=True,
    )
    if not referral or not referral.active:
        return None
    # Anti-abuso: ninguém usa o próprio código.
    if referee and referral.referrer == referee:
        return None
    return referral


def record_referral_conversion(referral_code, referee, course_name, enrollment_name):
    """
    Chamado por api.create_enrollment_if_paid após confirmação de pagamento.
    Cria o registro de conversão, gera o cupom de recompensa para quem indicou
    e envia e-mail de notificação. Nunca lança exceção — falha aqui não pode
    derrubar a matrícula que já foi confirmada.
    """
    try:
        referral = frappe.db.get_value(
            "Referral",
            referral_code,
            ["name", "referrer", "active", "reward_percent"],
            as_dict=True,
        )
        if not referral or not referral.active:
            return
        if referral.referrer == referee:
            return

        # Anti-abuso: cada indicado só gera 1 recompensa para o indicador,
        # mesmo que volte a comprar outro curso usando o mesmo código.
        if frappe.db.exists("Referral Conversion", {"referee": referee}):
            return

        reward_code = f"RECOMPENSA-{frappe.generate_hash(length=8).upper()}"
        reward_coupon = frappe.get_doc(
            {
                "doctype": "Coupon",
                "coupon_code": reward_code,
                "discount_percent": referral.reward_percent,
                "active": 1,
                "max_uses": 1,
                "valid_to": frappe.utils.add_days(frappe.utils.now_datetime(), 180),
            }
        )
        reward_coupon.insert(ignore_permissions=True)

        conversion = frappe.get_doc(
            {
                "doctype": "Referral Conversion",
                "referral": referral.name,
                "referrer": referral.referrer,
                "referee": referee,
                "course": course_name,
                "enrollment": enrollment_name,
                "reward_coupon": reward_code,
                "reward_percent": referral.reward_percent,
                "converted_on": frappe.utils.now_datetime(),
            }
        )
        conversion.insert(ignore_permissions=True)

        frappe.db.sql(
            """UPDATE `tabReferral`
               SET total_conversions = COALESCE(total_conversions, 0) + 1
               WHERE name = %s""",
            (referral.name,),
        )

        try:
            referrer_email = frappe.db.get_value("User", referral.referrer, "email") or referral.referrer
            referrer_first_name = frappe.db.get_value("User", referral.referrer, "first_name") or ""
            referee_name = frappe.db.get_value("User", referee, "full_name") or referee
            course_title = frappe.db.get_value("LMS Course", course_name, "title") or course_name
            frappe.sendmail(
                recipients=[referrer_email],
                subject="Sua indicação virou matrícula! 🎉 | Vedium",
                message=f"""
                    <h3>Boa{', ' + frappe.utils.escape_html(referrer_first_name) if referrer_first_name else ''}!</h3>
                    <p><strong>{frappe.utils.escape_html(referee_name)}</strong> se matriculou em
                    <strong>{frappe.utils.escape_html(course_title)}</strong> usando seu código de indicação.</p>
                    <p>Como recompensa, geramos um cupom de <strong>{int(referral.reward_percent or 0)}% de desconto</strong>
                    para sua próxima matrícula:</p>
                    <p style="font-size:20px;font-weight:700;">{reward_code}</p>
                    <p>Válido por 180 dias. Veja todas as suas indicações em
                    <a href="https://vediums.com/minhas-indicacoes">vediums.com/minhas-indicacoes</a>.</p>
                    <p>— Equipe Vedium</p>
                """,
                delayed=False,
            )
        except Exception:
            frappe.log_error(
                frappe.get_traceback(), "Vedium.referrals.notify_referrer"
            )

        # Visibilidade no CRM: o time de vendas ve "quem indicou quem" no
        # funil, sem precisar abrir o doctype Referral Conversion.
        try:
            _upsert_crm_lead_from_referral_conversion(
                referral.referrer, referee, course_name
            )
        except Exception:
            frappe.log_error(
                frappe.get_traceback(), "Vedium.referrals.crm_lead"
            )
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.referrals.record_referral_conversion"
        )


@frappe.whitelist()
def referral_metrics() -> dict:
    """Métricas do programa de indicação (P7 / alimenta o dashboard P8): quantos
    indicam, quantas indicações viraram matrícula e a receita mensal trazida
    pelos indicados. Base pra medir CAC por indicação (o custo é a recompensa em
    desconto, resgatada no próximo pagamento do indicador).

    Restrito à gestão: é métrica agregada de negócio, não pode ficar acessível a
    qualquer usuário logado. Ver QA 2026-08-09."""
    if not set(frappe.get_roles()) & {
        "System Manager", "Administrator", "Vedium Ops", "Sales Manager"
    }:
        frappe.throw(_("Acesso restrito à equipe."), frappe.PermissionError)
    total_referrers = frappe.db.count("Referral")
    active_referrers = frappe.db.count("Referral", {"active": 1})
    conversions = frappe.get_all(
        "Referral Conversion",
        fields=["enrollment", "reward_percent"],
        limit_page_length=0,
    )
    referred_mrr = 0.0
    for c in conversions:
        if c.enrollment:
            amount = frappe.db.get_value(
                "LMS Enrollment", c.enrollment, "custom_contract_monthly_amount"
            )
            referred_mrr += float(amount or 0)
    rewards = [float(c.reward_percent or 0) for c in conversions if c.reward_percent]
    return {
        "referrers_total": total_referrers,
        "referrers_active": active_referrers,
        "conversions": len(conversions),
        "referred_mrr": round(referred_mrr, 2),
        "avg_reward_percent": round(sum(rewards) / len(rewards), 1) if rewards else 0,
    }


def _upsert_crm_lead_from_referral_conversion(referrer, referee, course_name):
    """Cria/atualiza um CRM Lead para quem se matriculou via indicacao
    (referee), com nota indicando quem indicou -- assim o time de vendas
    enxerga a atividade de indicacao no CRM, mesmo o programa em si sendo
    100% automatico (recompensa ja sai sem intervencao manual)."""
    if not frappe.db.exists("DocType", "CRM Lead"):
        return

    referee_email = frappe.db.get_value("User", referee, "email") or referee
    referee_name = frappe.db.get_value("User", referee, "full_name") or referee
    referrer_name = frappe.db.get_value("User", referrer, "full_name") or referrer
    course_title = frappe.db.get_value("LMS Course", course_name, "title") or course_name

    note = (
        f"Matricula via programa de indicacao.\n"
        f"Indicado por: {referrer_name} ({referrer})\n"
        f"Curso: {course_title}"
    )

    from vedium_core.integrations import ensure_contact

    parts = (referee_name or "").strip().split(" ", 1)
    ensure_contact(
        referee_email,
        first_name=parts[0],
        last_name=parts[1] if len(parts) > 1 else None,
    )

    existing = frappe.db.get_value("CRM Lead", {"email": referee_email}, "name")
    if existing:
        frappe.get_doc("CRM Lead", existing).add_comment("Comment", note)
        return

    lead = frappe.new_doc("CRM Lead")
    lead.first_name = parts[0]
    if len(parts) > 1:
        lead.last_name = parts[1]
    lead.lead_name = (referee_name or "").strip()
    lead.email = referee_email
    # source é Link para CRM Lead Source — "Indicação" (acentuado) NÃO existe como
    # registro (o válido é "Indicacao"); gravar o acentuado faria o insert falhar
    # (mesmo bug do funil público). Resolve para uma origem válida.
    from vedium_core.crm_pipeline import resolve_lead_source, resolve_lead_status

    source = resolve_lead_source("referral")
    if source:
        lead.source = source
    status = resolve_lead_status("referral")
    if status:
        lead.status = status
    lead.insert(ignore_permissions=True)
    lead.add_comment("Comment", note)
