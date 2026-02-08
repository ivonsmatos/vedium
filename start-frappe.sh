#!/bin/bash

echo "🚀 Iniciando Vedium..."

# Aguardar MariaDB estar pronto
echo "⏳ Aguardando MariaDB..."
sleep 10

# Navegar para o diretório do bench
cd /home/frappe/frappe-bench

# Iniciar servidor
echo "🌐 Iniciando servidor Frappe..."
bench start

# Manter container rodando
tail -f /dev/null
