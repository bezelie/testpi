#!/bin/bash
echo "Please Wait for 10 seconds"
sleep 10
# DHCPサービスの起動
sudo service isc-dhcp-server start
# node-js起動
node /home/pi/bezelie/testpi/bezeMenu.js
# メッセージ
sh /home/pi/bezelie/testpi/openJTalk.sh "10.0.0.1コロン3000にアクセスしてください"
exit 0
