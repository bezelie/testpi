#!/usr/bin/python
# -*- coding: utf-8 -*-
# Google Cloud Vision API Test Program

import requests
import base64
import json

# POST https://vision.googleapis.com/v1/images:annotate
GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
API_KEY = 'AIzaSyDYM3UustOL3oQdQf1YhOK1HkeMImOpwo4' # GCPで登録したAPIキー

def request_cloud_vison_api(image_base64):
    api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_base64.decode('utf-8') # base64でencodeする。
            },
            'features': [{
                'type': 'LABEL_DETECTION',
#                'type': 'TEXT_DETECTION',
#                'type': 'LOGO_DETECTION',
                'maxResults': 10,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()

def main():
    filepath = '/home/pi/Pictures/tom1.jpg'
    with open(filepath, 'rb') as img:
        img_byte = img.read()
    img_base64 = base64.b64encode(img_byte) 
    result = request_cloud_vison_api(img_base64)
#    print(result)
    print(result['responses'][0]['labelAnnotations'][0]['description'].encode('utf-8'))
#    print(result['responses'][0]['textAnnotations'][0]['description'].encode('utf-8'))
#    print(result['responses'][0]['logoAnnotations'][0]['description'].encode('utf-8'))

if __name__ == "__main__":
    main()
