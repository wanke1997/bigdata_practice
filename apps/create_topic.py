from kafka.admin import KafkaAdminClient, NewTopic
import kafka

admin_client = KafkaAdminClient(
    bootstrap_servers="kafka1:9091,kafka2:9092,kafka3:9093", 
)

topic_list = []
topic_list.append(NewTopic(name="example_topic48", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list)

consumer = kafka.KafkaConsumer(bootstrap_servers=['kafka1:9091','kafka2:9092','kafka3:9093'])
topics = consumer.topics()
print("Here are topics that we have:")
print(topics)
print("Done")