# 22 — Contact Conversion Contract

Como `/contato` converte, com o que, e por quê. Referência para não
duplicar disparo de analytics nem inventar intent inexistente no
backend.

## 1. Pontos de conversão da página

| Ponto | Mecanismo | Destino |
|---|---|---|
| CTA principal do topo ("Falar pelo WhatsApp") | Link `wa.me`, mensagem neutra | WhatsApp oficial |
| 5 itens de "Escolha o Assunto" | Cada um seu próprio link `wa.me`, mensagem pré-preenchida específica ao assunto | WhatsApp oficial |
| "Contato Direto" | Link `wa.me` (mensagem neutra) + `mailto:` | WhatsApp oficial / contato@vediums.com |
| Formulário | `ContactForm` (Client Component) → `POST /api/contact` (Route Handler) → Frappe | Ticket humano + CRM Lead + e-mail |
| Bloco "Para Empresas" | `Button` interno (Next `Link`, sem tracking de WhatsApp) | `/empresas` |

Nenhum checkout, nenhum pagamento, nenhuma integração Stripe nesta
página (missão seção 25).

## 2. Contrato de analytics (WhatsApp)

Todo clique num link de WhatsApp desta página passa por
`TrackedWhatsappLink` (`src/components/ui/TrackedWhatsappLink.tsx`), que
dispara:

```js
dataLayer.push({ event: "public_cta_click", cta: <texto do CTA>, location: <pathname> })
```

**Mesmo nome de evento e mesmos campos** já usados em produção (ver
`docs/frontend-v2/21-contact-seo-parity.md`, seção 7, e o código-fonte
lido em `templates/includes/public_intent_page.html`). Nenhum nome novo
inventado.

Um clique = uma emissão: `TrackedWhatsappLink` é um `<a>` simples com um
único `onClick`, sem listener delegado adicional em nenhum ancestral
desta página que pudesse duplicar o disparo. Verificado por leitura de
código — a única fonte desse evento no Next hoje é este componente,
usado 1x por link (nunca dois componentes tracking o mesmo `<a>`).

**Escopo desta fase**: só os WhatsApp CTAs de `/contato` foram
instrumentados. As outras 9 páginas (Home, 5 idiomas, B2B, Como
Funciona, Sobre) ainda não têm esse evento portado para o Next — ele só
existia nas páginas legadas Jinja antes desta fase. Portar
retroativamente para as outras páginas é uma decisão de escopo maior,
fora desta missão (que pediu especificamente o contrato de WhatsApp
*desta* página).

## 3. Contrato de intent (formulário)

`ContactForm` mapeia cada opção do campo "Assunto" para um par
`intent`/`goal` usando só valores reais de `ALLOWED_INTENTS`
(`vedium_core/public_funnel.py`):

| Opção no formulário | `intent` enviado | `goal` enviado |
|---|---|---|
| Cursos e níveis | `lead` | "Cursos e níveis" |
| Aulas particulares | `lead` | "Aulas particulares" |
| Português para Estrangeiros | `lead` | "Português para Estrangeiros" |
| Empresas | `b2b` | "Empresas" |
| Outro assunto | `lead` | "Outro assunto" |

Não existe intent "contact" ou "particular" no backend — inventar um
faria o `frappe.throw(_("Tipo de intenção inválido."))` disparar
(`ALLOWED_INTENTS` é uma allowlist fechada). "Empresas" usa `b2b`
porque é o único assunto com resolução própria de CRM Lead
Source/Status (`resolve_lead_source("b2b")`).

## 4. Por que nenhum evento de conversão do formulário foi disparado nesta fase

O formulário só reporta sucesso quando `/api/contact` responde
`{ok:true}`, e `/api/contact` só responde isso depois de uma resposta
`ok` real do endpoint de produção (`submit_public_intent`). Como esta
sessão não faz deploy e os testes automatizados desta fase bloqueiam
deliberadamente qualquer chamada de rede para `app.vediums.com` (ver
`23-contact-form-integration-audit.md`, seção final), nenhum evento de
sucesso de formulário foi de fato emitido/testado end-to-end contra
produção. O evento equivalente ao `public_intent_submit` já usado no
formulário legado (mesmo nome, se portado) fica documentado aqui como
próximo passo, não implementado nesta fase por não haver como testá-lo
com segurança sem deploy.

## 5. O que NÃO fizemos (e por quê)

- **Não duplicamos `public_cta_click`**: não existe nenhum listener
  delegado global nem em `Header`/`Footer` capturando cliques em `a[href
  *="wa.me"]` — só o `TrackedWhatsappLink` desta página. Confirmado por
  leitura de código, não assumido.
- **Não criamos checkbox de marketing obrigatório**: consentimento
  comercial não é condição para enviar a mensagem de contato (missão
  seção 14).
- **Não expusemos o host `app.vediums.com` no bundle do cliente**: só o
  Route Handler (`src/app/api/contact/route.ts`, roda no servidor)
  conhece o endpoint real.
- **Não usamos CAPTCHA/Turnstile**: o rate-limit real já existente no
  backend (`rate_limit_by_ip`, 8/hora/IP) mais o honeypot client-side já
  cobrem os casos comuns de spam automatizado (missão seção 15).
