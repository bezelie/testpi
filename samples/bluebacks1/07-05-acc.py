# -*- coding: utf-8 -*-
# チップ: LIS3DH
# 型番など: 秋月電子通商(K-06791)
#
# ジャンパAを半田づけしてI2Cで用いる
#
# 接続: I2Cデバイス - Raspberry Pi
# 1 VDD - 3.3V
# 2 GND - GND
# 3 SCL - I2C SCL
# 4 SDA - I2C SDA
# 5 SAO - GND
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

def setup_lis3dh():
    # CTRL_REG4, High Resolutionモード
    bus.write_byte_data(address_lis3dh, 0x23, 0x08)
    sleep(0.01)
    # CTRL_REG1, Data rate =50Hz, X, Y, Z有効
    bus.write_byte_data(address_lis3dh, 0x20, 0x47)
    sleep(0.01)

def read_lis2dh(register):
    data_l =  bus.read_byte_data(address_lis3dh, register)
    data_h =  bus.read_byte_data(address_lis3dh, register+1)
    data = (data_h<<8) | data_l
    if data & 0x8000 == 0:  # 正または0の場合
        data = data
    else: # 負の場合、 絶対値を取ってからマイナスをかける
        data = ( (~data&0xffff) + 1)*-1
    return acc_coef*data

def calc_angle(x, y):
    return atan2(x, y)*180/pi

bus = smbus.SMBus(1)
address_lis3dh = 0x18
acc_coef = 2*9.81/32767

setup_lis3dh()

try:
    while True:
        acc_x = read_lis2dh(0x28)
        acc_y = read_lis2dh(0x2a)
        acc_z = read_lis2dh(0x2c)

        angle_x = calc_angle(acc_x, acc_z)
        angle_y = calc_angle(acc_y, acc_z)
        
        print("{0:.02f}, {1:.02f}, {2:.02f}".format(acc_x, acc_y, acc_z))
        print("angle_x={0:.02f}, angle_y={1:.02f}".format(angle_x, angle_y))

        sleep(0.2)

except KeyboardInterrupt:
    pass

