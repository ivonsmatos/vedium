import urllib.request

r = urllib.request.urlopen("http://127.0.0.1:8002/courses")
data = r.read().decode("utf-8", errors="replace")
with open("/tmp/cr.html", "w") as f:
    f.write(data)
print("HTTP Status:", r.status)
print("Size:", len(data), "bytes")
# Checar cursos
import re

titles = re.findall(r"Inglês - [A-Za-záéíóúàâêôãõçÁÉÍÓÚÀÂÊÔÃÕÇ\(\)\-\+ ]+", data)
print("Cursos encontrados:", list(set(titles))[:10])
# Checar erros
if "Nenhum curso" in data:
    print("⚠ Mostrando: 'Nenhum curso disponível'")
if "courses-one__single" in data:
    count = data.count("courses-one__single")
    print(f"✅ Cards de curso encontrados: {count}")
if "500" in data[:200] or "Traceback" in data:
    print("❌ ERRO 500 na página")
