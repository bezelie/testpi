#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python Module for Raspberry Pi

import RPi.GPIO as GPIO
from time import sleep
import smbus  # I2C module
import math

bus = smbus.SMBus(1) # I2C
address_pca9685 = 0x40 # When you connect other I2C devices, you may have to change this number.

# adjust
servo1Adj = 0
servo2Adj = 0
servo3Adj = 0
servo4Adj = 0
servo5Adj = 0

# Constants
dutyMax = 490     #
dutyMin = 110     #
dutyCenter = 300  #
steps = 1         #

# Global Valiables
servo1Now = servo2Now = servo3Now = servo4Now = servo5Now = dutyCenter

# Functions
def initPCA9685():
  bus.write_byte_data(address_pca9685, 0x00, 0x00)
  freq = 0.9*50
  prescaleval = 25000000.0    # 25MHz
  prescaleval /= 4096.0       # 12-bit
  prescaleval /= float(freq)
  prescaleval -= 1.0
  prescale = int(math.floor(prescaleval + 0.5))
  oldmode = bus.read_byte_data(address_pca9685, 0x00)
  newmode = (oldmode & 0x7F) | 0x10             
  bus.write_byte_data(address_pca9685, 0x00, newmode) 
  bus.write_byte_data(address_pca9685, 0xFE, prescale) 
  bus.write_byte_data(address_pca9685, 0x00, oldmode)
  sleep(0.005)
  bus.write_byte_data(address_pca9685, 0x00, oldmode | 0xa1)

def setPCA9685Duty(channel, on, off):
  channelpos = 0x6 + 4*channel
  try:
    bus.write_i2c_block_data(address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8] )
  except IOError:
    pass

def moveServo (id, degree, adj, max, min, speed, now):
  dst = (dutyMin-dutyMax)*(degree+adj+90)/180 + dutyMax
  if speed == 0:
    setPCA9685Duty(id, 0, dst)
    sleep(0.001 * math.fabs(dst-now))
    now = dst    
  if dst > max: dst = max
  if dst < min: dst = min
  while (now != dst):
    if now < dst:
      now += steps
      if now > dst: now = dst
    else:
      now -= steps
      if now < dst: now = dst
    setPCA9685Duty(id, 0, now)
    sleep(0.004 * steps *(speed))
  return (now)

def servo1 (degree, speed=1):
  global servo1Adj, servo1Now
  max = 360     # Downward limit
  min = 230     # Upward limit
  servo1Now = moveServo (1, degree, servo1Adj, max, min, speed, servo1Now)

def servo2 (degree, speed=1):
  global servo2Adj, servo2Now
  max = 360     # Downward limit
  min = 230     # Upward limit
  servo2Now = moveServo (2, degree, servo2Adj, max, min, speed, servo2Now)

def servo3 (degree, speed=1):
  global servo3Adj, servo3Now
  max = 360     # Downward limit
  min = 230     # Upward limit
  servo3Now = moveServo (3, degree, servo3Adj, max, min, speed, servo3Now)

def servo4 (degree, speed=1):
  global servo4Adj, servo4Now
  max = 360     # Downward limit
  min = 230     # Upward limit
  servo4Now = moveServo (4, degree, servo4Adj, max, min, speed, servo4Now)

def servo5 (degree, speed=1):
  global servo5Adj, servo5Now
  max = 360     # Downward limit
  min = 230     # Upward limit
  servo5Now = moveServo (5, degree, servo5Adj, max, min, speed, servo5Now)

def moveCenter ():
  servo1 (servo1Adj)
  servo2 (servo2Adj)
  servo3 (servo3Adj)
  servo4 (servo4Adj)
  servo5 (servo5Adj)

# Centering Servo Motors
if __name__ == "__main__":  # Do only when this is done as a script
  servo1 (5)
  servo1 (-5)
  servo1 (servo1Adj)
  servo2 (5)
  servo2 (-5)
  servo2 (servo2Adj)
  servo3 (5)
  servo3 (-5)
  servo3 (servo3Adj)
  servo4 (5)
  servo4 (-5)
  servo4 (servo4Adj)
  servo5 (5)
  servo5 (-5)
  servo5 (servo5Adj)
