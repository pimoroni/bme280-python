"""BME280 Driver."""
from i2cdevice import Device, Register, BitField, _int_to_bytes
from i2cdevice.adapter import LookupAdapter, Adapter
import struct
import time


__version__ = '0.1.1'

CHIP_ID = 0x60
I2C_ADDRESS_GND = 0x76
I2C_ADDRESS_VCC = 0x77


class S8Adapter(Adapter):
    """Convert unsigned 8bit integer to signed."""

    def _decode(self, value):
        if value & (1 << 7):
            value -= 1 << 8
        return value


class S16Adapter(Adapter):
    """Convert unsigned 16bit integer to signed."""

    def _decode(self, value):
        return struct.unpack('<h', _int_to_bytes(value, 2))[0]


class U16Adapter(Adapter):
    """Convert from bytes to an unsigned 16bit integer."""

    def _decode(self, value):
        return struct.unpack('<H', _int_to_bytes(value, 2))[0]


class H5Adapter(S16Adapter):
    def _decode(self, value):
        b = _int_to_bytes(value, 2)
        r = ((b[0] >> 4) & 0x0F) | (b[1] << 4)
        if r & (1 << 11):
            r = r - 1 << 12
        return r


class H4Adapter(S16Adapter):
    def _decode(self, value):
        b = _int_to_bytes(value, 2)
        r = (b[0] << 4) | (b[1] & 0x0F)
        if r & (1 << 11):
            r = r - 1 << 12
        return r


class BME280Calibration():
    def __init__(self):
        self.dig_t1 = 0
        self.dig_t2 = 0
        self.dig_t3 = 0

        self.dig_p1 = 0
        self.dig_p2 = 0
        self.dig_p3 = 0
        self.dig_p4 = 0
        self.dig_p5 = 0
        self.dig_p6 = 0
        self.dig_p7 = 0
        self.dig_p8 = 0
        self.dig_p9 = 0

        self.dig_h1 = 0.0
        self.dig_h2 = 0.0
        self.dig_h3 = 0.0
        self.dig_h4 = 0.0
        self.dig_h5 = 0.0
        self.dig_h6 = 0.0

        self.temperature_fine = 0

    def set_from_namedtuple(self, value):
        # Iterate through a tuple supplied by i2cdevice
        # and copy its values into the class attributes
        for key in self.__dict__.keys():
            try:
                setattr(self, key, getattr(value, key))
            except AttributeError:
                pass

    def compensate_temperature(self, raw_temperature):
        var1 = (raw_temperature / 16384.0 - self.dig_t1 / 1024.0) * self.dig_t2
        var2 = raw_temperature / 131072.0 - self.dig_t1 / 8192.0
        var2 = var2 * var2 * self.dig_t3
        self.temperature_fine = (var1 + var2)
        return self.temperature_fine / 5120.0

    def compensate_pressure(self, raw_pressure):
        var1 = self.temperature_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self.dig_p6 / 32768.0
        var2 = var2 + var1 * self.dig_p5 * 2
        var2 = var2 / 4.0 + self.dig_p4 * 65536.0
        var1 = (self.dig_p3 * var1 * var1 / 524288.0 + self.dig_p2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_p1
        pressure = 1048576.0 - raw_pressure
        pressure = (pressure - var2 / 4096.0) * 6250.0 / var1
        var1 = self.dig_p9 * pressure * pressure / 2147483648.0
        var2 = pressure * self.dig_p8 / 32768.0
        return pressure + (var1 + var2 + self.dig_p7) / 16.0

    def compensate_humidity(self, raw_humidity):
        var1 = self.temperature_fine - 76800.0
        var2 = self.dig_h4 * 64.0 + (self.dig_h5 / 16384.0) * var1
        var3 = raw_humidity - var2
        var4 = self.dig_h2 / 65536.0
        var5 = 1.0 + (self.dig_h3 / 67108864.0) * var1
        var6 = 1.0 + (self.dig_h6 / 67108864.0) * var1 * var5
        var6 = var3 * var4 * (var5 * var6)

        humidity = var6 * (1.0 - self.dig_h1 * var6 / 524288.0)
        return max(0.0, min(100.0, humidity))


class BME280:
    def __init__(self, i2c_addr=I2C_ADDRESS_GND, i2c_dev=None):
        self.calibration = BME280Calibration()
        self._is_setup = False
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev
        self._bme280 = Device([I2C_ADDRESS_GND, I2C_ADDRESS_VCC], i2c_dev=self._i2c_dev, bit_width=8, registers=(
            Register('CHIP_ID', 0xD0, fields=(
                BitField('id', 0xFF),
            )),
            Register('RESET', 0xE0, fields=(
                BitField('reset', 0xFF),
            )),
            Register('STATUS', 0xF3, fields=(
                BitField('measuring', 0b00001000),  # 1 when conversion is running
                BitField('im_update', 0b00000001),  # 1 when NVM data is being copied
            )),
            Register('CTRL_MEAS', 0xF4, fields=(
                BitField('osrs_t', 0b11100000,   # Temperature oversampling
                         adapter=LookupAdapter({
                             1: 0b001,
                             2: 0b010,
                             4: 0b011,
                             8: 0b100,
                             16: 0b101
                         })),
                BitField('osrs_p', 0b00011100,   # Pressure oversampling
                         adapter=LookupAdapter({
                             1: 0b001,
                             2: 0b010,
                             4: 0b011,
                             8: 0b100,
                             16: 0b101})),
                BitField('mode', 0b00000011,     # Power mode
                         adapter=LookupAdapter({
                             'sleep': 0b00,
                             'forced': 0b10,
                             'normal': 0b11})),
            )),
            Register('CTRL_HUM', 0xF2, fields=(
                BitField('osrs_h', 0b00000111,   # Humidity oversampling
                         adapter=LookupAdapter({
                             1: 0b001,
                             2: 0b010,
                             4: 0b011,
                             8: 0b100,
                             16: 0b101})),
            )),
            Register('CONFIG', 0xF5, fields=(
                BitField('t_sb', 0b11100000,     # Temp standby duration in normal mode
                         adapter=LookupAdapter({
                             0.5: 0b000,
                             62.5: 0b001,
                             125: 0b010,
                             250: 0b011,
                             500: 0b100,
                             1000: 0b101,
                             10: 0b110,
                             20: 0b111})),
                BitField('filter', 0b00011100),                   # Controls the time constant of the IIR filter
                BitField('spi3w_en', 0b0000001, read_only=True),  # Enable 3-wire SPI interface when set to 1. IE: Don't set this bit!
            )),
            Register('DATA', 0xF7, fields=(
                BitField('humidity', 0x000000000000FFFF),
                BitField('temperature', 0x000000FFFFF00000),
                BitField('pressure', 0xFFFFF00000000000)
            ), bit_width=8 * 8),
            Register('CALIBRATION', 0x88, fields=(
                BitField('dig_t1', 0xFFFF << 16 * 12, adapter=U16Adapter()),  # 0x88 0x89
                BitField('dig_t2', 0xFFFF << 16 * 11, adapter=S16Adapter()),  # 0x8A 0x8B
                BitField('dig_t3', 0xFFFF << 16 * 10, adapter=S16Adapter()),  # 0x8C 0x8D
                BitField('dig_p1', 0xFFFF << 16 * 9, adapter=U16Adapter()),   # 0x8E 0x8F
                BitField('dig_p2', 0xFFFF << 16 * 8, adapter=S16Adapter()),   # 0x90 0x91
                BitField('dig_p3', 0xFFFF << 16 * 7, adapter=S16Adapter()),   # 0x92 0x93
                BitField('dig_p4', 0xFFFF << 16 * 6, adapter=S16Adapter()),   # 0x94 0x95
                BitField('dig_p5', 0xFFFF << 16 * 5, adapter=S16Adapter()),   # 0x96 0x97
                BitField('dig_p6', 0xFFFF << 16 * 4, adapter=S16Adapter()),   # 0x98 0x99
                BitField('dig_p7', 0xFFFF << 16 * 3, adapter=S16Adapter()),   # 0x9A 0x9B
                BitField('dig_p8', 0xFFFF << 16 * 2, adapter=S16Adapter()),   # 0x9C 0x9D
                BitField('dig_p9', 0xFFFF << 16 * 1, adapter=S16Adapter()),   # 0x9E 0x9F
                BitField('dig_h1', 0x00FF),                                   # 0xA1 uint8
            ), bit_width=26 * 8),
            Register('CALIBRATION2', 0xE1, fields=(
                BitField('dig_h2', 0xFFFF0000000000, adapter=S16Adapter()),   # 0xE1 0xE2
                BitField('dig_h3', 0x0000FF00000000),                         # 0xE3 uint8
                BitField('dig_h4', 0x000000FFFF0000, adapter=H4Adapter()),    # 0xE4 0xE5[3:0]
                BitField('dig_h5', 0x00000000FFFF00, adapter=H5Adapter()),    # 0xE5[7:4] 0xE6
                BitField('dig_h6', 0x000000000000FF, adapter=S8Adapter())     # 0xE7 int8
            ), bit_width=7 * 8)
        ))

    def setup(self, mode='normal', temperature_oversampling=16, pressure_oversampling=16, humidity_oversampling=16, temperature_standby=500):
        if self._is_setup:
            return
        self._is_setup = True

        self._bme280.select_address(self._i2c_addr)
        self._mode = mode

        if mode == "forced":
            mode = "sleep"

        try:
            chip = self._bme280.get('CHIP_ID')
            if chip.id != CHIP_ID:
                raise RuntimeError("Unable to find bme280 on 0x{:02x}, CHIP_ID returned {:02x}".format(self._i2c_addr, chip.id))
        except IOError:
            raise RuntimeError("Unable to find bme280 on 0x{:02x}, IOError".format(self._i2c_addr))

        self._bme280.set('RESET', reset=0xB6)
        time.sleep(0.1)

        self._bme280.set('CTRL_HUM', osrs_h=humidity_oversampling)

        self._bme280.set('CTRL_MEAS',
                         mode=mode,
                         osrs_t=temperature_oversampling,
                         osrs_p=pressure_oversampling)

        self._bme280.set('CONFIG',
                         t_sb=temperature_standby,
                         filter=2)

        self.calibration.set_from_namedtuple(self._bme280.get('CALIBRATION'))
        self.calibration.set_from_namedtuple(self._bme280.get('CALIBRATION2'))

    def update_sensor(self):
        self.setup()

        if self._mode == "forced":
            self._bme280.set('CTRL_MEAS', mode="forced")
            while self._bme280.get('STATUS').measuring:
                time.sleep(0.001)

        raw = self._bme280.get('DATA')

        self.temperature = self.calibration.compensate_temperature(raw.temperature)
        self.pressure = self.calibration.compensate_pressure(raw.pressure) / 100.0
        self.humidity = self.calibration.compensate_humidity(raw.humidity)

    def get_temperature(self):
        self.update_sensor()
        return self.temperature

    def get_pressure(self):
        self.update_sensor()
        return self.pressure

    def get_humidity(self):
        self.update_sensor()
        return self.humidity

    def get_altitude(self, qnh=1013.25):
        self.update_sensor()
        pressure = self.get_pressure()
        altitude = 44330.0 * (1.0 - pow(pressure / qnh, (1.0 / 5.255)))
        return altitude
