# ラズパイをアクセスポイントに
#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
echo "Making RaspberryPi an Access Point"
# wlan0をアクセスポイントにする
sudo cp config/interfaces_changed /etc/network/interfaces
# IPアドレス固定 wlan0に固定IPアドレスを割り振る
sudo cp config/dhcpcd_changed.conf /etc/dhcpcd.conf
# サービスを再起動
sudo service dhcpcd start
# sudo service dhcpcd restart
# Hostapdでアクセスポイント化
sudo cp config/hostapd_changed.conf /etc/hostapd/hostapd.conf
# DEAMON_CONF の指定。
sudo cp config/hostapd_changed /etc/default/hostapd
# DHCPサーバ化
sudo cp config/dhcpd_changed.conf /etc/dhcp/dhcpd.conf
sudo cp config/isc-dhcp-server_changed /etc/default/isc-dhcp-server
# dhcpサービスとnode-jsを起動するため自動起動を設定する
sudo systemctl disable bezeMenu.service
sudo systemctl disable bezeHostAndApp.service
sudo systemctl disable bezeApp.service
sudo cp bezeHost.service /etc/systemd/system/
sudo systemctl enable bezeHost.service
sudo reboot
