import RPi.GPIO as GPIO
from time import sleep
import subprocess

def my_callback(channel):
    global isPlaying
    global process
    if channel==24:
        if isPlaying == False:
            isPlaying = True
            GPIO.output(25, GPIO.HIGH)
            args = ['mpg321', 'test.mp3']
            process = subprocess.Popen(args)
        else:
            isPlaying = False
            GPIO.output(25, GPIO.LOW)
            args = ['kill', str(process.pid)]
            subprocess.Popen(args)

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback, bouncetime=200)

isPlaying = False
process = None

try:
    while True:
        sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
