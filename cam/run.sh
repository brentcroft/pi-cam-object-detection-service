#!/bin/bash
set -e

# prepare and read service details
dos2unix -q service.properties
source service.properties

# establish current prefix
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE ${ACTION} [${NODE_ID}]:"


# two signals for abort
if [ "$SUSPENDED" = "1" ]; then
    echo "$PREFIX SUSPENDED."
    exit 1
fi

if [ "$DISABLED" = "1" ]; then
    echo "$PREFIX DISABLED."
    exit 2
fi


# check for running pids by service node id
pids=$(ps aux | grep "[s]ervice_node_id=$NODE_ID" | awk '{print $2}')

if [ "$pids" = "" ]; then
    echo
    echo
    echo "$PREFIX starting ..."
    
    # run the action
    python3 "./lib/${ACTION}.py" service_node_id=${NODE_ID} >> ./service.log
    
    # update current prefix after action
    DATE=`date '+%Y-%m-%d %H:%M:%S'`
    PREFIX="$DATE ${ACTION} [${NODE_ID}]:"       
    echo "${PREFIX} finished."
else
    echo "$PREFIX already running."
fi
