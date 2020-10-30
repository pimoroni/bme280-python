#!/usr/bin/env python

import time

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

print("""local_altitude.py -
Allows you to correct the QNH for your local area.
Do not rely on this approximation for landing planes.
Press Ctrl+C to exit!
""")

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# asks the user for their local QNH value and confirms it
local_qnh = input("""Please enter your local QNH value.
You can find this by searching for a local METAR on the internet.
>""")
print("You have told us the QNH is", local_qnh)

# converts the input into a floating point number
local_qnh = float(local_qnh)
time.sleep(1)

# workaround to get rid of the first reading
altitude = bme280.get_altitude()
print("Waiting a couple of seconds for the sensor to initialise...")
time.sleep(2)

while True:
    altitude = bme280.get_altitude(qnh=local_qnh)
    print(round(altitude), "metres above sea level")
    time.sleep(2)
