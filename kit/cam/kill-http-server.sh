#!/bin/bash
#
set -e

# prepare and read service details: ACTION & NODE_ID
dos2unix -q service.properties
source service.properties

#
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE http [${NODE_ID}]:"


#
pids=$(ps aux | grep "[h]ttp_server.py" | awk '{print $2}')

if [ ! "$pids" = "" ] || [ ! "$pids" = "" ]; then
    for pid in $pids; do
        echo "${PREFIX} sending kill to [${pid}]"
        sudo kill $pid
    done
else
    echo "${PREFIX} no pids"
fi