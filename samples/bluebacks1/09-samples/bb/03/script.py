import webiopi
import time

# デバッグ出力を有効に
webiopi.setDebug()

# GPIOライブラリの取得
GPIO = webiopi.GPIO

PWM1 = 25
PWM2 = 24
PWM3 = 23

# WebIOPiの起動時に呼ばれる関数
def setup():
    webiopi.debug("Script with macros - Setup")
    # GPIOのセットアップ
    GPIO.setFunction(PWM1, GPIO.PWM)
    GPIO.setFunction(PWM2, GPIO.PWM)
    GPIO.setFunction(PWM3, GPIO.PWM)
    # すべてのPWMの初期デューティ比を100%に（消灯）
    GPIO.pwmWrite(PWM1, 1.0)
    GPIO.pwmWrite(PWM2, 1.0)
    GPIO.pwmWrite(PWM3, 1.0)

    # 共通カソードの場合は下記の3行を有効にして初期デューティ比を0%に（消灯）
    #GPIO.pwmWrite(PWM1, 0.0)
    #GPIO.pwmWrite(PWM2, 0.0)
    #GPIO.pwmWrite(PWM3, 0.0)

# WebIOPiにより繰り返される関数
def loop():
    webiopi.sleep(5)

# WebIOPi終了時に呼ばれる関数
def destroy():
    webiopi.debug("Script with macros - Destroy")
    # GPIO関数のリセット（入力にセットすることで行う）
    GPIO.setFunction(PWM1, GPIO.IN)
    GPIO.setFunction(PWM2, GPIO.IN)
    GPIO.setFunction(PWM3, GPIO.IN)
