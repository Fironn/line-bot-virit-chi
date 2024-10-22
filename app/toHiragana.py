from goolabs import GoolabsAPI
import json
from langdetect import detect


codeUrl="gooToken.json"
f = open(codeUrl, 'r')

codeData = json.load(f)
f.close()

app_id = str(codeData["App-Id"])
api = GoolabsAPI(app_id)

def toHiragana(sentence):
    res=api.hiragana(
       request_id="hiragana-req002",
       sentence=sentence,
       output_type="hiragana" # hiragana or katakana
    )
    return res["converted"]

def reqLang(sentence):
    lang = detect(sentence)
    return lang

