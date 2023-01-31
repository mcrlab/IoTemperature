from machine import SoftI2C, Pin, unique_id, deepsleep
from sht30 import SHT30
from time import sleep
from network import WLAN
import urequests
from binascii import hexlify
from secrets import HOST,DB,SSID, PASSWORD


i2c=SoftI2C(sda=Pin(33), scl=Pin(35))
sht= SHT30(i2c=i2c, i2c_address=69)
led = Pin(15, Pin.OUT)

def connect_to_wifi():
    wlan = WLAN(0)
    wlan.active(True)
    sleep(1.0)
    if not wlan.isconnected():
        print("Connecting to {0}".format(SSID))
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():    
            sleep(1.0)
            pass

    print("IP: {0}".format(wlan.ifconfig()[0])) 
    sleep(1.0)

def get_location():
    try:
        file = open("config.txt","R")
        name = file.read()
        file.close()
        return name
    except e:
        return hexlify(unique_id()).decode()

def read_and_post():
    led.value(1)
    location_id = get_location()
    print("Using location id: {0}".format(location_id))
    temperature, humidity = sht.measure()
    print("Temperature: {0}c".format(temperature))
    print("Humitidy: {0}".format(humidity))
    
    r = urequests.post("http://{0}:8086/write?db={1}".format(HOST, DB), data="temperature,location=\"{0}\" value={1}".format(location_id, temperature))
    print(r.status_code)
    r.close()
    
    r = urequests.post("http://{0}:8086/write?db={1}".format(HOST, DB), data="humidity,location=\"{0}\" value={1}".format(location_id, humidity))
    print(r.status_code)
    r.close()
    print("Done")
    led.value(0)
    
    
def main():
    should_sleep = True
    
    try:
        connect_to_wifi()
        read_and_post()
    except Exception as e:
        should_sleep = False
        sleep(10)
        print(e)

    finally:
        if should_sleep:
            print("Deep sleeping in 10 seconds")
            sleep(10)
            deepsleep(30000)

if __name__ == '__main__':
    main()
    
