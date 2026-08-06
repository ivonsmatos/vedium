import json
from vedium_core.catalog_registry import generate_config_for_course, CATALOG

def execute():
    configs = []
    for c in CATALOG.keys():
        if CATALOG[c].get("blocked_status"):
            continue
        configs.append(generate_config_for_course(c))
    
    with open("/workspace/config_dump.json", "w") as f:
        json.dump(configs, f)
    print("Done")
