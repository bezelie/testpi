# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Simple Conversation

from datetime import datetime      # 現在時刻取得
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール
import subprocess                  #
import threading                   # マルチスレッド処理
import bezelie_new as bezelie      # べゼリー専用モジュール
import socket                      # ソケット通信モジュール
import json                        #
import csv                         #

csvFile = "chatDialog.csv"           # 対話リスト
jsonFile = "data_chat.json"          # 設定ファイル
openJTalkFile = "shell_openJTalk.sh" #
juliusFile = "shell_juliusChat.sh"   #
sensitivity = 50                     # マイク感度の設定。62が最大値。

# Variables
muteTime = 1      # 音声入力を無視する時間
bufferSize = 256  # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。
alarmStop = False # アラームのスヌーズ機能（非搭載）

# Servo Setting
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.setTrim(head=0, back=-5, stage=0) # センター位置の微調整
bez.moveCenters()                     # ０番から７番までのサーボをセンタリング
sleep(0.5)

# Julius
# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
subprocess.call("sh "+openJTalkFile+" "+"起動します", shell=True)
sleep(1)
print "Please Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh "+juliusFile], stdout=subprocess.PIPE, shell=True)
# subprocess.PIPEは標準ストリームに対するパイプを開くことを指定するための特別な値
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid
# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('10.0.0.1', 10500))  # Juliusサーバーに接続
client.connect(('localhost', 10500))  # Juliusサーバーに接続

# Functions
def writeFile(text): # デバッグ用機能
  f = open ('out.txt', 'r')
  textBefore = ""
  for row in f:
    print row+"\n"
    textBefore = textBefore + row
  f.close()
  f = open ('out.txt', 'w')
  f.write(textBefore+text+"\n")
  f.close()
  sleep(0.1)

def replyMessage(keyWord):        # 対話
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

  # 発話
  subprocess.call('sudo amixer -q sset Mic 0', shell=True)  # 自分の声を認識してしまわないようにマイクを切る
  print "Bezelie..."+data[ansNum][1]

  if timeCheck(): # 活動時間かどうかをチェック
    bez.moveRnd()
    subprocess.call("sh "+openJTalkFile+" "+data[ansNum][1], shell=True)
    bez.stop()
  else:
    print "活動時間外なので発声・動作しません"

  alarmStop = True # アラームを止める
  sleep (muteTime)
  subprocess.call('sudo amixer -q sset Mic '+str(sensitivity), shell=True)  #

def timeCheck(): # 活動時間内かどうかのチェック
  f = open (jsonFile,'r')
  jDict = json.load(f)
  awake1Start = jDict['data1'][0]['awake1Start']
  awake1End = jDict['data1'][0]['awake1End']
  awake2Start = jDict['data1'][0]['awake2Start']
  awake2End  = jDict['data1'][0]['awake2End']
  t = datetime.now()
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

def alarm():
  global alarmStop
  f = open (jsonFile,'r')
  jDict = json.load(f)
  alarmOn = jDict['data1'][0]['alarmOn']
  alarmTime = jDict['data1'][0]['alarmTime']
  alarmKind = jDict['data1'][0]['alarmKind']
  # alarmVol = jDict['data1'][0]['alarmVol']
  now = datetime.now()
  print 'Time: '+str(now.hour)+':'+str(now.minute)

  #if True: # アラーム動作のチェック用
  if int(now.hour) == int(alarmTime[0:2]) and int(now.minute) == int(alarmTime[3:5]):
    if alarmOn == "true":
      if alarmStop == False:
        print 'アラームの時間です'
        subprocess.call('sudo amixer -q sset Mic 0', shell=True)  #
        if alarmKind == 'mild':
          bez.moveAct('happy')
          subprocess.call("sh "+openJTalkFile+" "+"朝ですよ", shell=True)
          bez.stop()
        else:
          bez.moveAct('happy')
          subprocess.call("sh "+openJTalkFile+" "+"朝だよ起きて起きてー", shell=True)
          bez.stop()
        sleep (muteTime)
        subprocess.call('sudo amixer -q sset Mic '+str(sensitivity), shell=True)  #
      else:
        print '_'
        alarmStop = False
    else:
      print 'アラームの時間ですが、アラームはオフになっています'
  t=threading.Timer(20,alarm) # ｎ秒後にまたスレッドを起動する
  t.setDaemon(True)           # メインスレッドが終了したら終了させる
  t.start()

# Set up
subprocess.call('amixer cset numid=1 100%', shell=True)                  # Speakerr
subprocess.call('sudo amixer -q sset Mic '+str(sensitivity), shell=True) # Mic

t=threading.Timer(10,alarm)
t.setDaemon(True)
t.start()

# Main Loop
def main():
  try:
    data = ""
    print "Please Speak"
    bez.moveAct('happy')
    subprocess.call("sh "+openJTalkFile+" "+"どうもです", shell=True)
    bez.stop()
    while True:
      if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
        try:
          # dataから必要部分だけ抽出し、かつエラーの原因になる文字列を削除する。
          data = data[data.find("<RECOGOUT>"):].replace("\n.", "").replace("</s>","").replace("<s>","")
          # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接 $
          root = ET.fromstring('<?xml version="1.0"?>\n' + data)
          # root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n.", ""))
          keyWord = ""
          for whypo in root.findall("./SHYPO/WHYPO"):
            keyWord = keyWord + whypo.get("WORD")
            # writeFile("."+keyWord)
          print "You......."+keyWord
          replyMessage(keyWord)
        except:
          print "------------------------"
        data = ""  # 認識終了したのでデータをリセットする
      else:
        data = data + client.recv(bufferSize)  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

  except KeyboardInterrupt: # CTRL+Cで終了
    print "  終了しました"
    p.kill()
    subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
    client.close()
    bez.stop()

if __name__ == "__main__":
#    pass
    main()
