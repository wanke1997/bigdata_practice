FROM openjdk:11.0.11-jre-slim-buster as builder

# Add Dependencies for PySpark
ENV PATH="/opt/spark/bin:/opt/java/jdk-15.0.2/bin:/opt/spark/sbin:$PATH"

RUN apt-get update
RUN apt-get install -y curl vim iputils-ping wget software-properties-common ssh net-tools ca-certificates python3 python3-numpy python3-matplotlib python3-scipy python3-pandas 

# RUN apt-get install -y python3-pip 
RUN apt update && apt install python3-pip -y
# RUN pip install -y requests

WORKDIR /opt/java
RUN curl https://download.java.net/java/GA/jdk15.0.2/0d1cfde4252546c6931946de8db48ee2/7/GPL/openjdk-15.0.2_linux-x64_bin.tar.gz -o openjdk-15.0.2_linux-x64_bin.tar.gz
RUN tar -xzf openjdk-15.0.2_linux-x64_bin.tar.gz && \
    rm -rf openjdk-15.0.2_linux-x64_bin.tar.gz

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.4.1 \
HADOOP_VERSION=3 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

RUN wget --no-verbose -O apache-spark.tgz "https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz



FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8181 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8181 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8181 7077 7000 7001 5432 9090 9091 9092

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

COPY ./requirements.txt /
RUN pip3 install -r /requirements.txt

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]