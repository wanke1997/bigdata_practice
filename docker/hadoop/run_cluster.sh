#!/bin/bash

# build docker image with image name hadoop-base:3.3.1
docker build -t hadoop-base:3.3.1 -f Dockerfile .
# running image to container, -d to run it in daemon mode
docker-compose up -d
