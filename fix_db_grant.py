import subprocess

ROOT_PWD = "-8pUonusFq4EicBfcfOGBTtk@OobpR8R"
VEDIUM_PWD = "0Yuyzit1@3QWtKiy0%Gngs=c+HY=Igor"

# Fix: grant vedium@'%' access
sql = """
SELECT User, Host FROM mysql.user WHERE User='vedium';
GRANT ALL PRIVILEGES ON `vedium`.* TO 'vedium'@'%' IDENTIFIED BY '0Yuyzit1@3QWtKiy0%Gngs=c+HY=Igor';
FLUSH PRIVILEGES;
SELECT User, Host FROM mysql.user WHERE User='vedium';
"""

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
        sql,
    ],
    capture_output=True,
    text=True,
)
print("FIX GRANT:")
print("STDOUT:", r.stdout)
print("STDERR:", r.stderr)

# Verify
r2 = subprocess.run(
    [
        "docker",
        "exec",
        "vedium-mariadb",
        "mysql",
        "-u",
        "vedium",
        f"--password={VEDIUM_PWD}",
        "-h",
        "127.0.0.1",  # Use TCP instead of socket
        "vedium",
        "-e",
        "SELECT 'DB_OK' AS status; SHOW TABLES LIMIT 3;",
    ],
    capture_output=True,
    text=True,
)
print("\nVERIFY vedium@% ACCESS:")
print("STDOUT:", r2.stdout)
print("STDERR:", r2.stderr)
