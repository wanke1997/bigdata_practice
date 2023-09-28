from kafka import KafkaConsumer, KafkaProducer
import json

bootstrap_servers = ["kafka1:9091","kafka2:9092","kafka3:9093"]
topic_name = 'bigdata'

# create a Kafka consumer
consumer = KafkaConsumer(
    topic_name, 
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit = True,
    value_deserializer=lambda x:json.loads(x.decode('utf-8')))

print("start to receive messages")

count = 0
file = open("receive.txt",'w')
# this is a non-end loop, receiving real-time messages from Kafka clusters
for message in consumer:
    count += 1
    if count%10000==0:
        print(count/10000, type(message.value))
    file.write(str(message.value)+"\n")