# Roadmap

> Substitui o antigo `task.md`. Próximas entregas priorizadas.
> Itens detalhados viram GitHub Issues quando entram em sprint.

## P1 — Qualidade estrutural (próximas 2-3 semanas)

- [ ] Criar DocTypes faltantes (ou remover endpoints):
  - `LMS Forum Topic`, `LMS Community Link`, `LMS Course Language`,
    `LMS Accessibility Feature`, `LMS Session`, `LMS Quiz Question`.
- [ ] Suite de testes integração (`bench --site test_site run-tests`)
  - 60% cov em `api.py` (pagamentos, cupons, webhooks).
- [ ] Padronizar tratamento de erro:
  - `vedium_core/exceptions.py` com hierarquia (`VediumError`,
    `PaymentError`, `EnrollmentError`).
  - Convenção `frappe.log_error(msg, title=f"Vedium.{module}.{func}")`.
- [ ] Endpoint sitemap.xml com rota dedicada (não whitelisted JSON).

## P2 — Diferenciação e crescimento (1-2 meses)

- [ ] Programa de indicação (`referred_by` em LMS Enrollment + cupom auto).
- [ ] Certificado PDF com QR code de verificação.
- [ ] Trial 7 dias para curso pago (`status="Trial"` + scheduler de expiração).
- [ ] Cupons regionais auto-aplicados via geolocalização.
- [ ] B2B: pacote corporativo (10+ licenças) com dashboard por colaborador.
- [ ] Funil completo no Grafana (homepage → catálogo → curso → pagamento → 1ª aula).

## P3 — Compliance e robustez (3+ meses)

- [ ] Módulo `vedium_core/lgpd.py`:
  - `request_data_export(user)`, `request_data_deletion(user)`,
    `record_consent(user, purpose, scope)`.
- [ ] Página `/privacidade/meus-dados`.
- [ ] Restore drill mensal automatizado.
- [ ] DPA com Stripe documentado.
- [ ] Pentest agendado (OWASP ZAP + revisão manual).

## Desativado / removido

- ~~Prometheus~~ (ADR-005, 2026-06-11). Voltar quando MAU > 5k ou
  quando latency p95 virar problema declarado.
- ~~Análise fonética IA local~~ — requer GPU; reavaliar via API (Replicate).
