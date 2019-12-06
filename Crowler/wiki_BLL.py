from requests_html import HTMLSession
from lxml import html
import pandas as pd
import unicodedata
from hazm import *
import bleach
import csv
import re


# values Init
TokenList = []
IndexList = []
Command = ''
Search = []
Doc = ''
db = []

def CleanData (_command):

    # Command to String
    Token = str(_command)

    # Text Cleaning
    clean = bleach.clean(Token).replace('[ویرایش]','')
    clean = re.sub(r'http\S+', '', clean)
    clean = re.sub(r'\\S+', '', clean)
    clean = clean.replace(u'\ufeff', '')
    clean = unicodedata.normalize("NFKD", clean)

    # Text Noramalizetion
    normalizer = Normalizer()
    clean = normalizer.normalize(clean)

    # Return => clean text
    return _command


def TokenInit (_Text):
    
    # Creat Token
    TokenList = sent_tokenize(_Text)
    finallyList = []

    # Creat Word
    for v in TokenList:finallyList.extend(word_tokenize(v))
    
    Token = []
    stemmer=Stemmer()
    # Creat Rest Token
    for v in finallyList:Token.append(stemmer.stem(v))

    return finallyList

def LoadDatabase():
    # this.Doc
    global Doc,TokenList,IndexList,db

    # LoadDocClear
    # DocFile = open("DocFile.txt", 'r',encoding='utf-8', newline='')
    # Doc = DocFile.read()
    # DocFile.close()

    # LoadDatabase
    db = pd.read_csv("PandaDB.csv")
    TokenList = db["Token"].tolist()
    IndexList = db["Index"].tolist()

#--------------------- Main ---------------------

# LoadDataBase
LoadDatabase()

# Command Process
while Command != 'exit()':
    # Value Local
    Word = []
    Search = []
    
    # Impot
    Command = input('Pls Enter Command(exit() For End App)>\t').strip()

    # Exit Check
    if Command == 'exit()': exit()

    # TextCheck
    elif 'or' in Command.lower() :
        # Text To lower For Split
        Text = Command.lower()
        
        # [One Word,Tow Word]
        Word = Text.Split('or')

    elif 'and' in Command.lower() : 
        # Text To lower For Split
        Text = Command.lower()
        
        # [One Word,Tow Word]
        Word = Text.Split('and')
    else:
        # Text To lower For Split
        Word = [Command.lower()]

    # Pars Word
    for w in Word: Search.append( TokenInit( CleanData(w) ) )

    # :) does it exist !!?
    checkList = []
    for s in Search:
        for st in s:
            checkList.append( db['Index'].where(db['Token']==st).dropna() )
    
    print(checkList)