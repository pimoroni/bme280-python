import time

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280


bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

baseline_values = []
baseline_size = 100

print("Collecting baseline values for {:d} seconds. Do not move the sensor!\n".format(baseline_size))

for i in range(baseline_size):
    pressure = bme280.get_pressure()
    baseline_values.append(pressure)
    time.sleep(1)

baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])

while True:
    altitude = bme280.get_altitude(qnh=baseline)
    print('Relative altitude: {:05.2f} metres'.format(altitude))
    time.sleep(1)
