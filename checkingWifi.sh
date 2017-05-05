#!/bin/sh
sh /home/pi/bezelie/testpi/openJTalk.sh "無線ランの接続をチェックします"
i=0
while :
do
  sleep 2
#  a=`hostname -I | grep -o -E '^[0-9\.]+'`
  a=`hostname -I | grep -o -E '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
  if [ -n "$a" ]; then
    echo $a
    sh /home/pi/bezelie/testpi/openJTalk.sh "$a"
#    sh /home/pi/bezelie/testpi/openJTalk.sh "アイピーアドレスは"$a"です"
#    /home/pi/aquestalkpi/AquesTalkPi "アイピーアドレスは、"$a"です" | aplay
#    sudo systemctl disable checkWifi.service
#    sudo systemctl enable bezeMenu.service
#    node bezeMenu.js
    sh /home/pi/bezelie/testpi/exeApp.sh
    break
  fi
  echo "WiFi Checking "$i
  i=`expr $i + 1`
  if [ $i -gt 10 ]; then
    echo "missed"
    sh /home/pi/bezelie/testpi/openJTalk.sh "無線ランに接続できなかったのでリブートします"
#    /home/pi/aquestalkpi/AquesTalkPi "無線ランに接続できなかったのでリブートします" | aplay
    sudo sh accessPoint.sh
    break
  fi
done
