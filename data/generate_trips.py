import random
import csv
from datetime import datetime, timedelta
from collections import Counter

random.seed(42)
TOTAL_VIAJES = 10000

ciudades = {
    "Lima":      {"rutas": ["R101","R102","R103","R104","R105"], "sesgo": 0.55},
    "Arequipa":  {"rutas": ["R301","R302","R303"],               "sesgo": 0.48},
    "Cusco":     {"rutas": ["R201","R202","R203"],               "sesgo": 0.52},
    "Trujillo":  {"rutas": ["R401","R402","R403"],               "sesgo": 0.50},
    "Chiclayo":  {"rutas": ["R501","R502"],                      "sesgo": 0.47},
    "Piura":     {"rutas": ["R601","R602"],                      "sesgo": 0.53},
    "Puno":      {"rutas": ["R701","R702"],                      "sesgo": 0.49},
    "Ica":       {"rutas": ["R801","R802"],                      "sesgo": 0.51},
}

distancias = {
    "R101":11.4,"R102":8.2,"R103":15.3,"R104":6.8,"R105":12.1,
    "R301":12.1,"R302":14.2,"R303":9.5,
    "R201":15.3,"R202":10.5,"R203":18.2,
    "R401":11.0,"R402":8.7,"R403":13.5,
    "R501":9.3, "R502":12.8,
    "R601":10.2,"R602":7.8,
    "R701":16.4,"R702":12.9,
    "R801":8.5, "R802":11.3,
}

tipos_vehiculo = {
    "R101":"Bus","R102":"Combi","R103":"Bus","R104":"Combi","R105":"Bus",
    "R301":"Bus","R302":"Bus","R303":"Combi",
    "R201":"Bus","R202":"Combi","R203":"Bus",
    "R401":"Bus","R402":"Combi","R403":"Bus",
    "R501":"Bus","R502":"Combi",
    "R601":"Bus","R602":"Combi",
    "R701":"Bus","R702":"Combi",
    "R801":"Combi","R802":"Bus",
}

capacidad_max = {"Bus": 80, "Combi": 25}

fecha_base = datetime(2026, 5, 29, 5, 0, 0)
filas = []

for trip_id in range(1, TOTAL_VIAJES + 1):
    ciudad = random.choice(list(ciudades.keys()))
    config = ciudades[ciudad]
    route_id = random.choice(config["rutas"])
    distancia = distancias[route_id]
    vehiculo = tipos_vehiculo[route_id]
    cap_max = capacidad_max[vehiculo]

    minutos_inicio = random.randint(0, 17 * 60)
    start_time = fecha_base + timedelta(minutes=minutos_inicio)

    hora = start_time.hour
    if 7 <= hora <= 9 or 17 <= hora <= 19:
        pasajeros_base = int(cap_max * random.uniform(0.7, 1.0))
        duracion = random.randint(35, 90)
    elif 12 <= hora <= 14:
        pasajeros_base = int(cap_max * random.uniform(0.5, 0.8))
        duracion = random.randint(25, 70)
    else:
        pasajeros_base = int(cap_max * random.uniform(0.2, 0.6))
        duracion = random.randint(20, 60)

    end_time = start_time + timedelta(minutes=duracion)
    passengers = max(1, pasajeros_base + random.randint(-5, 5))

    if random.random() < 0.04:
        tipo_error = random.randint(1, 3)
        if tipo_error == 1:
            distancia = round(random.uniform(-5, 0), 1)
        elif tipo_error == 2:
            passengers = random.randint(-10, 0)
        else:
            route_id = ""
            vehiculo = ""

    filas.append({
        "trip_id":      trip_id,
        "city":         ciudad,
        "route_id":     route_id,
        "vehicle_type": vehiculo,
        "start_time":   start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time":     end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "passengers":   passengers,
        "distance_km":  distancia,
    })

campos = ["trip_id","city","route_id","vehicle_type",
          "start_time","end_time","passengers","distance_km"]

with open("trips.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(filas)

invalidos = sum(1 for f in filas if f["distance_km"] <= 0 or f["passengers"] <= 0 or f["route_id"] == "")
print(f"Generados {TOTAL_VIAJES:,} viajes en trips.csv")
print(f"Ciudades: {len(ciudades)}")
print(f"Registros invalidos: {invalidos} ({invalidos/TOTAL_VIAJES*100:.1f}%)")
print()
print("Viajes por ciudad:")
for ciudad, total in sorted(Counter(f["city"] for f in filas).items()):
    print(f"  {ciudad:12} -> {total:,} viajes")
