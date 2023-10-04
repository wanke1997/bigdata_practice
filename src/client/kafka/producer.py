from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import kafka
import json
from json import loads

bootstrap_servers = ["kafka1:9091","kafka2:9092","kafka3:9093"]
topic_name = 'bigdata'
file_name = '/data/GDS_logs_small.txt'

# create a topic
try:
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers, 
    )
    topic_list = []
    topic_list.append(NewTopic(name=topic_name, num_partitions=3, replication_factor=3))
    admin_client.create_topics(new_topics=topic_list)
except kafka.errors.TopicAlreadyExistsError:
    print("The topic that you entered already exists.")
else:
    print("The topic has been created.")

# create a producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
item_names = ['key','rowkey','time','MAC','PCM','departAirport','airline','agent','country','request','response','error','errorCode','errorType','success','fail']
file = open(file_name,'r')

line = file.readline()
count = 0

while line is not None and line != '':
    components = line.strip().split("|")
    components = [str(count)]+components
    jsonObject = json.dumps(dict(map(lambda i,j:(i,j), item_names, components))).encode('utf-8')
    ack = producer.send(topic_name,jsonObject)
    count += 1
    if count%10000==0:
        print(jsonObject)
        metadata = ack.get()
        print(count/10000, metadata.topic, metadata.partition)
    line = file.readline()
    

print("we sent",count,"messages")
file.close()