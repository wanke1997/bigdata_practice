FROM bde2020/hbase-master:1.0.0-hbase1.2.6

RUN rm /run.sh
RUN echo "#!/bin/bash" >> /run.sh
RUN echo "/opt/hbase-$HBASE_VERSION/bin/hbase-daemon.sh start thrift" >> /run.sh
RUN echo "/opt/hbase-$HBASE_VERSION/bin/hbase master start" >> /run.sh

RUN chmod +x /run.sh