import json

from models import *
from Player import Player
from Package import Package


class PlayerManager:
    def __init__(self):
        self.loginPlayers = {}

    async def login(self, websocket, nickname, password, lobbyManager, messageQueue):
        player = await self.loginByBD(nickname, password)
        if player is not None:
            self.loginPlayers[websocket] = Player(player)
            req = json.dumps({'action': 'login', 'type': 'login', 'login': True})
            messageQueue.append(Package(websocket, req))
            messageQueue.append(Package(websocket, lobbyManager.getLobbyListMessage()))
        else:
            req = json.dumps({'action': 'login', 'type': 'login', 'login': False})
            messageQueue.append(Package(websocket, req))

    async def loginByBD(self, login, password):
        try:
            player = PlayersModel.select().where((PlayersModel.players_login == login) & (PlayersModel.players_pass_hash == password)).get()
            return player
        except Exception as error:
            return None

    def notifyByState(self, state, message, messageQueue):
        for socket in self.loginPlayers.keys():
            if self.loginPlayers[socket].state == state:
                messageQueue.append(Package(socket, message))