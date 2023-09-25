# bigdata_practice

## 1. Clusters
There are two versions for the clusters of this project.

### 1.1 Version 1
Cluster 1: Kafka, Spark(Master), HBase(Master) \
Cluster 2: Kafka, Spark(Worker), HBase(Worker), MySQL \
Cluster 3L Kafka, Spark(Worker), HBase(Worker) \

### 1.2. Version 2
Cluster 1: Kafka, Hadoop(Master, HDFS, MapReduce), Storm(Master) \
Cluster 2: Kafka, Hadoop(Slave, HDFS, MapReduce), Storm(Slave), MySQL \
Cluster 3: Kafka, Hadoop(Slave, HDFS, MapReduce), Storm(Slave) \