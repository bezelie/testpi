# -*- coding: utf-8 -*-
# チップ: LPS331
# 型番など: 秋月電子通商(M-06679)
#
# 接続: I2Cデバイス - Raspberry Pi
# 1 VDD - 3.3V
# 2 SCL - I2C SCL
# 3 SDA - I2C SDA
# 4 SAO - GND
# 5 CS - 3.3V
# 6,7 - 接続せず
# 8 GND - GND
# 
import smbus
from time import sleep

def setup_lps331():
    # CTRL_REG1, active, 1Hz
    bus.write_byte_data(address_lps331, 0x20, 0x90)
    sleep(0.1)

def read_lps331():
    data_xl =  bus.read_byte_data(address_lps331, 0x28)
    data_l =  bus.read_byte_data(address_lps331, 0x29)
    data_h =  bus.read_byte_data(address_lps331, 0x2a)

    data = (data_h<<16) | (data_l<<8) | data_xl

    return data/4096.0

bus = smbus.SMBus(1)
address_lps331 = 0x5c

setup_lps331()

try:
    while True:
        pressure = read_lps331()

        print("{0:.02f}".format(pressure))

        sleep(1)

except KeyboardInterrupt:
    pass

