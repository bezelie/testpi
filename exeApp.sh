#!/bin/sh
ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | sh
cd /home/pi/bezelie/testpi
python demoFace1.py
exit 0
