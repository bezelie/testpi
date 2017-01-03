# -*- coding: utf-8 -*-
# Bezelie test code for Raspberry Pi : Launcher Menu

import sys
import Tkinter  # Tk Interface
import subprocess

mainWindow = Tkinter.Tk() # Tk Objectのインスタンスを生成
mainWindow.title("Test Menu")
mainWindow.geometry("320x280")

# X Window Systemアプリの起動
def editorFunction():
  subprocess.call('sudo leafpad /home/pi/bezelie/testpi/bezeTalk.csv', shell=True)
#  subprocess.call('gpicview /home/pi/Pictures/', shell=True)

# サウンドテスト
def speakerFunction():
  subprocess.call('aplay Front_Center.wav', shell=True)

# Webページを開く
def webFunction():
  subprocess.call('epiphany http://bezelie.com', shell=True)

# pythonプログラムの実行
def centeringFunction():
  subprocess.call('python /home/pi/bezelie/pi/bezelie.py', shell=True)

# タイトル表示
titleLabelWidget = Tkinter.Label(mainWindow, 
  height = 1, width = 30,
  background = "blue", foreground = "white",
  font = ("Times", 16, "normal"),
  text = "テストメニュー")

# pythonプログラムの実行
centeringButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "サーボのセンタリング",
  command = centeringFunction)

# サウンドテスト
speakerButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "スピーカーテスト",
  command = speakerFunction)

# X Window Systemアプリの実行
editorButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "せりふデータの編集",
  command = editorFunction)

# Webページの表示
webButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "オンラインマニュアル",
  command = webFunction)

# 閉じるボタン
exitButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "ウィンドウを閉じる",
  command = sys.exit)

titleLabelWidget.pack()
centeringButtonWidget.pack()
speakerButtonWidget.pack()
editorButtonWidget.pack()
webButtonWidget.pack()
exitButtonWidget.pack()

# Mail Loop
mainWindow.mainloop()  # このメインループを実行することで初めて画像が表示される。
