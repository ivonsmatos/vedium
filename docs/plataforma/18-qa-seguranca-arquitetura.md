# 18 — QA de Segurança & Arquitetura (2026-08-09)

Auditoria do app `vedium_core` (Frappe/ERPNext v16): superfície pública
(~33 `allow_guest` + ~26 logados), injeção SQL, `ignore_permissions`, segredos,
webhooks e arquitetura. Achados corrigidos no mesmo dia.

## Segurança — achados

| Sev | Achado | Fix |
|---|---|---|
| 🔴 Crítico | `careers.approve_candidatura_as_professor`: `@frappe.whitelist()` sem checar role, concedia role de professor via `insert/save(ignore_permissions=True)` → **qualquer aluno logado podia se auto-promover** (escalonamento de privilégio). | ✅ guard de gestão (`System Manager/Administrator/HR Manager/Vedium Ops`) |
| 🟠 Médio | `funnel_metrics()` e `referral_metrics()` expunham MRR/churn/leads/indicações a **qualquer usuário logado**. | ✅ restritos à gestão |

Os três guards estão travados em `test_pure_growth.py` / `test_pure_referrals.py`.

## Segurança — o que está correto (confirmado)

- **Sem injeção SQL:** queries parametrizadas (`%s`/`%(x)s`); `.format` só em
  strings de tradução `_()`.
- **Sem segredos hardcoded:** chaves vêm de `frappe.conf`; só há validações de
  prefixo (`sk_live_`) e placeholders de teste.
- **Webhook Stripe verificado por HMAC** (`construct_verified_event`).
- `get_student_360`, `get_monitoring_dashboard` corretamente gated a staff;
  funil público com `rate_limit_by_ip`; fluxos LGPD presentes; doctypes
  sensíveis (Support Ticket/Lesson Slot) já endurecidos.

## Segurança — pendências (não-código / a testar)

- Revisar caso a caso os `allow_guest` que mutam dado (rate-limit + validação).
- Teste dedicado de ownership em `issue_certificate` / `get_payment_history`
  (aparentam escopar por `session.user`).
- Popular roles `Vedium Ops` / `Sales Manager` nos usuários certos (os guards
  dependem delas).

## Arquitetura

**Forte:** separação site(marketing)/Frappe(função); não duplica nativo
(LMS/CRM/Helpdesk/Raven reusados); eventos desacoplados (Frappe emite, Brevo
consome); idempotência durável (Integration Request / campos `custom_*_on`);
gate de acesso financeiro (`custom_vedium_status`).

**Dívidas recorrentes (footguns):**
1. **CRLF** — editor grava CRLF em arquivos LF → diffs de arquivo inteiro.
   **Ação:** adicionar `.gitattributes` forçando LF em `*.py`/`*.html`.
2. **Custom fields** não criados de forma confiável no `after_migrate` — hoje
   exige `setup_custom_fields` manual pós-deploy. **Ação:** investigar o hook.
3. `api.py` (~1200 linhas) — candidato a split por domínio.

## Recomendações de tooling

### Skills (do repo `hcb2019/claude-code-skills`) — ver `.claude/skills/README.md`
Adotar: `protetor-git`, `humanizador-pt-br`, `melhorar-arquitetura`,
`diagnostico`, `tdd`, `passar-bastao`, `modo-caverna`, `contexto-em-arquivos`.
Adaptar: `setup-pre-commit` (é JS/husky → fazer pre-commit Python), `criar-skill`.
Pular: `postgresql-boas-praticas` (aqui é **MariaDB**); os de gestão (GSD) salvo se
adotarem o fluxo.

### Subagentes criados (`.claude/agents/`)
- **security-auditor** — audita a classe de bug deste doc (teria pego o priv-esc).
- **frappe-code-reviewer** — revisa PR pros footguns (CRLF, custom-field, hífen,
  ignore_permissions, Link inválido, testes afetados).
- **deploy-verifier** — automatiza o ritual de deploy (CRLF + testes afetados +
  Action + `setup_custom_fields`).
- **billing-e2e-tester** — cadeia checkout→webhook→matrícula→CRM/Brevo (BRL+USD).
- **brevo-events-qa** — valida eventos/atributos/params e a segurança do cutover.
