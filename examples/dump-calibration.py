#!/usr/bin/env python


from smbus2 import SMBus

from bme280 import BME280

print(
    """dump-calibration.py - Dumps calibration data.

Press Ctrl+C to exit!

"""
)

# Initialise the BME280
bme280 = BME280(i2c_dev=SMBus(1))
bme280.setup()

for key in dir(bme280.calibration):
    if key.startswith("dig_"):
        value = getattr(bme280.calibration, key)
        print(f"{key} = {value}")
