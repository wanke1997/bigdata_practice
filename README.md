# bigdata_practice

## 1. Clusters
There are two versions for the clusters of this project.

### 1.1 Version 1
Cluster 1: Kafka, Hadoop(Master, HDFS), Spark(Master), HBase(Master) \
Cluster 2: Kafka, Hadoop(Slave, HDFS), Spark(Worker), HBase(Worker), MySQL \
Cluster 3: Kafka, Hadoop(Slave, HDFS), Spark(Worker), HBase(Worker)

### 1.2. Version 2
Cluster 1: Kafka, Hadoop(Master, HDFS, MapReduce), Storm(Master) \
Cluster 2: Kafka, Hadoop(Slave, HDFS, MapReduce), Storm(Slave), MySQL \
Cluster 3: Kafka, Hadoop(Slave, HDFS, MapReduce), Storm(Slave)

build empty container's image:
```bash
docker build -t client-container .
```

get all container's ip address: 
```bash
docker ps -q | xargs -n 1 docker inspect --format '{{ .Name }} {{range .NetworkSettings.Networks}} {{.IPAddress}}{{end}}' | sed 's#^/##';
```

launch an example spark job
```bash
# Please submit this command with client container
cd /opt/apps
spark-submit --master spark://spark-master:7077 spark_script.py
```