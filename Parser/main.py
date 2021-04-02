from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request
import json
import io
import time

def getShikimoriParams(url):
    mas = url.split("/")
    id_str = mas[-1].split("-")[0]
    return mas[-2], id_str

output_file = io.open("output.txt", "a", encoding='utf8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


for i in range(1, 735):
    print(str(i))
    if i % 50 == 0:
        time.sleep(30)

    reg_url = "https://shikimori.one/animes/page/"+str(i)
    req = Request(url=reg_url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    anime_box = soup.find("div", {"class": "cc-entries"})
    animes = anime_box.find_all("article")
    for anime in animes:
        out_str = ""
        href = anime.find("a")
        _names = []

        text = anime.find("span", {"class": "name-en"})
        if text is not None:
            _names.append(str(text.text))

        text = anime.find("span", {"class": "name-ru"})
        if text is not None:
            _names.append(str(text.text))

        if len(_names) == 0:
            text = anime.find("span", {"itemprop": "name"})
            if text is not None:
                _names.append(str(text.text))

        type, id = getShikimoriParams(href.attrs["href"])
        obj = json.dumps({'names': _names, 'type': type, 'id': id}, ensure_ascii=False)
        output_file.write(obj + "\n")

output_file.close()
