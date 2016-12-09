# -*- coding: utf-8 -*- 
# Bezelie Demo Code for Family Computer Mini
# 

import csv
import datetime
from time import sleep
from random import randint
import subprocess
import picamera
import RPi.GPIO as GPIO
import bezelie

csvFile = "bezeTalkFamicom.csv"
openTime = 0
closeTime = 24

# Definition
def timeMessage(timeSlot):
  data = []
  with open(csvFile, 'rb') as f:  # opening the data file to read
    for i in csv.reader(f):       
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]==timeSlot:            # Checking time
      j = int(i[3])*randint(1,10) # Adding random to probability
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
try:
  while (True):
    now = datetime.datetime.now()
    print now
#    if now.hour >= openTime and now.hour < closeTime: # Activate only in the business hour
#      with picamera.PiCamera() as camera:
#        camera.resolution = (800, 480)                # Display Resolution
#        camera.framerate = 30                         # Frame Rate Max = 30fps
#        camera.rotation = 180                         # Up side Down
#        camera.led = False
#        camera.start_preview()
#        sleep (1)
#     
#        pit = 0
#        while (True):
    while (True):
      while (True):
        while (True):
          bezelie.moveRot (-10)
          sleep (0.3)
          bezelie.moveRot ( 10)
          sleep (0.5)
          bezelie.moveRot (  0)
          sleep (0.3)
          bezelie.movePit (-10)
          timeMessage("morning")
          sleep (1)
          bezelie.movePit (  0)
          sleep (5)

          bezelie.moveRot (-20, 1)
          sleep (0.5)
          bezelie.moveRot ( 20, 1)
          sleep (0.5)
          bezelie.moveRot (  0, 1)
          sleep (0.5)
          bezelie.movePit (-10)
          timeMessage("noon")
          sleep (1)
          bezelie.movePit (  0)
          sleep (5)

          bezelie.movePit ( 10)
          sleep (0.3)
          bezelie.movePit (-20)
          sleep (0.5)
          bezelie.movePit (-10)
          timeMessage("afternoon")
          sleep (1)
          bezelie.movePit (  0)
          sleep (10)
#  else:
#      print "営業時間外です"
#      sleep(60)

except:
  subprocess.call('ifconfig | grep inetアドレス.*ブロードキャスト', shell=True)
