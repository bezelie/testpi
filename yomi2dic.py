# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Recognition

import subprocess

subprocess.call(["sudo sh -c 'iconv -f utf8 -t eucjp bezeWord.yomi | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > bezeWord.dic'"], shell=True)
