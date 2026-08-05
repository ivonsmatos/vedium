import paramiko
import time

def fix_server_v2():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("Conectando ao modo de resgate...")
    client.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)
    print("Conectado com sucesso!")
    
    commands = [
        "mount /dev/sda1 /mnt",
        
        # 1. Injetar a chave SSH do Windows
        "mkdir -p /mnt/root/.ssh",
        'echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBE+SnTLkdybW3c803vzZT9aNjTOM1cz7nIg0fEekv5c actahub-local-dev" > /mnt/root/.ssh/authorized_keys',
        "chmod 700 /mnt/root/.ssh",
        "chmod 600 /mnt/root/.ssh/authorized_keys",
        
        # 2. Desabilitar a exclusao de chaves do cloud-init
        "if [ -f /mnt/etc/cloud/cloud.cfg ]; then sed -i 's/ - ssh/# - ssh/g' /mnt/etc/cloud/cloud.cfg; fi",
        
        # 3. Forcar aceitacao de root e senhas nos drop-ins do Ubuntu
        "echo 'PermitRootLogin yes' > /mnt/etc/ssh/sshd_config.d/99-force-root.conf",
        "echo 'PasswordAuthentication yes' >> /mnt/etc/ssh/sshd_config.d/99-force-root.conf",
        
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
    print("Cirurgia V2 concluída com sucesso! O cloud-init foi neutralizado.")

if __name__ == "__main__":
    fix_server_v2()
