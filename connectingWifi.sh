# ラズパイのアクセスポイント化を解除し、wifiに接続する
#!/bin/bash
echo "Connecting to WiFi..."
# サービス終了
sudo service isc-dhcp-server stop
# DHCPサーバ無効化
sudo cp /home/pi/bezelie/testpi/config/isc-dhcp-server_original /etc/default/isc-dhcp-server
sudo cp /home/pi/bezelie/testpi/config/dhcpd_original.conf /etc/dhcp/dhcpd.conf
# hostapd設定の初期化
sudo cp /home/pi/bezelie/testpi/config/hostapd_original /etc/default/hostapd
sudo cp /home/pi/bezelie/testpi/config/hostapd_original.conf /etc/hostapd/hostapd.conf
# IPアドレス固定化の無効化
sudo cp /home/pi/bezelie/testpi/config/dhcpcd_original.conf /etc/dhcpcd.conf
# wlan0をアクセスポイントにすることの無効化
sudo cp /home/pi/bezelie/testpi/config/interfaces_original /etc/network/interfaces
# DHCPサービスとnode-jsの自動起動を解除
# sudo systemctl disable wifiSetting.service
# sudo systemctl enable checkWifi.service
# wifiリセット
sudo ifdown wlan0
sudo ifup wlan0
cd /home/pi/bezelie/testpi
# MSG=`./checkingWifi.sh`
# echo $MSG
# reboot
# exit 0

MSG=`./openJTalk.sh "無線ランの接続をチェックします"`
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
    MSG=`./openJTalk.sh "$a"`
    echo $MSG
    sleep 3
    MSG=`node bezeMenu.js`
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
  exit 0
