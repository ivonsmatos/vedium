import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)

cmd = "docker exec -u frappe -w /home/frappe/frappe-bench vedium-frappe bench --site app.vediums.com execute vedium_core.health.run"
print("Executing:", cmd)

stdin, stdout, stderr = ssh.exec_command(cmd)
print("STDOUT:")
print(stdout.read().decode())
print("STDERR:")
print(stderr.read().decode())

ssh.close()
