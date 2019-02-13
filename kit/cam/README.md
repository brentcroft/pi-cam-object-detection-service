# Overview

The service runs continually unless:

1. The number of consecutive images with no detections exceeds *LOG_UNDETECTED_MAX_SEQ* in  in **./cam.properties**
2. **SUSPENDED=1** occurs in **./service.properties**
3. The service is otherwise killed

The service will attempt to restart regularly (assuming the cron job is set).

The service performs the following sequence:

* Re-read **./service.properties** & **./cam.properties**.
* Take a camera image.
* Take a crop from the image and submit it to an Object Detection graph.
* Store any detection results and the images to which they relate.
* Maybe create boxed images.
* Maybe adjust the crop frame, tracking detections.


This sequence is specified in the python file is **./lib/cam.py**. 

**cam.py** opens a TensorFlow Session and starts detecting forever, or until interrupted.

It defines four functions with default implementations to be modified as required.

A detection filter that returns Tue or False:
 
    detection_filter( class_name=None, score=None, box=None, frame=None )
    
A tracking filter that may, or may not, recentre the frame on the target:

    maybe_move( frame=None, target=None, step=0, max_size=None )

Two event handlers, where the context contains raw and frame images, and maybe associated meta-data:

    on_no_objects( context = None )
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


