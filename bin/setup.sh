#!/bin/bash
counter=0
export AMPY_PORT=/dev/cu.usbmodem1234561

while [ ! -e /dev/cu.usbmodem01 ]; do
    sleep 1
    counter=$((counter + 1))
    echo "Waiting for ESP32...."
    if [ $counter -ge 50 ]; then
        echo "Device not found"
        exit 1
    fi
done


esptool.py --chip esp32s2 --port /dev/cu.usbmodem01 --after no_reset erase_flash
sleep 1
esptool.py --chip esp32s2 --port /dev/cu.usbmodem01 --after no_reset write_flash -z 0x1000 ./firmware/LOLIN_S2_MINI-20220117-v1.18.bin 
sleep 1

echo "Press reset button on esp32"

counter=0

while [ ! -e $AMPY_PORT ]; do
    sleep 1
    counter=$((counter + 1))
    echo "Waiting for reset..."
    if [ $counter -ge 50 ]; then
        exit 1
    fi
done

echo "Upoading libs"
ampy put src/lib lib
sleep 1

echo "Uploading runtime config"
ampy put src/config.txt config.txt
sleep 1

echo "Uploading secrets"
ampy put src/secrets.py secrets.py

sleep 1
echo "Uploading main script"

ampy put src/main.py main.py
echo "All done!"
exit 0