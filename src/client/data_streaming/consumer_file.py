from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark import SparkConf
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.4.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 pyspark-shell'

appName = "Kafka-Spark File Writer"
master = "spark://spark-master:7077"
kafka_servers = "kafka1:9091,kafka2:9092,kafka3:9093"
topic = "bigdata"
file_name = "/data/consumer_file_output.txt"

spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .config("spark.executor.memory", "7g") \
    .getOrCreate()

sample_schema = (
    StructType()
    .add('key', StringType())
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

class FileWriter:
    file = None
    def open(self, partition_id, epoch_id):
        self.file = open(file_name, "a")
        return True
    def process(self, row):
        self.file.write(str(row)+"\n")
    def close(self, error):
        self.file.close()

print('################################################################')
# create a file
f = open(file_name, "w")
f.close()

# read stream from a Kafka topic
df = spark \
     .readStream \
     .format("kafka") \
     .option("kafka.bootstrap.servers", kafka_servers) \
     .option("subscribe", topic) \
     .option("startingOffsets", "earliest") \
     .load()

# write stream to a local file
query = df \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), sample_schema).alias("data")) \
        .select("data.*") \
        .writeStream \
        .foreach(FileWriter()) \
        .start() \
        .awaitTermination(timeout=30)

print('################################################################')