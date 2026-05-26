with open("/opt/vedium/docker-compose.yml", "r") as f:
    content = f.read()

old = "      test: ['CMD', 'curl', '-f', 'http://localhost:8000/api/method/ping']"
new = "      test: ['CMD', 'curl', '-f', '-H', 'Host: app.vediums.com', 'http://localhost:8000/api/method/ping']"
count = content.count(old)
content = content.replace(old, new)

with open("/opt/vedium/docker-compose.yml", "w") as f:
    f.write(content)

print(f"Fixed {count} occurrence(s)")
# Verify
import subprocess

r = subprocess.run(
    ["docker", "compose", "-f", "/opt/vedium/docker-compose.yml", "config", "--quiet"],
    capture_output=True,
    text=True,
    cwd="/opt/vedium",
)
print("YAML valid:", r.returncode == 0, r.stderr[:100] if r.stderr else "")
