#!/bin/bash
set -e

START_DIR="/home/pi/cam"

cd $START_DIR

# prepare and read service details
dos2unix -q service.properties
source service.properties

# establish current prefix
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE [${NODE_ID}] cron:"

echo "$PREFIX preparing to reboot" >> ./service.log


nohup sudo ./kill-http-server.sh >> ./service.log 2>&1 &

nohup sudo ./kill-pi-cam-od.sh >> ./service.log 2>&1 &

sleep 10

echo "$PREFIX rebooting..." >> ./service.log

sudo reboot
