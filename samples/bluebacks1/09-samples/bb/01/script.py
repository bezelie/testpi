import webiopi
import time

# デバッグ出力を有効に
webiopi.setDebug()

# GPIOライブラリの取得
GPIO = webiopi.GPIO

LED = 25
STATE = GPIO.LOW

# WebIOPiの起動時に呼ばれる関数
def setup():
    webiopi.debug("Script with macros - Setup")
    # GPIOのセットアップ
    GPIO.setFunction(LED, GPIO.OUT)
    GPIO.digitalWrite(LED, STATE)

# WebIOPiにより繰り返される関数
def loop():
    webiopi.sleep(5)

# WebIOPi終了時に呼ばれる関数
def destroy():
    webiopi.debug("Script with macros - Destroy")
    # GPIO関数のリセット（入力にセットすることで行う）
    GPIO.setFunction(LED, GPIO.IN)

# 自作のマクロ。JavaScriptから呼ぶことができる
@webiopi.macro
def toggleLED(gpio):
    global STATE
    STATE = not STATE
    GPIO.digitalWrite(int(gpio), STATE)
    return STATE
