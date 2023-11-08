import pytest


def test_setup_not_present(smbus2_mock, bme280):
    dev = smbus2_mock.SMBus(1)
    dev.regs[0xD0] = 0x00  # Incorrect chip ID

    sensor = bme280.BME280(i2c_dev=dev)
    with pytest.raises(RuntimeError):
        sensor.setup()


def test_setup_mock_present(smbus2_mock, bme280):
    sensor = bme280.BME280()
    sensor.setup()


def test_setup_forced_mode(smbus2_mock, bme280):

    sensor = bme280.BME280()
    sensor.setup(mode="forced")
