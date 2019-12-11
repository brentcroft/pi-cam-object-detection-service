#!/bin/bash
#set -e


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
    
        # might take some time
        python3 "./lib/can_start.py" service_node_id=${NODE_ID} >> ./service.log
        CAN_START_RESULT=$?

        if [ $CAN_START_RESULT -ne 0 ]; then
            echo "${PREFIX} no go: ${CAN_START_RESULT}."
            ./kill-http-server.sh
            ./kill-pi-cam-od.sh
        else
            echo "$PREFIX powersaving ..."
            ./powersave.sh > /dev/null 2>&1 &
        
            echo "$PREFIX starting ..."
            
            # maybe start (if not running)
            ./run-http-server.sh > /dev/null 2>&1 &

            # run the action - blocks
            python3 "./lib/${ACTION}.py" service_node_id=${NODE_ID} >> ./service.log

            SERVICE_RESULT=$?

            # update current prefix after action
            DATE=`date '+%Y-%m-%d %H:%M:%S'`
            PREFIX="$DATE [${NODE_ID}] ${ACTION}:"

            if [[ ( ! -z $REBOOT_CODE ) && ( $SERVICE_RESULT -eq $REBOOT_CODE ) ]]; then
                echo "${PREFIX} detected reboot return code: ${SERVICE_RESULT}."
                # requires a reboot
                nohup sudo ./reboot-from-cron.sh >> ./service.log 2>&1 &
            else
                echo "${PREFIX} finished: ${SERVICE_RESULT}."
            fi
        fi
    fi
else
    #echo "$PREFIX already running.: pids=$pids"

    if [ "$SUSPENDED" = "1" ]; then
        echo "$PREFIX suspended, stopping service..."
        ./stop-service.sh
    fi
fi
