from Server.models import *
from bs4 import BeautifulSoup
import requests
import re
import json

class Qestion:
    def __init__(self):
        self.answer = -1
        self.discription = ""

    async def getNewQestion(self):
        self.answer = self.getFilm()
        f_url = FilmModel.select().where(FilmModel.id == int(self.answer)).get().f_url
        self.answer = FilmNameModel.select().where(FilmNameModel.film_id == int(self.answer)).get().f_name
        r = requests.get(f_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # TODO: Make this more smart
        self.discription = str(soup.find("p", {"itemprop": "description"}))
        self.discription = self.discription.replace("<p itemprop=\"description\">", "")
        self.discription = self.discription.replace("[Written by MAL Rewrite]</p>", "")
        self.discription = self.discription.replace("<i/>", " ")
        self.discription = self.discription.replace("<i>", " ")
        self.discription = self.discription.replace("</i>", " ")
        self.discription = self.discription.replace("<br/>", " ")
        self.discription = self.discription.replace("\"", " \\\"")
        self.discription = re.sub("^\s+|\n|\r|\s+$", ' ', self.discription)

    def getQestionMessage(self):
        return json.dumps({'type': "game", 'action':"newAnswer", 'discription': self.discription})

    def getAnswerMessage(self):
        return json.dumps({'type': "game", 'action': "trueAnswer", 'trueAnswer': self.answer})

    def getFilm(self):
        f = FilmModel.select().order_by(fn.Random()).get()
        #ret = FilmNameModel.select().where(FilmNameModel.film_id == int(f.id)).get()
        return f.id