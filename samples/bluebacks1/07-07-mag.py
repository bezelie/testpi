# -*- coding: utf-8 -*-
# チップ: HMC6352
# 型番など: 千石電商(SEN-07915)
#
# 接続: I2Cデバイス - Raspberry Pi
# SCL - I2C SCL
# SDA - I2C SDA
# VCC - 3.3V
# GND - GND
#
# 基板上の矢印と北の方角が成す角度を出力します。
# 矢印が北を向いていれば0となります。
# 矢印が南を向いているときの精度が悪いようです。
#
import smbus
from time import sleep

def read_hmc6352():
    word_data =  bus.read_word_data(address_hmc6352, register_hmc6352)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8

    heading = 0.1*data

    if heading>180:
        heading = heading - 360

    return heading

bus = smbus.SMBus(1)
address_hmc6352 = 0x21
register_hmc6352 = 0x41

try:
    while True:
        # 時々起こるIOErrorを無視する
        try:
            inputValue = read_hmc6352()
            print(inputValue)
            sleep(0.2)
        except IOError:
            pass

except KeyboardInterrupt:
    pass

