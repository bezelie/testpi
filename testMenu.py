# -*- coding: utf-8 -*-
# Bezelie test code for Raspberry Pi : GUI

import sys
import Tkinter  # Tk Interface
from PIL import Image, ImageTk  # Python Image Library
import subprocess
import bezelie

mainWindow = Tkinter.Tk() # Tk Objectのインスタンスを生成
mainWindow.title("Bezelie Menu")
mainWindow.geometry("640x520")

head = Tkinter.IntVar()
back = Tkinter.IntVar()
stage = Tkinter.IntVar()
head.set(0)
back.set(0)
stage.set(0)

def runFunction1():
  titleLabelWidget.config(text = "せりふデータを編集します")
  subprocess.call('sudo leafpad /home/pi/bezelie/testpi/bezeTalk.csv', shell=True)

def speakerFunction():
  titleLabelWidget.config(text = "音がでましたか？")
  subprocess.call('aplay Front_Center.wav', shell=True)

def runFunction3():
  titleLabelWidget.config(text = "オンラインマニュアルを開きます")
  subprocess.call('epiphany http://bezelie.com', shell=True)

def centeringFunction():
  titleLabelWidget.config(text = "サーボをセンタリングしました")
  subprocess.call('python /home/pi/bezelie/pi/bezelie.py', shell=True)

def moveHeadFunction(n):
  bezelie.moveHead(head.get()) 
def moveBackFunction(n):
  bezelie.moveBack(back.get()) 
def moveStageFunction(n):
  bezelie.moveStage(stage.get()) 

def picturesFunction():
  titleLabelWidget.config(text = "Picturesディレクトリの中を表示しました")
  subprocess.call('gpicview /home/pi/Pictures/', shell=True)

def headPlusFunction():
  pass

def headMinusFunction():
  pass

def headAdjFunction():
  pass

def backPlusFunction():
  pass

def backMinusFunction():
  pass

def backAdjFunction():
  pass

def stagePlusFunction():
  pass

def stageMinusFunction():
  pass

def stageAdjFunction():
  pass


def configFunction():
  configWindow = Tkinter.Toplevel()
  configWindow.title("Config Menu")

  configFrame = Tkinter.Frame(configWindow,
    height = 20, width = 60,
    background = "yellow")

  titleConfigLabel = Tkinter.Label(configFrame,
    height = 1, width = 20,
    font = ("Times", 16, "normal"),
    text = "コンフィグメニュー")

  headAdjLabel = Tkinter.Label(configFrame,
    height = 1, width = 20,
    font = ("Times", 16, "normal"),
    text = "HEAD センタリング調整値")

  backAdjLabel = Tkinter.Label(configFrame,
    height = 1, width = 20,
    font = ("Times", 16, "normal"),
    text = "BACK センタリング調整値")

  stageAdjLabel = Tkinter.Label(configFrame,
    height = 1, width = 20,
    font = ("Times", 16, "normal"),
    text = "STAGE センタリング調整値")

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

  headAdjDisp = Tkinter.Label(configFrame,
    height = 1, width = 4,
    font = ("Times", 16, "normal"),
    text = " ")

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

  backAdjDisp = Tkinter.Label(configFrame,
    height = 1, width = 4,
    font = ("Times", 16, "normal"),
    text = " ")

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

  stageAdjDisp = Tkinter.Label(configFrame,
    height = 1, width = 4,
    font = ("Times", 16, "normal"),
    text = " ")

  configFrame.pack()
  titleConfigLabel.grid(
    column = 0, row = 0)
  headAdjLabel.grid(
    column = 0, row = 1)
  backAdjLabel.grid(
    column = 0, row = 2)
  stageAdjLabel.grid(
    column = 0, row = 3)
  headPlusButton.grid(
    column = 1, row = 1)
  headAdjDisp.grid(
    column = 2, row = 1)
  headMinusButton.grid(
    column = 3, row = 1)
  backPlusButton.grid(
    column = 1, row = 2)
  backAdjDisp.grid(
    column = 2, row = 2)
  backMinusButton.grid(
    column = 3, row = 2)
  stagePlusButton.grid(
    column = 1, row = 3)
  stageAdjDisp.grid(
    column = 2, row = 3)
  stageMinusButton.grid(
    column = 3, row = 3)

# フレーム
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
image = Image.open('header.jpg')  # Open Image File
im = ImageTk.PhotoImage(image)  # Convert jpg into PhotoImage
logoLabelWidget = Tkinter.Label(mainFrame, 
  image = im,
  height = 60, width = 640)

centeringButtonWidget = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "サーボのセンタリング",
  command = centeringFunction)

headScaleWidget = Tkinter.Scale(mainFrame,
  digits = 2,
  from_ = -90, to = 90,
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
  from_ = -90, to = 90,
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
  from_ = -90, to = 90,
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

buttonWidget1 = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "せりふデータの編集",
  command = runFunction1)

buttonWidget3 = Tkinter.Button(mainFrame,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "オンラインマニュアル",
  command = runFunction3)

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

mainFrame.pack()
titleLabelWidget.grid(
  column = 0, row = 0)
addressLabelWidget.grid(
  column = 0, row = 1)
#logoLabelWidget.grid(
#  column = 0, row = 2)
centeringButtonWidget.grid(
  column = 0, row = 3)
headScaleWidget.grid(
  column = 0, row = 4)
backScaleWidget.grid(
  column = 0, row = 5)
stageScaleWidget.grid(
  column = 0, row = 6)
speakerButtonWidget.grid(
  column = 0, row = 7)
picturesButtonWidget.grid(
  column = 0, row = 8)
buttonWidget1.grid(
  column = 0, row = 9)
buttonWidget3.grid(
  column = 0, row = 10)
configButtonWidget.grid(
  column = 0, row = 11)
exitButtonWidget.grid(
  column = 0, row = 12)


#  configWindow.mainloop()  # このメインループを実行することで初めて画像が表示される。

#button1Instance.bind('<Leave>', offFunction)

# Get Started
bezelie.initPCA9685()

# Mail Loop
getIP = subprocess.Popen(["hostname -I | awk -F' ' '{print $1}'"], stdout=subprocess.PIPE, shell=True)
myIP = getIP.stdout.read()
addressLabelWidget.config(text = "IP Address =" +myIP)
mainWindow.mainloop()  # このメインループを実行することで初めて画像が表示される。
