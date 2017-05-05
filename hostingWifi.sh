# ラズパイをアクセスポイントに
#!/bin/sh
echo "Making RaspberryPi an Access Point"
# wlan0をアクセスポイントにする
sudo cp ~/bezelie/testpi/config/interfaces_changed /etc/network/interfaces
# IPアドレス固定 wlan0に固定IPアドレスを割り振る
sudo cp ~/bezelie/testpi/config/dhcpcd_changed.conf /etc/dhcpcd.conf
# サービスを再起動
sudo service dhcpcd restart
# Hostapdでアクセスポイント化
sudo cp ~/bezelie/testpi/config/hostapd_changed.conf /etc/hostapd/hostapd.conf
# DEAMON_CONF の指定。
sudo cp ~/bezelie/testpi/config/hostapd_changed /etc/default/hostapd
# DHCPサーバ化
sudo cp ~/bezelie/testpi/config/dhcpd_changed.conf /etc/dhcp/dhcpd.conf
sudo cp ~/bezelie/testpi/config/isc-dhcp-server_changed /etc/default/isc-dhcp-server
# wifiリセット
# sudo ifdown wlan0
# sudo ifup wlan0
# dhcpサービスとnode-jsを起動するため自動起動を設定する
# sudo systemctl disable checkWifi.service
# sudo systemctl disable bezeMenu.service
sudo systemctl enable wifiSetting.service
#echo "Please Wait for 10 seconds"
#sleep 10
# DHCPサービスの起動
#sudo service isc-dhcp-server restart
# node-js起動
#node /home/pi/bezelie/testpi/wifiSetting.js
reboot

<< comment
# 再起動
while true;do
    echo "May I reboot? (y/n)"
    read answer
    case $answer in
        y)
            echo "tyeped y.\n"
            reboot
            break
            ;;
        n)
            echo "tyeped n.\n"
            break
            ;;
        *)
            echo -e "cannot understand $answer.\n"
            ;;
    esac
done
comment
