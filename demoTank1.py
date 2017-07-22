#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Servo Movement Test

from  time import sleep
import bezelie
import RPi.GPIO as GPIO

# Definition
ledRed = 16       # as Red
ledBlue = 20      # as Blue
ledGreen = 21     # as Green
interval = 0.1
wait = 0.5

# Set Up
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledBlue, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)
bezelie.initPCA9685()

# Functions
def ledOff():
  GPIO.output (ledRed, False)
  GPIO.output (ledBlue, False)
  GPIO.output (ledGreen, False)
  sleep(0.04)

def ledFlash():
    GPIO.output (ledRed, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledBlue, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledGreen, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledRed, True)
    GPIO.output (ledBlue, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledBlue, True)
    GPIO.output (ledGreen, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledGreen, True)
    GPIO.output (ledRed, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledRed, True)
    GPIO.output (ledBlue, True)
    GPIO.output (ledGreen, True)
    sleep(interval)
    ledOff()

# Main Loop
try:
  while (True):
    print "happy"
    sleep (wait)
    ledFlash()
    bezelie.actHappy()
    bezelie.moveCenter()
    print "talking"
    sleep (wait)
    ledFlash()
    bezelie.actTalk()
    bezelie.moveCenter()
    print "happy"
    sleep (wait)
    ledFlash()
    bezelie.actHappy()
    bezelie.moveCenter()
    print "yes"
    sleep (wait)
    ledFlash()
    bezelie.actYes()
    bezelie.moveCenter()
    print "happy"
    sleep (wait)
    ledFlash()
    bezelie.actHappy()
    bezelie.moveCenter()
    print "why"
    sleep (wait)
    ledFlash()
    bezelie.actWhy()
    bezelie.moveCenter()
    
except KeyboardInterrupt:
  print "  終了しました"

GPIO.cleanup()

