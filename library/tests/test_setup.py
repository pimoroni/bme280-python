import sys
import mock
import pytest


def test_setup_not_present():
    sys.modules['smbus'] = mock.MagicMock()
    from bme280 import BME280
    bme280 = BME280()
    with pytest.raises(RuntimeError):
        bme280.setup()


def test_setup_mock_present():
    from tools import SMBusFakeDevice
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from bme280 import BME280
    bme280 = BME280()
    bme280.setup()


def test_setup_forced_mode():
    from tools import SMBusFakeDevice
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from bme280 import BME280
    bme280 = BME280()
    bme280.setup(mode="forced")
