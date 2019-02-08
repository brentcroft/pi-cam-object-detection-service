# pi-cam-object-detector

This kit is a workshop for installing TensorFlow & Object Detection on a Raspberry Pi with a Camera.

The kit requires an appropriate Tensorflow wheel, see: https://github.com/lhelontra/tensorflow-on-arm/releases.

The file "01-build-tf-1.12-0-cp35.sh" has the following hard-coded, which may need to be amended:

    sudo pip3 install tensorflow-1.12.0-cp35-none-linux_armv7l.whl
    
    
## Installation
Unpack the kit into a directory on the pi.

1. Run "01-build-tf-1.12-0-cp35.sh" to install Tensorflow.
2. Run "02-build-tf-OD-cp35" to install Object Detection.

NB: I usually do these line by line, and I unpack directly into */home/pi*


## Configuration
Navigate to the *./cam* directory.

Edit the file "cam.properties".

You must set the property CURRENT_IMAGE_STORE to a directory where the pi can write files.

Other properties are described in the "README" file in the *./cam* directory.


## Running
To run an autonomous service, set a crontab entry as follows:

    * * * * * /home/pi/cam/run-from-cron.sh

The service detects when it is already running, but will regularly try to restart.

To start the service manualy, run the script:

    *start-service.sh*
    
The service regularly that *SUSPENDED=0* in the file "service.properties", and if not the service stops.