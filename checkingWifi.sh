#!/bin/bash
cd /home/pi/bezelie/testpi
MSG=`./openJTalk.sh "無線ランの接続をチェックします"`
echo $MSG

i=0
while :
do
  sleep 3
#  a=`hostname -I | grep -o -E '^[0-9\.]+'`
  a=`hostname -I | grep -o -E '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
  if [ -n "$a" ]; then
    echo "WiWi Connection Succeed"
    echo $a
    MSG=`./openJTalk.sh "$a"`
    echo $MSG
#    sh /home/pi/bezelie/testpi/openJTalk.sh "アイピーアドレスは"$a"です"
#    /home/pi/aquestalkpi/AquesTalkPi "アイピーアドレスは、"$a"です" | aplay
#    sudo systemctl disable checkWifi.service
#    sudo systemctl enable bezeMenu.service
#    node bezeMenu.js
    MSG=`./node bezeMenu.js`
    echo $MSG
    break
  fi
  echo "WiFi Checking "$i
  i=`expr $i + 1`
  if [ $i -gt 10 ]; then
    echo "missed"
    MSG=`./openJTalk.sh "無線ランに接続できなかったのでリブートします"`
    echo $MSG
#    /home/pi/aquestalkpi/AquesTalkPi "無線ランに接続できなかったのでリブートします" | aplay
    MSG=`./hostingWifi.sh`
    echo $MSG
    break
  fi
done
