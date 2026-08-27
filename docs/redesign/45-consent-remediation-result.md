# 45 — Resultado da remediação do Consent Mode (Fase C.1.3, Parte A)

> Autorização explícita desta fase: correção real do Consent Mode em produção local (não deploy, não publicação de GTM externo). Tudo abaixo foi aplicado nos arquivos compartilhados e verificado empiricamente via Chrome headless (CDP) — não apenas lido/inferido do código.

## 1. Ordem corrigida — prova empírica, não dedução

`consent default` agora roda **antes** do GTM em todas as combinações testadas. Verificado lendo `window.dataLayer` real após carregamento de página (não o HTML-fonte, o estado JS de fato):

| Página | `consentDefaultCount` | Payload do `default` | Barra visível na 1ª visita |
|---|---|---|---|
| `/` (GTM duplicado: head + footer) | **1** (guard evitou o 2º) | 4 sinais `denied`, `wait_for_update:500` | sim |
| `/contato` (GTM só via footer) | **1** | idem | sim |
| `/curso-de-ingles-online` (GTM só no head) | **1** | idem | sim |

Nunca 0, nunca >1 — confirmado via `dataLayer.filter(e => e[0]==='consent' && e[1]==='default').length`.

## 2. Os 8 pontos de entrada — estado antes/depois

| Arquivo | Estado anterior | Posição GTM | Posição `consent default` | Posição banner | Estado posterior |
|---|---|---|---|---|---|
| `www/index.html` | GTM incondicional, sem sinal prévio | `<head>`, linha ~14 (após redirect script) | Include inline, linha 13, **antes** do bloco GTM | body-bottom (script hardcoded) | `default` roda antes do GTM; guard ativo |
| `www/en/index.html` | idem | idem | idem | idem | idem |
| `www/es/index.html` | idem | idem | idem | idem | idem |
| `www/de/index.html` | idem | idem | idem | idem | idem |
| `www/fr/index.html` | idem | idem | idem | idem | idem |
| `www/ru/index.html` | idem | idem | idem | idem | idem |
| `www/curso.html` | idem | `<head>`, primeira linha | Include inline, imediatamente antes | idem | idem |
| `templates/includes/site_footer.html` | GTM com guard de rede (evita 2º `<script src>`, mas sem sinal de consentimento) | corpo do rodapé (~120 páginas) | Include inline, imediatamente antes do bloco GTM do rodapé | mesmo arquivo carrega cookie-consent.js via `<script>` hardcoded em cada página que o inclui | `default` roda antes do GTM nas ~120 páginas que dependem só deste ponto |

Mecanismo: `templates/includes/consent_default.html` (novo, compartilhado, incluído nos 8 pontos acima).

## 3. Evitar duplicação — guard testado, não só assumido

`window.__vediumConsentDefaultSet` — verificado (não só lido no código) que o valor fica `true` após a 1ª execução e a 2ª chamada (quando o HTML tem 2 cópias do include, ex. `/` com GTM duplicado) é pulada. Teste novo: `test_eight_real_entrypoints_include_consent_default_exactly_once` (garante 1 include por ARQUIVO) + `test_consent_default_include_precedes_gtm_block_in_each_entrypoint` (garante ordem). A prova de "exatamente 1 execução real" (não só 1 include por arquivo) é o teste empírico da seção 1 acima — pytest não roda browser, então essa parte fica documentada aqui, não automatizada.

## 4. Banner: Aceitar / Recusar / Gerenciar preferências

Implementado em `cookie-consent.js` (regenerado `cookie-consent.min.js` via `terser`, cache-bust bumpado de `?v=mobile-pwa-fix` para `?v=c1-3-consent-banner` — **crítico**: sem isso, navegadores com o arquivo antigo em cache HTTP nunca veriam o botão novo, mesmo com o servidor atualizado). Sem dark pattern: os 3 controles vivem no mesmo `<span class="vd-cookie-actions">`, Aceitar e Recusar são `<button>` de mesmo nível hierárquico (nenhum dos dois exige mais cliques ou está mais escondido que o outro); "Gerenciar preferências" é visualmente secundário (`vd-cookie-secondary`, sem cor de destaque) mas sempre visível na barra, nunca atrás de um menu.

Textos usados — confirmados via CDP nos 6 locales reais (`document.documentElement.lang` → texto renderizado, não assumido):

| Locale | Aceitar | Recusar | Gerenciar |
|---|---|---|---|
| pt-BR | Aceitar | Recusar | Gerenciar preferências |
| en | Accept | Reject | Manage preferences |
| es | Aceptar | Rechazar | Gestionar preferencias |
| fr | Accepter | Refuser | Gérer les préférences |
| de | Akzeptieren | Ablehnen | Einstellungen verwalten |
| ru | Принять | Отклонить | Управлять настройками |

## 5. Preferências granulares — categorias reais, nenhuma inventada

Painel "Gerenciar preferências" mostra 3 linhas:
- **Essenciais** — checkbox sempre marcado, `disabled` (não é sinal do Consent Mode, é sessão/CSRF do Frappe — tecnicamente indispensável, identificado claramente como tal, sem pedir consentimento pra algo que não precisa).
- **Analytics** → mapeia pra `analytics_storage`.
- **Marketing** → mapeia pros 3 sinais restantes (`ad_storage`, `ad_user_data`, `ad_personalization`) — viajam juntos porque no código atual (Meta Pixel + tags de anúncio do GTM) não há separação mais fina implementada.

Estado salvo em `localStorage.vedium_cookie_preferences` (JSON `{analytics, marketing}`), restaurado a cada carregamento por `consent-mode-v2.js`.

## 6. Persistência — 6 cenários testados via CDP, com estado real inspecionado

| Cenário | `localStorage_consent` | `localStorage_prefs` | dataLayer final (`update` mais recente) | Barra reaparece? |
|---|---|---|---|---|
| A. Primeira visita | `null` | `null` | só `default` (tudo denied) | — (aparece) |
| B. Aceitar | `"1"` | `{analytics:true,marketing:true}` | tudo `granted` | não |
| C. Recusar | `"rejected"` | `{analytics:false,marketing:false}` | tudo `denied` | não |
| D. Gerenciar → só Analytics | `"rejected"` | `{analytics:true,marketing:false}` | `analytics_storage:granted`, resto `denied` | não |
| E. Recarregar após qualquer decisão | idêntico ao estado salvo | idêntico | reaplicado corretamente no load | não |
| F. Trocar locale (`/` → `/en/`) | preservado (mesmo `localStorage`, mesma origem) | preservado | reaplicado igual | não |

Ordem de disparo corrigida no `persistDecision()`: evento genérico (`vedium:consent`/`vedium:consent-rejected`, que o Meta Pixel também escuta) dispara **primeiro**, evento granular (`vedium:consent-preferences`) dispara **por último** — garante que a escolha granular (ex. cenário D) tenha a palavra final sobre os 4 sinais, em vez de ser sobrescrita pelo evento genérico.

## 7. Revogação/alteração futura — proposta documentada, NÃO implementada (Footer congelado)

A missão pediu um "link discreto no Footer" — mas o Footer visual está congelado nesta série de fases, e adicionar um link exige mudança visual. **Parando esta parte para aprovação humana**, conforme instrução explícita ("se adicionar o acesso exigir mudança visual: documentar proposta e PARAR").

**Proposta**: adicionar um link de texto pequeno (ex. "Preferências de cookies") na área legal do rodapé (`vd-rich-footer__legal`, ao lado do CNPJ/copyright — área que já é texto pequeno/utilitário, não uma seção de destaque visual), chamando `showPreferencesPanel()` (já existe em `cookie-consent.js`, só precisa ser exposta globalmente e reaproveitada fora do fluxo de primeira visita). Baixo risco visual (mesma área que já tem texto pequeno), mas ainda É uma mudança visual do Footer — por isso não aplicada sem aprovação.

## 8. SITE-SIDE CONSENT CONTRACT

O que o código deste repositório GARANTE, de forma testada:
- `analytics_storage`, `ad_storage`, `ad_user_data`, `ad_personalization` começam `denied` antes de qualquer tag do GTM inicializar, em toda página pública.
- Update pra `granted`/`denied` acontece só após ação explícita do usuário (Aceitar/Recusar/Salvar preferências) — nunca antes, nunca automaticamente.
- Estado persiste em `localStorage`, sobrevive a reload/navegação/troca de locale, nunca repergunta desnecessariamente.
- Recusar é tão acessível quanto Aceitar (mesmo nível hierárquico, mesmo número de cliques).
- Nenhuma funcionalidade do site depende de consentimento pra funcionar (seção 12).

## 9. GTM-SIDE CONFIGURATION REQUIRED — não verificável nem publicável nesta fase

O código não pode garantir o que acontece **dentro** do container GTM (gerenciado externamente, fora deste repositório, "não publicar GTM externo" nesta fase). Checklist do que precisa ser verificado manualmente por quem administra o GTM:

| Tag | Comportamento esperado por consent state | Ação necessária no painel do GTM |
|---|---|---|
| GA4 Configuration | Não disparar (ou disparar em modo cookieless) enquanto `analytics_storage=denied` | Verificar "Consent Settings" da tag → confirmar se "Additional consent checks" está ativado (Advanced) ou não (Basic, recomendado) |
| Google Ads / Conversion Linker (se existir) | Não disparar enquanto `ad_storage`/`ad_user_data`/`ad_personalization` = `denied` | Mesma verificação, para cada tag de Ads configurada |
| Meta/Facebook Pixel | **Não roda via GTM** — carrega por `meta-pixel.js` direto, fora do escopo do Consent Mode do Google | Nenhuma ação no GTM necessária; ver achado da seção 11 abaixo (o arquivo não carrega hoje, gap separado) |
| Demais tags do container | Desconhecido — não inspecionado (fora do escopo) | Auditoria manual: listar todas as tags do container e confirmar que cada uma respeita os sinais corretos antes do próximo rollout |

## 10. Basic vs. Advanced — mantido sem declarar unilateralmente

Reafirmado de `43-consent-mode-final-integration.md`: o código não decide isso sozinho. Com o `default` agora corretamente posicionado (seção 1-2), o comportamento resultante depende inteiramente da configuração de cada tag (seção 9). Recomendação mantida: Basic como padrão mais conservador, a confirmar com quem administra o GTM.

## 11. Meta Pixel — regressão confirmada, achado NOVO adicional

`meta-pixel.js` continua com a lógica correta (`test_meta_pixel_logic_gates_on_consent_when_loaded`, regressão mantida). **Achado novo desta fase**: `meta-pixel.min.js` nunca é referenciado em nenhum `www/*.html` real — só existe em `hooks.py` (`web_include_js`, mecanismo que não se aplica a essas páginas, mesmo problema que `consent-mode-v2.js` tinha antes desta fase). Confirmado via CDP: `window.fbq` nunca é definido, mesmo após Aceitar. **Não corrigido nesta fase** — a missão pediu explicitamente para não reescrever/republicar o Meta Pixel; este achado fica registrado para decisão humana separada (é uma correção de inclusão de script, não de lógica de consentimento — mas envolve decidir ligar tracking de Ads que hoje nunca rodou). Teste de regressão: `test_meta_pixel_min_js_is_never_referenced_by_any_real_page`.

## 12. Navegação funciona sem consentimento — confirmado

Nenhuma mudança de código nesta fase tocou Header, locale switcher, menu de Cursos, Hero, Pathfinder, links, B2B, Blog, teste de nível, WhatsApp ou Footer — só `<head>` (1 include) e o carregamento de 2 scripts (`consent-mode-v2.js`, cache-bust de `cookie-consent.min.js`). Nenhum desses fluxos depende de `dataLayer`/GTM pra funcionar (chamadas de `pushDataLayer()` são fire-and-forget, nunca bloqueiam navegação) — confirmado por leitura de código, não alterado.

## 13. Testes

18 testes em `test_pure_consent_mode_v2.py` (reescrito, era 6) + 1 teste pré-existente corrigido (`test_pure_marketing_pages.py`, cache-bust). **Suíte completa: 362 passed / 0 failed / 11 skipped** (piso anterior 353 + 9 líquidos). Verificação empírica via CDP documentada nas seções 1, 4, 6, 12 acima — não reproduzida em pytest (exigiria browser headless na suíte, fora do padrão do projeto).

## 14. MEDIA — reverificado, sem mudança

`vedium-references/licenses/envato/` contém só o `README.md` desta fase — nenhum certificado foi adicionado manualmente. **MEDIA continua FAIL**, 11/11 assets ainda `NEEDS_LICENSE_EVIDENCE`.

## 15. Regressão visual

`/` capturada em 1440px — Header, navegação, Hero idênticos ao estado já aprovado (nenhuma diferença visual, só a barra de cookies nova no rodapé da viewport, que é literalmente a interface de consentimento sendo corrigida, exceção já esperada pela missão). Nenhuma seção congelada (Hero/Header/Cursos/Live/B2B/Conhecimento/CTA/Footer) foi tocada.
