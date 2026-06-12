import subprocess

NGINX_CONF = "/etc/nginx/sites-available/vediums.com"

with open(NGINX_CONF, "r") as f:
    content = f.read()

PWA_BLOCKS = """
    # PWA — Service Worker (deve ser servido na raiz para ter escopo total)
    location = /sw.js {
        proxy_pass http://127.0.0.1:8005/assets/vedium_core/js/sw.js;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        add_header Content-Type "application/javascript; charset=utf-8";
        add_header Service-Worker-Allowed "/";
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        expires 0;
    }

    # PWA — Web App Manifest
    location = /manifest.json {
        proxy_pass http://127.0.0.1:8005/assets/vedium_core/manifest.json;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        add_header Content-Type "application/manifest+json; charset=utf-8";
        add_header Cache-Control "no-cache";
    }

    location / {"""

# Insert PWA blocks before the generic proxy location
if "location = /sw.js" in content:
    print("PWA blocks already present — skipping")
else:
    content = content.replace("    location / {", PWA_BLOCKS, 1)
    with open(NGINX_CONF, "w") as f:
        f.write(content)
    print("PWA blocks inserted")

# Test nginx config
r = subprocess.run(["nginx", "-t"], capture_output=True, text=True)
print("nginx -t:", r.returncode, r.stderr.strip())

if r.returncode == 0:
    r2 = subprocess.run(
        ["systemctl", "reload", "nginx"], capture_output=True, text=True
    )
    print("nginx reload:", r2.returncode)
else:
    print("ERROR: nginx config invalid, NOT reloading")
