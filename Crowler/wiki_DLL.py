from requests_html import HTMLSession
from lxml import html
import pandas as pd
import unicodedata
from hazm import *
import bleach
import csv
import re

# Base Function
def SaveTable (DataTable):

    # Head
    fieldnames = ['Token', 'TokenIndex']
    
    # Creat Data Frame
    data_frameToken = pd.DataFrame({fieldnames[0]: DataTable[0]})
    data_frameIndex = pd.DataFrame({fieldnames[1]: DataTable[1]})

    # DataFrame To CSV
    data_frameToken.to_csv("PandaDBToken.csv", sep=",", encoding='utf-8')
    data_frameIndex.to_csv("PandaDBIndex.csv", sep=",", encoding='utf-8')

# Base Function
def SaveDoc (DataDoc):

    # Open File And set mode Write
    f = open("DocFile.txt", 'w',encoding='utf-8', newline='')
    f.write(DataDoc)
    f.close()

# values Init
page = 0
max_result = 1
Text = ''
Search = "دانشگاه_آزاد_اسلامی_واحد_کرج"
url = 'https://fa.wikipedia.org/wiki/{}'.format(Search)
finallyList = []

# objects Init
session = HTMLSession()

# Init Arrays
Token = []
TokenTemp = []

# Start APP
r = session.get(url)
body = r.html.find('#content',first=True)
Token = str(body.text)

# Text Cleaning
clean = bleach.clean(Token).replace('[ویرایش]','')
clean = re.sub(r'http\S+', '', clean)
clean = re.sub(r'\\S+', '', clean)
clean = clean.replace(u'\ufeff', '')
clean = unicodedata.normalize("NFKD", clean)

# Text Noramalizetion
normalizer = Normalizer()
clean = normalizer.normalize(clean)

# SaveDoc Test
SaveDoc(clean)

# Creat Token
ListToken = sent_tokenize(clean)

# Creat Word
for v in ListToken:finallyList.extend(word_tokenize(v))

Token = []
stemmer=Stemmer()
# Creat Rest Token
for v in finallyList:Token.append(stemmer.stem(v))

# Clear Token Copy
TokenTemp = Token

# Get unique values from a list
Token = list(set(Token))

# sort Token
Token.sort()

# Init Index List [ TokenIndex ]
TokenIndex = []
for T in Token: TokenIndex.append([j for j, x in enumerate(TokenTemp) if x == T])

# Marge TokenIndex by TokenNameID [ ID , TokenIndexIthem ]
TokenIndexMarge = []
for i in range(len(TokenIndex)): TokenIndexMarge.extend(list([i,j] for j in TokenIndex[i]))

# Save CSV DB
SaveTable([Token, TokenIndexMarge])