# pi-cam-object-detection-service

This kit provides the Pi Cam Object Detection Service.

The service is designed to run 24x7 on a Pi with a camera, and to produce output suitable for ground truth harvesting.

The images for the following video (made using https://ezgif.com/optimize) demonstrate the key features:

![demo](eb_12_v08_480x270_01c_500k-20.gif)

Typically the output would be cropped to the detection frame, but here it's shown raw to demonstrate detection frame tracking within the camera resolution.
NB: During the video, the minimum score thresholds for some of the classes are modified.


Please note that the kit requires the download of an appropriate Pi Tensorflow wheel, see: https://github.com/lhelontra/tensorflow-on-arm/releases.

A sample SSD Mobilenet PPN graph is provided as an arbitrary working example.

Other SSD MobileNet graphs are available from:

    https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

See the readme files in "./install" and "./kit" for further information