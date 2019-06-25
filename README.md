# line-bot-virit-chi
ひらがな変換bot

# 使い方

```
git clone https://github.com/Fironn/line-bot-virit-chi.git
```

```
cd line-bot-virit-chi
```

```
pip3 install flask
pip3 install linebot
pip3 install goolabs
pip3 install langdetect 
```

## LINE Developper設定をする
参考  <https://qiita.com/Takagenki/items/b2a67422e7226a16e2b1>


## gooラボAPIに登録する
参考  <https://labs.goo.ne.jp/apiusage/>


`token.json` と `gooToken.json` をつくる

token.json
```
{
    "Id":"YOUR_LINE_APP_ID",
    "Access-Secret":"YOUR_LINE_ACCESS_SECRET",
    "Access-Token":"YOUE_LINE_API_TOKEN"
}
```

gooToken.json
```
{
    "App-Id":"YOUR_GOOLAB_APP_ID"
}
```

```
python3 app.py
```


# Credit

supported by goo

[<img src="http://u.xgoo.jp/img/sgoo.png" width="110px">](http://www.goo.ne.jp/)