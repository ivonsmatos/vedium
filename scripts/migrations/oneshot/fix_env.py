#!/usr/bin/env python3
"""Fix env vars para workers: adicionar FRAPPE_REDIS_QUEUE, FRAPPE_REDIS_CACHE, FRAPPE_DB_HOST."""

worker_services = {
    "vedium-worker-default",
    "vedium-worker-short",
    "vedium-worker-long",
    "vedium-scheduler",
}

with open("/opt/vedium/docker-compose.yml", "r") as f:
    lines = f.readlines()

result = []
current_service = None
in_env_block = False
inserted = {
    "vedium-worker-default": False,
    "vedium-worker-short": False,
    "vedium-worker-long": False,
    "vedium-scheduler": False,
}

for i, line in enumerate(lines):
    stripped = line.rstrip()

    # Detect service name
    if (
        stripped.startswith("  ")
        and not stripped.startswith("   ")
        and stripped.endswith(":")
    ):
        svc = stripped.strip().rstrip(":")
        current_service = svc
        in_env_block = False

    if current_service in worker_services:
        # Detect environment block
        if stripped == "    environment:":
            in_env_block = True
            result.append(line)
            continue
        if in_env_block:
            # After SITES_PATH line, add FRAPPE_ vars if not already there
            if "SITES_PATH:" in stripped and not inserted[current_service]:
                result.append(line)
                result.append(
                    "      FRAPPE_REDIS_QUEUE: redis://vedium-redis-queue:6379\n"
                )
                result.append(
                    "      FRAPPE_REDIS_CACHE: redis://vedium-redis-cache:6379\n"
                )
                result.append("      FRAPPE_DB_HOST: vedium-mariadb\n")
                inserted[current_service] = True
                continue
            if stripped and not stripped.startswith("      "):
                in_env_block = False

    result.append(line)

with open("/opt/vedium/docker-compose.yml", "w") as f:
    f.writelines(result)

print("Done! Inserted FRAPPE_REDIS_QUEUE/CACHE for:", list(inserted.keys()))
