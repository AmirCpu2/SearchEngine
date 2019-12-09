from requests_html import HTMLSession
from lxml import html
import pandas as pd
import unicodedata
from hazm import *
import bleach
import csv
import re


# values Init
_limitLenghtShow   =  2
_limitLenghtShow **=  2
_words_print       = []
checkList          = []
Search             = []
db                 = []
dfTokenDoc         = ''
dfToken            = ''
dfIndex            = ''
Command            = ''
Doc                = ''
State              =  0

def CleanData (_command):

    # Command to String
    Token = str(_command).replace('\'','').replace('\"','')

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
    return clean


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

    return Token

def LoadDatabase():
    # this.value
    global dfToken,dfIndex,dfTokenDoc
    
    # LoadDatabase
        # Token[Id,Token]
    dfToken = pd.read_csv("PandaDBToken.csv")
    
        # TokenIndex[TokenId,Index]
    dfIndex = pd.read_csv("PandaDBIndex.csv")

        # TokenDoc[Id,Token]
    dfTokenDoc = pd.read_csv("PandaDBTokenDoc.csv")


def ShowSentence(_wordsIndex,_lenght):
   
    for _wordId in _wordsIndex:
        a = ''
        for i in range(_lenght+_limitLenghtShow):
            wTemp = list(dfTokenDoc['Token'].where(dfTokenDoc['Id'] == int(_wordId+i-_limitLenghtShow//2)).dropna().tolist()) 
            try:
                a += wTemp[0] + " "
            except:
                a += ""
        print(str(a))

#--------------------- Main ---------------------

# LoadDataBase
LoadDatabase()

# Command Process
while Command != 'exit()':
    # Value Local
    Word = []
    Search = []
    _words_print = []

    # Impot
    Command = input('Please enter Command(exit() to end the program)>>>  ').strip()

    # Exit Check
    if Command == 'exit()': exit()

    # TextCheck
    elif 'or' in Command.lower() :
        # Text To lower For Split
        Text = Command.lower()
        State = False

        # [One Word,Tow Word]
        Word = Text.split('or')

    elif 'and' in Command.lower() : 
        # Text To lower For Split
        Text = Command.lower()
        State = True
        
        # [One Word,Tow Word]
        Word = Text.split('and')
    else:
        # Text To lower For Split
        Word = [Command.lower()]

    # Pars Word
    for w in Word: Search.append( TokenInit( CleanData(w) ) )

    # :) does it exist !!?
    # Select by TokenId of Token Table
    for sl in Search:
        tmp = []
        (tmp.append( dfToken['Id'].where(dfToken['Token']==s).dropna().tolist() ) for s in sl)
        checkList.append(tmp)
        
    # If available Command => Check Index Number and creat Word
    for vl in checkList :
        tmp = []
        # If Not Null :/
        if vl and vl[0] != [] :
            # Select IndexId of Marge Table
            (tmp.append(set(dfIndex['Index'].where(dfIndex['TokenId']==int(v[0])).dropna().tolist())) for v in vl if v != [])
            
            #-----------Finde Words together--------------
            _lenght = len(tmp)
                # [x] =>x-index : for equals Words together index
            tmp = list((set(map(lambda x : x-i , tmp[i])) for i in range(len(tmp))))
                # {x} => filter equls index : for finde intersection 
            while(len(tmp) > 1): tmp = [ tmp[x]&tmp[x+1] for x in range(len(tmp)-1)] ,tmp.append(_lenght)
                # [x]finde => not False
            if len(tmp[0]) > 0 : _words_print.append(tmp)

    # Show Sentence
    if not _words_print or State :#if 'and' in Command || _words Finde length == 0  =>
        # Compare the length of the input command with the tokens found
        if len(_words_print) != len(Search) and not('\"' in Command or '\'' in Command) :
            print('No words found')
            continue

    for v in _words_print:# Finde And print, {_limitLenghtShow BeforeToken}+ {_word_Print} + {_limitLenghtShow AfterToken}
        ShowSentence(v[0],v[1])
