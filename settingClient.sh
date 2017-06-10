# ラズパイのアクセスポイント化を解除し、wifiに接続する設定にする
#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
echo "Connecting to WiFi..."
# サービス終了
sudo service isc-dhcp-server stop
# DHCPサーバ無効化
sudo cp config/isc-dhcp-server_original /etc/default/isc-dhcp-server
sudo cp config/dhcpd_original.conf /etc/dhcp/dhcpd.conf
# hostapd設定の初期化
sudo cp config/hostapd_original /etc/default/hostapd
sudo cp config/hostapd_original.conf /etc/hostapd/hostapd.conf
# IPアドレス固定化の無効化
sudo cp config/dhcpcd_original.conf /etc/dhcpcd.conf
# wlan0をアクセスポイントにすることの無効化
sudo cp config/interfaces_original /etc/network/interfaces
# DHCPサービスとnode-jsの自動起動を解除
sudo systemctl disable bezeHost.service
sudo cp bezeMenu.service /etc/systemd/system/
sudo systemctl enable bezeMenu.service
sudo reboot
