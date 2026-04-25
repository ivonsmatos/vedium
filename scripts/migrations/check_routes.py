import urllib.request

# Testar varias rotas
urls = [
    "http://127.0.0.1:8002/",
    "http://127.0.0.1:8002/about",
    "http://127.0.0.1:8002/courses",
    "http://127.0.0.1:8002/lms/courses",
]
for url in urls:
    try:
        r = urllib.request.urlopen(url, timeout=5)
        print(f"  {r.status} OK  -> {url}")
    except Exception as e:
        print(f"  ERR  -> {url} : {e}")
