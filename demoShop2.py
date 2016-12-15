# -*- coding: utf-8 -*- 
# Bezelie Special Code for Shanghi-Donya
# +Face Recognition 

import picamera
import picamera.array
import cv2
import pygame
import sys
import subprocess
import csv
import datetime
from time import sleep
from random import randint
#import RPi.GPIO as GPIO
import bezelie

csvFile = "bezeTalkShop.csv"
pygame.init()
size=(800,480)
screen = pygame.display.set_mode(size)
openTime = 0
closeTime = 24

# Definition
def timeMessage(timeSlot):
  data = []
  with open(csvFile, 'rb') as f:  # opening the data file to read
    for i in csv.reader(f):       
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]==timeSlot:            # Checking time
      j = int(i[3])*randint(1,100)# Adding random to probability
      data1.append(i+[j]+[index]) # Candidates data

  maxNum = 0
  for i in data1:                 # decision
    if i[5] > maxNum:             # Whitch is the max probability.
      maxNum = i[5]               # Max probability
      ansNum = i[6]               # Index of answer

  # AquesTalk
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
bezelie.centering()

# Main Loop
with picamera.PiCamera() as camera:
  with picamera.array.PiRGBArray(camera) as stream:
    camera.resolution = (800, 480) # ディスプレイの解像度に合わせてください。
    camera.hflip = True            # 上下反転。不要なら削除してください。
    camera.vflip = True            # 左右反転。不要なら削除してください。
    sleep (1)

    while True:
      # stream.arrayにBGRの順で映像データを格納
      camera.capture(stream, 'bgr', use_video_port=True)
      # グレースケール画像に変換しgrayに代入
      gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
      # grayから顔を探す
      facerect = cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=1, minSize=(200,200), maxSize=(400,400))
      # scaleFactor 大きな値にすると速度が早くなり、精度が落ちる。1.1〜1.9ぐらい。
      # minNeighbors 小さな値にするほど顔が検出されやすくなる。通常は3〜6。
      # minSize 検出する顔の最小サイズ。解像度に合わせて修正してください。
      # maxSize 検出する顔の最大サイズ。解像度に合わせて修正してください。
      if len(facerect) > 0:   # 顔が検出された場合の処理
        for rect in facerect: # 顔の場所に四角を表示 
          # rect[0:2]:長方形の左上の座標, rect[2:4]:長方形の横と高さ
          # rect[0:2]+rect[2:4]:長方形の右下の座標
          cv2.rectangle(stream.array, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (0,255,0), thickness=4)

try:
  while (True):
    now = datetime.datetime.now()
    print now
    if now.hour >= openTime and now.hour < closeTime: # Activate only in the business hour
      with picamera.PiCamera() as camera:
        camera.resolution = (800, 480)                # Display Resolution
        camera.framerate = 30                         # Frame Rate Max = 30fps
        camera.rotation = 180                         # Up side Down
        camera.led = False
        camera.start_preview()
        sleep (0.2)
      
        pit = 0
        while (True):
          bezelie.moveRot (-5)
          sleep (0.2)
          bezelie.moveYaw (-40, 2)
          sleep (0.5)
          bezelie.moveRot ( 5)
          sleep (0.2)
          bezelie.moveYaw ( 40, 2)
          sleep (1)
          bezelie.moveRot (-5)
          sleep (0.2)
          bezelie.moveYaw ( 0, 2)
          bezelie.moveRot ( 0)
          sleep (0.5)
          bezelie.movePit (-15)
          sleep (0.2)
          bezelie.moveRot ( 10)
          sleep (0.2)
          bezelie.moveRot (-10)
          sleep (0.4)
          bezelie.moveRot ( 0)
          timeMessage("afternoon")
          sleep (0.5)
          pit += 5
          if pit > 10:
            pit = -15
          bezelie.movePit (pit)
          sleep (0.2)
    else:
      print "営業時間外です"
      sleep(60)

except:
