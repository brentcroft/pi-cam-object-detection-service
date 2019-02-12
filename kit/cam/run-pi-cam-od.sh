#!/bin/bash
set -e

# prepare and read service details
dos2unix -q service.properties
source service.properties

# establish current prefix
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE ${ACTION} [${NODE_ID}]:"


if [ "$SUSPENDED" = "1" ]; then
    echo "$PREFIX suspended."
    exit 0
fi  

# check for running pids by service node id
pids=$(ps aux | grep "[s]ervice_node_id=$NODE_ID" | awk '{print $2}')

if [ "$pids" = "" ]; then
    if [ "$SUSPENDED" = "1" ]; then
        echo "$PREFIX suspended."
        exit 0
    fi  

    echo
    echo
    echo "$PREFIX starting ..."

    # run the action - blocks
    python3 "./lib/${ACTION}.py" service_node_id=${NODE_ID} >> ./service.log
    
    # update current prefix after action
    DATE=`date '+%Y-%m-%d %H:%M:%S'`
    PREFIX="$DATE ${ACTION} [${NODE_ID}]:"       
    echo "${PREFIX} finished."
else
    echo "$PREFIX already running.: pids=$pids"
    
    if [ "$SUSPENDED" = "1" ]; then
        ./stop-service.sh
        echo "$PREFIX suspended running service."
        exit 0
    fi    
fi
