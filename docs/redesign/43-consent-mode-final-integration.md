# 43 — Google Consent Mode v2: integração final (Fase C.1.2, Parte B)

> Continuação de `39-consent-mode-rollout.md` (Fase C.1.1). Não recria o consentimento do zero — reaproveita `consent-mode-v2.js` e o evento `vedium:consent` já existente. **Nenhum arquivo compartilhado de produção foi modificado nesta fase** — mapeamento e diffs prontos, aplicação continua pendente de decisão humana (mesma razão da Fase C.1.1: expandir escopo pra fora de `v2/`).
>
> **Atualização Fase C.1.3**: o diff mapeado aqui foi **aplicado e verificado empiricamente** — autorização explícita da missão C.1.3 para editar arquivos compartilhados. Ver resultado real (não mais plano) em `45-consent-remediation-result.md`. Este documento (43) permanece como registro histórico do mapeamento/investigação que tornou a aplicação possível.

## 1. Situação atual — confirmada, não recriada

`consent-mode-v2.js` (5 testes na Fase C.1.1, 6 agora) já implementa o sinal de `default` denied + `update` no aceite. Meta Pixel já checa consentimento (regression test já existe). O gap confirmado continua sendo só o carregamento do GTM.

## 2. Mapeamento REAL de entrypoints — mais amplo do que o documentado na Fase C.1.1

A Fase C.1.1 (`39-`) descreveu o gap como "`www/index.html` + 5 variantes de idioma". **Investigação mais profunda nesta fase encontrou uma superfície maior**:

| Grupo de entrypoint | Arquivos | Como carrega GTM |
|---|---|---|
| Home por idioma | `www/index.html`, `www/en/index.html`, `www/es/index.html`, `www/de/index.html`, `www/fr/index.html`, `www/ru/index.html` | Script inline, primeira coisa do `<head>` (linha 13-21 em todos os 6, estrutura idêntica confirmada) |
| Página de curso | `www/curso.html` | Script inline, primeira coisa do `<head>` (linha 17) — template único usado por TODAS as páginas de curso (5 idiomas × níveis) |
| **Todas as outras ~120 páginas** (`empresas.html`, `contato.html`, `faq.html`, `catalogo.html`, `sobre.html`, e as mesmas em `en/es/de/fr/ru/`, mais blog/marketing) | `templates/includes/site_footer.html` | Script completo (não só o `<noscript>`) embutido no rodapé, incluído por **128 arquivos diferentes** (contagem real via grep nesta fase) |

**Achado novo, não documentado antes**: `site_footer.html` carrega uma cópia PRÓPRIA e COMPLETA do snippet do GTM (script + noscript), não só o `<noscript>` de fallback. Isso confirma e generaliza o "bug de duplicação" já conhecido (Home real tem 4 ocorrências de `GTM-P6Q2FXLK` = script+noscript do head duplicado com script+noscript do footer) — mas o achado novo é que a MAIORIA das páginas do site (as ~120 que não têm snippet no head) dependem **inteiramente** dessa cópia do footer pra carregar o GTM.

## 3. Ordem real medida (não assumida) — GTM sempre antes do consentimento

Medido empiricamente nesta fase, direto na resposta HTTP renderizada (não no código-fonte, pra capturar a ordem real pós-render):

| Página | Posição do GTM (offset no HTML) | Posição do cookie-consent.js | GTM primeiro? |
|---|---|---|---|
| `/` (tem snippet no head) | caractere 798 de 105.086 | caractere 105.018 | Sim — por uma margem enorme (GTM roda a ~0,7% do documento, cookie-consent a ~99,9%) |
| `/contato` (só footer, sem head) | caractere 30.396 de 32.175 | caractere 32.109 | Sim — GTM ainda roda ~270 caracteres antes, mesmo estando no rodapé |

**Conclusão**: em 100% das páginas testadas, `cookie-consent.js` é literalmente o ÚLTIMO script do documento (carregado via `web_include_js`, que o Frappe injeta perto do fim do `<body>`, depois de `frappe-web.bundle.js`) — o GTM sempre roda antes, seja no head (Home/curso) ou no meio do body (footer). Isso confirma que o `default` denied **não pode** ser adicionado a `cookie-consent.js` nem a `consent-mode-v2.js` se ele continuar carregado via `web_include_js` — precisa ser um snippet inline, posicionado imediatamente antes de CADA um dos 8 pontos onde o GTM é inicializado (os 7 arquivos de head + `site_footer.html`).

## 4. Diff exato de integração (pronto, não aplicado)

**Ponto A — 7 arquivos, inline, antes do bloco `<!-- Google Tag Manager -->`** (`www/index.html`, `www/{en,es,de,fr,ru}/index.html`, `www/curso.html`):

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    'analytics_storage': 'denied', 'ad_storage': 'denied',
    'ad_user_data': 'denied', 'ad_personalization': 'denied',
    'wait_for_update': 500
  });
</script>
```

**Ponto A' — `templates/includes/site_footer.html`, mesmo snippet, imediatamente antes do bloco GTM do rodapé** — cobre as ~120 páginas restantes com uma única edição.

**Ponto B — inalterado desde a Fase C.1.1**: `consent-mode-v2.js` continua sendo carregado (via `web_include_js`, adicionando a entrada em `hooks.py`) — o timing dele não é crítico porque só cuida do `update` (aceite/recusa), que só precisa rodar depois de o usuário interagir com a barra.

**Total: 8 arquivos precisam do Ponto A/A', não 6 como a Fase C.1.1 registrou** — correção de escopo relevante para quem for aplicar o diff.

## 5. Basic vs. Advanced Consent Mode — identificação explícita

`consent-mode-v2.js` **não decide sozinho** entre Basic e Advanced — essa escolha depende da configuração de CADA tag dentro do container GTM (opção "Additional Consent Checks" de cada tag, ex. a tag de configuração do GA4), que é um dado que vive no painel do Google Tag Manager, fora deste repositório, e que esta fase não inspeciona nem publica (instrução explícita: "não publicar GTM").

O que o código real faz, com certeza:
- Envia `default` com os 4 sinais `denied` antes do GTM carregar (nos 8 pontos do diff acima).
- Envia `update` com os 4 sinais `granted` quando o usuário aceita.

**Comportamento padrão do Google, sem configuração adicional no GTM**: tags gerenciadas via GTM (como a tag de configuração do GA4) **bloqueiam o disparo completamente** quando o consentimento exigido está `denied`, a menos que alguém tenha ativado explicitamente "Advanced Consent Mode" na própria configuração da tag (opção que precisa ser ligada deliberadamente, não vem ligada por padrão). Ou seja: **o comportamento resultante, sem nenhuma configuração adicional no GTM, já tende a ser equivalente a BASIC** — mas isso não pode ser confirmado com certeza sem acessar o painel do GTM, o que está fora do escopo desta fase.

**Não afirmamos que isso, por si só, torna o site "conforme a LGPD"** — Consent Mode é um mecanismo técnico de sinalização entre o site e as tags do Google; conformidade depende também do texto legal exibido, da existência de opção real de recusa (seção 6 abaixo), e de políticas de retenção/uso de dado — pontos que este código não resolve sozinho.

**Recomendação de privacidade** (seção 11 da missão): se a configuração das tags no GTM permitir escolher, preferir Basic — nenhum dado é enviado ao Google antes da escolha explícita do usuário. Essa é uma decisão a confirmar (não assumir) com quem administra o container GTM.

## 6. Banner / escolha real — gap confirmado, não simulado

`cookie-consent.js` hoje só tem o botão **"Aceitar"** (+ link "Saiba mais" para `/privacidade`). **Não existe "Recusar" nem "Gerenciar preferências"** — confirmado lendo o arquivo linha a linha nesta fase, não assumido.

Efeito prático hoje: não clicar em "Aceitar" já resulta em consentimento negado por padrão (a barra continua visível, `localStorage` nunca é setado, `consent-mode-v2.js` nunca chama `grantConsentFromAcceptance()`) — isso cobre o requisito técnico de "default deny", mas **não** cobre o requisito de a pessoa poder recusar **ativamente e de forma tão fácil quanto aceitar** (prática recomendada de LGPD/GDPR — "recusar" não deveria exigir mais cliques ou ser mais difícil de achar do que "aceitar").

**Preparado nesta fase, pronto pra aplicar**: `consent-mode-v2.js` ganhou `denyConsentExplicitly()` (grava `localStorage.vedium_cookie_consent = "rejected"`, envia `consent update` com os 4 sinais `denied`) e escuta um novo evento `vedium:consent-rejected`, testado (`test_pure_consent_mode_v2.py`, 6 testes agora). Falta só o botão em si:

```html
<!-- diff sugerido para cookie-consent.js, dentro de show(), ao lado do botão existente -->
'<button id="vd-cookie-reject" type="button">' + copy.reject + '</button>' +
```
```js
var rejectBtn = document.getElementById("vd-cookie-reject");
if (rejectBtn) rejectBtn.addEventListener("click", function () {
  try { localStorage.setItem("vedium_cookie_consent", "rejected"); } catch (e) {}
  try { window.dispatchEvent(new Event("vedium:consent-rejected")); } catch (e) {}
  if (bar.parentNode) bar.parentNode.removeChild(bar);
});
```
(+ chave `reject` no dicionário `messages` de cada idioma — não incluída aqui pra não inventar tradução sem revisão humana do texto exato.)

**Enquanto esse botão não existir, `LGPD` permanece FAIL** — não por causa só da ordem do GTM (resolvida no diff da seção 4), mas porque não recusar explicitamente = não é a mesma coisa que ter a opção de recusar.

## 7. Sinais de consentimento validados

`analytics_storage`, `ad_storage`, `ad_user_data`, `ad_personalization` — os 4 usados em `default` e em `update`/`denyConsentExplicitly`, confirmados por teste (`test_sets_all_four_consent_mode_v2_signals_denied_by_default`). Nenhum outro sinal (`personalization_storage`, `functionality_storage`, `security_storage`) é usado pelo código atual — esses 3 adicionais do Consent Mode v2 completo não têm tag correspondente conhecida no GTM da Vedium (não inspecionado, fora do escopo).

## 8. Pathfinder, WhatsApp, locale, formulários — não dependem de tracking

Confirmado por leitura de código (não é novo nesta fase, mas revalidado): nenhum dos fluxos de navegação (`initPathfinderRouting`, `initLocaleMenu`, links de WhatsApp, formulários de contato/matrícula) depende de `dataLayer`/GTM pra FUNCIONAR — os `pushDataLayer()` chamados são "fire and forget" (não bloqueiam navegação nem esperam resposta). Consentimento negado não quebra nenhuma dessas funcionalidades.

## 9. Plano de teste dos 6 cenários (A–F) — não executável ainda

Os cenários pedidos pela missão (primeira visita, aceitar, recusar, recarregar, mudar preferência, trocar locale) só podem ser testados de ponta a ponta numa página que já tenha o diff da seção 4 aplicado — o que esta fase explicitamente não faz. Documentado como plano de teste pronto pra quando a integração for aplicada:

| Cenário | O que verificar |
|---|---|
| A. Primeira visita, sem escolha | `dataLayer` tem `consent default` com os 4 `denied` antes de qualquer evento de tag; nenhum cookie de terceiro (`_ga`, `_gid`, `fr`) é setado; barra de cookies visível |
| B. Aceitar | `dataLayer` recebe `consent update` com os 4 `granted`; `localStorage.vedium_cookie_consent = "1"`; Meta Pixel carrega (já testado isoladamente) |
| C. Recusar (após aplicar o botão da seção 6) | `dataLayer` recebe `consent update` com os 4 `denied`; `localStorage.vedium_cookie_consent = "rejected"`; nenhum cookie de terceiro setado; barra fecha |
| D. Recarregar a página | Estado do `localStorage` é lido de novo; `alreadyAccepted()`/estado "rejected" preservado sem novo prompt |
| E. Trocar de decisão (aceitar → recusar ou vice-versa) | Requer UI de "gerenciar preferências" — **não existe hoje**, gap adicional ao da seção 6, registrado aqui pra não ser esquecido quando o botão de recusar for implementado |
| F. Trocar locale | Consentimento é por `localStorage` (não por cookie de sessão nem por locale) — decisão já tomada persiste ao trocar de `/en`, `/es` etc.; confirmar que nenhum locale reseta `vedium_cookie_consent` |

## 10. Checklist para validação futura com Google Tag Assistant

Não executável neste ambiente (Tag Assistant precisa de um domínio real acessível publicamente ou modo preview conectado à conta GTM real — nenhum dos dois disponível neste ambiente local). Passos exatos para quando o diff for aplicado em produção/staging:

1. Abrir [Tag Assistant](https://tagassistant.google.com), conectar ao domínio.
2. Aba **Consent** → confirmar que o estado inicial mostra os 4 sinais como `Denied`.
3. Clicar em "Aceitar" no site → voltar ao Tag Assistant → confirmar transição pra `Granted`.
4. Verificar, na aba **Tags**, quais tags dispararam ANTES e DEPOIS do consentimento — tags que dispararam antes com sinal `denied` revelam se o container está em modo Advanced (cookieless ping) ou se há uma tag mal configurada sem consent check.
5. Repetir com "Recusar" (após o botão existir) — nenhuma tag de analytics/ads deveria aparecer como disparada.

## 11. Gate

`CONSENT` = **FAIL**, com progresso real desde a Fase C.1.1: passou de "consentimento carrega tarde demais" (1 causa, escopo mal mapeado) para "2 causas específicas, escopo completo mapeado (8 arquivos, não 6), ambas com solução pronta": (1) diff de `default` antes do GTM em 8 pontos, (2) botão de recusa explícita (código-cliente já pronto e testado, falta o HTML/CSS do botão + tradução revisada por humano).
