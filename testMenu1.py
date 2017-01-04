# -*- coding: utf-8 -*-
# Bezelie test code for Raspberry Pi : GUI

import csv
import sys
import Tkinter  # Tk Interface
from PIL import Image, ImageTk  # Python Image Library
import subprocess
import bezelie

csvFile = "bezeConfig.csv"
originalData = []  # Make empty list
configWindow = None

def centeringFunction():
  titleLabelWidget.config(text = "サーボをセンタリングしました")
  subprocess.call('python /home/pi/bezelie/pi/bezelie.py', shell=True)
  head.set(0)
  back.set(0)
  stage.set(0)

def speakerFunction():
  titleLabelWidget.config(text = "音がでましたか？")
  subprocess.call('aplay Front_Center.wav', shell=True)

def picturesFunction():
  titleLabelWidget.config(text = "Picturesディレクトリの中を表示しました")
  subprocess.call('gpicview /home/pi/Pictures/', shell=True)

def editorFunction():
  titleLabelWidget.config(text = "せりふデータを編集します")
  subprocess.call('sudo leafpad /home/pi/bezelie/testpi/bezeTalk.csv', shell=True)

def webFunction():
  titleLabelWidget.config(text = "オンラインマニュアルを開きます")
  subprocess.call('epiphany http://bezelie.com', shell=True)

def moveHeadFunction(n):
  bezelie.moveHead(head.get()) 
def moveBackFunction(n):
  bezelie.moveBack(back.get()) 
def moveStageFunction(n):
  bezelie.moveStage(stage.get()) 

# Make A Config Menu
def configFunction():
  global configWindow
  if configWindow == None or not configWindow.winfo_exists():
    configWindow = Tkinter.Toplevel()
    configWindow.title("Config Menu")
    configWindow.geometry("500x300")

    configFrame = Tkinter.Frame(configWindow,
      background = "white")

    titleConfigLabel = Tkinter.Label(configFrame,
      height = 1, width = 20,
      font = ("Times", 16, "normal"),
      text = "コンフィグメニュー")

    headAdjLabel = Tkinter.Label(configFrame,
      height = 1, width = 18,
      font = ("Times", 16, "normal"),
      text = "HEADセンタリング調整")

    headPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = headPlusFunction)

    headMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = headMinusFunction)

    global headAdjDisp
    headAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    backAdjLabel = Tkinter.Label(configFrame,
      height = 1, width = 18,
      font = ("Times", 16, "normal"),
      text = "BACKセンタリング調整")

    backPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = backPlusFunction)

    backMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = backMinusFunction)

    global backAdjDisp
    backAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    stageAdjLabel = Tkinter.Label(configFrame,
      height = 1, width = 18,
      font = ("Times", 16, "normal"),
      text = "STAGEセンタリング調整")

    stagePlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = stagePlusFunction)

    stageMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = stageMinusFunction)

    global stageAdjDisp
    stageAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    awakingAdjLabel = Tkinter.Label(configFrame,
      height = 1, width = 18,
      font = ("Times", 16, "normal"),
      text = "起床時間設定")

    awakingPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = awakingPlusFunction)

    awakingMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = awakingMinusFunction)

    global awakingAdjDisp
    awakingAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    sleepingAdjLabel = Tkinter.Label(configFrame,
      height = 1, width = 18,
      font = ("Times", 16, "normal"),
      text = "就寝時間設定")

    sleepingPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = sleepingPlusFunction)

    sleepingMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = sleepingMinusFunction)

    global sleepingAdjDisp
    sleepingAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    intervalAdjLabel = Tkinter.Label(configFrame,
      height = 1, width = 18,
      font = ("Times", 16, "normal"),
      text = "発話間隔設定")

    intervalPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = intervalPlusFunction)

    intervalMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = intervalMinusFunction)

    global intervalAdjDisp
    intervalAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    doneConfigButton = Tkinter.Button(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = "決定",
      command = doneConfigFunction)

    cancelConfigButton = Tkinter.Button(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = "閉じる",
      command = cancelConfigFunction)

    # Place widgets on the ConfigWindow
    configFrame.pack()
    titleConfigLabel.grid(column = 0, row = 0)
    headAdjLabel.grid(column = 0, row = 1)
    headPlusButton.grid(column = 1, row = 1)
    headAdjDisp.grid(column = 2, row = 1)
    headMinusButton.grid(column = 3, row = 1)
    backAdjLabel.grid(column = 0, row = 2)
    backPlusButton.grid(column = 1, row = 2)
    backAdjDisp.grid(column = 2, row = 2)
    backMinusButton.grid(column = 3, row = 2)
    stageAdjLabel.grid(column = 0, row = 3)
    stagePlusButton.grid(column = 1, row = 3)
    stageAdjDisp.grid(column = 2, row = 3)
    stageMinusButton.grid(column = 3, row = 3)
    awakingAdjLabel.grid(column = 0, row = 4)
    awakingPlusButton.grid(column = 1, row = 4)
    awakingAdjDisp.grid(column = 2, row = 4)
    awakingMinusButton.grid(column = 3, row = 4)
    sleepingAdjLabel.grid(column = 0, row = 5)
    sleepingPlusButton.grid(column = 1, row = 5)
    sleepingAdjDisp.grid(column = 2, row = 5)
    sleepingMinusButton.grid(column = 3, row = 5)
    intervalAdjLabel.grid(column = 0, row = 6)
    intervalPlusButton.grid(column = 1, row = 6)
    intervalAdjDisp.grid(column = 2, row = 6)
    intervalMinusButton.grid(column = 3, row = 6)
    doneConfigButton.grid(column = 2, row = 7)
    cancelConfigButton.grid(column = 0, row = 7)

    # Read data from csv file
    originalData = []
    with open(csvFile, 'rb') as f:  # Open csv file to read
      for i in csv.reader(f):  # Read csv to i
        originalData.append(i)

    for i in originalData:
      if i[0] == "headAdj":headAdjDisp.config(text = i[1])
      if i[0] == "backAdj":backAdjDisp.config(text = i[1])
      if i[0] == "stageAdj":stageAdjDisp.config(text = i[1])
      if i[0] == "awakingTime":awakingAdjDisp.config(text = i[1])
      if i[0] == "sleepingTime":sleepingAdjDisp.config(text = i[1])
      if i[0] == "intervalTime":intervalAdjDisp.config(text = i[1])

def doneConfigFunction():
  for i in originalData:
    if i[0] == "headAdj":i[1] = headAdjDisp.cget("text")
    if i[0] == "backAdj":i[1] = backAdjDisp.cget("text")
    if i[0] == "stageAdj":i[1] = stageAdjDisp.cget("text")
    if i[0] == "awakingTime":i[1] = awakingAdjDisp.cget("text")
    if i[0] == "sleepingTime":i[1] = sleepingAdjDisp.cget("text")
    if i[0] == "intervalTime":i[1] = intervalAdjDisp.cget("text")
 
  with open(csvFile, 'wb') as f:  # opening the file to overwrite
    csv.writer(f).writerows(originalData)
  cancelConfigFunction()

def cancelConfigFunction():
  global configWindow
  configWindow.withdraw()
  configWindow = None

def headPlusFunction():
  s = headAdjDisp.cget("text")
  i = int(s)+1
  headAdjDisp.config(text = i)
  bezelie.moveHead(i)

def headMinusFunction():
  s = headAdjDisp.cget("text")
  i = int(s)-1
  headAdjDisp.config(text = i)
  bezelie.moveHead(i)

def backPlusFunction():
  s = backAdjDisp.cget("text")
  i = int(s)+1
  backAdjDisp.config(text = i)
  bezelie.moveBack(i)

def backMinusFunction():
  s = backAdjDisp.cget("text")
  i = int(s)-1
  backAdjDisp.config(text = i)
  bezelie.moveBack(i)

def stagePlusFunction():
  s = stageAdjDisp.cget("text")
  i = int(s)+1
  stageAdjDisp.config(text = i)
  bezelie.moveStage(i)

def stageMinusFunction():
  s = stageAdjDisp.cget("text")
  i = int(s)-1
  stageAdjDisp.config(text = i)
  bezelie.moveStage(i)

def awakingPlusFunction():
  s = awakingAdjDisp.cget("text")
  i = int(s)+1
  awakingAdjDisp.config(text = i)

def awakingMinusFunction():
  s = awakingAdjDisp.cget("text")
  i = int(s)-1
  awakingAdjDisp.config(text = i)

def sleepingPlusFunction():
  s = sleepingAdjDisp.cget("text")
  i = int(s)+1
  sleepingAdjDisp.config(text = i)

def sleepingMinusFunction():
  s = sleepingAdjDisp.cget("text")
  i = int(s)-1
  sleepingAdjDisp.config(text = i)

def intervalPlusFunction():
  s = intervalAdjDisp.cget("text")
  i = round(float(s)+0.1,1)
  intervalAdjDisp.config(text = i)

def intervalMinusFunction():
  s = intervalAdjDisp.cget("text")
  i = round(float(s)-0.1,1)
  intervalAdjDisp.config(text = i)

# メインウィンドウ
mainWindow = Tkinter.Tk() # Tk Objectのインスタンスを生成
mainWindow.title("Bezelie Menu")
mainWindow.geometry("640x520")

head = Tkinter.IntVar()
back = Tkinter.IntVar()
stage = Tkinter.IntVar()
head.set(0)
back.set(0)
stage.set(0)

# メインフレーム
mainFrame=Tkinter.Frame(mainWindow,
  height = 20, width = 60,
  borderwidth = 2,
  background = "orange")

# タイトル
titleLabelWidget = Tkinter.Label(mainFrame, 
  height = 1, width = 40,
  borderwidth = 2,
  background = "blue", foreground = "white",
  font = ("Times", 16, "normal"),
  text = "ベゼリーメニュー")

# IPアドレス
addressLabelWidget = Tkinter.Label(mainFrame, 
  height = 2, width = 28,
  borderwidth = 2,
  background = "white", foreground = "blue",
  font = ("Times", 12, "normal"),
  text = "IP Address = ")

# タイトルグラフィック
#image = Image.open('header.jpg')  # Open Image File
#im = ImageTk.PhotoImage(image)  # Convert jpg into PhotoImage
#logoLabelWidget = Tkinter.Label(mainFrame, 
#  image = im,
#  height = 60, width = 640)

centeringButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "サーボのセンタリング",
  command = centeringFunction)

headScaleWidget = Tkinter.Scale(mainFrame,
  digits = 2,
  from_ = -20, to = 20,
  length = 240, width = 15,
  sliderlength = 30,
  orient = "horizontal",
  resolution = 1,
  label = "HEAD SERVO",
  showvalue = "True",
  variable = head,
  command = moveHeadFunction)

backScaleWidget = Tkinter.Scale(mainFrame,
  digits = 2,
  from_ = -30, to = 30,
  length = 240, width = 15,
  sliderlength = 30,
  orient = "horizontal",
  resolution = 1,
  label = "BACK SERVO",
  showvalue = "True",
  variable = back,
  command = moveBackFunction)

stageScaleWidget = Tkinter.Scale(mainFrame,
  digits = 2,
  from_ = -50, to = 50,
  length = 240, width = 15,
  sliderlength = 30,
  orient = "horizontal",
  resolution = 1,
  label = "STAGE SERVO",
  showvalue = "True",
  variable = stage,
  command = moveStageFunction)

speakerButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "スピーカーテスト",
  command = speakerFunction)

picturesButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "画像ディレクトリの表示",
  command = picturesFunction)

editorButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "せりふデータの編集",
  command = editorFunction)

webButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "オンラインマニュアル",
  command = webFunction)

configButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "コンフィグ画面を開く",
  command = configFunction)

exitButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "ウィンドウを閉じる",
  command = sys.exit)

# Place widgets on the mainWindow
mainFrame.pack()
titleLabelWidget.grid(column = 0, row = 0)
addressLabelWidget.grid(column = 0, row = 1)
#logoLabelWidget.grid(column = 0, row = 2)
centeringButtonWidget.grid(column = 0, row = 3)
headScaleWidget.grid(column = 0, row = 4)
backScaleWidget.grid(column = 0, row = 5)
stageScaleWidget.grid(column = 0, row = 6)
speakerButtonWidget.grid(column = 0, row = 7)
picturesButtonWidget.grid(column = 0, row = 8)
editorButtonWidget.grid(column = 0, row = 9)
webButtonWidget.grid(column = 0, row = 10)
configButtonWidget.grid(column = 0, row = 11)
exitButtonWidget.grid(column = 0, row = 12)

#button1Instance.bind('<Leave>', offFunction)

# Get Started
bezelie.initPCA9685()

# Mail Loop
getIP = subprocess.Popen(["hostname -I | awk -F' ' '{print $1}'"], stdout=subprocess.PIPE, shell=True)
myIP = getIP.stdout.read()
addressLabelWidget.config(text = "IP Address =" +myIP)
mainWindow.mainloop()  # このメインループを実行することで初めて画像が表示される。
