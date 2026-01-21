import re
import csv
from collections import Counter

RUTA_LOG = "log.txt"
SALIDA = "reporte.csv"

# 1) Regex para IPs (igual que antes)
regex_ip = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

# 2) Mapa: keyword -> tipo (tú defines las categorías)
#    Puedes agregar más keywords o cambiar los tipos.
keyword_a_tipo = {
    "warning": "WARNING",
    "failed": "FAILED",
    "error": "ERROR",
    "denied": "DENIED"
}

# Contadores
conteo_ips = Counter()

# Guardamos conteos por (tipo, keyword)
conteo_kw = Counter()

with open(RUTA_LOG, "r", encoding="utf-8", errors="ignore") as f:
    for linea in f:
        lower = linea.lower()

        # IPs
        for ip in regex_ip.findall(linea):
            conteo_ips[ip] += 1

        # Keywords
        for kw, tipo in keyword_a_tipo.items():
            if kw in lower:
                # Contamos por dupla (tipo, keyword)
                conteo_kw[(tipo, kw)] += 1

# Guardar CSV
with open(SALIDA, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["categoria", "tipo", "keyword", "valor", "conteo"])

    # Sección: keywords (con tipo)
    for (tipo, kw), c in conteo_kw.most_common():
        writer.writerow(["keyword", tipo, kw, "", c])

    # Sección: IPs
    for ip, c in conteo_ips.most_common(20):
        writer.writerow(["ip", "", "", ip, c])

print("Listo. Reporte generado:", SALIDA)
