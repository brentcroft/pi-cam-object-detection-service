#!/bin/bash
set -e

# prepare and read service details
dos2unix -q service.properties
source service.properties

# establish current prefix
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE [${NODE_ID}] ${ACTION}:"


# check for service_node_id pids
pids=$(ps aux | grep "[s]ervice_node_id=$NODE_ID" | awk '{print $2}')

if [ "$pids" = "" ]; then
    if [ "$SUSPENDED" = "1" ]; then
        echo "$PREFIX suspended, not starting."
    else
        echo
        echo
        echo "$PREFIX starting ..."

        # run the action - blocks
        python3 "./lib/${ACTION}.py" service_node_id=${NODE_ID} >> ./service.log
        
        # update current prefix after action
        DATE=`date '+%Y-%m-%d %H:%M:%S'`
        PREFIX="$DATE [${NODE_ID}] ${ACTION}:"       
        echo "${PREFIX} finished."
    fi  
else
    echo "$PREFIX already running.: pids=$pids"
    
    if [ "$SUSPENDED" = "1" ]; then
        echo "$PREFIX suspended, stopping service..."
        ./stop-service.sh
    fi    
fi
