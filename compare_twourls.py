import requests
import argparse
import re
from collections import Counter
from bs4 import BeautifulSoup
def get_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(" ")
def word_freq(text):
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    return Counter(words)
def hash64(word):
    p = 53
    m = 2**64
    h = 0
    power = 1
    for c in word:
        h = (h + ord(c) * power) % m
        power = (power * p) % m
    return h
def simhash(counts):
    v = [0] * 64
    for word, cnt in counts.items():
        h = hash64(word)
        for i in range(64):
            if (h >> i) & 1:
                v[i] += cnt
            else:
                v[i] -= cnt
    fp = 0
    for i in range(64):
        if v[i] > 0:
            fp |= (1 << i)
    return fp
def common_bits(h1, h2):
    diff = bin(h1 ^ h2).count("1")
    return 64 - diff
parser = argparse.ArgumentParser()
parser.add_argument("url1")
parser.add_argument("url2")
args = parser.parse_args()
t1 = get_text(args.url1)
t2 = get_text(args.url2)
f1 = word_freq(t1)
f2 = word_freq(t2)
s1 = simhash(f1)
s2 = simhash(f2)
print("The Common bits are:", common_bits(s1, s2), "/ 64")
