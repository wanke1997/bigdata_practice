from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark import SparkConf
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.4.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 pyspark-shell'

appName = "Kafka Examples"
master = "spark://spark-master:7077"
kafka_servers = "kafka1:9091,kafka2:9092,kafka3:9093"
topic = "bigdata_small"

spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .config("spark.executor.memory", "4g") \
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

class HBaseWriter:
    file = None
    def open(self, partition_id, epoch_id):
        print("Opened %d, %d" % (partition_id, epoch_id))
        self.file = open("/data/tutor_output.txt", "a")
        return True
    def process(self, row):
        # self.file.write(row['rowkey']+"\n")
        self.file.write(str(row)+"\n")
    def close(self, error):
        self.file.close()

def print_row(row):
    file = open("/data/tutor_output.txt", "a")
    file.write(row['rowkey']+"\n")
    file.close()

print('################################################################')

f = open("/data/tutor_output.txt", "w")
f.close()

df = spark \
     .readStream \
     .format("kafka") \
     .option("kafka.bootstrap.servers", kafka_servers) \
     .option("subscribe", topic) \
     .option("startingOffsets", "earliest") \
     .load()

print('started to query')
query = df \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), sample_schema).alias("data")) \
        .select("data.*") \
        .writeStream \
        .foreach(HBaseWriter()) \
        .start() \
        .awaitTermination(timeout=600)
print('################################################################')
