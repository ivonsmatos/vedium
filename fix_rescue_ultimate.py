import paramiko
import os
import sys
import time

def fix_server_ultimate():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    gh_key_path = os.path.expanduser("~/.ssh/github_actions_deploy_key.pub")
    gh_pub = ""
    if os.path.exists(gh_key_path):
        with open(gh_key_path, "r") as f:
            gh_pub = f.read().strip()
            
    win_pub = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBE+SnTLkdybW3c803vzZT9aNjTOM1cz7nIg0fEekv5c actahub-local-dev"
    
    print("Aguardando o servidor de resgate iniciar (tentando conectar a cada 10s)...")
    connected = False
    for i in range(30):
        try:
            client.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=5)
            connected = True
            print("Conectado com sucesso!")
            break
        except Exception as e:
            print(f"Tentativa {i+1} falhou, aguardando...")
            time.sleep(10)
            
    if not connected:
        print("Erro: Nao foi possivel conectar ao servidor de resgate apos 5 minutos.")
        sys.exit(1)
    
    commands = [
        "mount /dev/sda1 /mnt",
        "mount --bind /dev /mnt/dev",
        "mount --bind /proc /mnt/proc",
        "mount --bind /sys /mnt/sys",
        
        # 1. Resetar a senha do root DE FATO pelo sistema interno (chroot)
        "chroot /mnt bash -c \"echo 'root:Protonsysdba@1986' | chpasswd\"",
        
        # 2. Varrer TODOS os arquivos de configuração do SSH e arrancar bloqueios
        "sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /mnt/etc/ssh/sshd_config",
        "sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /mnt/etc/ssh/sshd_config",
        "sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' /mnt/etc/ssh/sshd_config",
        
        "if ls /mnt/etc/ssh/sshd_config.d/*.conf 1> /dev/null 2>&1; then sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /mnt/etc/ssh/sshd_config.d/*.conf; fi",
        "if ls /mnt/etc/ssh/sshd_config.d/*.conf 1> /dev/null 2>&1; then sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /mnt/etc/ssh/sshd_config.d/*.conf; fi",
        "if ls /mnt/etc/ssh/sshd_config.d/*.conf 1> /dev/null 2>&1; then sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' /mnt/etc/ssh/sshd_config.d/*.conf; fi",
        
        # 3. Blindar contra o Cloud-Init
        "if [ -f /mnt/etc/cloud/cloud.cfg ]; then sed -i 's/ - ssh/# - ssh/g' /mnt/etc/cloud/cloud.cfg; fi",
        
        # 4. Injetar AMBAS as chaves (Windows e GitHub) diretamente no arquivo
        "mkdir -p /mnt/root/.ssh",
        f"echo '{win_pub}' > /mnt/root/.ssh/authorized_keys",
        f"echo '{gh_pub}' >> /mnt/root/.ssh/authorized_keys" if gh_pub else "echo 'Sem chave GH'",
        "chmod 700 /mnt/root/.ssh",
        "chmod 600 /mnt/root/.ssh/authorized_keys",
        
        # Desmontar
        "umount /mnt/sys",
        "umount /mnt/proc",
        "umount /mnt/dev",
        "umount /mnt"
    ]
    
    for cmd in commands:
        print(f"Executando: {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        if out: print(f"  Saida: {out}")
        if err: print(f"  Erro: {err}")
    
    print("Reiniciando o servidor para voltar ao modo normal...")
    try:
        client.exec_command("reboot")
    except Exception as e:
        pass
        
    client.close()
    print("Cirurgia ULTIMATE concluída com sucesso!")

if __name__ == "__main__":
    fix_server_ultimate()
