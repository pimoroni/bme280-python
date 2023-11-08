TEST_TEMP_RAW = 529191
TEST_TEMP_CMP = 24.7894877676

TEST_PRES_RAW = 326816
TEST_PRES_CMP = 1006.61517564
TEST_ALT_CMP = 55.385

TEST_HUM_RAW = 30281
TEST_HUM_CMP = 68.66996648709039


def test_temperature(smbus2_mock, bme280):
    from calibration import BME280Calibration

    dev = smbus2_mock.SMBus(1)

    # Load the fake temperature into the virtual registers
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    sensor = bme280.BME280(i2c_dev=dev)
    sensor.setup()

    # Replace the loaded calibration with our known values
    sensor.calibration = BME280Calibration()

    assert round(sensor.get_temperature(), 4) == round(TEST_TEMP_CMP, 4)


def test_temperature_forced(smbus2_mock, bme280):
    from calibration import BME280Calibration

    dev = smbus2_mock.SMBus(1)

    # Load the fake temperature into the virtual registers
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    sensor = bme280.BME280(i2c_dev=dev)
    sensor.setup(mode="forced")

    # Replace the loaded calibration with our known values
    sensor.calibration = BME280Calibration()

    assert round(sensor.get_temperature(), 4) == round(TEST_TEMP_CMP, 4)


def test_pressure(smbus2_mock, bme280):
    from calibration import BME280Calibration

    dev = smbus2_mock.SMBus(1)

    # Load the fake temperature values into the virtual registers
    # Pressure is temperature compensated!!!
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake pressure values
    dev.regs[0xF9] = (TEST_PRES_RAW & 0x0000F) << 4
    dev.regs[0xF8] = (TEST_PRES_RAW & 0x00FF0) >> 4
    dev.regs[0xF7] = (TEST_PRES_RAW & 0xFF000) >> 12

    sensor = bme280.BME280(i2c_dev=dev)
    sensor.setup()

    # Replace the loaded calibration with our known values
    sensor.calibration = BME280Calibration()

    assert round(sensor.get_pressure(), 4) == round(TEST_PRES_CMP, 4)


def test_altitude(smbus2_mock, bme280):
    from calibration import BME280Calibration

    dev = smbus2_mock.SMBus(1)

    # Load the fake temperature values into the virtual registers
    # Pressure is temperature compensated!!!
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake pressure values
    dev.regs[0xF9] = (TEST_PRES_RAW & 0x0000F) << 4
    dev.regs[0xF8] = (TEST_PRES_RAW & 0x00FF0) >> 4
    dev.regs[0xF7] = (TEST_PRES_RAW & 0xFF000) >> 12

    sensor = bme280.BME280(i2c_dev=dev)
    sensor.setup()

    # Replace the loaded calibration with our known values
    sensor.calibration = BME280Calibration()

    assert round(sensor.get_altitude(), 4) == round(TEST_ALT_CMP, 4)


def test_humidity(smbus2_mock, bme280):
    from calibration import BME280Calibration

    dev = smbus2_mock.SMBus(1)

    # Load the fake temperature values into the virtual registers
    # Humidity is temperature compensated!!!
    dev.regs[0xFC] = (TEST_TEMP_RAW & 0x0000F) << 4
    dev.regs[0xFB] = (TEST_TEMP_RAW & 0x00FF0) >> 4
    dev.regs[0xFA] = (TEST_TEMP_RAW & 0xFF000) >> 12

    # Load the fake humidity values
    dev.regs[0xFD] = TEST_HUM_RAW >> 8
    dev.regs[0xFE] = TEST_HUM_RAW & 0xFF

    sensor = bme280.BME280(i2c_dev=dev)
    sensor.setup()

    # Replace the loaded calibration with our known values
    sensor.calibration = BME280Calibration()

    assert round(sensor.get_humidity(), 4) == round(TEST_HUM_CMP, 4)
