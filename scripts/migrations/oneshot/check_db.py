import subprocess

ROOT_PWD = "-8pUonusFq4EicBfcfOGBTtk@OobpR8R"
VEDIUM_PWD = "0Yuyzit1@3QWtKiy0%Gngs=c+HY=Igor"

# Test root access
r = subprocess.run(
    [
        "docker",
        "exec",
        "vedium-mariadb",
        "mysql",
        "-u",
        "root",
        f"--password={ROOT_PWD}",
        "-e",
        "SELECT User, Host FROM mysql.user WHERE User='vedium'; SHOW DATABASES;",
    ],
    capture_output=True,
    text=True,
)
print("ROOT ACCESS:")
print("STDOUT:", r.stdout)
print("STDERR:", r.stderr)

# Test vedium user access
r2 = subprocess.run(
    [
        "docker",
        "exec",
        "vedium-mariadb",
        "mysql",
        "-u",
        "vedium",
        f"--password={VEDIUM_PWD}",
        "vedium",
        "-e",
        "SELECT 'DB_OK' AS status;",
    ],
    capture_output=True,
    text=True,
)
print("\nVEDIUM USER ACCESS:")
print("STDOUT:", r2.stdout)
print("STDERR:", r2.stderr)
