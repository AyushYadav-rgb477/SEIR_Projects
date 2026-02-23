import requests
import argparse
from bs4 import BeautifulSoup
def get_text(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    tags=soup(["script","style","noscript"])
    for t in tags:
        t.decompose()
    return soup.get_text(" ")
def build_frequency(text):
    frq={}
    word=""
    text=text.lower()
    for ch in text:
        if ch.isalnum():
            word+=ch
        else:
            if word!="":
                if word in frq:
                    frq[word]+=1
                else:
                    frq[word]=1
                word=""
    if word!="":
        if word in frq:
            frq[word]+=1
        else:
            frq[word]=1
    return frq
def hash64(word):
    p=53
    m=2**64
    h=0
    power=1
    for c in word:
        h=(h+ord(c)*power)%m
        power=(power*p)%m
    return h
def simhash(freq):
    v=[0]*64
    for word in freq:
        cnt=freq[word]
        h=hash64(word)
        for i in range(64):
            bit=(h>>i)&1
            if bit==1:
                v[i]+=cnt
            else:
                v[i]-=cnt
    fingerprint=0
    for i in range(64):
        if v[i]>0:
            fingerprint|=(1<<i)
    return fingerprint
def common_bits(h1,h2):
    x=h1^h2
    diff=0
    while x:
        diff+=x&1
        x>>=1
    return 64-diff
parser=argparse.ArgumentParser()
parser.add_argument("url1")
parser.add_argument("url2")
args=parser.parse_args()
t1=get_text(args.url1)
t2=get_text(args.url2)
freq1=build_frequency(t1)
freq2=build_frequency(t2)
sm1=simhash(freq1)
sm2=simhash(freq2)
print("The Common bits are:",common_bits(sm1,sm2),"/ 64")
