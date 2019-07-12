#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
print('Content-type: text/html; charset=UTF-8\n')

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import toHiragana
import wordNet
from translate_text import tran
import json

codeUrl="token.json"
f = open(codeUrl, 'r')

codeData = json.load(f)
f.close()

LINE_CHANNEL_ACCESS_TOKEN = codeData["Access-Token"]
LINE_CHANNEL_SECRET=codeData["Access-Secret"]

api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

langList = ['ja','ko','zh-cn']



@app.route('/')
def index():
    return "index page"
 
@app.route('/hello')
def hello():
    return "Hello, World!"
 
# if __name__=='__main__':
#     CGIHandler().run(app)
#     DEBUG = os.path.exists(os.path.expanduser('~/debug'))
#     if DEBUG:
#         run(host='localhost', port=8080, debug=True)
#     else:
#         run(host='0.0.0.0', port=80, server="cgi")			


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if(event.message.text.strip().replace(" ", "").replace("\u3000", "")[0]=='-' and event.message.text.strip().replace(" ", "").replace("\u3000", "")[1]=='s'):
        word=event.message.text.replace("-s ", "")
        wordList=word.split()
        res=''
        for w in wordList:
            synonym = wordNet.getSynonym(w)
            # print(synonym)
            res+=w+' : '
            for s in synonym:
                res+=synonym[s][1]+'('+toHiragana.toHiragana(synonym[s][1])+') '
            res+='\n'
        api.reply_message( event.reply_token, TextSendMessage(text=res))

    if(event.message.text.strip().replace(" ", "").replace("\u3000", "")[0]=='-' and event.message.text.strip().replace(" ", "").replace("\u3000", "")[1]=='m'):
        word=event.message.text.replace("-m ", "")
        wordList=word.split()
        res=''
        for w in wordList:
            synonym = wordNet.getSynonym(w)
            # print(synonym)
            res+=w+' : '
            res+='\n\n'
            i=0
            for s in synonym:
                res+='['+str(i+1)+']'
                res+=synonym[s][0]+'\n('+toHiragana.toHiragana(synonym[s][0])+')\n\n'
                i=i+1
            # print(res)
            res+='\n'
        api.reply_message( event.reply_token, TextSendMessage(text=res))

    elif(event.message.text.strip().replace(" ", "").replace("\u3000", "")[0]=='-' and event.message.text.strip().replace(" ", "").replace("\u3000", "")[1]=='h'):
        res='''日本語の文をひらがな変換して返します。
:option
-h help
-s [word][] synonym
-m [word][] definition
-t [sentense] translate to Thai'''
        api.reply_message(
            event.reply_token,
            TextSendMessage(text=res))
    elif(event.message.text.strip().replace(" ", "").replace("\u3000", "")[0]=='-' and event.message.text.strip().replace(" ", "").replace("\u3000", "")[1]=='t'):
        res=tran(event.message.text.replace("-t ", ""))[0]
        if(res['translations'][0]):
            api.reply_message(
                event.reply_token,
                TextSendMessage(text=res['translations'][0]['text']))
    elif(toHiragana.reqLang(event.message.text) in langList):
        res=toHiragana.toHiragana(event.message.text)
        if(res.strip().replace(" ", "").replace("\u3000", "")!=event.message.text.strip().replace(" ", "").replace("\u3000", "")):
            api.reply_message(
                event.reply_token,
                TextSendMessage(text=res))

if __name__ == "__main__":
    app.run()