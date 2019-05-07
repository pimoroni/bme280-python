TEST_TEMP_RAW = 529191
TEST_TEMP_CMP = 24.7894877676

TEST_PRES_RAW = 326816
TEST_PRES_CMP = 1006.61517564
TEST_ALT_CMP = 55.385


def test_temperature():
    from tools import SMBusFakeDevice
    from bme280 import BME280
    from calibration import BME280Calibration
    dev = SMBusFakeDevice(1)

    # Load the fake temperature into the virtual registers
    dev.regs[0xfc] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xfb] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xfa] = (TEST_TEMP_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup()

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_temperature(), 4) == round(TEST_TEMP_CMP, 4)


def test_temperature_forced():
    from tools import SMBusFakeDevice
    from bme280 import BME280
    from calibration import BME280Calibration
    dev = SMBusFakeDevice(1)

    # Load the fake temperature into the virtual registers
    dev.regs[0xfc] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xfb] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xfa] = (TEST_TEMP_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup(mode="forced")

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_temperature(), 4) == round(TEST_TEMP_CMP, 4)


def test_pressure():
    from tools import SMBusFakeDevice
    from bme280 import BME280
    from calibration import BME280Calibration
    dev = SMBusFakeDevice(1)

    # Load the fake temperature values into the virtual registers
    # Pressure is temperature compensated!!!
    dev.regs[0xfc] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xfb] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xfa] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake pressure values
    dev.regs[0xf9] = (TEST_PRES_RAW & 0x0000F) << 4
    dev.regs[0xf8] = (TEST_PRES_RAW & 0x00FF0) >> 4
    dev.regs[0xf7] = (TEST_PRES_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup()

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_pressure(), 4) == round(TEST_PRES_CMP, 4)


def test_altitude():
    from tools import SMBusFakeDevice
    from bme280 import BME280
    from calibration import BME280Calibration
    dev = SMBusFakeDevice(1)

    # Load the fake temperature values into the virtual registers
    # Pressure is temperature compensated!!!
    dev.regs[0xfc] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xfb] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xfa] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake pressure values
    dev.regs[0xf9] = (TEST_PRES_RAW & 0x0000F) << 4
    dev.regs[0xf8] = (TEST_PRES_RAW & 0x00FF0) >> 4
    dev.regs[0xf7] = (TEST_PRES_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup()

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_altitude(), 4) == round(TEST_ALT_CMP, 4)
