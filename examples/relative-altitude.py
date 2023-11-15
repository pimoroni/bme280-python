#!/usr/bin/env python

import time

from smbus2 import SMBus

from bme280 import BME280

print(
    """relative-altitude.py - Calculates relative altitude from pressure.

Press Ctrl+C to exit!

"""
)

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

baseline_values = []
baseline_size = 100

print(f"Collecting baseline values for {baseline_size:d} seconds. Do not move the sensor!\n")

# Collect some values to calculate a baseline pressure
for i in range(baseline_size):
    pressure = bme280.get_pressure()
    baseline_values.append(pressure)
    time.sleep(1)

# Calculate average baseline
baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])

while True:
    altitude = bme280.get_altitude(qnh=baseline)
    print(f"Relative altitude: {altitude:05.2f} metres")
    time.sleep(1)
