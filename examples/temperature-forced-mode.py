#!/usr/bin/env python

import time

from smbus2 import SMBus

from bme280 import BME280

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Set up in "forced" mode
# In this mode `get_temperature` and `get_pressure` will trigger
# a new reading and wait for the result.
# The chip will return to sleep mode when finished.
bme280.setup(mode="forced")

while True:
    temperature = bme280.get_temperature()
    print(f"{temperature:05.2f}°C")
    time.sleep(1)
