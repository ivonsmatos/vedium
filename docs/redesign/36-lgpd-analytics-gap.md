# 36 — Gap de LGPD/consentimento em analytics (Fase C.1)

> Registro de um gap **pré-existente** encontrado durante a auditoria — não introduzido por esta fase, mas exposto por ela porque a Home V2 replica o mesmo padrão da Home atual. **Não corrigido silenciosamente aqui** — documentado para decisão humana, conforme pedido explícito da missão.

## 1. Comportamento atual (real, verificado)

- A barra de cookies existe (`public/js/cookie-consent.js`, carregada via `web_include_js` + script nas páginas do tema — ver memória do projeto) e é **informativa**: ela avisa sobre uso de cookies, mas **não bloqueia o carregamento de tags antes do clique** em "aceitar".
- O snippet do GTM (`GTM-P6Q2FXLK`) está no `<head>` (inline, produção) e agora também no `footer.html` da V2 — em ambos os casos, **carrega incondicionalmente**, antes de qualquer interação do usuário com a barra de cookies.
- GTM por sua vez dispara GA4 e outras tags configuradas no container — nenhuma delas está hoje atrás de um gate de consentimento (nenhum Consent Mode do Google configurado, até onde os arquivos deste repositório revelam).
- A Home V2 **replica exatamente esse mesmo comportamento** — não piora nem melhora a situação existente.

## 2. Risco

- LGPD (Lei 13.709/2018) trata dado de navegação/analytics como dado pessoal quando associado a identificadores (cookies, IP, client ID do GA4). Carregar essas tags **antes** do consentimento explícito é uma prática que a ANPD (Autoridade Nacional de Proteção de Dados) já sinalizou como problemática em orientações públicas, por analogia direta ao entendimento consolidado sob o GDPR europeu (base legal correspondente).
- Risco concreto: reclamação de titular, notificação da ANPD, ou simplesmente desalinhamento com a política de privacidade do próprio site (se ela afirmar algo como "só usamos cookies de analytics mediante consentimento", o comportamento real do código a contradiz).

## 3. Tags que carregam antes do consentimento (levantamento real)

| Tag | Onde | Carrega antes do clique em "aceitar"? |
|---|---|---|
| GTM (`GTM-P6Q2FXLK`) | `<head>` inline (produção, todas as páginas) + `footer.html` (V2, Fase C) | **Sim** |
| GA4 (via GTM) | Disparada pelo container GTM | **Sim** (segue o GTM) |
| Meta Pixel / outras tags de mídia paga (se configuradas no mesmo container) | Via GTM | **Sim**, mesmo mecanismo — não auditado individualmente nesta fase (fora do escopo: o container GTM é uma caixa-preta gerenciada fora deste repositório) |

## 4. Impacto

- Afeta **toda a Home atual** e agora também a Home V2 (mesmo padrão, nenhuma regressão nova).
- Não é um problema "criado" por esta fase — é um débito técnico/legal pré-existente que a auditoria da Fase C.1 expôs por estar no escopo de comparação `/` vs `/_home_v2`.

## 5. Solução recomendada (não implementada nesta fase)

1. Adotar **Google Consent Mode v2** (suporte nativo do GTM/GA4 para carregar tags em modo "denied" por padrão e só liberar coleta completa após consentimento).
2. Fazer a barra de cookies (`cookie-consent.js`) chamar `gtag('consent', 'update', {...})` no aceite, em vez de ser puramente informativa.
3. Alternativa mais simples (sem reescrever o Consent Mode): atrasar o carregamento do próprio snippet GTM até o clique em "aceitar" (injetar o script dinamicamente só então) — mais barato de implementar, menos robusto que Consent Mode (perde a distinção "negado mas com sinal agregado" que o Google oferece).
4. Nos dois casos, a política de privacidade (`/privacidade` ou equivalente) deve refletir com precisão o que o código realmente faz — hoje há risco de descompasso entre o texto jurídico e o comportamento técnico real (não auditado byte-a-byte nesta fase; fica como gate adicional).

## 6. Classificação de prioridade

**P1 — imediatamente após o rollout da Home V2, não bloqueador do rollout em si.**

Justificativa:
- Este gap **já existe hoje em produção**, na Home atual, com o mesmo GTM incondicional. A Home V2 não piora a exposição — ela replica um comportamento que já está no ar e sendo aceito (implicitamente) pelo negócio há tempo.
- Bloquear a troca de Home por causa de um problema que já existe na página que está sendo substituída não reduziria o risco real (o site inteiro continuaria exposto do mesmo jeito nas outras páginas enquanto se resolve).
- Por outro lado, não é aceitável adiar indefinidamente: por isso a classificação é P1 **imediatamente** após o rollout (não "algum dia") — o rollout da Home V2 é justamente o momento em que o assunto está sendo revisto de perto, o que torna natural resolver a causa raiz (o carregamento do GTM em si, sitewide) logo em seguida, em vez de tratar só a Home.
- **Não inventar conformidade aqui**: nenhuma alegação de que o site "está em conformidade com a LGPD" é feita neste documento — o achado é reportado como está, com a tag ainda carregando sem gate, para decisão humana informada.

## 7. Fora do escopo desta fase

- Qualquer alteração em `cookie-consent.js`, no snippet GTM, ou na política de privacidade — **nenhuma mudança de código relacionada a consentimento foi feita nesta fase**, conforme a instrução explícita da missão ("não corrigir silenciosamente").
- Auditoria completa de todas as tags configuradas *dentro* do container GTM (fora do repositório, gerenciado no painel do Google Tag Manager) — fica registrado como necessário para o item 5.3 da lista de solução, mas não executado aqui.
