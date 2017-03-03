#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests

# constants
API_URL = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY='
API_KEY = '7445504c6f574d48614734364341597563366449735879762e6c396e42356f74792e486f53573061572f38'
url_key = API_URL + API_KEY

# variables
message = "おやすみなさい"
payloadDic = {
    "utt": message,
    "context": "",
    "nickname": "光",
    "nickname_y": "ヒカリ",
    "sex": "女",
    "bloodtype": "B",
    "birthdateY": "1997",
    "birthdateM": "5",
    "birthdateD": "30",
    "age": "16",
    "constellations": "双子座",
    "place": "東京",
    "mode": "dialog"
}

# main
payloadStr = json.dumps(payloadDic)
response = requests.post(url_key, data=payloadStr)
print response

answer = response['responses'][0]['labelAnnotations'].encode('utf-8')
print answer
