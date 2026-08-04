import paramiko
import sys
import time

def execute_remote_commands():
    host = "45.151.122.234"
    username = "root"
    password = "Protonsysdba@1986"

    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=username, password=password, timeout=10)
        print("Connected successfully.\n")
        
        cmd = "cd /opt/vedium && docker exec -u root vedium-frappe chown -R frappe:frappe /home/frappe/frappe-bench/apps/vedium_core && docker exec -w /home/frappe/frappe-bench vedium-frappe bench --site app.vediums.com migrate"
        print(f"> {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Print output in real-time
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
            if stderr.channel.recv_stderr_ready():
                print(stderr.channel.recv_stderr(1024).decode('utf-8', errors='replace'), end='')
            time.sleep(0.1)
            
        # Print any remaining
        print(stdout.read().decode('utf-8', errors='replace'), end='')
        print(stderr.read().decode('utf-8', errors='replace'), end='')
        
        exit_status = stdout.channel.recv_exit_status()
        print(f"\n[Exit Status: {exit_status}]\n")
            
    except Exception as e:
        print(f"Connection failed: {str(e)}")
    finally:
        ssh.close()

if __name__ == "__main__":
    execute_remote_commands()
