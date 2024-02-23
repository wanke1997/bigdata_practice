# build from hadoop-base:3.3.5
# that we built before using docker build -t hadoop-base:3.3.5 .
FROM hadoop-base:3.3.5

HEALTHCHECK CMD curl -f http://localhost:8088/ || exit 1

EXPOSE 8088

COPY run.sh /
CMD ["/bin/bash", "/run.sh"]
