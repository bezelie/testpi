import webiopi
import time
import smbus

# デバッグ出力を有効に
webiopi.setDebug()

# I2Cを用いるための設定
bus = smbus.SMBus(1)
address_adt7410 = 0x48
register_adt7410 = 0x00
temp = 0.0

# センサから温度を取得する関数（7章で用いたもの）
def read_adt7410():
    word_data =  bus.read_word_data(address_adt7410, register_adt7410)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>3 # 13 bit data

    if data & 0x1000 == 0:  # 温度が正
        temperature = data*0.0625
    else: # 温度が負
        temperature = ( (~data&0x1fff) + 1)*-0.0625

    return temperature

# WebIOPiの起動時に呼ばれる関数
def setup():
    webiopi.debug("Script with macros - Setup")

# WebIOPiにより繰り返される関数
def loop():
    global temp
    temp = read_adt7410()
    webiopi.sleep(1)

# WebIOPi終了時に呼ばれる関数
def destroy():
    webiopi.debug("Script with macros - Destroy")

# 自作のマクロ。JavaScriptから呼ぶことができる
@webiopi.macro
def getTemp():
    return temp
