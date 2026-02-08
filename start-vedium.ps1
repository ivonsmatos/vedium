# =====================================================
# Script de Inicialização do Ambiente Vedium (Windows)
# =====================================================

Write-Host "🚀 Iniciando ambiente Vedium..." -ForegroundColor Cyan

# Verificar se Docker está rodando
try {
    docker info | Out-Null
    Write-Host "✓ Docker está rodando" -ForegroundColor Green
} catch {
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
} catch {
    Write-Host "⚠️  Frappe ainda não está pronto. Aguarde mais alguns segundos." -ForegroundColor Yellow
}

# Instruções finais
Write-Host "`n✅ Ambiente iniciado!" -ForegroundColor Green
Write-Host "`n📋 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Acesse o container: docker exec -it vedium-frappe bash"
Write-Host "2. Verifique apps instalados: bench --site vediums.com list-apps"
Write-Host "3. Execute migrações: bench --site vediums.com migrate"
Write-Host "4. Acesse a interface: http://localhost:8005"
Write-Host "`n📖 Consulte o guia completo em: guia_instalacao_lms.md" -ForegroundColor Yellow
