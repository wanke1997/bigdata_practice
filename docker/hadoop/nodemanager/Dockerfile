# build from hadoop-base:3.2.1
# that we built before using docker build -t hadoop-base:3.2.1 .
FROM hadoop-base:3.3.5

HEALTHCHECK CMD curl -f http://localhost:8042/ || exit 1

EXPOSE 8042

COPY run.sh /
CMD ["/bin/bash", "/run.sh"]
