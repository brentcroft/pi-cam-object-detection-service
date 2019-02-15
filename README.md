# pi-cam-object-detection-service

The Pi Cam Object Detection Service is intended to run 24x7 on a Pi with a camera, 
to survive restarts, 
and to produce output suitable for ground truth harvesting, 
i.e. detection files in PASCAL VOC XML, associated image files, and optionally, boxed image files.

The following animation demonstrates the key features.
Typically the output would be cropped to the detection frame, but here it's shown raw to demonstrate detection frame tracking within the camera resolution.

![demo](eb_12_v08_480x270_01c_500k-20.gif)

To construct the animation, having printed out and located the animals (see: **sample-bird-prints.doc**), the following properties were set (see: **./cam/cam.properties**):

    CAMERA_RESOLUTION=[ 720, 405 ]
    DETECTION_APERTURE=[ 480, 270 ]
    DETECTION_MIN_SCORE=0.4
    DETECTION_CLASS_MIN_SCORE={'mouse':0.2}  
    CURRENT_IMAGE_RAW=True 
    CALENDAR_IMAGE_STORE=/demo
    CALENDAR_DETECTION_STORE=/demo
    CALENDAR_IMAGE_RAW=True

Note that:
-  The actual detection frame rate was ~ 0.4 images/second
-  Towards the end of the animation, minimum score thresholds for some of the classes were increased to 0.999, then to zero, and then back to 0.4.

The boxed image files were collected from **/demo**, appended into an animated GIF, and then the GIF was compressed using the tool at https://ezgif.com/optimize.

See the readme file in **./kit** for further information.


## Please Note
This kit has been tested on multiple **Pi 3 B+s** & **Pi 3 Bs**, with **Raspian Stretch Lite 2018-11-13** and **Camera Module V2**.

This kit requires the download of an appropriate Pi Tensorflow wheel, see: https://github.com/lhelontra/tensorflow-on-arm/releases.

A sample custom SSD Mobilenet PPN graph is provided as an arbitrary working example, 
however, other SSD MobileNet graphs are available: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

This kit has been tried on **Pi 3 B+s** & **Pi 3 Bs** with the following graphs from the detection model zoo (using the same properties as above):

| Graph | File Size | Seconds / Image | Images / Second |
|---|---|---|---|
| ssd_mobilenet_v1_0.75_depth_300x300_coco14_sync_2018_07_03               | 18m | 1.8 | 0.55 | 
| ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03 | 50m | Fails | | 
| ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03 | 11m | 2.0 | 0.49 |
| ssd_mobilenet_v2_coco_2018_03_29                                         | 68m | Fails | |
| ssdlite_mobilenet_v2_coco_2018_05_09                                     | 20m | 2.2 | 0.47 | 
