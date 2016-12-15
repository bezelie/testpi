# -*- coding: utf-8 -*-
# チップ: MPL115A2
# 型番など: 秋月電子通商(I-04692)
#
# 接続: I2Cデバイス - Raspberry Pi
# 1 VDD - 3.3V
# 2 CAP - 1マイクロFのコンデンサの一端を接続し、もう一端をGNDに
# 3 GND - GND
# 4 SHDN - 3.3V
# 5 RST - 3.3V
# 6 NC - 接続なし
# 7 SDA - I2C SDA
# 8 SCL - I2C SCL
# 
import smbus
from time import sleep

def setup_mpl115a2():
    global a0, b1, b2, c12
    a0_h = bus.read_byte_data(address_mpl115a2, 0x04)
    a0_l = bus.read_byte_data(address_mpl115a2, 0x05)
    b1_h = bus.read_byte_data(address_mpl115a2, 0x06)
    b1_l = bus.read_byte_data(address_mpl115a2, 0x07)
    b2_h = bus.read_byte_data(address_mpl115a2, 0x08)
    b2_l = bus.read_byte_data(address_mpl115a2, 0x09)
    c12_h = bus.read_byte_data(address_mpl115a2, 0x0a)
    c12_l = bus.read_byte_data(address_mpl115a2, 0x0b)

    a0 = ((a0_h<<8) | a0_l)/8.0
    b1 = - ((~((b1_h<<8) | b1_l) & 0xffff) + 1)/8192.0
    b2 = - ((~((b2_h<<8) | b2_l) & 0xffff) + 1)/16384.0
    c12 = (((c12_h<<8) | + c12_l)/16777216.0)


def read_mpl115a2():
    bus.write_byte_data(address_mpl115a2, 0x12, 0x01)
    sleep(0.003)

    P_h = bus.read_byte_data(address_mpl115a2, 0x00)
    P_l = bus.read_byte_data(address_mpl115a2, 0x01)
    T_h = bus.read_byte_data(address_mpl115a2, 0x02)
    T_l = bus.read_byte_data(address_mpl115a2, 0x03)

    P = ((P_h<<8) | P_l)>>6
    T = ((T_h<<8) | T_l)>>6

    Pcomp = a0 + (b1+c12*T)*P + b2*T
    Pressure = Pcomp*(650.0/1023.0) + 500.0

    return Pressure
    
bus = smbus.SMBus(1)
address_mpl115a2 = 0x60

a0 = 0
b1 = 0
b2 = 0
c12 = 0

setup_mpl115a2()

try:
    while True:
        inputValue = read_mpl115a2()

        print("{0:.02f}".format(inputValue))

        sleep(1)

except KeyboardInterrupt:
    pass

