import paramiko

def check():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)
        print("CONECTADO COM SENHA!")
        stdin, stdout, stderr = client.exec_command("docker ps")
        print("DOCKER PS:")
        print(stdout.read().decode())
        
        # Testar exatamente o comando do GitHub Actions:
        stdin, stdout, stderr = client.exec_command("docker exec -i -w /home/frappe/frappe-bench vedium-frappe bench --site app.vediums.com set-config STRIPE_SECRET_KEY test_key")
        print("BENCH SET CONFIG:")
        print("SAIDA:", stdout.read().decode())
        print("ERRO:", stderr.read().decode())
        
    except Exception as e:
        print("FALHA GERAL:", str(e))
        
if __name__ == "__main__":
    check()
