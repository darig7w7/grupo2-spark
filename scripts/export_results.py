from pyspark.sql import SparkSession
import os

spark = SparkSession.builder \
    .appName("ExportResultados") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

os.makedirs("results", exist_ok=True)

print("[1] Exportando pasajeros por ruta...")
df1 = spark.read.parquet("output/passengers_by_route")
df1.orderBy("total_passengers", ascending=False) \
   .toPandas() \
   .to_csv("results/passengers_by_route.csv", index=False)
print(f"    Guardado: results/passengers_by_route.csv ({df1.count()} filas)")

print("[2] Exportando duracion por ciudad...")
df2 = spark.read.parquet("output/avg_duration_by_city")
df2.orderBy("total_passengers", ascending=False) \
   .toPandas() \
   .to_csv("results/avg_duration_by_city.csv", index=False)
print(f"    Guardado: results/avg_duration_by_city.csv ({df2.count()} filas)")

print("[3] Exportando analisis hora pico...")
df3 = spark.read.parquet("output/peak_hour_analysis")
df3.orderBy("total_passengers", ascending=False) \
   .toPandas() \
   .to_csv("results/peak_hour_analysis.csv", index=False)
print(f"    Guardado: results/peak_hour_analysis.csv ({df3.count()} filas)")

print("\nResultados exportados a results/")
spark.stop()
