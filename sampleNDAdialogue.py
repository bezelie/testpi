#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Recognition

from time import sleep
import socket  # ソケット通信モジュール
import xml.etree.ElementTree as ET  # XMLエレメンタルツリー変換モジュール
import json
import requests
import subprocess

# constants
API_URL = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY='
API_KEY = '7445504c6f574d48614734364341597563366449735879762e6c396e42356f74792e486f53573061572f38'
url_key = API_URL + API_KEY

# variables
message = "おやすみなさい"
context = ""
payloadDic = {
    "utt": message,
    "context": context,
    "nickname": "光",
    "nickname_y": "ヒカリ",
    "sex": "女",
    "bloodtype": "B",
    "birthdateY": "1997",
    "birthdateM": "5",
    "birthdateD": "30",
    "age": "16",
    "constellations": "双子座",
    "place": "東京",
    "mode": "dialog"
}
bufferSize = 1024  # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。

# functions
def postAPI
payloadStr = json.dumps(payloadDic)
responseClass = requests.post(url_key, data=payloadStr)
responseDic = responseClass.json()
responseStr = responseDic['utt'].encode('utf-8')
print responseStr
subprocess.call('/home/pi/bezelie/testpi/openJTalk.sh '+ responseStr, shell=True)


# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Pleas Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh /home/pi/bezelie/pi/julius.sh"], stdout=subprocess.PIPE, shell=True)
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
client.connect(('localhost', 10500))  # Juliusサーバーに接続。portはデフォルトが10500。

# Get Started
subprocess.call('sudo amixer -q sset Mic 62', shell=True)  # マイク感度を最大にする

# Main Loop
try:
  data = ""
  print "Please Speak"
  while True:
    if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
      try:
        root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n.", ""))
        # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接取り込む
        for whypo in root.findall("./SHYPO/WHYPO"):
          keyWord = whypo.get("WORD")
        print "You might speak..."+keyWord
        subprocess.call('sudo amixer -q sset Mic 0', shell=True)  # 自分の声を取り込まないようにマイクをオフにする
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ keyWord +'" | aplay -q', shell=True)
        subprocess.call('sudo amixer -q sset Mic 62', shell=True)  #
      except:
        print "error"
      data = ""  # 認識終了したのでデータをリセットする
    else:
      response = client.recv(bufferSize)
      data = data + response  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

except KeyboardInterrupt:
  # CTRL+Cで終了
  print "  ありがとうございました"
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()





