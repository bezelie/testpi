# -*- coding: utf-8 -*-
# チップ: ADXL345
# 型番など: 秋月電子通商(M-06724)
#
# 接続: I2Cデバイス - Raspberry Pi
# VDD - 3.3V
# GND - GND
# Vs - 3.3V
# Cs - 3.3V 
# SCL - I2C SCL
# SDA - I2C SDA
# SDO - 3.3V
# 残りのピンは使用せず
#
# x方向加速度、y方向加速度、z方向加速度
# x方向傾き、y方向傾き
# が表示される
#
import smbus
from time import sleep
from math import atan2
from math import pi

def setup_adxl345():
    # full range
    bus.write_byte_data(address_adxl345, 0x31, 0x08)
    sleep(0.01)

    # start measure
    bus.write_byte_data(address_adxl345, 0x2d, 0x08)
    sleep(0.01)


def read_adxl345(register):
    data_l =  bus.read_byte_data(address_adxl345, register)
    data_h =  bus.read_byte_data(address_adxl345, register+1)

    data = (data_h<<8) | data_l

    if data & 0x8000 == 0:  # 正または0の場合
        data = data
    else: # 負の場合、 絶対値を取ってからマイナスをかける
        data = ( (~data&0xffff) + 1)*-1

    return acc_coef*data

def calc_angle(x, y):

    return atan2(x, y)*180/pi
 
bus = smbus.SMBus(1)
address_adxl345 = 0x1d
acc_coef = 4*9.81/1000 # 4mg

setup_adxl345()

try:
    while True:
        acc_x = read_adxl345(0x32)
        acc_y = read_adxl345(0x34)
        acc_z = read_adxl345(0x36)

        angle_x = calc_angle(acc_x, acc_z)
        angle_y = calc_angle(acc_y, acc_z)

        print("{0:.02f}, {1:.02f}, {2:.02f}".format(acc_x, acc_y, acc_z))
        print("angle_x={0:.02f}, angle_y={1:.02f}".format(angle_x, angle_y))

        sleep(0.2)

except KeyboardInterrupt:
    pass

