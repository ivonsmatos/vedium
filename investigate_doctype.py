import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)

print("=== Command 1 ===")
cmd1 = "docker exec vedium-frappe bash -c \"cat /home/frappe/frappe-bench/sites/apps.txt; echo '--- DOCTYPE NO CONTAINER ---'; ls /home/frappe/frappe-bench/apps/vedium_core/vedium_core/doctype/ | grep -i price\""
stdin, stdout, stderr = ssh.exec_command(cmd1)
print(stdout.read().decode())
print(stderr.read().decode())

print("=== Command 2 ===")
cmd2 = "docker exec -w /home/frappe/frappe-bench vedium-frappe bench --site app.vediums.com migrate 2>&1 | tail -30"
stdin, stdout, stderr = ssh.exec_command(cmd2)
print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
