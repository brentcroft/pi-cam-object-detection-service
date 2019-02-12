# Summary

The service performs the following sequence continually:

* Take a camera image.
* Take a crop from the image and submit it to the Object Detection graph.
* Store any detection results and the images to which they relate.
* Maybe create boxed images.
* Maybe adjust the crop frame.

Review this information: https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes


The camera will take images at the resolution specified by CAM_IMAGE_RESOLUTION. 
If DETECTION_APERTURE is smaller, then it can be adjusted within CAM_IMAGE_RESOLUTION by the box tracker.

If BOX_TRACKER is True then:
1. If objects are detected the DETECTION_APERTURE is moved towards the centre of the detected boxes 
2. If no objects are detected the DETECTION_APERTURE is moved back towards the centre of the camera image.
 
Review the file "cam.properties" and make amendments as required.

NB: CURRENT_IMAGE_STORE must be set to a location where the service can write files.

Disable the service by setting SUSPENDED=1 in "service.properties"

Start and stop the service manually, by running the scripts:

    start-service.sh
    stop-service.sh


Review the python code in the directory *./lib*.


