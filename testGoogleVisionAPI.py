# coding:utf-8
# import socket
import subprocess
# import threading
import picamera
# from math import fabs
import re
# import os
# import binascii
import json
# from pprint import pprint
from  time import sleep
# import bezelie
import generatejson
import requests

answer = [u'空いた',\
           u"いくつ",\
]

def talk(talkword):
    syscom = '/home/pi/bezelie/aquestalkpi/AquesTalkPi -s 120 ' + talkword + ' | sudo  aplay'
    subprocess.call( syscom , shell=True)

def main():
    # TCPクライアントを作成し接続
#    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    client.connect(('localhost', 10500))
#    sf = client.makefile('')
# re 正規表現ライブラリ
# re.compile : 正規表現パタンを正規表現オブジェクトにする
# Juliusから出力されるXML構造
# <RECOGOUT>
#   <SHYPO RANK="" SCORE="">
#     <WHYPO WORD="" CLASSID="" PHONE="" CM=""/>
#   </SHYPO>
# </RECOGOUT>
#    reHungry = re.compile(u'WHYPO WORD="空いた" .* CM="(\d\.\d*)"')
#    reHow = re.compile(u'WHYPO WORD="いくつ" .* CM="(\d\.\d*)"')

    try:
        while True:
#            line = sf.readline().decode('utf-8').strip("\n\r")
#            word0 = reHungry.search( line )
#            word1 = reHow.search( line )

#            if word1:   # いくつ食べていい？
#                if float(word1.group(1)) > 0.9:
                   with picamera.PiCamera() as camera:
                       camera.resolution = (800, 480)
                       camera.rotation = 180
                       camera.start_preview()
                       sleep(1)
                       talk("どれどれ、写真撮って確認するよ")
                       camera.stop_preview()
                       camera.capture('/home/pi/bezelie/'+ 'detect.jpg')
                       sleep(2)
                       recogData = generatejson.imageRecog('image_detect.txt')
                       response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key=',data=recogData,headers={'Content-Type': 'application/json'})
                       jsondata = json.loads(response.text)
                       print jsondata["responses"][0]["labelAnnotations"][0]["mid"]
                       if jsondata["responses"][0]["labelAnnotations"][0]["mid"] == "/m/06ht1":
                           talk("カップラーメンだね"+"346キロカロリーだよ")
                       else:
                           talk("カロリーメートだね"+"200キロカロリーだよ")
#            else:
#                pass
    except KeyboardInterrupt:
        print "KeyboardInterrupt occured."
        client.close()

if __name__ == "__main__":
    main()
