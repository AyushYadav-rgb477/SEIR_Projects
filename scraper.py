import time
import argparse
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
parser = argparse.ArgumentParser()
parser.add_argument("urls", nargs="+")
args = parser.parse_args()
if len(args.urls) == 1:
    url = args.urls[0]
    session = requests.Session()
    session.headers.update({"User-Agent": UserAgent().random})
    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("Error:", e)
        exit()
    time.sleep(2)
    soup = BeautifulSoup(r.text, "html.parser")
    print("1. PAGE TITLE")
    print(soup.title.text.strip() if soup.title else "THERE IS NO TITLE")
    print("\n2.PAGE BODY TEXT")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n")
    for line in text.splitlines():
        line = line.strip()
        if line:
            print(line)
    print("\n3.LINKS FOUND")
    for mylink in soup.find_all("a"):
        print(mylink)
elif len(args.urls) == 2:
    url1 = args.urls[0]
    url2 = args.urls[1]
    def get_text(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        tags = soup(["script", "style", "noscript"])
        for t in tags:
            t.decompose()
        return soup.get_text(" ")
    def build_frequency(text):
        frq = {}
        word = ""
        text = text.lower()

        for ch in text:
            if ch.isalnum():
                word += ch
            else:
                if word != "":
                    if word in frq:
                        frq[word] += 1
                    else:
                        frq[word] = 1
                    word = ""
        if word != "":
            if word in frq:
                frq[word] += 1
            else:
                frq[word] = 1
        return frq
    def hash64(word):
        p = 53
        m = 2**64
        h = 0
        power = 1
        for c in word:
            h = (h + ord(c) * power) % m
            power = (power * p) % m
        return h
    def simhash(freq):
        v = [0] * 64
        for word in freq:
            cnt = freq[word]
            h = hash64(word)
            for i in range(64):
                bit = (h >> i) & 1
                if bit == 1:
                    v[i] += cnt
                else:
                    v[i] -= cnt
        fingerprint = 0
        for i in range(64):
            if v[i] > 0:
                fingerprint |= (1 << i)
        return fingerprint
    def common_bits(h1, h2):
        x = h1 ^ h2
        diff = 0
        while x:
            diff += x & 1
            x >>= 1
        return 64 - diff
    t1 = get_text(url1)
    t2 = get_text(url2)
    freq1 = build_frequency(t1)
    freq2 = build_frequency(t2)
    sm1 = simhash(freq1)
    sm2 = simhash(freq2)
    print("The Common bits are:", common_bits(sm1, sm2), "/ 64")
else:
    print("Error: Please provide either 1 URL or 2 URLs only.")
