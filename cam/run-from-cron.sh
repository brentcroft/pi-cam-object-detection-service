#!/bin/bash
set -e

# just in case any drives got dropped
sudo mount -a

START_DIR="/home/pi/cam"

cd $START_DIR

nohup sudo ./run.sh >> ./service.log 2>&1 &