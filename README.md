# Grupo 2: Proyecto Spark — Analítica de Transporte Urbano

Este repositorio contiene un proyecto local de ingeniería de datos para
enseñar **Apache Spark, PySpark y Parquet** usando un caso real: el análisis
de viajes de transporte urbano en múltiples ciudades del Perú.

## Descripción del Proyecto

Un departamento de transporte público recibe registros de viajes de taxi y bus
de cinco ciudades. El equipo necesita procesar esos datos para generar métricas
analíticas que ayuden a los planificadores de transporte.

El pipeline completo corre con **Docker y Docker Compose** — no requiere
instalar Spark ni Java en la máquina local.

## Tecnologías

| Tecnología | Versión | Rol |
|---|---|---|
| Apache Spark | 3.5.5 | Motor de procesamiento distribuido |
| PySpark | 3.5.5 | API Python para Spark |
| Parquet | — | Formato de salida columnar |
| Docker | 24+ | Contenedor del cluster |
| Python | 3.x | Generador de datos y script ETL |

## Arquitectura

```
┌─────────────────────────── Docker Cluster ──────────────────────────────┐
│                                                                          │
│  📁 CSV de viajes                                                        │
│  trips.csv ──────────────→ ⚡ Spark Master                              │
│                                   ↓ distribuye particiones               │
│                    ┌──────────────┴──────────────┐                      │
│              Worker 1                       Worker 2                     │
│           (partición 1)                 (partición 2)                   │
│                    └──────────────┬──────────────┘                      │
│                                   ↓                                      │
│                         🧹 Limpieza de datos                            │
│                    (elimina registros inválidos)                         │
│                                   ↓                                      │
│                         🔢 PySpark SQL                                  │
│                    (agrega métricas por ruta y ciudad)                  │
│                                   ↓                                      │
│                    📦 Parquet particionado por ciudad                   │
│                    output/passengers_by_route/                           │
│                    output/avg_duration_by_city/                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Estructura de Carpetas

```
grupo2_spark/
├── data/
│   ├── generate_trips.py    # Generador de datos aleatorios
│   └── trips.csv            # Datos generados (1000 viajes)
├── src/
│   └── transport_analytics.py  # Job PySpark principal
├── output/                  # Resultado Parquet (generado al correr)
│   ├── passengers_by_route/ # Particionado por ciudad
│   └── avg_duration_by_city/
└── docker-compose.yml       # Cluster Spark
```

## Formato de los Datos

Cada registro de viaje tiene este formato:

```text
trip_id,city,route_id,start_time,end_time,passengers,distance_km
1,Lima,R101,2026-05-29T18:39:00Z,2026-05-29T19:16:00Z,20,11.4
2,Lima,R102,2026-05-29T17:54:00Z,2026-05-29T18:41:00Z,26,8.2
3,Cusco,R201,2026-05-29T09:00:00Z,2026-05-29T09:45:00Z,45,15.3
```

## Ciudades y Rutas

| Ciudad | Rutas |
|---|---|
| Lima | R101, R102, R103, R104 |
| Arequipa | R301, R302, R303 |
| Cusco | R201, R202, R203 |
| Trujillo | R401, R402 |
| Chiclayo | R501, R502 |

## Requisitos

- Docker y Docker Compose instalados
- Python 3 instalado (solo para generar datos)
- Al menos 4 GB de RAM disponibles para Docker

## Instrucciones de Ejecución

### Paso 1 — Generar datos de viajes

```bash
cd data
python3 generate_trips.py
```

Salida esperada:

```text
✅ Generados 1000 viajes en trips.csv
   Arequipa     → 198 viajes
   Chiclayo     → 201 viajes
   Cusco        → 195 viajes
   Lima         → 208 viajes
   Trujillo     → 198 viajes
```

### Paso 2 — Levantar el cluster Spark

```bash
cd ..
docker compose up spark-master spark-worker -d
```

Verifica que estén corriendo:

```bash
docker ps
```

Debes ver `grupo2-spark-master` y `grupo2-spark-worker`.

Puedes ver la UI del Spark Master en:
```
http://localhost:8080
```

### Paso 3 — Ejecutar el job PySpark

```bash
docker compose up spark-job
```

### Paso 4 — Verificar resultados

```bash
ls output/passengers_by_route/
ls output/avg_duration_by_city/
```

## Resultados Obtenidos

### Pasajeros totales por ruta:

```
+--------+--------+----------------+-----------+
|    city|route_id|total_passengers|total_trips|
+--------+--------+----------------+-----------+
|Trujillo|    R402|            4216|        117|
|Chiclayo|    R502|            3344|        102|
|Trujillo|    R401|            3164|         94|
|Chiclayo|    R501|            2967|         81|
|   Cusco|    R203|            2301|         62|
|   Cusco|    R202|            2152|         60|
|Arequipa|    R302|            2113|         61|
|   Cusco|    R201|            2071|         58|
|Arequipa|    R301|            1822|         56|
|Arequipa|    R303|            1776|         58|
|    Lima|    R103|            1772|         54|
|    Lima|    R104|            1756|         50|
|    Lima|    R102|            1734|         51|
|    Lima|    R101|            1481|         47|
+--------+--------+----------------+-----------+
```

### Duración promedio por ciudad:

```
+--------+--------------------+----------------+
|    city|avg_duration_minutes|total_passengers|
+--------+--------------------+----------------+
|Chiclayo|               48.39|            6311|
|    Lima|               48.23|            6743|
|Trujillo|               47.93|            7380|
|Arequipa|               47.53|            5711|
|   Cusco|               47.06|            6524|
+--------+--------------------+----------------+
```

### Limpieza de datos:

```
Registros leídos:     1,000
Registros eliminados:    49  (distancia ≤ 0, pasajeros ≤ 0, ruta vacía)
Registros limpios:      951
```

## Salida Parquet Particionada

```
output/passengers_by_route/
├── city=Arequipa/
│   └── part-00000-*.snappy.parquet
├── city=Chiclayo/
│   └── part-00000-*.snappy.parquet
├── city=Cusco/
│   └── part-00000-*.snappy.parquet
├── city=Lima/
│   └── part-00000-*.snappy.parquet
└── city=Trujillo/
    └── part-00000-*.snappy.parquet
```

## Lo que hace el Job PySpark

| Paso | Operación | Descripción |
|---|---|---|
| 1 | `spark.read.csv()` | Lee el archivo CSV de viajes |
| 2 | `.filter()` | Elimina registros inválidos |
| 3 | `.withColumn()` | Calcula duración en minutos |
| 4 | `.groupBy().agg()` | Suma pasajeros por ruta |
| 5 | `.groupBy().agg()` | Promedia duración por ciudad |
| 6 | `.write.parquet()` | Escribe resultado particionado |

## Limpieza

Para detener el cluster:

```bash
docker compose down
```

Para borrar los resultados y empezar de cero:

```bash
rm -rf output/
```

## Preguntas de Discusión

### ¿Cuál es la diferencia entre Spark Driver y Spark Workers?

El Driver coordina la aplicación — crea el SparkSession, define el plan de
ejecución (DAG) y asigna tareas. Los Workers (Executors) reciben esas tareas
y las ejecutan en paralelo sobre sus particiones de datos. El Driver tiene
visibilidad global del job; cada Worker solo conoce su partición.

### ¿Por qué Parquet es útil para analítica?

Parquet almacena datos por columnas en vez de por filas. Para consultas como
`SUM(passengers)` solo lee la columna `passengers` — ignora todas las demás.
Además incluye compresión automática (Snappy) que reduce el tamaño hasta 10x
comparado con CSV, y guarda el esquema para evitar inferencia.

### ¿En qué se diferencia Spark de Hadoop MapReduce?

La diferencia fundamental es dónde se procesan los datos. Hadoop escribe en
disco después de cada fase Map y Reduce — eso genera latencia alta. Spark
procesa todo en memoria RAM y solo escribe al disco al final, siendo 100x más
rápido para algoritmos iterativos. Además Spark tiene SQL nativo, ML integrado
y streaming — Hadoop solo tiene MapReduce básico.

### ¿Qué es una partición en Spark?

Una partición es una porción del dataset que se procesa en un solo Executor.
Si tienes 1000 viajes y 2 Executors — Spark crea particiones y las procesa en
paralelo. El número óptimo de particiones es 2x el número de cores del cluster.
