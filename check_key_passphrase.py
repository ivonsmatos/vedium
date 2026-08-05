import paramiko
import os

key_path = os.path.expanduser("~/.ssh/id_ed25519")
try:
    private_key = paramiko.Ed25519Key.from_private_key_file(key_path)
    print("A chave id_ed25519 NÃO tem senha (passphrase).")
except paramiko.ssh_exception.PasswordRequiredException:
    print("A chave id_ed25519 TEM senha (passphrase)!")
except Exception as e:
    print(f"Erro ao ler a chave: {e}")
