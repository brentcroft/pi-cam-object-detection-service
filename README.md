# pi-cam-object-detection-service

The Pi Cam Object Detection Service is intended to run 24x7 on a Pi with a camera, to survive restarts, and to produce output suitable for ground truth harvesting.

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

The boxed image files were collected from **/demo**, and then compressed into an animation (using https://ezgif.com/optimize).

See the readme file in **./kit** for further information.


## Please Note
This kit has been tested only on multiple **Pi 3 B+s** with **Raspian Stretch Lite 2018-11-13** and **Camera Module V2**.

This kit requires the download of an appropriate Pi Tensorflow wheel, see: https://github.com/lhelontra/tensorflow-on-arm/releases.

One sample SSD Mobilenet PPN graph is provided as an arbitrary working example.

Other SSD MobileNet graphs are available: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md


This kit has been tested with the following graphs (suning same properties as above):

| Graph | File Size | Seconds/Image | Images/Second |
|---|---|---|---|
| ssd_mobilenet_v1_0.75_depth_300x300_coco14_sync_2018_07_03               | 18m | 1.8 s/i | 0.55 i/s | 
| ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03 | 50m | Fails   | Doesn't start | 
| ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03 | 11m | 2.0 s/i | 0.49 i/s |
| ssd_mobilenet_v2_coco_2018_03_29                                         | 68m | Fails | std::bad_alloc |
| ssdlite_mobilenet_v2_coco_2018_05_09                                     | 20m | 2.2 s/i | 0.47 i/s | 


To run the service with another graph:

1. Create a new directory in **./cam/** named for the graph.
> The name of the directory is the "graph signature" and is referenced by the GRAPH property in **./cam/cam.properties**.

2. Copy the frozen graph and labels file into the folder.
>The frozen graph must have the filename **frozen_inference_graph.pb**.
>The labels file must have the name **object-detection.pbtxt**.
>Determine the number of output categories in the graph.

3. Modify **./cam/cam.properties** accordingly.
>The property GRAPH must refer to the graph directory.
>The property GRAPH_NUM_CLASSES must be the number of categories in the graph.

4. Restart the service


