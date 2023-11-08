import sys

import mock
import pytest
from i2cdevice import MockSMBus


class SMBusFakeDevice(MockSMBus):
    def __init__(self, i2c_bus):
        MockSMBus.__init__(self, i2c_bus)
        self.regs[0xD0] = 0x60  # Fake chip ID


@pytest.fixture(scope="function", autouse=False)
def bme280():
    import bme280
    yield bme280
    del sys.modules["bme280"]


@pytest.fixture(scope="function", autouse=False)
def smbus2_mock():
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules["smbus2"] = smbus
    yield smbus
    del sys.modules["smbus2"]


@pytest.fixture(scope="function", autouse=False)
def smbus2():
    smbus = mock.Mock()
    sys.modules["smbus2"] = smbus
    yield smbus
    del sys.modules["smbus2"]
