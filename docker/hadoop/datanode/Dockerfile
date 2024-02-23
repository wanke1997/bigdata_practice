# build from hadoop-base:3.3.5
# that we built before using docker build -t hadoop-base:3.3.5 .
FROM hadoop-base:3.3.5

HEALTHCHECK CMD curl -f http://localhost:9864/ || exit 1

ENV HDFS_CONF_dfs_datanode_data_dir=file:///hadoop/dfs/data
RUN mkdir -p /hadoop/dfs/data
VOLUME /hadoop/dfs/data

EXPOSE 9864

COPY run.sh /
CMD ["/bin/bash", "/run.sh"]
