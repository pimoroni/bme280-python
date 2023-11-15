#!/usr/bin/env python

import time
from subprocess import PIPE, Popen

from smbus2 import SMBus

from bme280 import BME280

print(
    """compensated-temperature.py - Use the CPU temperature to compensate temperature
readings from the BME280 sensor. Method adapted from Initial State's Enviro pHAT
review: https://medium.com/@InitialState/tutorial-review-enviro-phat-for-raspberry-pi-4cd6d8c63441

Press Ctrl+C to exit!

"""
)

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


# Gets the CPU temperature in degrees C
def get_cpu_temperature():
    process = Popen(["vcgencmd", "measure_temp"], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()
    return float(output[output.index("=") + 1 : output.rindex("'")])


factor = 0.6  # Smaller numbers adjust temp down, vice versa
smooth_size = 10  # Dampens jitter due to rapid CPU temp changes

cpu_temps = []

while True:
    cpu_temp = get_cpu_temperature()
    cpu_temps.append(cpu_temp)

    if len(cpu_temps) > smooth_size:
        cpu_temps = cpu_temps[1:]

    smoothed_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    comp_temp = raw_temp - ((smoothed_cpu_temp - raw_temp) / factor)

    print(f"Raw: {raw_temp:05.2f}°C, Compensated: {comp_temp:05.2f}°C")

    time.sleep(1.0)
