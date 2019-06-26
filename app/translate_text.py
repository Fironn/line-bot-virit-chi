# -*- coding: utf-8 -*-
import os
import requests
import uuid
import json

codeUrl="azureToken.json"
f = open(codeUrl, 'r')

codeData = json.load(f)
f.close()

# Checks to see if the Translator Text subscription key is available
# as an environment variable. If you are setting your subscription key as a
# string, then comment these lines out.
# if 'TRANSLATOR_TEXT_KEY' in os.environ:
#     subscriptionKey = os.environ['TRANSLATOR_TEXT_KEY']
# else:
#     print('Environment variable for TRANSLATOR_TEXT_KEY is not set.')
#     exit()
# If you want to set your subscription key as a string, uncomment the line
# below and add your subscription key.
subscriptionKey = codeData['key1']

base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
params = '&to=th'
constructed_url = base_url + path + params

def tran(text):
    headers = {
                'Ocp-Apim-Subscription-Key': subscriptionKey,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    return response