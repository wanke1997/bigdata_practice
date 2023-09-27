#!/bin/bash
# Kick-off nodemanager to manage namenode, datanode inside cluster
# This is second level of resource manager
# Nodemanager will manage resource hand in hand with yarn
cd $HADOOP_HOME/bin && ./yarn --config $HADOOP_CONF_DIR nodemanager
