#!/usr/bin/env python3
"""Fix worker/scheduler volumes to use volumes_from."""

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
in_volumes_block = False
skip_next = False

for i, line in enumerate(lines):
    stripped = line.rstrip()

    # Detect service name (2-space indent, no leading dash)
    if (
        stripped.startswith("  ")
        and not stripped.startswith("   ")
        and stripped.endswith(":")
    ):
        svc = stripped.strip().rstrip(":")
        current_service = svc
        in_volumes_block = False

    # Track volumes block inside worker services
    if current_service in worker_services:
        if stripped == "    volumes:":
            # Replace with volumes_from
            result.append("    volumes_from:\n")
            result.append("      - service:vedium-frappe\n")
            in_volumes_block = True
            continue
        if in_volumes_block:
            if stripped.startswith("      - ") and "frappe-bench-data" in stripped:
                # Skip the old volume mount line
                continue
            else:
                in_volumes_block = False

    result.append(line)

with open("/opt/vedium/docker-compose.yml", "w") as f:
    f.writelines(result)

print("Done! Updated volumes for worker services.")
