# -*- coding: utf-8 -*-
# チップ: L3GD20
# 型番など: 秋月電子通商(K-06779)
#
# 接続: I2Cデバイス - Raspberry Pi
# 1 VDD - 3.3V
# 2 SCL - I2C SCL
# 3 SDA - I2C SDA
# 4 SAO - GND
# 5 CS - 3.3V
# 6, 7 - 接続なし
# 8 GND - GND
#
# x軸周り角速度、y軸周り角速度、z軸周り角速度
#
# が表示される
#
import smbus
from time import sleep

def setup_l3gd20():
    # ノーマルモード, XYZ有効
    bus.write_byte_data(address_l3gd20, 0x20, 0x0f)
    sleep(0.01)

def read_l3gd20(register):
    data_l =  bus.read_byte_data(address_l3gd20, register)
    data_h =  bus.read_byte_data(address_l3gd20, register+1)

    data = (data_h<<8) | data_l

    if data & 0x8000 == 0:  # 正または0の場合
        data = data*0.00875
    else: # 負の場合、 絶対値を取ってからマイナスをかける
        data = ( (~data&0xffff) + 1)*-0.00875

    return data

bus = smbus.SMBus(1)
address_l3gd20 = 0x6a

setup_l3gd20()

try:
    while True:
        gyro_x = read_l3gd20(0x28)
        gyro_y = read_l3gd20(0x2a)
        gyro_z = read_l3gd20(0x2c)

        print("{0:.04f}, {1:.04f}, {2:.04f}".format(gyro_x, gyro_y, gyro_z))

        sleep(0.5)

except KeyboardInterrupt:
    pass

