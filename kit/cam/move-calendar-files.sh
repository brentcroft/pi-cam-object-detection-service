#!/bin/bash

cd /home/pi/cam

# prepare and read service details
dos2unix -q service.properties
source service.properties

# from service.properties
# NODE_ID, ACTION, CAM_NO, GRAPH

# establish current prefix
DATE=`date '+%Y-%m-%d %H:%M:%S'`
PREFIX="$DATE [${NODE_ID}] ${ACTION}:"

LOCAL_CALENDAR_IMAGE_STORE="/home/pi/cam-ram/images"
LOCAL_CALENDAR_DETECTION_STORE="/home/pi/cam-ram/detections"

REMOTE_CALENDAR_IMAGE_STORE="/XENOPHON/animals-count/CAM-0${CAM_NO}"
REMOTE_CALENDAR_DETECTION_STORE="/XENOPHON/animals-count/CAM-0${CAM_NO}-CLASSIFIED"


move_files() {

    START_DIR=$1
    
    echo "Start dir: ${START_DIR}"
    
    LOCK_DIR="${START_DIR}/.lock-move-images"
    LOG_FILE="${START_DIR}/move-images.log"

    #
    #
    DATE=`date '+%Y-%m-%d %H:%M:%S'`
    PREFIX="$DATE move-images:"

    #
    DAY=`date '+%Y-%m-%d'`

    SOURCE_DIR="$1/*"
    TARGET_DIR="$2"

    cd $START_DIR


    pids=$(ps aux | grep "[m]v -v ${SOURCE_DIR}" | awk '{print $2}')

    if [ ! "$pids" = "" ]; then
        echo "Already running: pids=${pids}"
        exit 1
    else
        # if no pids then just delete any LOCK_DIR
        echo "$PREFIX Clearing any lock file."
        rm -r $LOCK_DIR || true
    fi



    if mkdir $LOCK_DIR; then
        echo "$PREFIX Created lock file: $LOCK_DIR"
        
        echo "${PREFIX} Moving files: source=[${SOURCE_DIR}] target=[${TARGET_DIR}]"
        
        if [ ! -d "$TARGET_DIR" ]; then
            sudo mkdir -p $TARGET_DIR
            echo "${PREFIX} Created new target directory: [$TARGET_DIR]"
        fi
        
        # don't use update flag as target directory will have thousands of files
        sudo mv $SOURCE_DIR $TARGET_DIR
        
        
        DATE=`date '+%Y-%m-%d %H:%M:%S'`
        PREFIX="$DATE move-images:"        
        echo "${PREFIX} Finished."
    else
        echo "$PREFIX Lock file already exists: $LOCK_DIR"
        exit 1
    fi



    rm -r $LOCK_DIR

    cd $START_DIR

    echo "$PREFIX finished, lock removed."
}



#
DAY=`date '+%Y-%m-%d'`

move_files $LOCAL_CALENDAR_IMAGE_STORE/$DAY $REMOTE_CALENDAR_IMAGE_STORE/$DAY
move_files $LOCAL_CALENDAR_DETECTION_STORE/$DAY/$GRAPH $REMOTE_CALENDAR_DETECTION_STORE/$DAY/$GRAPH
