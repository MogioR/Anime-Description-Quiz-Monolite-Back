import json

from PlayerManager import PlayerManager
from LobbyManager import LobbyManager
from GameManager import GameManager

class ActionManager:
    def __init__(self):
        self.lobbyManager = LobbyManager()
        self.playerManager = PlayerManager()
        self.gameManager = GameManager()

    # async def registrationInDB(self, login, pas, messageQueue):
    #     try:
    #         p = PlayerModel(p_name=login, p_pas_hash=pas, is_relative=True)
    #         p.save()
    #     except Exception as error:
    #         print('A New Exception occured: ', str(error))

    async def login(self, websocket, data, messageQueue):
        await self.playerManager.login(websocket, data["nickname"], data["password"], self.lobbyManager, messageQueue)

    def lobbyAction(self, websocket, data, messageQueue):
        if data["action"] == "create":
            self.lobbyManager.create(websocket, self.playerManager, messageQueue)

        elif data["action"] == "connect":
            self.lobbyManager.connectToLobby(websocket, data["id"], self.playerManager, messageQueue)
        elif data["action"] == "start":
            self.lobbyManager.gameStart(0, messageQueue)

    def gameAction(self, websocket, data, messageQueue):
        if data["action"] == "reqestHints":
            self.gameManager.sendHits(websocket, data, messageQueue)

    async def chackMessage(self, websocket, message, messageQueue):
        data = json.loads(message)
        if data["type"] == "login":
            await self.login(websocket, data, messageQueue)
        elif data["type"] == "lobby":
            self.lobbyAction(websocket, data, messageQueue)
        elif data["type"] == "game":
            self.gameAction(websocket, data, messageQueue)
