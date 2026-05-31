from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum, avg, round, unix_timestamp,
    count, max, min, hour, when
)

spark = SparkSession.builder \
    .appName("TransporteUrbano") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("=" * 60)
print("  GRUPO 2 - ANALITICA DE TRANSPORTE URBANO")
print("  Apache Spark + PySpark + Parquet")
print("=" * 60)

print("\n[1] Leyendo datos de viajes...")
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("data/trips.csv")
print(f"    Total leidos: {df.count()}")
df.show(5)

print("\n[2] Limpiando datos invalidos...")
df_clean = df \
    .filter(col("distance_km") > 0) \
    .filter(col("route_id").isNotNull()) \
    .filter(col("route_id") != "") \
    .filter(col("passengers") > 0)
eliminados = df.count() - df_clean.count()
print(f"    Eliminados: {eliminados}")
print(f"    Limpios:    {df_clean.count()}")

print("\n[3] Calculando metricas...")
df_enriched = df_clean \
    .withColumn("duration_minutes",
        round((unix_timestamp(col("end_time")) -
               unix_timestamp(col("start_time"))) / 60, 2)) \
    .withColumn("hora_inicio", hour(col("start_time"))) \
    .withColumn("hora_pico",
        when((col("hora_inicio") >= 7) & (col("hora_inicio") <= 9), "manana")
        .when((col("hora_inicio") >= 17) & (col("hora_inicio") <= 19), "tarde")
        .when((col("hora_inicio") >= 12) & (col("hora_inicio") <= 14), "mediodia")
        .otherwise("normal"))

print("\n[4] Pasajeros por ruta...")
passengers_by_route = df_enriched \
    .groupBy("city", "route_id", "vehicle_type") \
    .agg(
        sum("passengers").alias("total_passengers"),
        count("trip_id").alias("total_trips"),
        round(avg("passengers"), 1).alias("avg_passengers_trip"),
        round(avg("duration_minutes"), 2).alias("avg_duration_min")
    ) \
    .orderBy("total_passengers", ascending=False)
passengers_by_route.show(15)

print("\n[5] Duracion promedio por ciudad...")
avg_by_city = df_enriched \
    .groupBy("city") \
    .agg(
        round(avg("duration_minutes"), 2).alias("avg_duration_min"),
        sum("passengers").alias("total_passengers"),
        count("trip_id").alias("total_trips"),
        round(avg("distance_km"), 2).alias("avg_distance_km")
    ) \
    .orderBy("total_passengers", ascending=False)
avg_by_city.show()

print("\n[6] Analisis por hora pico...")
peak_analysis = df_enriched \
    .groupBy("hora_pico") \
    .agg(
        count("trip_id").alias("total_trips"),
        round(avg("passengers"), 1).alias("avg_passengers"),
        sum("passengers").alias("total_passengers")
    ) \
    .orderBy("total_passengers", ascending=False)
peak_analysis.show()

print("\n[7] Escribiendo Parquet...")
passengers_by_route.write.mode("overwrite").partitionBy("city").parquet("output/passengers_by_route")
avg_by_city.write.mode("overwrite").parquet("output/avg_duration_by_city")
peak_analysis.write.mode("overwrite").parquet("output/peak_hour_analysis")
print("    Parquet escrito en output/")

print("\n" + "=" * 60)
print("  RESULTADO FINAL")
print("=" * 60)
passengers_by_route.select("city","route_id","total_passengers","avg_duration_min").show(10)
avg_by_city.show()
print("\nJob completado exitosamente!")
spark.stop()
