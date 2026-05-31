from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, round, unix_timestamp, count

spark = SparkSession.builder.appName("TransporteUrbano").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.option("header", "true").option("inferSchema", "true").csv("data/trips.csv")
print("Registros leidos:", df.count())
df.show(5)

df_clean = df.filter(col("distance_km") > 0).filter(col("route_id") != "").filter(col("passengers") > 0)
print("Eliminados:", df.count() - df_clean.count())
print("Limpios:", df_clean.count())

df_duration = df_clean.withColumn(
    "duration_minutes",
    round((unix_timestamp(col("end_time")) - unix_timestamp(col("start_time"))) / 60, 2)
)
df_duration.select("trip_id", "city", "route_id", "passengers", "duration_minutes").show(5)

passengers_by_route = df_duration.groupBy("city", "route_id").agg(
    sum("passengers").alias("total_passengers"),
    count("trip_id").alias("total_trips")
).orderBy("total_passengers", ascending=False)
passengers_by_route.show()

avg_duration = df_duration.groupBy("city").agg(
    round(avg("duration_minutes"), 2).alias("avg_duration_minutes"),
    sum("passengers").alias("total_passengers")
).orderBy("avg_duration_minutes", ascending=False)
avg_duration.show()

passengers_by_route.write.mode("overwrite").partitionBy("city").parquet("output/passengers_by_route")
avg_duration.write.mode("overwrite").parquet("output/avg_duration_by_city")

print("Job completado!")
spark.stop()
