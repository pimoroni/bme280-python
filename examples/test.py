#!/usr/bin/env python

import time
from bme280 import _bme280, CHIP_ID

print('0x{:02x} {}'.format(_bme280.CHIP_ID.get_id(), 'ok' if _bme280.CHIP_ID.get_id() == CHIP_ID else 'err'))

with _bme280.CTRL_MEAS as reg:
    reg.set_mode('normal')
    reg.set_osrs_t(16)  # 16x temperature oversampling
    reg.set_osrs_p(16)  # 16x pressure oversampling
    reg.write()

with _bme280.CONFIG as reg:
    reg.set_t_sb(500)
    reg.set_filter(2)
    reg.write()

with _bme280.CALIBRATION as reg:
    dig_t1 = reg.get_dig_t1()
    dig_t2 = reg.get_dig_t2()
    dig_t3 = reg.get_dig_t3()

    dig_p1 = reg.get_dig_p1()
    dig_p2 = reg.get_dig_p2()
    dig_p3 = reg.get_dig_p3()
    dig_p4 = reg.get_dig_p4()
    dig_p5 = reg.get_dig_p5()
    dig_p6 = reg.get_dig_p6()
    dig_p7 = reg.get_dig_p7()
    dig_p8 = reg.get_dig_p8()
    dig_p9 = reg.get_dig_p9()

    print(dig_t1, dig_t2, dig_t3)
    print(dig_p1, dig_p2, dig_p3, dig_p4, dig_p5, dig_p6, dig_p7, dig_p8, dig_p9)

try:
    while True:
        raw_temp = _bme280.DATA.get_temperature()
        raw_pres = _bme280.DATA.get_pressure()

        print('0b{:020b}'.format(raw_temp))

        var1 = (raw_temp / 16384.0 - dig_t1 / 1024.0) * dig_t2
        var2 = (raw_temp / 131072.0 - dig_t1 / 8192.0) * (raw_temp / 131072.0 - dig_t1 / 8192.0) * dig_t3
        temp = (var1 + var2) / 5120.0
        t_fine = (var1 + var2)

        print(temp)
        time.sleep(1)

except KeyboardInterrupt:
    pass
