#!/bin/bash
# =====================================================
# Vedium — Hardening do servidor existente
# =====================================================
# O que faz:
#   1. AUDITA o sistema (mostra logins recentes, processos, portas)
#   2. CRIA um usuário 'deploy' com sudo
#   3. INSTALA a chave SSH pública (passada via stdin) em deploy + root
#   4. GERA uma senha root nova e forte
#   5. PREPARA /opt/vedium para deploy futuro
#   6. NÃO desabilita SSH por senha ainda (faz depois, manual, quando confirmar acesso por chave)
# =====================================================

set -e

echo "════════════════════════════════════════════════════"
echo "  VEDIUM — HARDENING DO SERVIDOR"
echo "  $(date)"
echo "════════════════════════════════════════════════════"

# A chave SSH pública vem via variável de ambiente SSH_PUB_KEY
if [ -z "${SSH_PUB_KEY:-}" ]; then
    echo "❌ Variável SSH_PUB_KEY não foi enviada."
    exit 1
fi

# ────────────────────────────────────────────────────
# 1. AUDIT — mostrar o que está rodando
# ────────────────────────────────────────────────────
echo ""
echo "═══ 1. AUDITORIA DO SISTEMA ═══"
echo ""

echo "▶ Sistema operacional:"
lsb_release -d 2>/dev/null || cat /etc/os-release | head -2

echo ""
echo "▶ Uptime e carga:"
uptime

echo ""
echo "▶ RAM e disco:"
free -h | head -2
echo ""
df -h / 2>/dev/null

echo ""
echo "▶ Logins recentes (últimos 10):"
last -n 10 2>/dev/null | head -10 || echo "(sem dados)"

echo ""
echo "▶ Quem está logado AGORA:"
who
echo ""
w 2>/dev/null | head -5

echo ""
echo "▶ Processos consumindo mais CPU:"
ps -eo pid,%cpu,%mem,user,comm --sort=-%cpu | head -10

echo ""
echo "▶ Portas escutando:"
ss -tunlp 2>/dev/null | grep LISTEN | head -20 || netstat -tunlp 2>/dev/null | grep LISTEN | head -20

echo ""
echo "▶ Cron do root:"
crontab -l 2>/dev/null | grep -v '^#' | head || echo "(vazio)"

echo ""
echo "▶ /etc/cron.d/:"
ls /etc/cron.d/ 2>/dev/null

echo ""
echo "▶ Containers Docker (se Docker existe):"
which docker >/dev/null 2>&1 && docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null || echo "(Docker não instalado)"

echo ""
echo "▶ Binários estranhos em /tmp e /var/tmp:"
find /tmp /var/tmp -maxdepth 2 -type f -executable 2>/dev/null | head -10 || echo "(nenhum)"

# ────────────────────────────────────────────────────
# 2. CRIAR USUÁRIO 'deploy' COM SUDO
# ────────────────────────────────────────────────────
echo ""
echo "═══ 2. USUÁRIO 'deploy' ═══"

if id deploy >/dev/null 2>&1; then
    echo "✓ Usuário 'deploy' já existe"
else
    useradd -m -s /bin/bash deploy
    echo "✓ Usuário 'deploy' criado"
fi

# sudo sem senha (vamos exigir chave SSH, sudo com senha vai bloquear deploy automático)
echo "deploy ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-deploy
chmod 0440 /etc/sudoers.d/90-deploy
echo "✓ deploy adicionado ao sudo"

# ────────────────────────────────────────────────────
# 3. INSTALAR CHAVE SSH
# ────────────────────────────────────────────────────
echo ""
echo "═══ 3. CHAVE SSH ═══"

# deploy
mkdir -p /home/deploy/.ssh
echo "$SSH_PUB_KEY" > /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys
echo "✓ Chave instalada em deploy"

# root (backup, vamos eventualmente desabilitar root login)
mkdir -p /root/.ssh
grep -qF "$SSH_PUB_KEY" /root/.ssh/authorized_keys 2>/dev/null || echo "$SSH_PUB_KEY" >> /root/.ssh/authorized_keys
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys
echo "✓ Chave instalada em root (fallback)"

# ────────────────────────────────────────────────────
# 4. NOVA SENHA ROOT (forte, aleatória)
# ────────────────────────────────────────────────────
echo ""
echo "═══ 4. NOVA SENHA ROOT ═══"

NEW_ROOT_PWD=$(tr -dc 'A-Za-z0-9!@#%^&*-_+=' < /dev/urandom | head -c 32)
echo "root:$NEW_ROOT_PWD" | chpasswd
echo ""
echo "🔐 NOVA SENHA ROOT (anote no Bitwarden agora):"
echo ""
echo "    $NEW_ROOT_PWD"
echo ""
echo "    (Você não vai precisar usar — vai logar com chave SSH)"

# ────────────────────────────────────────────────────
# 5. PREPARAR /opt/vedium
# ────────────────────────────────────────────────────
echo ""
echo "═══ 5. ESTRUTURA /opt/vedium ═══"

mkdir -p /opt/vedium/{nginx,site,site/css,backups}
chown -R deploy:deploy /opt/vedium
echo "✓ /opt/vedium criado e propriedade do deploy"

# ────────────────────────────────────────────────────
# 6. RESUMO
# ────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════"
echo "  RESUMO"
echo "════════════════════════════════════════════════════"
echo ""
echo "✅ Audit feito (verifique a saída acima)"
echo "✅ Usuário 'deploy' criado com sudo NOPASSWD"
echo "✅ Sua chave SSH instalada (deploy + root)"
echo "✅ Senha root trocada (mostrada acima — anote!)"
echo "✅ /opt/vedium pronto para deploy"
echo ""
echo "❗ PRÓXIMO PASSO MANUAL:"
echo "   Da sua máquina, teste o login com chave SSH:"
echo ""
echo "       ssh -i ~/.ssh/vedium_ed25519 deploy@45.151.122.234"
echo ""
echo "   Se entrar SEM PEDIR SENHA → tudo certo, podemos seguir."
echo "   Se pedir senha → algo deu errado, me avise."
echo ""
echo "❗ AINDA NÃO DESABILITAMOS SSH POR SENHA."
echo "   Vamos fazer isso DEPOIS de confirmar que chave funciona."
echo ""
