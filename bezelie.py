#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie Python Module for Raspberry Pi
import RPi.GPIO as GPIO
from time import sleep
import smbus  # I2C module
import math
import csv

bus = smbus.SMBus(1) # I2C
address_pca9685 = 0x40 # When you connect other I2C devices, you may have to change this number.

# Constants
dutyMax = 490     #
dutyMin = 110     #
dutyCenter = 300  #
steps = 1         #

# Global Valiables
headNow = backNow = stageNow = dutyCenter

# Read Config File
headAdj = backAdj = stageAdj = 0
csvFile = "bezeConfig.csv"
data = []
with open(csvFile, 'rb') as f:
  for i in csv.reader(f):
    data.append(i)

  for i in data:
    if i[0] == "headAdj":headAdj=int(i[1])
    if i[0] == "backAdj":backAdj=int(i[1])
    if i[0] == "stageAdj":stageAdj=int(i[1])

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

def moveHead (degree, speed=1):
  global headAdj
  max = 360     # Downward limit
  min = 280     # Upward limit
  global headNow
  headNow = moveServo (2, degree, headAdj, max, min, speed, headNow)

def moveBack (degree, speed=1):
  global backAdj
  max = 380     # AntiClockwise limit
  min = 220     # Clockwise limit
  global backNow
  backNow = moveServo (1, degree, backAdj, max, min, speed, backNow)

def moveStage (degree, speed=1):
  global stageAdj
  max = 390    # AntiClockWise limit
  min = 210    # Clocwise limit
  global stageNow
  stageNow = moveServo (0, degree, stageAdj, max, min, speed,stageNow)

def moveCenter ():
  moveHead (headAdj)
  moveBack (backAdj)
  moveStage (stageAdj)

# Centering Servo Motors
if __name__ == "__main__":  # Do only when this is done as a script
  moveHead (20)
  moveHead (-20)
  moveHead (headAdj)
  moveBack (20)
  moveBack (-20)
  moveBack (backAdj)
  moveStage (20)
  moveStage (-20)
  moveStage (stageAdj)
