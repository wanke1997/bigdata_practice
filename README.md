# Bigdata Practice

## Launch Docker Containers
1. Start Zookeeper and Kafka
```bash
cd <dir_to_project>/docker/zookeeper_kafka
docker-compose up -d
```
2. Start Hadoop
```bash
cd <dir_to_project>/docker/hadoop
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

## Example Programs

### About Spark

You can launch an example spark job on the client container by following the commands below. 
```bash
# Please run tutorial file on client container
cd /apps/tutorial
spark-submit --master spark://spark-master:7077 spark_tutorial.py
```

### About Hadoop
#### 1. Create a directory
```bash
hadoop fs -mkdir /input
```

#### 2. Upload a file
```bash
hadoop fs -put /data/benda.txt /input
```

#### 3. List files in a directory
```bash
hadoop fs -ls /input
```

#### 4. MapReduce Example Program
We run MapReduce programs on `Namenode` container. Let's take `WordCount` program for example. Firstly, we create a `/input` directory and upload a data file to it, then we check if `/output` directory exists. If `/output` directory exists, we should delete it in advance. Finally, we run `WordCount.jar` file to execute the MapReduce program. The commands are shown below. 
```bash
# please run these commands on namenode container
hadoop fs -mkdir /input
hadoop fs -put /data/benda.txt /input
hadoop jar /code/WordCount.jar WordCount /input /output
```
After this, we can check the outputs in HDFS `/output` directory. 

## Containers Information
| Name | Container | Port | Webserver Link |
|------|------|-----|-----|
| Zookeeper | zookeeper | 2181 | N/A |
| Kafka | kafka1/2/3 | 9091,9092,9093 | N/A |
| HDFS | namenode | 9870 | http://localhost:9870 |
| MapReduce Tasks | resourcemanager | 8089 | http://localhost:8089 |
| DataNode | datanode1/2/3 | 9864,9864,9864 | N/A |
| HBase | hbase-master | 16010 | http://localhost:16010 |
| HBase Thrift | hbase-master | 9090 | N/A |
| MySQL | mysql | 8989:3306 | N/A |
| Spark | spark-master | 9000:8181 | http://localhost:9000 |

## MySQL Login
Default variable settings are shown below
| Name | Value |
|------|------|
| MYSQL_HOST | mysql |
| MYSQL_VERSION | 8.0.21 |
| MYSQL_DATABASE | test |
| MYSQL_ROOT_USER | root |
| MYSQL_ROOT_PASSWORD | root |
| MYSQL_USER | dev |
| MYSQL_PASSWORD | dev |

Follow the command below to login mySQL.
```bash
# command to start mysql from mysql container, the password can be found from the table above
mysql -u root -p
```

## Data Processing
Data processing files mainly responsible to retrieve data from HBase database, then do aggregation calculation with Spark. `questions.py` Python script in `/src/client/data_processing` directory answers questions of this project (see page 3 of description). Please run the Python scripts by following the commands below. Note that the  `/src/client/data_processing` directory is mapped to `/apps/data_processing` in client container. 
```bash
# Please run tutorial file in client container
cd /apps/data_processing
spark-submit --master spark://spark-master:7077 questions.py
```

## Notes and Trouble Shooting
1. If you start Hadoop for the first time, namenode may exit with code 1 saying that it has not been formatted \
Solution: `uncommment` the last 2nd command in `docker/hadoop/namenode/run.sh` file to format the file system. That command is: `cd $HADOOP_HOME/bin && ./hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME`. After this, delete and rebuild the base image. Then restart the docker containers. 

2. If you start the containers and find that resourcemanager exits, 

Solution: You should `commment` the last 2nd command in `docker/hadoop/namenode/run.sh` file. That command is: `cd $HADOOP_HOME/bin && ./hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME`. After this, delete and rebuild the base image. Then restart the docker containers. 

3. Get all container's ip address: 
```bash
docker ps -q | xargs -n 1 docker inspect --format '{{ .Name }} {{range .NetworkSettings.Networks}} {{.IPAddress}}{{end}}' | sed 's#^/##';
```