import paramiko
import os
import sys

def fix_github_key():
    # Caminhos das chaves no computador do usuario
    private_key_path = os.path.expanduser("~/.ssh/id_ed25519")
    github_pub_key_path = os.path.expanduser("~/.ssh/github_actions_deploy_key.pub")
    
    if not os.path.exists(github_pub_key_path):
        print(f"Erro: Chave publica do github nao encontrada em {github_pub_key_path}")
        sys.exit(1)
        
    with open(github_pub_key_path, "r") as f:
        github_pub_key = f.read().strip()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("Conectando ao servidor com a chave do Windows (que injetamos no resgate)...")
    try:
        # Tenta conectar com a chave privada (sem senha!)
        client.connect('45.151.122.234', username='root', key_filename=private_key_path, timeout=10)
        print("Conectado com sucesso (sem precisar de senha)!")
        
        print("Injetando a chave do GitHub Actions no servidor...")
        command = f"echo '{github_pub_key}' >> ~/.ssh/authorized_keys"
        stdin, stdout, stderr = client.exec_command(command)
        
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("SUCESSO ABSOLUTO! A chave do GitHub foi injetada.")
        else:
            print("Erro ao injetar a chave:", stderr.read().decode())
            
    except Exception as e:
        print(f"Falha na conexao: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    fix_github_key()
