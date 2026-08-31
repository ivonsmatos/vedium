# Plano de Deployment no Staging (Fase G.3)
**Data:** 2026-08-30

## 1. Preparação Local (Infraestrutura)

1. O container do Next.js foi adicionado no `deploy/docker-compose.yml`.
2. A configuração de roteamento híbrido foi criada em `deploy/nginx/staging.vediums.com.conf`.

## 2. Instruções de Teste Local Seguras (Para QA e Validação do Nginx sem afetar DNS)

Antes de publicarmos o DNS oficial, testaremos o proxy reverso do Nginx e a convivência híbrida através de uma modificação do arquivo `hosts`.

### Passo A: Enviar as novas configurações para o VPS Real

Execute localmente para enviar os novos arquivos de build sem recarregar o Nginx:

```bash
# Sincroniza o compose com o Next.js
scp deploy/docker-compose.yml user@ip-do-servidor:/opt/vedium/deploy/
scp deploy/Dockerfile.frontend user@ip-do-servidor:/opt/vedium/deploy/

# Sincroniza a configuração de staging do Nginx (mas não a habilita ainda)
scp deploy/nginx/staging.vediums.com.conf user@ip-do-servidor:/opt/vedium/deploy/nginx/
```

### Passo B: Construir e Ligar o Next.js (Sem Tráfego Público)

Faça SSH no servidor e execute:

```bash
cd /opt/vedium
docker compose -f deploy/docker-compose.yml up -d --build vedium-next
```
Isso levantará o Next.js na porta `3000`. Teste se está rodando:
```bash
curl 127.0.0.1:3000
```

### Passo C: Configurar o Nginx Staging e Reload

```bash
sudo cp /opt/vedium/deploy/nginx/staging.vediums.com.conf /etc/nginx/sites-available/staging.vediums.com
sudo ln -sf /etc/nginx/sites-available/staging.vediums.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```
Como o DNS ainda não existe para `staging.vediums.com`, nenhum usuário real será redirecionado para cá.

### Passo D: Host Machine Validation

No seu computador local (Windows), abra como Administrador:
`C:\Windows\System32\drivers\etc\hosts`

Adicione a linha (Substitua pelo IP do Servidor):
```text
123.456.789.012 staging.vediums.com
```
Acesse no navegador: `https://staging.vediums.com`. (O certificado pode acusar erro por conta do nome de domínio não bater com o `.pem` do `vediums.com` em produção que aplicamos no arquivo. Ignore o alerta de segurança no Chrome temporariamente digitando `thisisunsafe`).

Valide a navegação Híbrida:
1. `staging.vediums.com/` (Next.js)
2. `staging.vediums.com/blog/` (Frappe)
3. Headers `X-Robots-Tag`
