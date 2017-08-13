# アプリの自動起動を設定する
#!/bin/sh
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
echo "auto start setting"
sudo cp autoStart_app.service /etc/systemd/system/
sudo systemctl enable autoStart_app.service
