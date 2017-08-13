#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
echo "Please Wait for 10 seconds"
sleep 10
# DHCPサービスの起動
sudo service isc-dhcp-server start
# node-js起動
node webServer_editChat.js
exit 0
