import paramiko

def fetch():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)
    
    stdin, stdout, stderr = client.exec_command(
        'docker exec -i -w /home/frappe/frappe-bench vedium-frappe bench --site app.vediums.com execute vedium_core.custom_setup.setup_custom_fields'
    )
    print("OUTPUT:", stdout.read().decode())
    print("ERR:", stderr.read().decode())
        
fetch()
