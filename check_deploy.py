import paramiko

def fetch():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)
    
    stdin, stdout, stderr = client.exec_command(
        'docker exec -i -w /home/frappe/frappe-bench/apps/vedium_core/vedium_core/vedium_core vedium-frappe cat catalog_sync.py'
    )
    print(stdout.read().decode())
        
fetch()
