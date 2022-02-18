from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request
import json
import io
import time
import re
import ssl

def getShikimoriParams(url):
    mas = url.split("/")
    id_str = mas[-1].split("-")[0]
    return mas[-2], id_str


def getAnimeData(_names, type, id):
    url_anime = "https://shikimori.one/"
    req_current = Request(url=url_anime + type + '/' + str(id), headers=headers)
    html_current = urlopen(req_current).read()
    soup_current = BeautifulSoup(html_current, 'html.parser')

    left_info_box = soup_current.find("div", {"class": "c-info-left"})
    left_info_box = left_info_box.find("div", {"class": "block"})

    info_lines = left_info_box.find_all("div", {"class": "line-container"})

    i = 0
    subtype = info_lines[i].find("div", {"class": "value"}).text
    i += 1

    episodes_count = "1"
    if info_lines[i].find("div", {"class": "key"}).text == "Эпизоды:":
        episodes_count = info_lines[i].find("div", {"class": "value"}).text
        i += 1

    episodes_size = info_lines[i].find("div", {"class": "value"}).text
    i += 1
    date_relise = info_lines[i].find("div", {"class": "value"}).text
    i += 1

    geners_box = info_lines[i].find("div", {"class": "value"})
    i += 1
    geners = geners_box.find_all("span", {"class": "b-tag"})

    _geners = []
    for g in geners:
        buf = g.attrs["data-href"]
        num = int(re.sub("[^0-9]", ' ', buf))
        _geners.append(num)

    PG = info_lines[i].find("div", {"class": "value"}).text
    raiting = soup_current.find("div", {"class": "c-info-right"}).find("meta", {"itemprop": "ratingValue"}).attrs["content"]


    descr_box = soup_current.find("div", {"itemprop": "description"})
    descr = "none"

    if descr_box is not None:
        descr = str(descr_box)
        descr = re.sub('<br.*?>', "\n", descr)
        descr = re.sub('<.*?>', "<sp>", descr)


    obj = json.dumps({'names': _names, 'type': type, 'id': id, 'subtype': subtype, 'episodes-count': episodes_count, 'episodes-size': episodes_size, 'relise-date': date_relise, 'geners': _geners, 'PG': PG, 'raiting': raiting,'description': str(descr)}, ensure_ascii=False)
    return obj

base_output_file = io.open("output_new.txt", "a", encoding='utf8')
err_output_file = io.open("trash_base.txt", "a", encoding='utf8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

# print(getAnimeData(["w"], "animes", "y28851"))

for i in range(456, 739):
    reg_url = "https://shikimori.one/animes/page/"+str(i)
    req = Request(url=reg_url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    anime_box = soup.find("div", {"class": "cc-entries"})
    animes = anime_box.find_all("article")
    j=0
    for anime in animes:
        j += 1
        print(str(i) + " - " + str(j))
        if j % 2 == 0:
            time.sleep(10)

        out_str = ""
        href = anime.find("a")
        _names = []
        text = anime.find("span", {"class": "name-en"})
        if text is not None:
            _names.append(str(text.text))

        text = anime.find("span", {"class": "name-ru"})
        if text is not None:
            _names.append(str(text.text))

        text = anime.find("span", {"class": "name-jp"})
        if text is not None:
            _names.append(str(text.text))

        if len(_names) == 0:
            text = anime.find("span", {"itemprop": "name"})
            if text is not None:
                _names.append(str(text.text))

        if len(_names) != 0:
            type, id = getShikimoriParams(href.attrs["href"])
            base_output_file.write(getAnimeData(_names, type, id) + "\n")

err_output_file.close()
base_output_file.close()
