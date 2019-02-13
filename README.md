# pi-cam-object-detection-service

This kit provides the Pi Cam Object Detection Service. 
The service is designed to run 24x7 on a Pi with a camera, to survive restarts, and to produce output suitable for ground truth harvesting.

The following animation demonstrates the key features.
Typically the output would be cropped to the detection frame, but here it's shown raw to demonstrate detection frame tracking within the camera resolution.

![demo](eb_12_v08_480x270_01c_500k-20.gif)

To construct the animation, having printed out and located the animals (see: **sample-bird-prints.doc**), the following settings were used (see: **./cam/cam.properties**):

    CAMERA_RESOLUTION=[ 720, 405 ]
    DETECTION_APERTURE=[ 480, 270 ]
    DETECTION_MIN_SCORE=0.4
    DETECTION_CLASS_MIN_SCORE={'mouse':0.2}  
    CURRENT_IMAGE_RAW=True 
    CALENDAR_IMAGE_STORE=/demo
    CALENDAR_DETECTION_STORE=/demo
    CALENDAR_IMAGE_RAW=True
    
Towards the end of the animation, minimum score thresholds for some of the classes were increased to 0.999, then to zero, and then back to 0.4 
(configuration is refreshed on every cycle).

The boxed images were collected from **/demo** and then compressed into an animation (using https://ezgif.com/optimize).


## Please Note
The kit requires the download of an appropriate Pi Tensorflow wheel, see: https://github.com/lhelontra/tensorflow-on-arm/releases.

One sample SSD Mobilenet PPN graph is provided as an arbitrary working example.

Other SSD MobileNet graphs are available from: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

See the readme file in **./kit** for further information.