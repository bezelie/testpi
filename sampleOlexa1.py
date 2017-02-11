#!/usr/bin/env python
# -*- coding: utf-8 -*-
# demo Code for Raspberry Pi : Olexa Translator

from time import sleep
import csv
import subprocess
import socket #  ソケット通信モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール
import bezelie

csvFile = "sampleOlexa.csv"  # 対話リスト

# Variables
muteTime = 3     # Alexaの返答を音声認識してしまわないように、音声入力を無視する時間
bufferSize = 1024   # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Please Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh sampleOlexa.sh"], stdout=subprocess.PIPE, shell=True)
  # subprocess.PIPEは標準ストリームに対するパイプを開くことを指定するための特別な値
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid

# Juliusサーバーにアクセスするため自分のIPアドレスを取得する 
# getIP = subprocess.Popen(["hostname -I | awk -F' ' '{print $1}'"], stdout=subprocess.PIPE, shell=True)
# myIP = getIP.stdout.read()
# print "My IP is " +myIP

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
# client.connect((myIP, 10500))  # Juliusサーバーに接続
client.connect(('localhost', 10500))  # localhostでも通るぽい

# Functions
def replyMessage(keyWord):
  data = []
  with open(csvFile, 'rb') as f:  # opening the datafile to read as utf_8
    for i in csv.reader(f):
      data.append(i)              # raw data

  message = ""
  for i in data:  #
    if unicode(i[0], 'utf-8')==keyWord:  # i[0]はstrなのでutf-8に変換して比較する必要がある
      message = i[1]  # str

  # Talk
  if keyWord != unicode("不一致", 'utf-8'):  # キーワードが「不一致」でなければ以下を実行
    if message != "":  # 該当するキーワードがあれば以下を実行
      print "You might speak..."+keyWord
      subprocess.call('sudo amixer -q sset Mic 0', shell=True)  # 自分の声を取り込まないようにマイクをオフにする
      bezelie.moveHead (-10)
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ほいきた" | aplay -q', shell=True)
      bezelie.moveHead (0)
      bezelie.moveStage (40)
      subprocess.call('flite -voice "kal16" -t "Alexa"', shell=True) # Wake Word
#     other voices :kal awb_time kal16 awb rms slt
      sleep (2)
      print "My reply is..."+message
      subprocess.call('flite -voice "kal16" -t "'+ message +'"', shell=True)
      sleep (2)
      bezelie.moveStage (0)
      sleep (muteTime)
      subprocess.call('sudo amixer -q sset Mic 62', shell=True)  # マイクを再びオンにする

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()
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
        replyMessage(keyWord)
      except:
        print "error"
      data = ""  # 認識終了したのでデータをリセットする
    else:
      data = data + client.recv(bufferSize)  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

except KeyboardInterrupt:
  # CTRL+Cで終了
  print "  終了しました"
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()
