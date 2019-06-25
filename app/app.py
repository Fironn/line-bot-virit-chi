from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import toHiragana

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

@app.route("/")
def hello_world():
    return "hello world"

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
    if(toHiragana.reqLang(event.message.text) in langList):
        res=toHiragana.toHiragana(event.message.text)
        if(res.strip().replace(" ", "").replace("\u3000", "")!=event.message.text.strip().replace(" ", "").replace("\u3000", "")):
            api.reply_message(
                event.reply_token,
                TextSendMessage(text=res))

if __name__ == "__main__":
    app.run()