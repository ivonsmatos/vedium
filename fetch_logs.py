import urllib.request
import json

job_id = "92160516898"
try:
    req = urllib.request.Request(
        f"https://api.github.com/repos/ivonsmatos/vedium/actions/jobs/{job_id}/logs",
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    with urllib.request.urlopen(req) as response:
        logs = response.read().decode('utf-8')
        lines = logs.split('\n')
        for line in lines[-200:]: # last 200 lines
            print(line)
except Exception as e:
    print("Error:", str(e))
