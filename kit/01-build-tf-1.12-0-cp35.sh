#!/bin/bash
set -e

# clean start
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get autoremove -y
sudo apt-get autoclean -y

# and again
sudo apt-get update -y

#
sudo apt-get install -y --no-install-recommends \
	libblas-dev liblapack-dev python3-dev \
	libatlas-base-dev gfortran python3-setuptools



# and again
sudo apt-get update -y

# used to install tfOD
sudo apt-get install -y unzip

sudo apt-get install -y dos2unix

sudo apt-get install -y protobuf-compiler python3-pil python3-lxml python3-tk
sudo apt-get install -y python-opencv


# ensure pip3
sudo apt-get install -y python3-pip

# and again
sudo apt-get update -y

sudo pip3 install matplotlib

# see: https://github.com/lhelontra/tensorflow-on-arm/releases
sudo pip3 install tensorflow-1.12.0-cp35-none-linux_armv7l.whl


# and again
sudo apt-get update -y
sudo apt-get upgrade -y

sudo pip3 install datetime
sudo pip3 install picamera



# and again
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get autoremove
sudo apt-get autoclean


# prepare cam scripts
sudo dos2unix ./cam/*.sh
sudo chmod +x ./cam/*.sh


# maybe set a crontab for auto start
#
# crontab
# * * * * * /home/pi/cam/run-from-cron.sh

# maybe set a ram drive for current images
#
# sudo mkdir /cam-ram
# sudo nano /etc/fstab
# tmpfs /cam-ram  tmpfs defaults,noatime 0 0
