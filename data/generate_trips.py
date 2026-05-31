import random
import csv
from datetime import datetime, timedelta

random.seed(42)
TOTAL_VIAJES = 1000

ciudades = {
    "Lima":     ["R101", "R102", "R103", "R104"],
    "Arequipa": ["R301", "R302", "R303"],
    "Cusco":    ["R201", "R202", "R203"],
    "Trujillo": ["R401", "R402"],
    "Chiclayo": ["R501", "R502"],
}

distancias = {
    "R101": 11.4, "R102": 8.2,  "R103": 15.3, "R104": 6.8,
    "R301": 12.1, "R302": 14.2, "R303": 9.5,
    "R201": 15.3, "R202": 10.5, "R203": 18.2,
    "R401": 11.0, "R402": 8.7,
    "R501": 9.3,  "R502": 12.8,
}

fecha_base = datetime(2026, 5, 29, 6, 0, 0)
filas = []

for trip_id in range(1, TOTAL_VIAJES + 1):
    ciudad = random.choice(list(ciudades.keys()))
    route_id = random.choice(ciudades[ciudad])
    distancia = distancias[route_id]
    minutos_inicio = random.randint(0, 14 * 60)
    start_time = fecha_base + timedelta(minutes=minutos_inicio)
    duracion = random.randint(20, 75)
    end_time = start_time + timedelta(minutes=duracion)
    passengers = random.randint(5, 60)

    if random.random() < 0.05:
        tipo_error = random.randint(1, 3)
        if tipo_error == 1:
            distancia = -1.0
        elif tipo_error == 2:
            passengers = -5
        else:
            route_id = ""

    filas.append({
        "trip_id": trip_id,
        "city": ciudad,
        "route_id": route_id,
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "passengers": passengers,
        "distance_km": distancia,
    })

campos = ["trip_id","city","route_id","start_time","end_time","passengers","distance_km"]
with open("trips.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(filas)

print(f"✅ Generados {TOTAL_VIAJES} viajes en trips.csv")
from collections import Counter
for ciudad, total in sorted(Counter(f["city"] for f in filas).items()):
    print(f"   {ciudad:12} → {total} viajes")
