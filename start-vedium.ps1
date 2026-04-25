# =====================================================
# Script de Inicialização do Ambiente Vedium (Windows)
# =====================================================

Write-Host "🚀 Iniciando ambiente Vedium..." -ForegroundColor Cyan

# Verificar se Docker está rodando
try {
    docker info | Out-Null
    Write-Host "✓ Docker está rodando" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker não está rodando. Por favor, inicie o Docker Desktop primeiro." -ForegroundColor Red
    exit 1
}

# Subir containers
Write-Host "📦 Subindo containers..." -ForegroundColor Cyan
docker-compose up -d

# Aguardar containers iniciarem
Write-Host "⏳ Aguardando containers iniciarem..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar status
Write-Host "`n📊 Status dos containers:" -ForegroundColor Cyan
docker ps --filter "name=vedium"

# Verificar se Frappe está acessível
Write-Host "`n🔍 Verificando serviços..." -ForegroundColor Cyan
try {
    docker exec vedium-frappe bench --version | Out-Null
    Write-Host "✓ Frappe está acessível" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Frappe ainda não está pronto. Aguarde mais alguns segundos." -ForegroundColor Yellow
}

# Iniciar bench start automaticamente (necessário após restart do container)
Write-Host "`n🌐 Iniciando servidor web Frappe (bench start)..." -ForegroundColor Cyan
docker exec -d vedium-frappe bash -c "cd /home/frappe/frappe-bench && bench start > /tmp/bench.log 2>&1"
Start-Sleep -Seconds 18

# Verificar se bench serve subiu
$benchLog = docker exec vedium-frappe bash -c "cat /tmp/bench.log 2>/dev/null | tail -10"
if ($benchLog -match "Running on") {
    Write-Host "✓ Servidor web rodando (bench serve ativo)" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Verificar log: docker exec vedium-frappe bash -c 'tail -20 /tmp/bench.log'" -ForegroundColor Yellow
}

# Instruções finais
Write-Host "`n✅ Ambiente iniciado!" -ForegroundColor Green
Write-Host "`n📋 Acesso:" -ForegroundColor Cyan
Write-Host "  Site principal:    http://vedium.local:8005"
Write-Host "  Catálogo cursos:   http://vedium.local:8005/catalogo"
Write-Host "  LMS (Frappe):      http://vedium.local:8005/lms/courses"
Write-Host "  Admin:             http://vedium.local:8005/app"
Write-Host "`n💡 Dica: /courses redireciona para o LMS padrão Frappe. Use /catalogo." -ForegroundColor Yellow
