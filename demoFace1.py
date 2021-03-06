# -*- coding: utf-8 -*-
# Bezelie Face Recognition Test
# カメラで顔を認識したら喋る
# 以前はopenGLのエラーでていたためpygameで画像を出力しているが、
# 現在はこの対処の必要はなく、cv2.inshowで表示してよい。

import picamera
import picamera.array
import cv2              # Open CV 2
import pygame
import sys              # for sys.exit()
import subprocess
import bezelie
import csv
from time import sleep
from random import randint

csvFile = "bezeTalkFace.csv"
pygame.init()
size=(320,240)
screen = pygame.display.set_mode(size)

def bezeTalk(distance):
  data = []
  with open(csvFile, 'rb') as f:  # opening the data file to read
    for i in csv.reader(f):
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]=="long" or i[1]=="short":            # matching check
      j = int(i[3])*randint(1,100)# Adding random to probability
      data1.append(i+[j]+[index]) # Candidates data

  maxNum = 0
  for i in data1:                 # decision
    if i[5] > maxNum:             # Whitch is the max probability.
      maxNum = i[5]               # Max probability
      ansNum = i[6]               # Index of answer

  # AquesTalk

  k = int(randint(1,4))
  if k == 1:
    bezelie.moveHead (20)
  elif k == 2:
    bezelie.moveBack (10)
  elif k == 3:
    bezelie.moveHead (-10)
    sleep(0.2)
    bezelie.moveHead (0)
    sleep(0.2)
    bezelie.moveHead (-10)
  elif k == 4:
    bezelie.moveBack (-10)
    sleep(0.2)
    bezelie.moveBack (10)
    sleep(0.2)
    bezelie.moveBack (-10)
    sleep(0.2)
    bezelie.moveBack (0)

  print data[ansNum][2]
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum ][2] +'" | aplay', shell=True)

def pygame_imshow(array):
  b,g,r = cv2.split(array)
  rgb = cv2.merge([r,g,b])
  surface1 = pygame.surfarray.make_surface(rgb)       
  surface2 = pygame.transform.rotate(surface1, -90)
  surface3 = pygame.transform.flip(surface2, True, False)
  screen.blit(surface3, (0,0))
  pygame.display.flip()

cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)

# Get Started
bezelie.initPCA9685()
#bezelie.moveCenter()
bezelie.moveHead (0)
sleep(0.5)
bezelie.moveBack (0)
sleep(0.5)
yaw = 0
delta = 1

# Main Loop
with picamera.PiCamera() as camera:
  with picamera.array.PiRGBArray(camera) as stream:
    camera.resolution = (320, 240) # ディスプレイの解像度に合わせてください。
    camera.hflip = True            # 上下反転。不要なら削除してください。
    camera.vflip = True            # 左右反転。不要なら削除してください。
    sleep (1)

    while True:
      # stream.arrayにBGRの順で映像データを格納
      camera.capture(stream, 'bgr', use_video_port=True)
      # グレースケール画像に変換しgrayに代入
      gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
      # grayから顔を探す
      facerect = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2, minSize=(60,80), maxSize=(200,220))
      # scaleFactor 大きな値にすると速度が早くなり、精度が落ちる。1.1〜1.9ぐらい。
      # minNeighbors 小さな値にするほど顔が検出されやすくなる。通常は3〜6。
      # minSize 検出する顔の最小サイズ。解像度に合わせて修正してください。
      # maxSize 検出する顔の最大サイズ。解像度に合わせて修正してください。
      if len(facerect) > 0:   # 顔が検出された場合の処理
        for rect in facerect: # 顔の場所に四角を表示 
          # rect[0:2]:長方形の左上の座標, rect[2:4]:長方形の横と高さ
          # rect[0:2]+rect[2:4]:長方形の右下の座標
          cv2.rectangle(stream.array, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (0,255,0), thickness=4)

#        bezelie.moveHead (20)
#        sleep (0.2)
        bezeTalk ("long")
        #subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "こんにちわー" | aplay', shell=True)
        bezelie.moveHead (0)
        sleep(0.5)
        bezelie.moveBack (0)
        sleep(0.5)

      # pygameで画像を表示
      pygame_imshow(stream.array)

      # "q"を入力でアプリケーション終了
      for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_q:
            pygame.quit()
            sys.exit()

      # streamをリセット
      stream.seek(0)
      stream.truncate()

      # yawサーボを回す
      bezelie.moveStage (yaw)
      sleep (0.1)
      yaw = yaw + delta
      if yaw > 15 or yaw < -15:
        delta = delta * -1
