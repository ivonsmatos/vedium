import paramiko
import sys

def run_audits():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('45.151.122.234', username='root', password='Protonsysdba@1986', timeout=10)
    
    scripts = [
        "seed_espanhol_basico_catalog",
        "seed_espanhol_intermediario_catalog",
        "seed_espanhol_avancado_catalog",
        "seed_ple_basico_catalog",
        "seed_ple_intermediario_catalog",
        "seed_ple_avancado_catalog",
        "seed_hebraico_a0_catalog",
        "seed_hebraico_moderno_a1_catalog",
        "seed_hebraico_moderno_a2_b1_catalog",
        "seed_hebraico_biblico_leitura_guiada_catalog",
        "seed_hebraico_particular_catalog"
    ]
    
    success = True
    
    for script in scripts:
        print(f"\n--- AUDITANDO {script} ---")
        stdin, stdout, stderr = client.exec_command(
            f'docker exec -i -w /home/frappe/frappe-bench vedium-frappe bench --site app.vediums.com execute vedium_core.scripts.migrations.oneshot.{script}.execute'
        )
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:")
        print(out)
        
        if err:
            print("STDERR:")
            print(err)
            success = False
            
    if success:
        print("\n\nAUDITORIA BEM SUCEDIDA EM TODOS OS 6 CURSOS.")
    else:
        print("\n\nAUDITORIA FINALIZADA COM ERROS.")
        
run_audits()
