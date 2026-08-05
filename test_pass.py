import paramiko

def test():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)
        print("LOGIN COM SENHA FUNCIONOU!")
    except Exception as e:
        print("LOGIN COM SENHA FALHOU:", str(e))

if __name__ == "__main__":
    test()
