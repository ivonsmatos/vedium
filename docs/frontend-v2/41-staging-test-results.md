# Staging Test Results (Fase G.3)
**Data:** 2026-08-30

## 1. Verificações Obrigatórias (Gate)

| Teste | Status | Detalhes |
|---|---|---|
| STAGING HTTPS | PENDENTE | A testar no navegador. |
| STAGING NOINDEX | PENDENTE | A testar presença de header `X-Robots-Tag`. |
| NEXT ROUTES | PENDENTE | Validar rotas `_next/` (Status 200). |
| FRAPPE ROUTES | PENDENTE | Validar `/blog` servido pelo Gunicorn (Status 200). |
| HYBRID ROUTING | PENDENTE | Proxy redirecionando corretamente. |
| CROSS-BACKEND NAVIGATION | PENDENTE | Navegação Home -> Blog sem erros/loops. |
| CONSENT CROSS-BACKEND | PENDENTE | Aceitação no GTM mantida entre roteamentos. |
| ASSETS | PENDENTE | Imagens (`/images`) carregando do estático ou Next/Frappe. |
| SEO TECHNICAL | PENDENTE | SSR tags geradas na resposta bruta. |
| PERFORMANCE | PENDENTE | Lighthouse Scores iniciais. |
| SECURITY | PENDENTE | Revisão de Headers concluída sem vazamento de Secrets. |
| ROLLBACK TEST | PENDENTE | Simulação executada. |

## 2. Notas de Qualidade de Produção

*(Preencher após a validação real com subdomínio Staging no VPS).*
