# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
import spidev

# MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
def readadc_spidev(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    commandout = adcnum
    commandout |= 0x08  # シングルエンドビット
    commandout = commandout<<4
    ret = spi.xfer2([1,commandout,0,0])    
    adcout = ((ret[1]&0x03)<<10) | (ret[2]<<2) | ret[3]&0x03
    return adcout

GPIO.setmode(GPIO.BCM)
spi=spidev.SpiDev()
spi.open(0, 0) # bus0, CE0

try:
    while True:
        inputVal0 = readadc_spidev(0)
        print(inputVal0)
        sleep(0.2)

except KeyboardInterrupt:
    pass

spi.close()
