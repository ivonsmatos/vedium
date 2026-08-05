import paramiko
import getpass
import os
import sys

pub_key_path = os.path.expanduser("~/.ssh/github_actions_deploy_key.pub")
if not os.path.exists(pub_key_path):
    print(f"Erro: Chave publica não encontrada em {pub_key_path}")
    sys.exit(1)

with open(pub_key_path, "r") as f:
    pub_key = f.read().strip()

host = "45.151.122.234"
username = "root"
password = getpass.getpass(f"Digite a senha do Root (Contabo) para {username}@{host}: ")

print("Conectando ao servidor...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=username, password=password)
    print("Conectado! Autorizando a chave SSH...")
    
    command = f"mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '{pub_key}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
    stdin, stdout, stderr = ssh.exec_command(command)
    
    err = stderr.read().decode()
    if err:
        print("Erro no servidor:", err)
    else:
        print("\n✅ SUCESSO! A chave pública foi configurada no servidor.")
        print("O GitHub Actions agora conseguirá acessar seu servidor com segurança.")
except Exception as e:
    print(f"\n❌ Falha na conexão: {str(e)}")
finally:
    ssh.close()
