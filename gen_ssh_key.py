import os
import subprocess

ssh_dir = os.path.expanduser("~/.ssh")
os.makedirs(ssh_dir, exist_ok=True)
key_path = os.path.join(ssh_dir, "github_actions_deploy_key")

if not os.path.exists(key_path):
    subprocess.run(["ssh-keygen", "-t", "ed25519", "-C", "github-actions-deploy", "-f", key_path, "-N", ""])
    print("Key generated.")
else:
    print("Key already exists.")
