#!/bin/sh
echo "checking WiFi..."
MSG=`sh /home/pi/bezelie/testpi/openJTalk.sh "無線ランの接続をチェックします"`
echo $MSG
sleep 3

i=0
while :
do
  sleep 3
#  a=`hostname -I | grep -o -E '^[0-9\.]+'`
  a=`hostname -I | grep -o -E '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
  if [ -n "$a" ]; then
    echo "WiWi Connection Succeed"
    echo $a
    MSG=`sh /home/pi/bezelie/testpi/openJTalk.sh "$a"`
    echo $MSG
    sleep 3
    MSG=`node /home/pi/bezelie/testpi/bezeMenu.js`
    echo $MSG
    break
  fi
  echo "WiFi Checking "$i
  i=`expr $i + 1`
  if [ $i -gt 10 ]; then
    echo "missed"
    MSG=`sh /home/pi/bezelie/testpi/openJTalk.sh "無線ランに接続できなかったのでリブートします"`
    echo $MSG
#    /home/pi/aquestalkpi/AquesTalkPi "無線ランに接続できなかったのでリブートします" | aplay
    MSG=`sh /home/pi/bezelie/testpi/settingHost.sh`
    echo $MSG
    break
    fi
  done
  exit 0
