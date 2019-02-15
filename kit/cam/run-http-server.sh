#!/bin/bash
set -e

# prepare and read service details
dos2unix -q service.properties
source service.properties

# establish current prefix
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE [${NODE_ID}] http:"


# check for http_server pids
pids=$(ps aux | grep "[h]ttp_server.py" | awk '{print $2}')

if [ "$pids" = "" ]; then
    if [ "$SUSPENDED" = "1" ]; then
        echo "$PREFIX suspended, not starting."
    else  
        # maybe start the http-server (if HTTP_SERVER specified in service.properties)
        if [ "$HTTP_SERVER" = "1" ]; then
            echo "$PREFIX starting..."
            python3 "./lib/http_server.py"
        fi
    fi
else
    echo "$PREFIX already running: pids=$pids"
    
    if [ ! "$HTTP_SERVER" = "1" ]; then
        echo "$PREFIX suspended, killing..."
        ./kill-http-server.sh
    fi    
fi