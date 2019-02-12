



# map a RAM drive for dynamic storage
ram_drive_dir=/cam_ram

if [ ! -d /$ram_drive_dir ]; then
    sudo mkdir /$ram_drive_dir
fi


# sudo nano /etc/fstab
# tmpfs /class-cam  tmpfs defaults,noatime 0 0