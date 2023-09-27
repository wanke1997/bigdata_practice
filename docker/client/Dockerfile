# client-container image
# to build this image, please use the command below.
# docker build -t client-container .

FROM openjdk:11.0.11-jre-slim-buster as builder

# Add Dependencies for PySpark
ENV PATH="/opt/java/jdk-15.0.2/bin:$PATH"

RUN apt-get update
RUN apt-get install -y curl vim iputils-ping wget software-properties-common ssh net-tools ca-certificates python3 python3-numpy python3-matplotlib python3-scipy python3-pandas mariadb-server 
RUN apt update && apt install python3-pip -y

WORKDIR /opt/java
RUN curl https://download.java.net/java/GA/jdk15.0.2/0d1cfde4252546c6931946de8db48ee2/7/GPL/openjdk-15.0.2_linux-x64_bin.tar.gz -o openjdk-15.0.2_linux-x64_bin.tar.gz
RUN tar -xzf openjdk-15.0.2_linux-x64_bin.tar.gz && \
    rm -rf openjdk-15.0.2_linux-x64_bin.tar.gz

ENV SPARK_VERSION=3.4.1 \
HADOOP_VERSION=3 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

RUN wget --no-verbose -O apache-spark.tgz "https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz

ENV PATH="$PATH:/opt/spark/bin"

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

COPY ./requirements.txt /
RUN pip3 install -r /requirements.txt