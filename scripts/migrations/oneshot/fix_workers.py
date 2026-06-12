#!/usr/bin/env python3
"""Fix worker/scheduler services to use volumes_from vedium-frappe."""

import re

with open("/opt/vedium/docker-compose.yml", "r") as f:
    content = f.read()

# For each worker/scheduler section, replace the volumes line with volumes_from
# We need to add: volumes_from: [vedium-frappe] and remove: volumes: - frappe-bench-data:/home/frappe/frappe-bench

services = [
    "vedium-worker-default",
    "vedium-worker-short",
    "vedium-worker-long",
    "vedium-scheduler",
]
vol_line = "      - frappe-bench-data:/home/frappe/frappe-bench"

for svc in services:
    # Find the service block
    pattern = f"(  {svc}:.*?)(?=  [a-z]{{2,}}[^-]|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        block = match.group(0)
        new_block = block
        # Replace volumes section
        new_block = new_block.replace(
            "    volumes:\n" + vol_line + "\n",
            "    volumes_from:\n      - service:vedium-frappe\n",
        )
        content = content.replace(block, new_block)
        print(f"Updated {svc}")
    else:
        print(f"NOT FOUND: {svc}")

with open("/opt/vedium/docker-compose.yml", "w") as f:
    f.write(content)

print("Done!")
