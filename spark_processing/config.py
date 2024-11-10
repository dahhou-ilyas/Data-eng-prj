from pyspark.sql import SparkSession
import os

# Configuration de Spark avec les paramètres de sécurité
spark = SparkSession.builder \
    .master("spark://localhost:7077") \
    .appName("Ecome process") \
    .config("spark.driver.host", "localhost") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-common:3.3.1") \
    .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
    .config("spark.executor.extraJavaOptions", "-Djava.security.manager=allow") \
    .config("spark.cores.max", "2") \
    .config("spark.executor.memory", "2g") \
    .config("spark.executor.cores", "2") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Configuration du niveau de log
spark.sparkContext.setLogLevel("WARN")

# Votre code
data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
columns = ["Name", "Value"]
df = spark.createDataFrame(data, columns)
df.show()

# Fermer la session Spark
spark.stop()