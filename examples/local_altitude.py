#!/usr/bin/env python

import time

from smbus2 import SMBus

from bme280 import BME280

print(
    """local_altitude.py -
Allows you to correct the QNH for your local area.
Do not rely on this approximation for landing planes.
Press Ctrl+C to exit!
"""
)

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# asks the user for their local QNH value and confirms it
local_qnh = input(
    """Please enter your local QNH value (air pressure at the mean sea level).

You can find this by searching for a local METAR report,
    eg: "Cambridge METAR"

And looking for the number prefixed with a "Q",
    eg: Q1015
>"""
)

# remove a Q prefix if there is one
if local_qnh.startswith("Q") or local_qnh.startswith("q"):
    local_qnh = local_qnh[1:]

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
    print(f"{altitude:0.0f} metres above sea level")
    time.sleep(2)
