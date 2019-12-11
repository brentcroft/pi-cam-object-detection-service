
# power saving
# see: https://www.raspberrypi.org/forums/viewtopic.php?t=208110


sudo tvservice --off
echo 0 | sudo tee /sys/devices/platform/soc/3f980000.usb/buspower >/dev/null

sudo ifconfig eth0 down

sudo systemctl disable bluetooth
sudo service bluetooth stop
sudo systemctl disable hciuart
sudo service  hciuart stop

