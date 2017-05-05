# ラズパイのアクセスポイント化を解除し、wifiに接続する
#!/bin/sh
echo "Connecting to WiFi..."
# wlan0をアクセスポイントにすることの無効化
sudo cp ~/bezelie/testpi/config/interfaces_original /etc/network/interfaces
# サービス終了
sudo service isc-dhcp-server stop
# DHCPサーバ無効化
sudo cp ~/bezelie/testpi/config/isc-dhcp-server_original /etc/default/isc-dhcp-server
sudo cp ~/bezelie/testpi/config/dhcpd_original.conf /etc/dhcp/dhcpd.conf
# hostapd設定の初期化
sudo cp ~/bezelie/testpi/config/hostapd_original /etc/default/hostapd
sudo cp ~/bezelie/testpi/config/hostapd_original.conf /etc/hostapd/hostapd.conf
# IPアドレス固定化の無効化
sudo cp ~/bezelie/testpi/config/dhcpcd_original.conf /etc/dhcpcd.conf
# DHCPサービスとnode-jsの自動起動を解除
# sudo systemctl disable wifiSetting.service
# sudo systemctl enable checkWifi.service
# wifiリセット
sudo ifdown wlan0
sudo ifup wlan0
sudo sh /home/pi/bezelie/testpi/checkingWifi.sh
#reboot
