"""First normal-mode read must wait for a conversion, rather than reset data."""

import struct

import pytest
from calibration import BME280Calibration
from i2cdevice import MockSMBus
from test_compensation import TEST_HUM_RAW, TEST_PRES_CMP, TEST_PRES_RAW, TEST_TEMP_RAW


class ConvertingDevice(MockSMBus):
    def __init__(self, clock, conversion_seconds):
        super().__init__(1)
        self.clock = clock
        self.conversion_seconds = conversion_seconds
        self.ready_at = None
        self.regs[0xD0] = 0x60
        calibration = BME280Calibration()
        fields = [
            calibration.dig_t1,
            calibration.dig_t2,
            calibration.dig_t3,
            calibration.dig_p1,
            calibration.dig_p2,
            calibration.dig_p3,
            calibration.dig_p4,
            calibration.dig_p5,
            calibration.dig_p6,
            calibration.dig_p7,
            calibration.dig_p8,
            calibration.dig_p9,
        ]
        self.regs[0x88:0xA0] = struct.pack("<HhhHhhhhhhhh", *fields)
        self.regs[0xA1] = calibration.dig_h1
        self.regs[0xE1:0xE8] = struct.pack(
            "<hBBBBb", calibration.dig_h2, calibration.dig_h3, calibration.dig_h4 >> 4, (calibration.dig_h5 & 15) << 4 | (calibration.dig_h4 & 15), calibration.dig_h5 >> 4, calibration.dig_h6
        )
        # Datasheet reset values: temperature/pressure 0x80000, humidity 0x8000.
        self.regs[0xF7:0xFF] = bytes.fromhex("8000008000008000")

    def write_i2c_block_data(self, address, register, values):
        super().write_i2c_block_data(address, register, values)
        if register == 0xF4 and values[0] & 3 == 3:
            self.ready_at = self.clock[0] + self.conversion_seconds

    def read_i2c_block_data(self, address, register, length):
        if register == 0xF7 and self.ready_at is not None and self.clock[0] + 1e-12 >= self.ready_at:
            self.regs[0xF7:0xFF] = (TEST_PRES_RAW << 4).to_bytes(3, "big") + (TEST_TEMP_RAW << 4).to_bytes(3, "big") + TEST_HUM_RAW.to_bytes(2, "big")
        return super().read_i2c_block_data(address, register, length)


# Maximum conversion times from Bosch BME280 datasheet, section 9.1.
@pytest.mark.parametrize("oversampling,conversion_seconds", [(1, 0.0093), (16, 0.1128)])
def test_first_normal_measurement(bme280, monkeypatch, oversampling, conversion_seconds):
    clock = [0.0]
    monkeypatch.setattr(bme280.time, "sleep", lambda duration: clock.__setitem__(0, clock[0] + duration))
    bus = ConvertingDevice(clock, conversion_seconds)
    sensor = bme280.BME280(i2c_dev=bus)
    sensor.setup(temperature_oversampling=oversampling, pressure_oversampling=oversampling, humidity_oversampling=oversampling)
    assert sensor.get_pressure() == pytest.approx(TEST_PRES_CMP)
    elapsed = clock[0]
    assert sensor.get_pressure() == pytest.approx(TEST_PRES_CMP)
    assert clock[0] == elapsed  # No extra delay for subsequent normal-mode reads.


def test_implicit_setup_waits_for_first_measurement(bme280, monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(bme280.time, "sleep", lambda duration: clock.__setitem__(0, clock[0] + duration))
    sensor = bme280.BME280(i2c_dev=ConvertingDevice(clock, 0.1128))
    assert sensor.get_pressure() == pytest.approx(TEST_PRES_CMP)


def test_forced_setup_does_not_start_a_conversion(bme280, monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(bme280.time, "sleep", lambda duration: clock.__setitem__(0, clock[0] + duration))
    bus = ConvertingDevice(clock, 0.1128)
    sensor = bme280.BME280(i2c_dev=bus)
    sensor.setup(mode="forced")
    assert bus.ready_at is None
    assert clock[0] == pytest.approx(0.1)  # Existing reset delay only.
