#!/usr/bin/env python

import time
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

print("""temperature-compare.py - Compares oversampling levels
(requires two BME280s with different addresses).

Press Ctrl+C to exit!

""")

# Initialise the BME280
bus = SMBus(1)
bme280A = BME280(i2c_dev=bus)
bme280B = BME280(i2c_dev=bus, i2c_addr=0x77)

# Set up in "forced" mode
# In this mode `get_temperature` and `get_pressure` will trigger
# a new reading and wait for the result.
# The chip will return to sleep mode when finished.
bme280A.setup(mode="normal", temperature_oversampling=1, pressure_oversampling=1)
bme280B.setup(mode="normal", temperature_oversampling=16, pressure_oversampling=16)

while True:
    temperatureA = bme280A.get_temperature()
    temperatureB = bme280B.get_temperature()
    print('Forced: {:05.2f}*C Normal: {:05.2f}*C D: {:05.2f}'.format(temperatureA, temperatureB, abs(temperatureA - temperatureB)))
    time.sleep(1)
