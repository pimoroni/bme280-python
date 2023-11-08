TEST_TEMP_RAW = 529191
TEST_TEMP_CMP = 24.7894877676

TEST_PRES_RAW = 326816
TEST_PRES_CMP = 1006.61517564
TEST_ALT_CMP = 55.385

TEST_HUM_RAW = 30281
TEST_HUM_CMP = 68.66996648709039


def test_temperature():
    from calibration import BME280Calibration
    from tools import SMBusFakeDevice

    from bme280 import BME280

    dev = SMBusFakeDevice(1)

    # Load the fake temperature into the virtual registers
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup()

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_temperature(), 4) == round(TEST_TEMP_CMP, 4)


def test_temperature_forced():
    from calibration import BME280Calibration
    from tools import SMBusFakeDevice

    from bme280 import BME280

    dev = SMBusFakeDevice(1)

    # Load the fake temperature into the virtual registers
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup(mode="forced")

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_temperature(), 4) == round(TEST_TEMP_CMP, 4)


def test_pressure():
    from calibration import BME280Calibration
    from tools import SMBusFakeDevice

    from bme280 import BME280

    dev = SMBusFakeDevice(1)

    # Load the fake temperature values into the virtual registers
    # Pressure is temperature compensated!!!
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake pressure values
    dev.regs[0xF9] = (TEST_PRES_RAW & 0x0000F) << 4
    dev.regs[0xF8] = (TEST_PRES_RAW & 0x00FF0) >> 4
    dev.regs[0xF7] = (TEST_PRES_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup()

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_pressure(), 4) == round(TEST_PRES_CMP, 4)


def test_altitude():
    from calibration import BME280Calibration
    from tools import SMBusFakeDevice

    from bme280 import BME280

    dev = SMBusFakeDevice(1)

    # Load the fake temperature values into the virtual registers
    # Pressure is temperature compensated!!!
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake pressure values
    dev.regs[0xF9] = (TEST_PRES_RAW & 0x0000F) << 4
    dev.regs[0xF8] = (TEST_PRES_RAW & 0x00FF0) >> 4
    dev.regs[0xF7] = (TEST_PRES_RAW & 0xFF000) >> 12

    bme280 = BME280(i2c_dev=dev)
    bme280.setup()

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_altitude(), 4) == round(TEST_ALT_CMP, 4)


def test_humidity():
    from calibration import BME280Calibration
    from tools import SMBusFakeDevice

    from bme280 import BME280

    dev = SMBusFakeDevice(1)

    # Load the fake temperature values into the virtual registers
    # Humidity is temperature compensated!!!
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake humidity values
    dev.regs[0xFD] = TEST_HUM_RAW >> 8
    dev.regs[0xFE] = TEST_HUM_RAW & 0xFF

    bme280 = BME280(i2c_dev=dev)
    bme280.setup()

    # Replace the loaded calibration with our known values
    bme280.calibration = BME280Calibration()

    assert round(bme280.get_humidity(), 4) == round(TEST_HUM_CMP, 4)
