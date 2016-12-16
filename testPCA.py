# Servo Moter Control Program for PCA9685
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
import smbus
import math

#GPIO.setmode(GPIO.BCM)
bus = smbus.SMBus(1)
address_pca9685 = 0x40 # maybe 50

resetPCA9685()
setPCA9685Freq(50)

# Constants
pulseMax = 520 #
pulseMin = 100 #
pulseMid = pulseMin + (pulseMax - pulseMin)/2 # center of pulse
pitAdj = 0     # pitch adjustment
rotAdj = 0     # rotation adjustment
yawAdj = 0     # yaw adjustment
pitMin = -30   # Upward
pitMax =  30   # Downward
rotMin = -30   # Clockwise
rotMax =  30   # AntiClockwise
yawMin = -40   # Clocwise
yawMax =  40   # AntiClockWise
#pwm = PWM(0x40)
#pwm.setPWMFreq(47)   # Set frequency to 50 Hz
servoStep = 5
defaultSpeed = 0

# Global Valiables
pitNow = rotNow = yawNow = pulseMid

def resetPCA9685():
  bus.write_byte_data(address_pca9685, 0x00, 0x00)

def setPCA9685Freq(freq):
  freq = 0.9*freq # Arduinoのライブラリより
  prescaleval = 25000000.0    # 25MHz
  prescaleval /= 4096.0       # 12-bit
  prescaleval /= float(freq)
  prescaleval -= 1.0
  prescale = int(math.floor(prescaleval + 0.5))
  oldmode = bus.read_byte_data(address_pca9685, 0x00)
  newmode = (oldmode & 0x7F) | 0x10             # スリープモード
  bus.write_byte_data(address_pca9685, 0x00, newmode) # スリープモードへ
  bus.write_byte_data(address_pca9685, 0xFE, prescale) # プリスケーラーをセット
  bus.write_byte_data(address_pca9685, 0x00, oldmode)
  sleep(0.005)
  bus.write_byte_data(address_pca9685, 0x00, oldmode | 0xa1)

def getPCA9685Duty(id, val):
  val_min = -90
  val_max = 90
  servo_min = 143 # 50Hzで0.7ms
  servo_max = 410 # 50Hzで2.0ms  (中心は276)
  if id==1 :
    servo_min = 193 # 50Hzで0.95ms
    servo_max = 360 # 50Hzで1.8ms
  duty = (servo_min-servo_max)*(val-val_min)/(val_max-val_min) + servo_max
  return int(duty)

def setPCA9685Duty(channel, on, off):
  channelpos = 0x6 + 4*channel
  try:
    bus.write_i2c_block_data(address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8] )
  except IOError:
    pass

def movePit (pit, speed=defaultSpeed):
  global pitNow
  if pit > pitMax:
    pit = pitMax
  if pit < pitMin:
    pit = pitMin
  pitDest = int( float(pit + 90)/180 * (pulseMax - pulseMin) + pulseMin)
  while (pitNow != pitDest):
    if pitNow < pitDest:
      pitNow += servoStep
      if pitNow > pitDest:
        pitNow = pitDest
    if pitNow > pitDest:
      pitNow -= servoStep
      if pitNow < pitDest:
        pitNow = pitDest
    pwm.setPWM(2, 0, pitNow + pitAdj)


degree = 0
servoID = 0
duty = 380
# mid 380
# min 140 = clock 90 degree
# max 620 = anti-Clock 90 degree

try:
  while duty < 700:
#    duty0 = getPCA9685Duty(0, degree)
    print duty
    setPCA9685Duty(servoID, 0, duty)
    sleep(0.2)
    duty += 1

except KeyboardInterrupt:
  pass

GPIO.cleanup()
