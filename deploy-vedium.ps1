# =====================================================
# Vedium Production Deploy Script
# =====================================================
# Executa deploy automatizado para o servidor vedium.com
# Servidor: ***REDACTED-IP***
# Domain: vedium.com
# =====================================================

param(
    [string]$ServerIP = "***REDACTED-IP***",
    [string]$User = "root", 
    [string]$Domain = "vedium.com"
)

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "       VEDIUM PRODUCTION DEPLOY" -ForegroundColor Green  
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Servidor: $ServerIP" -ForegroundColor Yellow
Write-Host "Domínio: $Domain" -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Green

# =====================================================
# Função para executar comandos SSH
# =====================================================
function Invoke-SSHCommand {
    param([string]$Command, [string]$Description = "")
    
    if ($Description) {
        Write-Host "🔄 $Description" -ForegroundColor Cyan
    }
    
    $sshCommand = "ssh -o StrictHostKeyChecking=no ${User}@${ServerIP} `"$Command`""
    Write-Host "Executando: $Command" -ForegroundColor Gray
    
    Invoke-Expression $sshCommand
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Falha ao executar: $Command"
        exit 1
    }
    
    Write-Host "✅ Sucesso!" -ForegroundColor Green
}

# =====================================================
# Função para enviar arquivos SCP
# =====================================================
function Send-File {
    param([string]$LocalPath, [string]$RemotePath, [string]$Description = "")
    
    if ($Description) {
        Write-Host "📤 $Description" -ForegroundColor Cyan
    }
    
    $scpCommand = "scp -o StrictHostKeyChecking=no `"$LocalPath`" ${User}@${ServerIP}:`"$RemotePath`""
    Write-Host "Enviando: $LocalPath -> $RemotePath" -ForegroundColor Gray
    
    Invoke-Expression $scpCommand
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Falha ao enviar: $LocalPath"
        exit 1
    }
    
    Write-Host "✅ Arquivo enviado!" -ForegroundColor Green
}

try {
    Write-Host "`n🔍 ETAPA 1: VERIFICAÇÃO INICIAL" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    
    # Verificar conectividade
    Write-Host "Testando conectividade..." -ForegroundColor Yellow
    $ping = Test-Connection -ComputerName $ServerIP -Count 2 -Quiet
    if (-not $ping) {
        Write-Error "❌ Servidor não está acessível: $ServerIP"
        exit 1
    }
    Write-Host "✅ Servidor acessível" -ForegroundColor Green
    
    # Verificar se arquivos locais existem
    $requiredFiles = @(
        "deploy\nginx\vedium.com.conf",
        "deploy\docker-compose.yml",
        "deploy\site\index.html",
        "vedium_core\vedium_core\public\css\vedium.css"
    )
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-Error "❌ Arquivo não encontrado: $file"
            exit 1
        }
    }
    Write-Host "✅ Todos os arquivos necessários encontrados" -ForegroundColor Green
    
    Write-Host "`n🛠️  ETAPA 2: PREPARAÇÃO DO SERVIDOR" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    
    # Criar diretórios necessários
    Invoke-SSHCommand "mkdir -p /opt/vedium/nginx /opt/vedium/site /opt/vedium/backups" "Criando diretórios"
    
    # Instalar dependências se necessário
    Invoke-SSHCommand "apt-get update && apt-get install -y nginx docker.io docker-compose certbot python3-certbot-nginx" "Instalando dependências"
    
    # Verificar Docker
    Invoke-SSHCommand "systemctl start docker && systemctl enable docker" "Iniciando Docker"
    
    Write-Host "`n📦 ETAPA 3: ENVIO DE ARQUIVOS" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    
    # Backup da configuração atual (se existir)
    Invoke-SSHCommand "if [ -f /etc/nginx/sites-available/vedium.com ]; then cp /etc/nginx/sites-available/vedium.com /opt/vedium/backups/vedium.com.conf.backup-$(date +%Y%m%d-%H%M%S); fi" "Backup da configuração nginx"
    
    # Enviar arquivos
    Send-File "deploy\nginx\vedium.com.conf" "/opt/vedium/nginx/vedium.com.conf" "Enviando configuração nginx"
    Send-File "deploy\docker-compose.yml" "/opt/vedium/docker-compose.yml" "Enviando docker-compose"
    Send-File "deploy\site\index.html" "/opt/vedium/site/index.html" "Enviando site principal"
    
    # Enviar CSS compilado
    Send-File "vedium_core\vedium_core\public\css\vedium.css" "/opt/vedium/site/css/vedium.css" "Enviando CSS compilado"
    
    Write-Host "`n🌐 ETAPA 4: CONFIGURAÇÃO NGINX" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    
    # Configurar nginx
    Invoke-SSHCommand "cp /opt/vedium/nginx/vedium.com.conf /etc/nginx/sites-available/vedium.com" "Copiando configuração nginx"
    Invoke-SSHCommand "ln -sf /etc/nginx/sites-available/vedium.com /etc/nginx/sites-enabled/vedium.com" "Habilitando site"
    Invoke-SSHCommand "rm -f /etc/nginx/sites-enabled/default" "Removendo site padrão"
    
    # Testar configuração nginx
    Invoke-SSHCommand "nginx -t" "Testando configuração nginx"
    
    Write-Host "`n🔒 ETAPA 5: CONFIGURAÇÃO SSL" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    
    # Restart nginx primeiro para funcionar sem SSL
    Invoke-SSHCommand "systemctl restart nginx" "Reiniciando nginx"
    
    Write-Host "⚠️  CONFIGURAÇÃO SSL MANUAL NECESSÁRIA" -ForegroundColor Yellow
    Write-Host "Execute os comandos abaixo no servidor:" -ForegroundColor Yellow
    Write-Host "certbot --nginx -d vedium.com -d www.vedium.com -d app.vedium.com" -ForegroundColor Cyan
    Write-Host "systemctl restart nginx" -ForegroundColor Cyan
    
    Write-Host "`n🐳 ETAPA 6: DOCKER CONTAINERS" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    
    # Iniciar containers Docker
    Invoke-SSHCommand "cd /opt/vedium && docker-compose up -d" "Iniciando containers Docker"
    Invoke-SSHCommand "docker-compose ps" "Verificando status dos containers"
    
    Write-Host "`n✅ DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "Site principal: http://vedium.com" -ForegroundColor Cyan
    Write-Host "LMS: http://app.vedium.com:8005 (temporário)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  PRÓXIMOS PASSOS MANUAIS:" -ForegroundColor Yellow
    Write-Host "1. Configure DNS: vedium.com -> $ServerIP" -ForegroundColor White
    Write-Host "2. Execute SSL: certbot --nginx -d vedium.com -d www.vedium.com -d app.vedium.com" -ForegroundColor White
    Write-Host "3. Reinicie nginx: systemctl restart nginx" -ForegroundColor White
    Write-Host "4. Teste: https://vedium.com" -ForegroundColor White
    
}
catch {
    Write-Error "❌ ERRO NO DEPLOY: $($_.Exception.Message)"
    exit 1
}