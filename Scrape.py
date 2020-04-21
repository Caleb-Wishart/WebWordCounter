import requests
import sys
from bs4 import BeautifulSoup
from re import sub as sub
from string import punctuation as punctuation
from string import digits as digits

charlist = punctuation.replace('\'','') + str(digits) + '\\n'
### Var ###

URL = 'https://en.wikipedia.org/wiki/Geology'
URL2 = 'https://en.wikipedia.org/wiki/Australia'
### Function ###

def queryWebPage(URL):
    res = requests.get(URL)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        return soup
    else:
        print >> sys.stderr, "Query Failed"
        return False

def siftContent(soup):
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
    	'[document]','noscript','header','html','meta','head','input',
    	'script','style'
    ]
    for content in text:
    	if content.parent.name not in blacklist:
            try:
                output += '{} '.format(sub('['+charlist+']', '', content))
            except:
                continue
    output = output.lower().split(' ') # split to array
    output = filter(None, output) # remove '' elements
    return output

def countContent(content):
    # creates dictionary with number of words
    dict = {}
    for text in content:
        if text in dict:
            dict[text] += 1
        else:
            dict[text] = 1
    return dict

def mostCommonWord(content):
    a = []
    b = []
    for x,y in content.items():
        a.append(x)
        b.append(y)
    if len(a) > 20:
        num = 10
    else: num = len(a)
    for j in range(num):
        for i in range(len(b)):
            if b[i] == max(b):
                print a[i]+' : '+str(b[i])
                num = i
        a.remove(a[num])
        b.remove(b[num])

def removeUncommonWords(content,num=100):
    a = []
    for text in content:
        if content[text] < num:
            a.append(text)
    for i in range(len(a)):
        content.pop(a[i])
    return content
### MAIN ###

mostCommonWord(removeUncommonWords(countContent(siftContent(queryWebPage(URL)))))
