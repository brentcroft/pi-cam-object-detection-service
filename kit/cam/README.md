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


## Manual Scripts
Start and stop the service manually, by running the scripts:

    start-service.sh
    stop-service.sh

## Further Info
* Review the file **./service.properties** & **./cam.properties**, making amendments as required
* Review this information: https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
* Review the python code in the directory **./lib**
* Review the html file in the directory **./site**
