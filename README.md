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

### About Spark

launch an example spark job
```bash
# Please run this command on client container
cd /opt/apps
spark-submit --master spark://spark-master:7077 spark_script.py
```

### About hadoop
1. Create a directory
```bash
hadoop fs -mkdir /input
```

2. Upload a file
```bash
hadoop fs -put /data/benda.txt /input
```

3. List files in a directory
```bash
hadoop fs -ls /input
```

4. MapReduce example program \
We should run MapReduce programs on Namenode container. Let's take WordCount program for example. Firstly, we should create a /input directory and upload a data file to it, then we should check if /output directory exists. If /output directory exists, we should delete it in advance. Finally, we run WordCount.jar file to execute the MapReduce program. The commands are shown below. 
```bash
# please run these commands on namenode container
hadoop fs -mkdir /input
hadoop fs -put /data/benda.txt /input
hadoop jar /code/WordCount.jar WordCount /input /output
```
After this, we can check the outputs in HDFS /output directory. 

## Containers Information:
| Name | Container | Port | Webserver Link |
|------|------|-----|-----|
| Zookeeper | zookeeper | 2181 | N/A |
| Kafka | kafka1/2/3 | 9091,9092,9093 | N/A |
| HDFS | namenode | 9870 | http://localhost:9870 |
| MapReduce Tasks | resourcemanager | 8089 | http://localhost:8089 |
| DataNode | datanode1/2/3 | 9864,9864,9864 | N/A |
| HBase | master | 16010 | http://localhost:16010 |
| MySQL | mysql | 8989:3306 | N/A |
| Spark | master | 9000:8181 | http://localhost:9000 |

## Start containers
1. Start Zookeeper and Kafka
```bash
cd <dir_to_project>/docker/zookeeper_kafka
docker-compose up -d
```
2. Start Hadoop
```bash
cd <dir_to_project>/docker/zookeeper_kafka
docker build -t hadoop-base:3.3.1 -f Dockerfile .
docker-compose up -d
```
3. Start HBase. Note that the prerequisite of starting HBase is that Zookeeper and Hadoop are running
```bash
cd <dir_to_project>/docker/hbase
docker-compose up -d
```
4. Start MySQL
```bash
cd <dir_to_project>/docker/mysql
docker-compose up -d
```
5. Start Spark cluster
```bash
cd <dir_to_project>/docker/spark
docker-compose up -d
```
6. Start client container
```bash
cd <dir_to_project>/docker/client
docker-compose up -d
```

### Potential Problems and Solutions
1. When starting Hadoop, namenode doesn't work, saying that it has not been firmatted \
Solution: uncommment the last second command in namenode/run.sh file to format the file system. That is:
```bash
cd $HADOOP_HOME/bin && ./hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
```

## Notes:
所有的开发都在client里面完成，使用python脚本和插件，remote访问所有的服务（hadoop,mysql,spark,kafka,etc）