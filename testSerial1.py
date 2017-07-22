#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie Test Code for Raspberry Pi : Serial Transmission Test

from  time import sleep
import bezelie
import os
import serial

#open serial port
os.system('sudo chmod 777 /dev/ttyAMA0')
ser = serial.Serial('/dev/ttyAMA0', 57600)

# Set Up
i = 0
bezelie.initPCA9685()

# Functions

def happy():
    print "happy"
    bezelie.actHappy()
    bezelie.moveCenter()

# Main Loop
try:
    while (True):
        message = 'a' + str(i)
        print('TX:' + message)
        ser.write(message + '\r\n')
        i = i + 1
        sleep(3)

except KeyboardInterrupt:
    print "  終了しました"

ser.close()
