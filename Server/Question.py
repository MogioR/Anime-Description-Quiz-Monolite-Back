from models import *
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
        print(self.answer)
        self.discription = TitlesDescriptionsModel.select().where(TitlesDescriptionsModel.titles_descriptions_title_id == int(self.answer)).get().titles_descriptions_descriptions_text

    def getQestionMessage(self):
        return json.dumps({'action': "game", 'type': "newQuestion", 'questionType': 'text',
                           'text': self.discription})

    def getAnswerMessage(self):
        return json.dumps({'action': "game", 'type': "trueAnswer", 'trueAnswer': TitlesNamesModel.select().where(TitlesNamesModel.titles_names_title_id == self.answer).get().titles_names_name})

    def getFilm(self):
        f = TitlesModel.select().where(TitlesModel.titles_has_description == True).order_by(fn.Random()).get()
        return f.titles_id
