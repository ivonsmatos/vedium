# 39 — Google Consent Mode v2: rollout (Fase C.1.1, Parte C)

> Código real, testado isoladamente. **Ainda NÃO cableado em nenhuma página de produção** — decisão desta fase, não uma limitação técnica (ver seção 6). Nenhuma tag do GTM externo foi publicada.
>
> **Atualização Fase C.1.2**: mapeamento de entrypoints ampliado e corrigido — não são só `www/index.html` + 5 variantes (6 arquivos), são **8 pontos** (os 6 + `www/curso.html` + `templates/includes/site_footer.html`, este último incluído por ~120 páginas). Ordem GTM-antes-do-consentimento medida empiricamente (não só deduzida do código). Identificação explícita Basic vs. Advanced Consent Mode. Confirmado que não existe "Recusar"/"Gerenciar preferências" no banner atual (gap real, LGPD continua FAIL por essa razão também) — metade cliente da recusa já implementada e testada. Ver `43-consent-mode-final-integration.md` para tudo isso.
>
> **Atualização Fase C.1.3**: correção aplicada e verificada de verdade — ver `45-consent-remediation-result.md`. O código deste arquivo (39) descreve a PRIMEIRA versão de `consent-mode-v2.js`; a versão atual em produção tem também preferências granulares (`applyGranularPreferences`) e guard de duplicação (`window.__vediumConsentDefaultSet`), adicionados na Fase C.1.3.

## 1. Auditoria real do que carrega hoje, e quando

| Script | Onde | Carrega antes do consentimento? | Achado |
|---|---|---|---|
| GTM (`GTM-P6Q2FXLK`) | `<head>` inline, primeira coisa da página (`www/index.html` linha 13-22, replicado nas 5 variantes de idioma) | **Sim, incondicional** | Confirmado na Fase C.1; continua sendo o gap real |
| GA4 | Disparado via tag dentro do container GTM | **Sim, segue o GTM** | Consequência do item acima, não um carregamento independente |
| Meta Pixel (`meta-pixel.js`) | Via `web_include_js` (hooks.py), todas as páginas | **NÃO — já espera consentimento** | **Correção ao relatório da Fase C.1** (doc 36 generalizou demais): o arquivo já checa `localStorage.vedium_cookie_consent` e só carrega após aceite ou evento `vedium:consent`. Não é um gap. |
| `push-notifications.min.js` | `web_include_js` | Não avaliado nesta fase (fora do escopo de tags de marketing/analytics) | — |

**Correção registrada**: o gap real é só o GTM (e por consequência o GA4/outras tags configuradas dentro dele) — não "todas as tags de marketing", como uma leitura apressada do doc 36 poderia sugerir. O Meta Pixel já é um exemplo correto do padrão que falta aplicar ao GTM.

## 2. Mecanismo de consentimento existente — reaproveitado, não recriado

`cookie-consent.js` já expõe exatamente o gancho necessário: ao clicar "Aceitar", além de gravar `localStorage.vedium_cookie_consent = "1"`, ele despacha `window.dispatchEvent(new Event("vedium:consent"))` — um `CustomEvent` sitewide que já existe desde antes desta fase (usado hoje só pelo Meta Pixel). Não foi necessário modificar este arquivo.

## 3. Implementação — Google Consent Mode v2

Novo arquivo: `vedium_core/vedium_core/public/js/v2/consent-mode-v2.js`. Mapeia os 4 sinais exigidos pelo Consent Mode v2 (obrigatórios desde março/2024 para contas que atendem usuários no EEE/Reino Unido — a Vedium atende via `/en /es /fr /de /ru`, então os 4 se aplicam, não só os 2 legados):

```js
gtag('consent', 'default', {
  analytics_storage: 'denied',
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  wait_for_update: 500,
});
```

No aceite (via listener do evento `vedium:consent` já existente, ou imediatamente se `alreadyAccepted()`):

```js
gtag('consent', 'update', {
  analytics_storage: 'granted',
  ad_storage: 'granted',
  ad_user_data: 'granted',
  ad_personalization: 'granted',
});
```

Ambas as chamadas só fazem `window.dataLayer.push(arguments)` — não dependem de `gtag.js` nem do GTM já estarem carregados, exatamente como o Google documenta para o padrão funcionar mesmo se o usuário nunca aceitar nada.

Testado (`tests/test_pure_consent_mode_v2.py`, 5 testes): os 4 sinais estão presentes no default denied, o update usa os mesmos 4 sinais, o listener do evento existente está correto, o arquivo não duplica/reimplementa a barra de cookies, e o achado sobre o Meta Pixel já estar correto está fixado como teste de regressão.

## 4. Restrição técnica real — por que a integração final exige 2 pontos, não 1

O snippet de `default` **precisa rodar antes do snippet do GTM** (que hoje é a primeira tag do `<head>`, `www/index.html` linha 13). Um `<script src="..." defer>` não garante isso — só um `<script>` inline e síncrono, posicionado antes do bloco do GTM, garante a ordem. Por isso a integração final (quando decidida) precisa de:

**Ponto A — inline, ANTES do bloco `<!-- Google Tag Manager -->`, em `www/index.html` e nas 5 variantes de idioma** (diff exato a aplicar, não aplicado nesta fase):

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

**Ponto B — carregar `consent-mode-v2.js` (ou só a metade de "grant") em qualquer ponto depois, via `web_include_js`** — timing não é crítico aqui, só precisa rodar depois que `vedium:consent` possa disparar.

## 5. Não quebra a navegação com consentimento negado

Consent Mode v2 é aditivo por design: tags continuam disparando mesmo com sinais "denied" (só operam em modo degradado — sem cookies/identificadores individuais, usando modelagem agregada do Google quando disponível). dataLayer, Pathfinder (`pathfinder_language_select/goal_select/submit`), WhatsApp e UTMs continuam funcionando de forma idêntica — nenhum desses depende de `analytics_storage`/`ad_storage` para *funcionar*, só a granularidade de atribuição/remarketing é que muda.

## 6. Por que não foi cableado nesta fase

Modificar `www/index.html` e as 5 variantes de idioma é uma mudança **sitewide**, fora do perímetro estrito de arquivos `v2/` que toda esta série de fases respeitou até aqui — e afeta o comportamento de coleta de dados de marketing em produção, uma decisão com peso de negócio/jurídico que vai além de "não redesenhar visualmente". A missão autorizou explicitamente preparar isso **localmente** (Parte C, seção 17: "código versionado do site pode ser preparado localmente") sem publicar — o código está pronto, testado e com o diff exato de integração documentado acima; falta uma decisão humana explícita para expandir o escopo desta iniciativa a arquivos fora de `v2/` antes de aplicar o Ponto A/B.

## 7. Gate de rollout

`LGPD` = **READY_TO_APPLY, ainda NOT LIVE**. Não é mais "ajuste cosmético pendente" (framing da Fase C.1) — é uma implementação completa, testada, com diff de integração pronto, aguardando só a decisão de aplicar em arquivos sitewide. Classificação de prioridade mantida de C.1: recomendado aplicar antes ou imediatamente junto do cutover da Home V2, já que a troca de Home é o momento natural de revisão desse comportamento sitewide.
