import paramiko
import os
import glob

ssh_dir = os.path.expanduser("~/.ssh")
host = "45.151.122.234"
username = "frappe"

keys = glob.glob(os.path.join(ssh_dir, "*"))

valid_keys = []

for key_path in keys:
    if key_path.endswith(".pub") or key_path.endswith("known_hosts") or key_path.endswith("config") or key_path.endswith("old"):
        continue
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        try:
            private_key = paramiko.Ed25519Key.from_private_key_file(key_path)
        except paramiko.ssh_exception.SSHException:
            try:
                private_key = paramiko.RSAKey.from_private_key_file(key_path)
            except Exception:
                continue 
        
        ssh.connect(host, username=username, pkey=private_key, timeout=5)
        print(f"✅ SUCESSO: A chave {os.path.basename(key_path)} está autorizada no servidor para o usuário FRAPPE!")
        valid_keys.append(key_path)
        ssh.close()
    except Exception as e:
        pass

if not valid_keys:
    print("❌ Nenhuma chave funcionou para o usuário frappe também.")
