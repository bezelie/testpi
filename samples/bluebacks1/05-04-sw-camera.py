import RPi.GPIO as GPIO
from time import sleep
import subprocess
import datetime

def my_callback(channel):
    if channel==24:
        d = datetime.datetime.today()
        filename = "{0}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}.jpg".format(d.year, d.month, d.day, d.hour, d.minute, d.second)
        args = ['raspistill', '-o', filename, '-t', '1']
        subprocess.Popen(args)

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback, bouncetime=200)

try:
    while True:
        sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
