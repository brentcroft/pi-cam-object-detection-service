#!/bin/bash
set -e


object_detection_archive="models.zip"
title="TensorFlow Object Detection"

if [ ! -f $object_detection_archive ]; then
    echo "${title} archive not found: ${object_detection_archive}"
    
    wget -nc https://github.com/tensorflow/models/archive/master.zip
    mv master.zip $object_detection_archive
fi


#
install_dir="tfod_install"

if [ ! -d $install_dir ]; then
    mkdir $install_dir
fi

if [ ! -d $install_dir/models-master/research ]; then
    # copy and unpack the tensorflow models archive
    unzip $object_detection_archive -d $install_dir/
else
    echo "${title} archive already unpacked."
fi

cd ~/$install_dir/models-master/research


echo "${title} compiling proto files..."

FILES=object_detection/protos/*.proto
for f in $FILES
do
  echo " compiling: ${f}"
  protoc $f --python_out=.
done



echo "${title}: building..."

echo " building object_detection egg..."
python3 setup.py build

echo " installing object_detection egg..."
sudo python3 setup.py install

echo "${title} installed. (python3)"



echo "${title} SLIM: building..."

cd ~/$install_dir/models-master/research/slim

echo " building slim egg..."
python3 setup.py build

echo " installing slim egg..."
sudo python3 setup.py install

echo "${title} SLIM installed (python3)"
