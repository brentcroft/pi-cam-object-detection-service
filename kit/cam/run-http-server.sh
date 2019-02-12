#!/bin/bash
set -e

# prepare and read service details
dos2unix -q service.properties
source service.properties

# establish current prefix
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE http [${NODE_ID}]:"


if [ "$SUSPENDED" = "1" ]; then
    echo "$PREFIX suspended."
    exit 0
fi  


# check for http_server
pids=$(ps aux | grep "[h]ttp_server.py" | awk '{print $2}')
if [ "$pids" = "" ]; then
    # maybe start the http-server (if HTTP_SERVER specified in service.properties)
    if [ "$HTTP_SERVER" = "1" ]; then
        echo "$PREFIX starting..."
        python3 "./lib/http_server.py"
    fi
else
    echo "$PREFIX already running: pids=$pids"
    
    if [ "$SUSPENDED" = "1" ]; then
        echo "$PREFIX killing..."
        ./kill-http-server.sh
        exit 0
    fi    
fi