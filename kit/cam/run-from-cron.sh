#!/bin/bash
set -e

# just in case any drives got dropped
sudo mount -a

START_DIR="/home/pi/cam"

cd $START_DIR

nohup sudo ./run-pi-cam-od.sh >> ./service.log 2>&1 &

# maybe start the http server
#nohup sudo ./run-http-server.sh >> ./server.log 2>&1 &
nohup sudo ./run-http-server.sh >/dev/null 2>&1 &
