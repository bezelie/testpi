#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Servo Movement Test

from  time import sleep
import bezelie

# Set Up
bezelie.initPCA9685()

# Main Loop
try:
  while (True):
    print "happy"
    sleep (2)
    bezelie.actHappy()
    bezelie.moveCenter()
    print "talking"
    sleep (2)
    bezelie.actTalk()
    bezelie.moveCenter()
    print "yes"
    sleep (2)
    bezelie.actYes()
    bezelie.moveCenter()
    print "sad"
    sleep (2)
    bezelie.actSad()
    bezelie.moveCenter()
    print "alarm"
    sleep (2)
    bezelie.actAlarm()
    bezelie.moveCenter()
    print "why"
    sleep (2)
    bezelie.actWhy()
    bezelie.moveCenter()
    print "sleeping"
    sleep (2)
    bezelie.actSleep()
    bezelie.moveCenter()
    
except KeyboardInterrupt:
  print "  終了しました"
