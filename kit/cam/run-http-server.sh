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
        python3 "./lib/can_start.py"
        CAN_START_RESULT=$?

        if [ $CAN_START_RESULT -ne 0 ]; then
            echo "${PREFIX} no go: ${CAN_START_RESULT}."
        else    
    
            # maybe start the http-server (if HTTP_SERVER specified in service.properties)
            if [ "$HTTP_SERVER" = "1" ]; then
                echo "$PREFIX starting..."
                python3 "./lib/http_server.py"
            fi
        fi
    fi
else
    echo "$PREFIX already running: pids=$pids"
    
    if [ ! "$HTTP_SERVER" = "1" ]; then
        echo "$PREFIX suspended, killing..."
        ./kill-http-server.sh
    fi    
fi