# Next.js Hosting Decision (G.3)
**Data:** 2026-08-30

## 1. Objetivo

Definir e documentar a estratégia de hospedagem para a aplicação Next.js desenvolvida para o frontend público da Vedium, substituindo o atual site estático mantido pelo Nginx.

## 2. Opções Avaliadas

### Opção A: Container Next.js na Infraestrutura Atual (VPS Único)
*   **Descrição:** Adicionar um novo serviço `vedium-next` no `deploy/docker-compose.yml` atual, hospedando o servidor Node do Next.js. O Nginx existente servirá como Proxy Reverso também para este container.
*   **Vantagens:**
    *   Custo zero adicional (aproveita a CPU/RAM ociosa do VPS atual).
    *   Zero latência de rede entre Next.js e a API Frappe (para chamadas SSR e WebMCP backend).
    *   Manutenção centralizada. Um único deploy via `docker compose`.
    *   Simplicidade total no roteamento Híbrido (Nginx como *single source of truth*).
*   **Desvantagens:**
    *   Escalonabilidade vertical limitada ao VPS atual (se o tráfego estourar, ambos caem).

### Opção B: Servidor Next.js Separado (Novo VPS)
*   **Descrição:** Hospedar a aplicação Next.js em um servidor virtual (VPS) inteiramente separado, gerenciado individualmente.
*   **Vantagens:**
    *   Isolamento de falhas.
    *   Escalonamento independente.
*   **Desvantagens:**
    *   Custo financeiro de manter um segundo servidor.
    *   Latência de rede SSL entre servidores.
    *   Maior complexidade na configuração de roteamento híbrido no DNS.

### Opção C: Plataformas Serverless (Vercel, Netlify, Cloudflare Pages)
*   **Descrição:** Hospedar o código na Vercel (provedor oficial do Next.js).
*   **Vantagens:**
    *   Infraestrutura e CD automático.
    *   Global Edge CDN nativo para assets e Serverless Functions.
*   **Desvantagens:**
    *   Custo potencialmente alto para sites comerciais em tiers pagos.
    *   Possíveis timeouts (limite padrão de 10s-50s) nas chamadas para a API do Frappe.
    *   Roteamento híbrido (Next.js Edge Proxy -> Frappe via Vercel `rewrites`) seria complexo, lento e consumiria tráfego "Serverless" na Vercel desnecessariamente.

## 3. Decisão: Opção A (Container na Infraestrutura Atual)

**Decisão técnica:** Optamos pela **Opção A**. O Next.js será hospedado em um container Docker diretamente no servidor atual, gerenciado pelo `docker-compose.yml` já existente.

**Fundamentação técnica para roteamento:**
Para permitir o Roteamento Híbrido entre o novo site e páginas legadas do Frappe (ex: `/blog`), o Nginx precisa atuar como Gateway (orquestrador). Hospedar o Next.js e o Frappe no mesmo Docker Engine torna o Nginx capaz de orquestrar a decisão (ex: "Se for `/cursos`, mande para a porta 3000. Se for `/blog`, mande para a 8005"). Isso seria consideravelmente mais lento se a Vercel precisasse rotear o tráfego para nosso VPS.

## 4. Implementação

1.  O serviço `vedium-next` será adicionado ao `deploy/docker-compose.yml`, expondo a porta interna `3000`.
2.  Um `Dockerfile.frontend` construirá o app (`npm run build`) e inicializará (`npm start`).
3.  O Nginx enviará o tráfego web para a porta `3000` via proxy.
