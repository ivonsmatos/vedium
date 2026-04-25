# =====================================================
# Vedium Production Deploy Script (PowerShell)
# =====================================================
# Use chave SSH (sem senha). Defina:
#   $env:VEDIUM_SERVER = "ip-ou-hostname"
#   $env:VEDIUM_USER   = "usuario-nao-root"
# Ou passe via parâmetro: .\deploy-vedium.ps1 -ServerIP x -User y
# =====================================================

param(
    [string]$ServerIP = $env:VEDIUM_SERVER,
    [string]$User     = $env:VEDIUM_USER,
    [string]$Domain   = "vediums.com"
)

if (-not $ServerIP) { Write-Error "Defina ServerIP (-ServerIP ou \$env:VEDIUM_SERVER)"; exit 1 }
if (-not $User)     { Write-Error "Defina User (-User ou \$env:VEDIUM_USER)";         exit 1 }

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "       VEDIUM PRODUCTION DEPLOY" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Servidor: $ServerIP" -ForegroundColor Yellow
Write-Host "Domínio:  $Domain"   -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Green

function Invoke-SSHCommand {
    param([string]$Command, [string]$Description = "")
    if ($Description) { Write-Host "🔄 $Description" -ForegroundColor Cyan }
    & ssh "$User@$ServerIP" $Command
    if ($LASTEXITCODE -ne 0) { Write-Error "❌ Falha: $Command"; exit 1 }
    Write-Host "✅ Sucesso!" -ForegroundColor Green
}

function Send-File {
    param([string]$LocalPath, [string]$RemotePath, [string]$Description = "")
    if ($Description) { Write-Host "📤 $Description ($LocalPath → $RemotePath)" -ForegroundColor Cyan }
    & scp $LocalPath "$User@${ServerIP}:$RemotePath"
    if ($LASTEXITCODE -ne 0) { Write-Error "❌ Falha ao enviar: $LocalPath"; exit 1 }
    Write-Host "✅ Arquivo enviado!" -ForegroundColor Green
}

try {
    Write-Host "`n🔍 ETAPA 1: VERIFICAÇÃO INICIAL" -ForegroundColor Magenta
    $requiredFiles = @(
        "deploy\nginx\$Domain.conf",
        "deploy\docker-compose.yml",
        "deploy\site\index.html",
        "vedium_core\vedium_core\public\css\vedium.css"
    )
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) { Write-Error "❌ Arquivo não encontrado: $file"; exit 1 }
    }
    Write-Host "✅ Todos os arquivos necessários encontrados" -ForegroundColor Green

    Write-Host "`n🛠️  ETAPA 2: PREPARAÇÃO DO SERVIDOR" -ForegroundColor Magenta
    Invoke-SSHCommand "sudo mkdir -p /opt/vedium/{nginx,site,site/css,backups} && sudo chown -R $User`:$User /opt/vedium" "Criando diretórios"
    Invoke-SSHCommand "sudo apt-get update && sudo apt-get install -y nginx docker.io docker-compose-v2 certbot python3-certbot-nginx" "Instalando dependências"
    Invoke-SSHCommand "sudo systemctl enable --now docker" "Habilitando Docker"

    Write-Host "`n📦 ETAPA 3: ENVIO DE ARQUIVOS" -ForegroundColor Magenta
    Invoke-SSHCommand "[ -f /etc/nginx/sites-available/$Domain ] && sudo cp /etc/nginx/sites-available/$Domain /opt/vedium/backups/$Domain.conf.backup-`$(date +%Y%m%d-%H%M%S) || true" "Backup nginx"
    Send-File "deploy\nginx\$Domain.conf" "/opt/vedium/nginx/$Domain.conf"  "Configuração nginx"
    Send-File "deploy\docker-compose.yml" "/opt/vedium/docker-compose.yml"   "Docker compose"
    Send-File "deploy\site\index.html"    "/opt/vedium/site/index.html"     "Site principal"
    Send-File "vedium_core\vedium_core\public\css\vedium.css" "/opt/vedium/site/css/vedium.css" "CSS compilado"

    Write-Host "`n🌐 ETAPA 4: CONFIGURAÇÃO NGINX" -ForegroundColor Magenta
    Invoke-SSHCommand "sudo cp /opt/vedium/nginx/$Domain.conf /etc/nginx/sites-available/$Domain" "Configurando nginx"
    Invoke-SSHCommand "sudo ln -sf /etc/nginx/sites-available/$Domain /etc/nginx/sites-enabled/$Domain" "Habilitando site"
    Invoke-SSHCommand "sudo rm -f /etc/nginx/sites-enabled/default" "Removendo site padrão"
    Invoke-SSHCommand "sudo nginx -t" "Testando configuração nginx"
    Invoke-SSHCommand "sudo systemctl restart nginx" "Reiniciando nginx"

    Write-Host "`n🐳 ETAPA 5: DOCKER CONTAINERS" -ForegroundColor Magenta
    Invoke-SSHCommand "cd /opt/vedium && docker compose up -d" "Iniciando containers"
    Invoke-SSHCommand "cd /opt/vedium && docker compose ps" "Status containers"

    Write-Host "`n✅ DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "Site:    http://$Domain"     -ForegroundColor Cyan
    Write-Host "LMS:     http://app.$Domain" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  PRÓXIMOS PASSOS:" -ForegroundColor Yellow
    Write-Host "1. Configure DNS: $Domain → $ServerIP" -ForegroundColor White
    Write-Host "2. SSL: sudo certbot --nginx -d $Domain -d www.$Domain -d app.$Domain" -ForegroundColor White
    Write-Host "3. Teste: https://$Domain" -ForegroundColor White
}
catch {
    Write-Error "❌ ERRO NO DEPLOY: $($_.Exception.Message)"
    exit 1
}
