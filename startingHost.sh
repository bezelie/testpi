#!/bin/bash
echo "Please Wait for 10 seconds"
sleep 10
# DHCPサービスの起動
sudo service isc-dhcp-server start
# node-js起動
node /home/pi/bezelie/testpi/bezeHost.js
exit 0
