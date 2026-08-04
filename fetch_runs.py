import urllib.request
import json
import sys

run_id = "30959649928"
try:
    req = urllib.request.Request(
        f"https://api.github.com/repos/ivonsmatos/vedium/actions/runs/{run_id}/jobs",
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        for job in data['jobs']:
            print(f"Job: {job['id']} - {job['name']} - {job['conclusion']}")
            if job['conclusion'] == 'failure':
                for step in job['steps']:
                    if step['conclusion'] == 'failure':
                        print(f"  Failed Step: {step['name']}")
except Exception as e:
    print("Error:", str(e))
