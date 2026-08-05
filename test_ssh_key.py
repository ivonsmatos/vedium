import paramiko
import os

key_path = os.path.expanduser("~/.ssh/id_ed25519")
host = "45.151.122.234"
username = "root"

print(f"Testando conexão SSH para {username}@{host} usando a chave {key_path}...")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Carrega a chave privada
    private_key = paramiko.Ed25519Key.from_private_key_file(key_path)
    
    # Tenta conectar
    ssh.connect(host, username=username, pkey=private_key, timeout=10)
    
    # Executa um comando simples para provar que conectou
    stdin, stdout, stderr = ssh.exec_command("echo '✅ Conexão SSH via Chave Pública realizada com sucesso!'")
    print(stdout.read().decode().strip())
    
except Exception as e:
    print(f"❌ Falha no teste: {str(e)}")
finally:
    ssh.close()
