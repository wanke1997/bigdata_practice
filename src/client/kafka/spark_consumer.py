from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.4.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 pyspark-shell'

appName = "Kafka Examples"
master = "spark://spark-master:7077"
kafka_servers = "kafka1:9091,kafka2:9092,kafka3:9093"
topic = "bigdata"

spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .getOrCreate()

sample_schema = (
    StructType()
    .add('rowkey', StringType())
    .add('time', StringType())
    .add('MAC', StringType())
    .add('PCM', StringType())
    .add('departAirport', StringType())
    .add('airline', StringType())
    .add('agent', StringType())
    .add('country', StringType())
    .add('request', StringType())
    .add('response', StringType())
    .add('error', StringType())
    .add('errorCode', StringType())
    .add('errorType', StringType())
    .add('success', StringType())
    .add('fail', StringType())
)

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_servers) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

print('################################################################')
count_df = df.selectExpr("topic").agg(count("topic")).alias("count")
print(count_df.show())
# base_df = df.selectExpr("CAST(value AS STRING)")
# info_dataframe = base_df.select(
#         from_json(col("value"), sample_schema).alias("sample"))
# info_df_fin = info_dataframe.select("sample.*")
# info_df_fin.writeStream.format("console").start().awaitTermination()
# print(len(info_df_fin.collect()))
# info_df_fin.show()
# query = info_df_fin.select('rowkey')
# print(query)
# print(sample_schema)
# print(query)
# query.collect()
print('################################################################')
