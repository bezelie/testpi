#!/bin/sh
ps aux | grep julius | grep -v grep | awk '{ print "kill -9", $2 }' | sh
exit 0
