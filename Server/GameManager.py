import json

from Server.models import *
from Server.Package import Package

MIN_MASK_SIZE = 1

class GameManager:
    async def sendHits(self, websocket, data, messageQueue):
        if (len(data["data"]) >= MIN_MASK_SIZE):
            hints = self.getAnimeBySubName(data["data"])

            message_buf = []
            for hint in hints:
                message_buf.append(hint.f_name)
            messageQueue.append(Package(websocket, json.dumps({'type': "game", 'action': "newHints", 'hints': message_buf})))

    def getAnimeBySubName(self, subname):
        return FilmNameModel.select().where(FilmNameModel.f_name.contains(subname))


