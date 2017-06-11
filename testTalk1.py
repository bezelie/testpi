#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import subprocess

# Main Loop
try:
  while (True):
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "アクエストーク" | aplay', shell=True)
    sleep(0.5)
    subprocess.call('sh /home/pi/bezelie/testpi/openJTalk.sh '+'ジェイトーク', shell=True)
    sleep(0.5)
except KeyboardInterrupt:
  print ' Interrupted by Keyboard'
