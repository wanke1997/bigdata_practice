# bigdata_practice

## 1. Clusters
There are two versions for the clusters of this project.

### 1.1 Version 1
Cluster 1: Kafka, Hadoop(Master, HDFS), Spark(Master), HBase(Master) \
Cluster 2: Kafka, Hadoop(Slave, HDFS), Spark(Worker), HBase(Worker), MySQL \
Cluster 3: Kafka, Hadoop(Slave, HDFS), Spark(Worker), HBase(Worker)

### 1.2. Version 2
Cluster 1: Kafka, Hadoop(Master, HDFS, MapReduce) \
Cluster 2: Kafka, Hadoop(Slave, HDFS, MapReduce) MySQL \
Cluster 3: Kafka, Hadoop(Slave, HDFS, MapReduce)

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

### About hadoop
1. Create a directory
```bash
hadoop fs -mkdir /test
```

2. Upload a file
```bash
hadoop fs -put example1.txt /test
```

3. List files in a directory
```bash
hadoop fs -ls /test
```

4. MapReduce commands
Firstly, we should create a /input directory and upload a data file to it, then we should execute the command below. 
```bash
hadoop jar WordCount.jar WordCount /input /output
```
Then we can check the outputs in HDFS /output directory. If /output directory exists, we should delete it in advance. 

5. Check cluster web pages:
HDFS: http://localhost:9870 \
Resource Manager(MapReduce tasks): http://localhost:8089/ \
HBase: http://localhost:16010/

### Potential Problems and Solutions
1. When starting Hadoop, namenode doesn't work, saying that it has not been firmatted \
Solution: uncommment the last second command in namenode/run.sh file to format the file system. That is:
```bash
cd $HADOOP_HOME/bin && ./hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
```