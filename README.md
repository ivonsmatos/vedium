# 📈 Roadmap de Melhorias (2026)

- Pagamentos: Mercado Pago/Basecommerce, checkout central, cupons, testes automatizados
- Cursos: Certificado digital, quiz/prova de nível, IA feedback, gamificação, comunidade, acessibilidade
- UI/UX: Microinterações, onboarding gamificado, performance, white-label
- Backend: Factory de gateways, observabilidade, painel de suporte
- Segurança: Pentest, alertas automáticos, gestão de segredos
- Documentação: API pública, onboarding prof/alunos, OpenAPI Schemas

## 📚 Documentação

- [Documentação da API](vedium_core/docs/api.md) — exemplos reais de endpoints
- Recomenda-se Swagger/Redoc para documentação interativa
- Geração automática de OpenAPI Schemas para pagamentos e integrações

### Exemplo de uso de endpoint (REST)

```http
POST /api/method/vedium_core.vedium_core.api.create_checkout
{
   "course_name": "CURSO_ID",
   "gateway": "mercadopago",
   "coupon_code": "PROMO10"
}
```

## 👩‍🏫 Onboarding Rápido para Professores

- Guia do educador, templates de curso e vídeos de treinamento em `vedium_core/docs/`
- Suporte e abertura de chamados via painel integrado

## 🛠️ Observabilidade e Suporte

- Painel de suporte: abertura e acompanhamento de chamados
- Dashboard interno: status de containers, disco, memória, alertas críticos
- Integração de métricas: Google Analytics 4, Hotjar/Clarity, banner LGPD

## 📖 Documentação e Onboarding

- API pública documentada em `vedium_core/docs/api.md`
- Recomenda-se uso de Swagger ou Redoc para documentação interativa (exemplo: [Redoc CLI](https://github.com/Redocly/redoc))
- Onboarding rápido para professores: criar guia, templates de curso e vídeos de treinamento em `docs/`

## 📊 Métricas e LGPD

- Integração recomendada: Google Analytics 4, Hotjar ou Clarity
- Sempre exibir banner de consentimento LGPD para rastreamento
- Exemplo de integração: inserir snippet no template base.html
  ![Security Status](https://github.com/vedium/vedium/actions/workflows/security-check.yml/badge.svg)

# Vedium LMS

## 🔒 Segurança e Auditoria

- Auditoria automática diária: [security-check.yml](.github/workflows/security-check.yml)
- Monitoramento de containers, SSL, disco, memória e logs
- Scripts de backup, ativação SSL, auditoria e monitoramento em `deploy/scripts/`

**Vedium** é a primeira plataforma de **Inteligência Cultural** para profissionais globais. Uma solução completa de LMS (Learning Management System) construída sobre o **Frappe Framework v16 (Stable)**, oferecendo cursos de Inglês Executivo, Hebraico Tech e Iorubá Ancestral com uma experiência premium.

🌐 **Site**: [https://vediums.com](https://vediums.com)
📚 **Plataforma LMS**: [https://app.vediums.com](https://app.vediums.com)

---

## 🚀 Stack Tecnológica (Modernizada)

| Componente         | Tecnologia              | Versão       |
| ------------------ | ----------------------- | ------------ |
| **Backend**        | Frappe Framework        | **v16**      |
| **Linguagem**      | Python                  | **3.14**     |
| **Frontend**       | Jinja2 + Tailwind CSS   | v3.4         |
| **Runtime JS**     | Node.js                 | **v24**      |
| **Banco de Dados** | MariaDB                 | 10.6         |
| **Cache**          | Redis                   | 7-alpine     |
| **Web Server**     | NGINX                   | Latest       |
| **Infraestrutura** | Docker & Docker Compose | v3.8         |
| **Design System**  | Raízes de Luxo          | **v2**       |

---

## 📂 Estrutura do Projeto

```
vedium/
├── vedium_core/              # Aplicação Frappe (Custom App)
│   ├── vedium_core/          # Código fonte Python
│   │   ├── controllers/      # Controllers da API
│   │   ├── templates/        # Templates Jinja2
│   │   ├── public/           # Assets estáticos
│   │   └── www/              # Páginas web
│   ├── input.css             # Entrada Tailwind CSS
│   └── hooks.py              # Configurações Frappe
│
├── deploy/                   # 🆕 Configurações de Deploy
│   ├── docker-compose.yml    # Docker Compose produção
│   ├── nginx/                # Configurações NGINX
│   │   └── vediums.com.conf  # Virtual host
│   ├── scripts/              # Scripts de automação
│   │   ├── backup.sh         # Backup automático
│   │   ├── deploy.sh         # Deploy script
│   │   ├── security-monitor.sh # Monitoramento
│   │   ├── audit-log.sh      # Configuração de auditoria
│   │   └── ativar-ssl.sh     # Ativação SSL
│   ├── site/                 # Site estático institucional
│   │   ├── index.html        # Home page
│   │   ├── sobre.html        # Página sobre
│   │   ├── css/              # Estilos
│   │   ├── images/           # Imagens e logos
│   │   ├── manifest.json     # PWA manifest
│   │   └── sw.js             # Service Worker
│   ├── SECURITY.md           # Documentação de segurança
│   └── .env.example          # Variáveis de ambiente
│
├── .github/workflows/        # 🆕 GitHub Actions CI/CD
│   ├── deploy.yml            # Deploy automático
│   ├── security-check.yml    # Verificação de segurança
│   └── backup.yml            # Backup automático
│
├── docker-compose.yml        # Docker Compose local
├── init.sh                   # Inicialização ambiente dev
└── install_apps.sh           # Instalação de apps
```

---

## 🛠️ Instalação Local

### Pré-requisitos

- Docker e Docker Compose
- Git
- Node.js 18+ (para build CSS)

### Setup Rápido

```bash
# Clone o repositório
git clone https://github.com/vedium-global/vedium.git
cd vedium

# Inicie os containers
docker-compose up -d

# Execute a inicialização
./init.sh

# Instale os apps
./install_apps.sh
```

### Acessos Locais

| Serviço | URL                   |
| ------- | --------------------- |
| Frappe  | <http://localhost:8005> |
| MariaDB | localhost:3307        |

---

## 🚀 Deploy para Produção

### Configuração Inicial

1. **Configure os secrets no GitHub:**

   Vá em `Settings > Secrets and variables > Actions` e adicione:

   | Secret            | Descrição                                |
   | ----------------- | ---------------------------------------- |
   | `SSH_PRIVATE_KEY` | Chave SSH privada para o servidor        |
   | `SSH_KNOWN_HOSTS` | Output de `ssh-keyscan seu-servidor.com` |
   | `DEPLOY_USER`     | Usuário SSH (ex: `root`)                 |
   | `DEPLOY_HOST`     | IP ou hostname do servidor               |

2. **Copie as configurações para o servidor:**

   ```bash
   scp -r deploy/ root@seu-servidor:/opt/vedium/
   ```

3. **No servidor, execute:**

   ```bash
   cd /opt/vedium
   cp deploy/.env.example .env
   # Edite o .env com suas credenciais
   nano .env

   # Inicie os containers
   docker-compose -f deploy/docker-compose.yml up -d

   # Configure SSL
   ./deploy/scripts/ativar-ssl.sh
   ```

### Deploy Automático

Após configurar os secrets, todo push para `main` que modifique arquivos em `deploy/` dispara o deploy automático.

```bash
# Deploy manual via GitHub Actions
gh workflow run deploy.yml -f deploy_type=full
```

---

## 🔒 Segurança

O Vedium segue as melhores práticas de segurança:

- ✅ **SSL/TLS** com Let's Encrypt (TLSv1.2/1.3 apenas)
- ✅ **HSTS** habilitado (2 anos, includeSubDomains, preload)
- ✅ **Rate Limiting** no login (5 req/min)
- ✅ **Fail2ban** para proteção SSH
- ✅ **Backups criptografados** (AES-256)
- ✅ **Conformidade** LGPD/GDPR

📖 Veja [deploy/SECURITY.md](deploy/SECURITY.md) para detalhes completos.

---

## 📊 Monitoramento

### Scripts Disponíveis

```bash
# Verificar status de segurança
/opt/vedium/scripts/security-monitor.sh

# Executar backup manual
/opt/vedium/scripts/backup.sh

# Ver logs
tail -f /var/log/vedium-security.log
```

### GitHub Actions

- **Deploy**: Acionado em push para `main`
- **Security Check**: Diário às 06:00 UTC
- **Backup**: Diário às 02:00 UTC

---

## 🌐 Domínios

| Domínio         | Função             | Servidor         |
| --------------- | ------------------ | ---------------- |
| vediums.com     | Site institucional | NGINX (estático) |
| <www.vediums.com> | Redirect           | → vediums.com    |
| app.vediums.com | Plataforma LMS     | Frappe/ERPNext   |

---

## 📱 PWA

O site institucional é uma Progressive Web App com:

- ✅ Manifest configurado
- ✅ Service Worker para cache offline
- ✅ Instalável em dispositivos móveis
- ✅ Ícones para iOS/Android

---

## 📝 Licença

Copyright © 2026 Vedium Global Education. Todos os direitos reservados.

---

## 📞 Contato

- **Email**: <contato@vediums.com>
- **Site**: <https://vediums.com>
- **LinkedIn**: [Vedium Global](https://linkedin.com/company/vedium)
