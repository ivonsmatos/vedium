import paramiko
import os

def test_key():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key_path = os.path.expanduser("~/.ssh/id_ed25519")
    try:
        client.connect('45.151.122.234', username='root', key_filename=key_path, timeout=10)
        print("LOGIN COM CHAVE FUNCIONOU PERFEITAMENTE!")
        
        # Testar se podemos injetar a do github
        gh_key_path = os.path.expanduser("~/.ssh/github_actions_deploy_key.pub")
        if os.path.exists(gh_key_path):
            with open(gh_key_path, "r") as f:
                gh_pub = f.read().strip()
            client.exec_command(f"echo '{gh_pub}' >> ~/.ssh/authorized_keys")
            print("Chave do github injetada tb!")
            
    except Exception as e:
        print("LOGIN COM CHAVE FALHOU:", str(e))
    finally:
        client.close()

if __name__ == "__main__":
    test_key()
