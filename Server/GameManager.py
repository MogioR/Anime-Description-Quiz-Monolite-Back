from Server.models import *

minHintMaskSize = 1
class GameManager:
    async def sendHits(self, websocket, data):
        if (len(data["data"]) >= minHintMaskSize):
            req = "{\"type\": \"game\", \"action\": \"newHints\", \"hints\": ["
            hints = self.getAnimeBySubName(data["data"])
            i = 0
            for h in hints:
                req += "\"" + str(hints[i].f_name) + "\""
                i += 1
                if (i < len(hints)):
                    req += ','
            req += "]}"
            await websocket.send(req)
        else:
            await websocket.send("")

    def getAnimeBySubName(self, subname):
        return FilmNameModel.select().where(FilmNameModel.f_name.contains(subname))


