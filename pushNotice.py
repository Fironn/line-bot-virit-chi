# -*- coding: utf-8 -*-

from linebot import LineBotApi
from linebot.models import TextSendMessage
import json

codeUrl="token.json"
f = open(codeUrl, 'r')

codeData = json.load(f)
f.close()

LINE_CHANNEL_ACCESS_TOKEN = codeData["Access-Token"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


def main():
    user_id = "Ud1490f8802fcbac0e7255609c82a08a8"

    messages = TextSendMessage(text="こんにちは😁\n最近はいかがお過ごしでしょうか?")
    line_bot_api.push_message(user_id, messages=messages)


if __name__ == "__main__":
    main()