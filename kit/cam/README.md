# Overview

The service runs continually unless:

1. The number of consecutive images with no detections exceeds *LOG_UNDETECTED_MAX_SEQ* in **./cam.properties**
2. **SUSPENDED=1** occurs in **./service.properties**
3. The service is otherwise killed

NB: The service will attempt to restart regularly if the cron job is set.

## Flow
The service starts when the python file **./lib/cam.py** is executed.

The service first performs the following initialisation sequence:

* read **./service.properties** & **./cam.properties**.
* maybe cache the graph and label files if not found locally
* initialize the graph
* initialize the camera
* initialize the current detection frame
* start the camera

The service then opens a TensorFlow Session and repeats the following sequence forever, or until interrupted.

* re-read **./service.properties** & **./cam.properties**
* get camera image
* crop detection frame from camera image and submit to graph
* store any detection results and related images
* maybe create boxed images
* maybe adjust crop frame - tracking detections

NB: Once the camera is started, its properties are never refreshed; the service has to be restarted to change camera properties.

 
## Customization
The python file **./lib/cam.py** defines four functions with default implementations to be modified as required.

1. A detection filter that returns Tue or False:
 
    detection_filter( class_name=None, score=None, box=None, frame=None )

2. A tracking filter that may, or may not, recentre the frame on the target:

    maybe_move( frame=None, target=None, step=0, max_size=None )
    
Given **context** contains raw and frame images, and maybe associated meta-data:

3. An event handler called when there are no detections for an image (after filtering):

    on_no_objects( context = None )
    
4. An event handler called when there are detections, responsible for storage:

    on_detected_objects( context = None )


    
## Manual Scripts
Start and stop the service manually, by running the scripts:

    start-service.sh
    stop-service.sh

    
## Further Info
* Review the file **./service.properties** & **./cam.properties**, making amendments as required
* Review this information: https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
* Review the python code in the directory **./lib**
* Review the html file in the directory **./site**


