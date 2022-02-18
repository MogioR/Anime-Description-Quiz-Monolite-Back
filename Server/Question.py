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
        self.discription = TitlesDescriptionsModel.select().where(
            TitlesDescriptionsModel.titles_descriptions_title_id == int(
                self.answer)).get().titles_descriptions_descriptions_text

    def getQestionMessage(self):
        return json.dumps({'action': "game", 'type': "newQuestion", 'questionType': 'text',
                           'text': self.getUnspoilerDescription(self.discription)})

    def getAnswerMessage(self):
        return json.dumps({'action': "game", 'type': "trueAnswer", 'trueAnswer': TitlesNamesModel.select().where(
            TitlesNamesModel.titles_names_title_id == self.answer).get().titles_names_name,
                           'questionType': 'text', 'fullQuestion': self.discription.replace('<sp>', '')})

    def getFilm(self):
        f = TitlesModel.select().where((TitlesModel.titles_has_description == True) & (TitlesModel.titles_rating >= 7.5)).order_by(fn.Random()).get()
        print(f.titles_id)
        print(f.titles_rating)
        print(TitlesNamesModel.select().where(TitlesNamesModel.titles_names_title_id == f.titles_id).get().titles_names_name)
        return f.titles_id

    def check_answer(self, answer):
        try:
            title = TitlesNamesModel.select().where(fn.Lower(TitlesNamesModel.titles_names_name) == answer.lower()).get()
        except:
            title = None
        return title is not None and title.titles_names_title_id.titles_id == self.answer



    @staticmethod
    def getUnspoilerDescription(str):
        i = 0
        end = len(str) - 3
        ret = ""
        spoil = False

        while i < end:
            if str[i] == '<' and str[i + 1] == 's' and str[i + 2] == 'p' and str[i + 3] == '>':
                i += 4
                spoil = not spoil
                continue

            if not spoil:
                ret += str[i]
            else:
                ret += '*'

            i += 1

        return ret
