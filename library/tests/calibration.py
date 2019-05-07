import bme280


class BME280Calibration(bme280.BME280Calibration):
    """Prefil the calibration class with known values."""
    def __init__(self):
        bme280.BME280Calibration.__init__(self)

        self.dig_t1 = 28009
        self.dig_t2 = 25654
        self.dig_t3 = 50

        self.dig_p1 = 39145
        self.dig_p2 = -10750
        self.dig_p3 = 3024
        self.dig_p4 = 5667
        self.dig_p5 = -120
        self.dig_p6 = -7
        self.dig_p7 = 15500
        self.dig_p8 = -14600
        self.dig_p9 = 6000
