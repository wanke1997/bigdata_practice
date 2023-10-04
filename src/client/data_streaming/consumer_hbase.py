from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
from happybase import *

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.4.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 pyspark-shell'
appName = "Kafka-Spark-HBase Writer"
spark_master = "spark://spark-master:7077"
kafka_servers = "kafka1:9091,kafka2:9092,kafka3:9093"
topic = "bigdata"
host = 'hbase-master'
port = 9090
table_name = 'bigdata_table'

# configure spark jobs
spark = SparkSession.builder \
    .master(spark_master) \
    .appName(appName) \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()

# kafka message schema
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

# define hbase writer
class HBaseWriter:
    def open(self, partition_id, epoch_id):
        global table_name
        self.connection = Connection(
            host=host, 
            port=port, 
            autoconnect=False,
        )
        self.connection.open()
        self.table = self.connection.table(table_name)
        return True
    def process(self, row):
        self.table.put(row['key'].encode('utf-8'), {
            b'basic:rowkey':row['rowkey'].encode('utf-8'),
            b'basic:time':row['time'].encode('utf-8'),
            b'property:MAC':row['MAC'].encode('utf-8'),
            b'property:PCM':row['PCM'].encode('utf-8'),
            b'property:departAirport':row['departAirport'].encode('utf-8'),
            b'property:airline':row['airline'].encode('utf-8'),
            b'property:agent':row['agent'].encode('utf-8'),
            b'property:country':row['country'].encode('utf-8'),
            b'connection:request':row['request'].encode('utf-8'),
            b'connection:response':row['response'].encode('utf-8'),
            b'error:error':row['error'].encode('utf-8'),
            b'error:errorCode':row['errorCode'].encode('utf-8'),
            b'error:errorType':row['errorType'].encode('utf-8'),
            b'status:success':row['success'].encode('utf-8'),
            b'status:fail':row['fail'].encode('utf-8')
        })
    def close(self, error):
        try:
            self.connection.close()
        except Exception as e:
            print("exception: unable to close connection with HBase")
            print(e)

print('################################################################')
# load streaming data from Kafka topic
df = spark \
     .readStream \
     .format("kafka") \
     .option("kafka.bootstrap.servers", kafka_servers) \
     .option("subscribe", topic) \
     .option("startingOffsets", "earliest") \
     .load()

# connect to hbase
connection = Connection(
    host=host, 
    port=port, 
    autoconnect=False,
)
connection.open()

# create hbase table
if table_name.encode('utf-8') not in connection.tables():
    connection.create_table(
        table_name, {
            'basic': dict(),
            'property': dict(),
            'connection': dict(),
            'error': dict(),
            'status': dict(),
        }
    )

# write kafka stream to hbase
query = df \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), sample_schema).alias("data")) \
        .select("data.*") \
        .writeStream \
        .foreach(HBaseWriter()) \
        .start() \
        .awaitTermination(2400)
print('################################################################')