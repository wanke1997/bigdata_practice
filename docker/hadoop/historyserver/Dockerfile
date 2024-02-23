# build from hadoop-base:3.3.5 if your architectur is AMD64
# that we built before using docker build -t hadoop-base:3.3.5 .
FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

HEALTHCHECK CMD curl -f http://localhost:8188/ || exit 1

ENV YARN_CONF_yarn_timeline___service_leveldb___timeline___store_path=/hadoop/yarn/timeline
RUN mkdir -p /hadoop/yarn/timeline
VOLUME /hadoop/yarn/timeline

EXPOSE 8188

COPY run.sh /
CMD ["/bin/bash", "/run.sh"]
