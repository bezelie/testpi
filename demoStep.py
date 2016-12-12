# -*- coding: utf-8 -*- 
# Confatable IOT Contest
# Distance Sensor on the steps

import csv
import time
from time import sleep
from random import randint
import subprocess
import RPi.GPIO as GPIO
import bezelie
csvFile = "bezeTalkStep.csv"

# Definition
trigger_pin = 18    # GPIO 18
echo_pin = 23       # GPIO 23
short = 10
long = 400

# Set Up
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Definition
def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    sleep(0.0001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count -= 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance  = pulse_len / 0.000058
    return (distance)

def timeMessage(timeSlot):
  data = []
  with open(csvFile, 'rb') as f:  # opening the data file to read
    for i in csv.reader(f):       
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]==timeSlot:            # Checking time
      j = int(i[3])*randint(80,120)# Adding random to probability
      data1.append(i+[j]+[index]) # Candidates data

  maxNum = 0
  for i in data1:                 # decision
    if i[5] > maxNum:             # Whitch is the max probability.
      maxNum = i[5]               # Max probability
      ansNum = i[6]               # Index of answer

  # AquesTalk
  print data[ansNum][2]
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum ][2] +'" | aplay', shell=True)

# Get Started
bezelie.centering()
sleep (1)

# Main Loop
while True:
  d = get_distance()
  print(round(d,1))
  if d > short and d < long:
    bezelie.moveRot (20)
    time.sleep(0.5)
    bezelie.moveRot (-20)
    time.sleep(0.5)
    bezelie.moveRot (0)
    time.sleep(0.5)
    timeMessage("step")
  else:
    time.sleep(0.5)

GPIO.cleanup()
