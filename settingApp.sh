# ラズパイをアクセスポイントに
#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
sudo systemctl disable bezeMenu.service
sudo systemctl disable bezeHost.service
sudo systemctl disable bezeHostAndApp.service
sudo cp bezeApp.service /etc/systemd/system/
sudo systemctl enable bezeApp.service
sudo reboot
