# -*- coding: utf-8 -*-
import socket
import cStringIO

# Raspberry PiのIPアドレス
host = '192.168.10.2'
# juliusの待ち受けポート
port = 10500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

xml_buff = ""
in_recoguout = False

while True:
    data = cStringIO.StringIO(sock.recv(4096))
    line = data.readline()
    # 認識結果はRECOGOUTタグで返ってくるのでそこだけ抽出
    while line:
        if line.startswith("<RECOGOUT>"):
            in_recoguout = True
            xml_buff += line
        elif line.startswith("</RECOGOUT>"):
            xml_buff += line
            print xml_buff
            in_recoguout = False
            xml_buff = ""
        else:
            if in_recoguout:
                xml_buff += line
        line = data.readline()
sock.close()
