#!/usr/bin/env python
# -*- coding: utf-8 -*-
# demo Code for Raspberry Pi : Elevator Voice Command

from time import sleep
import csv
import subprocess
import socket #  ソケット通信モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール
import servo

csvFile = "demoElevator.csv"  # 対話リスト

# Variables
stroke = 10  # エレベータのボタンを押すためにサーボを回転させる角度
muteTime = 1  # 音声入力を無視する時間（の半分の秒数）
bufferSize = 1024  # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Please Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh demoElevator.sh"], stdout=subprocess.PIPE, shell=True)
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
client.connect(('localhost', 10500))  # Juliusサーバーに接続

# Functions
def replyMessage(keyWord):
  data = []
  with open(csvFile, 'rb') as f:  # opening the datafile to read as utf_8
    for i in csv.reader(f):
      data.append(i)              # raw data

  message = ""
  for i in data:
    if unicode(i[0], 'utf-8')==keyWord:  # i[0]はstrなのでutf-8に変換して比較する必要がある
      message = i[1]  # str

  # Talk
  if message != "":
    subprocess.call('sudo amixer -q sset Mic 0', shell=True)  #
    print "You might speak..."+keyWord
    print "My reply is..."+message
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ message +'" | aplay -q', shell=True)
    if keyWord == unicode('一階', 'utf-8'):
      servo.servo1(stroke)
    if keyWord == unicode('二階', 'utf-8'):
      servo.servo2(stroke)
    if keyWord == unicode('三階', 'utf-8'):
      servo.servo3(stroke)
    if keyWord == unicode('四階', 'utf-8'):
      servo.servo4(stroke)
    if keyWord == unicode('五階', 'utf-8'):
      servo.servo5(stroke)
    servo.moveCenter()
    subprocess.call('sudo amixer -q sset Mic 62', shell=True)  #

# Get Started
servo.initPCA9685()
servo.moveCenter()
subprocess.call('sudo amixer -q sset Mic 62', shell=True)  #

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
        if keyWord != unicode("不一致", 'utf-8'):
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
