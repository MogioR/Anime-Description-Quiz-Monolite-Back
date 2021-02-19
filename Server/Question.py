from models import *
from bs4 import BeautifulSoup
import requests
import re

class Qestion:
    def __init__(self):
        self.answer = self.getFilm()
        f_url = FilmModel.select().where(FilmModel.id == int(self.answer)).get().f_url
        self.answer = FilmNameModel.select().where(FilmNameModel.film_id == int(self.answer)).get().f_name
        r = requests.get(f_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.discription = str(soup.find("p", {"itemprop": "description"}))
        self.discription = self.discription.replace("<p itemprop=\"description\">", "")
        self.discription = self.discription.replace("[Written by MAL Rewrite]</p>", "")
        self.discription = self.discription.replace("<i/>", " ")
        self.discription = self.discription.replace("<i>", " ")
        self.discription = self.discription.replace("</i>", " ")
        self.discription = self.discription.replace("<br/>", " ")
        self.discription = self.discription.replace("\"", " \\\"")
        self.discription = re.sub("^\s+|\n|\r|\s+$", ' ', self.discription)

    def getQestion(self):
        return "{\"type\": \"game\", \"action\": \"newAnswer\", \"discription\": \"" + self.discription + "\"}"

    def getAnswer(self):
        return "{\"type\": \"game\", \"action\": \"trueAnswer\", \"trueAnswer\": " + str(self.answer) + "}"

    def getFilm(self):
        f = FilmModel.select().order_by(fn.Random()).get()
        ret = FilmNameModel.select().where(FilmNameModel.film_id == int(f.id)).get()
        return f.id