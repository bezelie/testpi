#!/bin/sh
HTSVOICE=/usr/share/hts-voice/mei/mei_happy.htsvoice
#HTSVOICE=/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice
DICDIRE=/var/lib/mecab/dic/open-jtalk/naist-jdic/
VOICEDATA=/tmp/voice.wav
sudo echo "$1" | open_jtalk \
-x $DICDIRE \
-m $HTSVOICE \
-ow $VOICEDATA \
-s 17000 \
-p 100 \
-a 0.03 \
-b 0.0 \
-r 1.5 \
-fm 0.0 \
-u 0.0 \
-jm 1.0 \
-jf 1.0 \
-z 0.0 \

aplay -q $VOICEDATA
sudo rm -f $VOICEDATA
