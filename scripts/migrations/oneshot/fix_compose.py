with open("/opt/vedium/docker-compose.yml", "r") as f:
    content = f.read()

# 1. Add vedium-sites to vedium-frappe volumes
old1 = """    volumes:
      - frappe-bench-data:/home/frappe/frappe-bench
    networks:
      - vedium-network
    depends_on:
      - vedium-mariadb
      - vedium-redis-cache
      - vedium-redis-queue
      - vedium-redis-socketio"""
new1 = """    volumes:
      - frappe-bench-data:/home/frappe/frappe-bench
      - vedium-sites:/home/frappe/frappe-bench/sites
    networks:
      - vedium-network
    depends_on:
      - vedium-mariadb
      - vedium-redis-cache
      - vedium-redis-queue
      - vedium-redis-socketio"""
n = content.count(old1)
content = content.replace(old1, new1, 1)
print(f"[1] Added vedium-sites to frappe volumes ({n} matches replaced)")

# 2. Replace volumes_from in workers with explicit volumes
old2 = """    volumes_from:
      - vedium-frappe
    networks:"""
new2 = """    volumes:
      - frappe-bench-data:/home/frappe/frappe-bench
      - vedium-sites:/home/frappe/frappe-bench/sites
    networks:"""
n2 = content.count(old2)
content = content.replace(old2, new2)
print(f"[2] Replaced volumes_from in {n2} workers")

# 3. Declare vedium-sites in top-level volumes
old3 = "volumes:\n  frappe-bench-data:"
new3 = "volumes:\n  frappe-bench-data:\n  vedium-sites:"
n3 = content.count(old3)
content = content.replace(old3, new3)
print(f"[3] Added vedium-sites declaration ({n3} matches)")

with open("/opt/vedium/docker-compose.yml", "w") as f:
    f.write(content)

print("\nDONE! Lines with vedium-sites or volumes_from:")
with open("/opt/vedium/docker-compose.yml") as f:
    for i, line in enumerate(f, 1):
        if "vedium-sites" in line or "volumes_from" in line:
            print(f"  {i}: {line.rstrip()}")
