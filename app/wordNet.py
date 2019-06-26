# ref:
#   WordList_JP: http://compling.hss.ntu.edu.sg/wnja/
#   python3: http://sucrose.hatenablog.com/entry/20120305/p1
import sys, sqlite3
from collections import namedtuple
from pprint import pprint

conn = sqlite3.connect("./wnjpn.db")

Word = namedtuple('Word', 'wordid lang lemma pron pos')

def getWords(lemma):
    cur = conn.execute("select * from word where lemma=?", (lemma,))
    return [Word(*row) for row in cur]

 
Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')

def getSenses(word):
    cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
    return [Sense(*row) for row in cur]

Synset = namedtuple('Synset', 'synset pos name src')

def getSynset(synset):
    cur = conn.execute("select * from synset where synset=?", (synset,))
    return Synset(*cur.fetchone())

def getWordsFromSynset(synset, lang):
    cur = conn.execute("select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;", (synset,lang))
    return [Word(*row) for row in cur]

def getWordsFromSenses(sense, lang="jpn"):
    synonym = {}
    for s in sense:
        lemmas = []
        syns = getWordsFromSynset(s.synset, lang)
        defer=getDefFromSynset(s.synset)
        lemmas.append(defer)
        for sy in syns:
            lemmas.append(sy.lemma)
            synonym[getSynset(s.synset).name] = lemmas
    return synonym

def getDefFromSynset(synset,lang="jpn"):
    cur = conn.execute("select def from synset_def where (synset=? and lang=?)",(synset,lang))
    defList=[]
    for row in cur:
        defList.append(row[0])
    return defList[0]
    # return [Word(*row) for row in cur]


def getSynonym (word):
    synonym = {}
    words = getWords(word)
    if words:
        for w in words:
            sense = getSenses(w)
            s = getWordsFromSenses(sense)
            synonym = dict(list(synonym.items()) + list(s.items()))
    return synonym


# if __name__ == '__main__':
#     if len(sys.argv) >= 2:
#         synonym = getSynonym(sys.argv[1])
#         pprint(synonym)
#         i=0
#         for w in synonym:
#             print(synonym[w][0])
#     else:
#         print("You need at least 1 argument as a word like below.\nExample:\n  $ python3 wordnet_jp 楽しい")