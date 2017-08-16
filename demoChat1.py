#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Simple Conversation

import time
from time import sleep
from datetime import datetime
import datetime
import csv
from random import randint
import subprocess
import socket #  ソケット通信モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール
import json
import bezelie

csvFile = "chatDialog.csv"  # 対話リスト
jsonFile = "data_chat.json"  # 設定ファイル
sensitivity = 30 

# Variables
muteTime = 1  # 音声入力を無視する時間
bufferSize = 256 # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。
alarmStop = False # アラーム
beforeTime = time.time()

# 設定ファイルの読み込み
f = open (jsonFile,'r')
jDict = json.load(f)
alarmOn = jDict['data1'][0]['alarmOn']
alarmTime = jDict['data1'][0]['alarmTime']
alarmKind = jDict['data1'][0]['alarmKind']
alarmVol = jDict['data1'][0]['alarmVol']
awake1Start = jDict['data1'][0]['awake1Start']
awake1End = jDict['data1'][0]['awake1End']
awake2Start = jDict['data1'][0]['awake2Start']
awake2End  = jDict['data1'][0]['awake2End']
print (jDict)

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
subprocess.call('sh openJTalk.sh "ちょっとまってて"', shell=True)
print "Please Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh chat.sh"], stdout=subprocess.PIPE, shell=True)
  # subprocess.PIPEは標準ストリームに対するパイプを開くことを指定するための特別な値
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
# client.connect(('10.0.0.1', 10500))  # Juliusサーバーに接続
client.connect(('localhost', 10500))  # Juliusサーバーに接続

# Functions
def writeFile(text):
  f = open ('out.txt', 'r')
  textBefore = ""
  for row in f:
#    print row+"\n"
    textBefore = textBefore + row
  f.close()
  f = open ('out.txt', 'w')
  f.write(textBefore+text+"\n")
  f.close()
  sleep(0.1)

def replyMessage(keyWord):
  # writeFile("reply start")
  data = []
  with open(csvFile, 'rb') as f:  # opening the datafile to read as utf_8
    for i in csv.reader(f):
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making a candidate list
    if unicode(i[0], 'utf-8')==keyWord:  # i[0]はstrなのでutf-8に変換して比較する必要がある
      j = randint(1,100)          # Adding random value to probability
      data1.append(i+[j]+[index]) # Candidates data

  if data1 == []:
    for index,i in enumerate(data): # making a candidate list
      if i[0]=='不一致':  # 該当するキーワードが見つからなかった場合は、「不一致」から返答する
        j = randint(1,100)          # Adding random value to probability
        data1.append(i+[j]+[index]) # Candidates data

  maxNum = 0
  for i in data1:                 # decision
    if i[2] > maxNum:             # Whitch is the max probability.
      maxNum = i[2]               # Max probability
      ansNum = i[3]               # Index of answer

  # Talk
  subprocess.call('sudo amixer -q sset Mic 0', shell=True)  #
  bezelie.actTalk()
  # bezelie.moveHead (20)
  print "Bezelie..."+data[ansNum][1]

  if timeCheck():
    subprocess.call('sh openJTalk.sh "'+data[ansNum][1]+'"', shell=True)
  # subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum ][1] +'" | aplay -q', shell=True)
  else:
    print "活動時間外なので発声はしません"

#  alarmStop = True # アラームを止める
  bezelie.moveCenter()
  # bezelie.moveHead (0, 1)
  sleep (muteTime)
  subprocess.call('sudo amixer -q sset Mic 40', shell=True)  #

def timeCheck(): # 活動時間内かどうかのチェック
  f = open (jsonFile,'r')
  jDict = json.load(f)
  awake1Start = jDict['data1'][0]['awake1Start']
  awake1End = jDict['data1'][0]['awake1End']
  awake2Start = jDict['data1'][0]['awake2Start']
  awake2End  = jDict['data1'][0]['awake2End']
  t = datetime.datetime.now()
  if   int(t.hour) >  int(awake1Start[0:2]) and int(t.hour) <    int(awake1End[0:2]):
    flag = True
  elif int(t.hour) == int(awake1Start[0:2]) and int(t.minute) >= int(awake1Start[3:5]):
    flag = True
  elif int(t.hour) == int(awake1End[0:2])   and int(t.minute) <= int(awake1End[3:5]):
    flag = True
  elif int(t.hour) >  int(awake2Start[0:2]) and int(t.hour) <    int(awake2End[0:2]):
    flag = True
  elif int(t.hour) == int(awake2Start[0:2]) and int(t.minute) >= int(awake2Start[3:5]):
    flag = True
  elif int(t.hour) == int(awake2End[0:2])   and int(t.minute) <= int(awake2End[3:5]):
    flag = True
  else:
    flag = False # It is not Active Time
  return flag

def alarmCheck():
  global beforeTime
  global alarmStop
  flag = False
  nowTime = time.time()
  if (nowTime - beforeTime) > 10: # check by 20 seconds
    f = open (jsonFile,'r')
    jDict = json.load(f)
    alarmOn = jDict['data1'][0]['alarmOn']
    alarmTime = jDict['data1'][0]['alarmTime']
    alarmKind = jDict['data1'][0]['alarmKind']
    alarmVol = jDict['data1'][0]['alarmVol']
    t = datetime.datetime.now()
    print t.hour
    print t.minute
    print alarmTime[0:2]
    print alarmTime[3:5]

    if int(t.hour) == int(alarmTime[0:2]) and int(t.minute) == int(alarmTime[3:5]):
      if alarmStop == False:
        print 'アラームの時間です'
        flag = True
    else:
      print '_'
      alarmStop = False
    beforeTime = nowTime
  return flag

def alarmRing():
  writFile("Ring")

# Get Started
# bezelie.moveCenter()
subprocess.call('sudo amixer -q sset Mic 40', shell=True)  # マイク感度の設定。62が最大値。

# Main Loop
try:
  data = ""
  print "Please Speak"
#  bezelie.actHappy()
  subprocess.call('sh openJTalk.sh "もしもし"', shell=True)
#  bezelie.moveCenter()
#  writeFile("start")
#  print timeCheck()
  while True:
#    flag = timeCheck()
    if True:
      if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
        try:
          # dataから必要部分だけ抽出し、かつエラーの原因になる文字列を削除する。
          data = data[data.find("<RECOGOUT>"):].replace("\n.", "").replace("</s>","").replace("<s>","")
#           writeFile("data setted----------------------")
#           writeFile(data)
          # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接 $
          root = ET.fromstring('<?xml version="1.0"?>\n' + data)
          # root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n.", ""))
#        writeFile("root setted----------------------")
#        writeFile(root)
          keyWord = ""
          for whypo in root.findall("./SHYPO/WHYPO"):
            keyWord = keyWord + whypo.get("WORD")
            # writeFile("."+keyWord)
          print "You......."+keyWord
#          writeFile("lets start reply")
          replyMessage(keyWord)
#          writeFile("answerd")
        except:
          print "------------------------"
#          writeFile("except")
        data = ""  # 認識終了したのでデータをリセットする
      else:
        data = data + client.recv(bufferSize)  # Juliusサーバーから受信
#        writeFile("data added")

          # /RECOGOUTに達するまで受信データを追加していく

except KeyboardInterrupt: # CTRL+Cで終了
  print "  終了しました"
#  writeFile("---------------------------")
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()

