import json

from models import *
from Package import Package

MIN_MASK_SIZE = 4

class GameManager:
    def sendHits(self, websocket, data, messageQueue):
        if (len(data["data"]) >= MIN_MASK_SIZE):
            hints = self.getAnimeBySubName(data["data"])
            message_buf = []
            print(hints)
            for hint in hints:
                message_buf.append(hint.titles_names_name)
            messageQueue.append(Package(websocket, json.dumps({'type': "game", 'action': "newHints", 'hints': message_buf})))

    def getAnimeBySubName(self, subname):
        return TitlesNamesModel.select().where(TitlesNamesModel.titles_names_name.contains(subname))