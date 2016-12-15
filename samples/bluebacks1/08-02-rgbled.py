# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

# MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout

GPIO.setmode(GPIO.BCM)
# ピンの名前を変数として定義
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8
# SPI通信用の入出力を定義
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
p0 = GPIO.PWM(25, 50)  # GPIO=25、周波数50Hz
p1 = GPIO.PWM(24, 50)  # GPIO=24、周波数50Hz
p2 = GPIO.PWM(23, 50)  # GPIO=23、周波数50Hz
p0.start(0)
p1.start(0)
p2.start(0)
adc_pin0 = 0
adc_pin1 = 1
adc_pin2 = 2

try:
    while True:
        inputVal0 = readadc(adc_pin0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        inputVal1 = readadc(adc_pin1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        inputVal2 = readadc(adc_pin2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        duty0 = inputVal0*100/4095
        duty1 = inputVal1*100/4095
        duty2 = inputVal2*100/4095
        # カソードコモンの場合、以下の3行を無効に
        duty0 = 100 - duty0
        duty1 = 100 - duty1
        duty2 = 100 - duty2
        p0.ChangeDutyCycle(duty0)
        p1.ChangeDutyCycle(duty1)
        p2.ChangeDutyCycle(duty2)
        sleep(0.2)

except KeyboardInterrupt:
    pass

p0.stop()
p1.stop()
p2.stop()
GPIO.cleanup()

