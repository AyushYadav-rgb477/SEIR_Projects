import time
import argparse
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
parser = argparse.ArgumentParser()
parser.add_argument("url")
url = parser.parse_args().url
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
