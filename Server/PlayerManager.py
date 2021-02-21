from Server.models import *
from Server.Player import Player
from Server.Package import Package

class PlayerManager:
    def __init__(self):
        self.onlinePlayers = {}

    async def login(self, websocket, nickname, password, lobbyManager, messageQueues):
        if (self.loginByBD(nickname, password) == 1):
            req = "{\"type\": \"login\", \"login\": 1}"
            self.onlinePlayers[websocket] = Player(websocket, nickname)
            lobbyManager.getLobbyList(websocket, messageQueues)
        else:
            req = ""
        messageQueues.append(Package(websocket, req))

    def loginByBD(self, login, password):
        try:
            p = PlayerModel.select().where(PlayerModel.p_name == login and PlayerModel.p_pass_hash == password).get()
            return 1
        except Exception as error:
            return 0