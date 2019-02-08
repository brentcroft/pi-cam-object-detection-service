# Summary
Take a crop from each camera image and submit it to the Object Detection graph.
Store any detection results and the images to which they relate.
Maybe create boxed images.

Review this information: https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes

Review the file "cam.properties" and make amendmednts as required.

Disable the service by setting SUSPENDED=1 in "service.properties"

Start and stop the service manualy, by running the scripts:

    start-service.sh
    stop-service.sh


Review the python code in the directory *./lib*.


