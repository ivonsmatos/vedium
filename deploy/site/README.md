# Vedium - Cloudflare Pages (Site Institucional)

Este diretório contém o site institucional estático do Vedium para deploy no Cloudflare Pages.

## Estrutura

```
cloudflare-pages/
├── index.html          # Home page
├── sobre.html          # Página Sobre
├── manifest.json       # PWA manifest
├── sw.js               # Service Worker (PWA)
├── _redirects          # Regras de redirecionamento Cloudflare
├── _headers            # Cabeçalhos de segurança/cache
├── css/
│   └── vedium.css      # Estilos customizados
├── images/             # Imagens e ícones
└── js/                 # Scripts (se necessário)
```

## Deploy no Cloudflare Pages

1. **Via Dashboard:**
   - Acesse [Cloudflare Pages](https://pages.cloudflare.com/)
   - Connect to Git → Selecione o repositório
   - Build settings:
     - Build command: (deixe vazio)
     - Build output directory: `cloudflare-pages`
   - Deploy

2. **Via Wrangler CLI:**
   ```bash
   npm install -g wrangler
   wrangler login
   wrangler pages deploy cloudflare-pages --project-name=vedium
   ```

## Domínios

| Domínio         | Destino                          | Tipo               |
| --------------- | -------------------------------- | ------------------ |
| vediums.com     | Cloudflare Pages                 | Site institucional |
| www.vediums.com | vediums.com                      | Redirect           |
| app.vediums.com | Servidor Frappe (45.151.122.234) | LMS Platform       |

## URLs e Redirecionamentos

O arquivo `_redirects` configura:

- URLs limpas (sem .html)
- Rotas do LMS → `https://app.vediums.com/lms/*`
- API → `https://app.vediums.com/api/*`
- Blog → `https://app.vediums.com/blog/*`

## Configuração DNS (Cloudflare)

```
Type    Name    Content              Proxy
A       @       45.151.122.234       ✅ Proxied
CNAME   www     vediums.com          ✅ Proxied
A       app     45.151.122.234       ✅ Proxied
```

**Nota:** Para Cloudflare Pages, o domínio `vediums.com` precisa ser configurado como Custom Domain no projeto Pages.

## Atualizando o CSS

O arquivo `css/vedium.css` é copiado de `vedium_core/vedium_core/public/css/vedium.css`.

Após alterações no Tailwind:

```bash
cd vedium_core
npm run build-css
cp vedium_core/public/css/vedium.css ../cloudflare-pages/css/
```

## PWA

O site é uma Progressive Web App com:

- ✅ Manifest configurado
- ✅ Service Worker para cache offline
- ✅ Meta tags PWA no HTML
- ✅ Ícones para iOS/Android

## Segurança

Headers configurados em `_headers`:

- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection
- Referrer-Policy
- Cache-Control otimizado por tipo de arquivo
