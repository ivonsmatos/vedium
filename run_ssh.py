import paramiko
import sys
import time

def execute_remote_commands():
    host = "45.151.122.234"
    username = "root"
    password = "Protonsysdba@1986"

    commands = [
        "cd /root/vedium || cd /home/vedium/vedium || cd /var/www/vedium || echo 'Finding project dir...'",
        "cd $(find / -name docker-compose.yml -path '*/vedium/*' 2>/dev/null | head -n 1 | xargs dirname) && pwd",
        "docker compose exec vedium-frappe bench --site app.vediums.com backup --with-files",
        "docker compose exec vedium-frappe bench --site app.vediums.com migrate"
    ]

    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=username, password=password, timeout=10)
        print("Connected successfully.\n")
        
        # We need an interactive shell to chain cd and docker compose properly if they rely on aliases or paths, 
        # but paramiko exec_command is fine for absolute commands. Let's find the project directory first.
        
        print("Finding project directory...")
        stdin, stdout, stderr = ssh.exec_command("find / -maxdepth 4 -name deploy-vedium.sh -type f 2>/dev/null | head -n 1")
        deploy_script = stdout.read().decode().strip()
        
        if not deploy_script:
            print("Could not find deploy-vedium.sh. Attempting a guess at /root/vedium")
            proj_dir = "/root/vedium"
        else:
            import os
            proj_dir = os.path.dirname(deploy_script)
            
        print(f"Project directory is likely: {proj_dir}")

        commands_to_run = [
            f"cd {proj_dir} && git pull origin main",
            f"cd {proj_dir} && docker compose exec vedium-frappe bench --site app.vediums.com backup --with-files",
            f"cd {proj_dir} && docker compose exec vedium-frappe bench --site app.vediums.com migrate"
        ]
        
        for cmd in commands_to_run:
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
            if exit_status != 0:
                print("Stopping due to error.")
                break
                
    except Exception as e:
        print(f"Connection failed: {str(e)}")
    finally:
        ssh.close()

if __name__ == "__main__":
    execute_remote_commands()
