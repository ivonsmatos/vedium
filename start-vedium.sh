#!/bin/bash

# =====================================================
# Script de Inicialização do Ambiente Vedium
# =====================================================

echo "🚀 Iniciando ambiente Vedium..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker Desktop primeiro."
    exit 1
fi

echo "✓ Docker está rodando"

# Subir containers
echo "📦 Subindo containers..."
docker-compose up -d

# Aguardar containers iniciarem
echo "⏳ Aguardando containers iniciarem..."
sleep 10

# Verificar status
echo "📊 Status dos containers:"
docker ps --filter "name=vedium"

# Verificar se Frappe está acessível
echo ""
echo "🔍 Verificando serviços..."
if docker exec vedium-frappe bench --version > /dev/null 2>&1; then
    echo "✓ Frappe está acessível"
else
    echo "⚠️  Frappe ainda não está pronto. Aguarde mais alguns segundos."
fi

# Instruções finais
echo ""
echo "✅ Ambiente iniciado!"
echo ""
echo "📋 Próximos passos:"
echo "1. Acesse o container: docker exec -it vedium-frappe bash"
echo "2. Verifique apps instalados: bench --site vediums.com list-apps"
echo "3. Execute migrações: bench --site vediums.com migrate"
echo "4. Acesse a interface: http://localhost:8005"
echo ""
echo "📖 Consulte o guia completo em: guia_instalacao_lms.md"
