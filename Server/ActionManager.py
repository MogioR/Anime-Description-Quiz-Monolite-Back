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
        if websocket in self.playerManager.loginPlayers.keys():
            if data["action"] == "create":
                if self.playerManager.loginPlayers[websocket].state['screen'] == 'lobby_list':
                    self.lobbyManager.create(websocket, self.playerManager,
                                             self.get_sockets_by_state({'screen': 'lobby_list', 'screen_id': -1}),
                                             messageQueue)
                else:
                    print('Error state')
            elif data["action"] == "connect":
                if self.playerManager.loginPlayers[websocket].state['screen'] == 'lobby_list':
                    self.lobbyManager.connectToLobby(websocket, data["id"], self.playerManager,
                                                     self.get_sockets_by_state({'screen': 'lobby_list', 'screen_id': -1}),
                                                     messageQueue)
                else:
                    print('Error state')
            elif data["action"] == "start":
                if self.playerManager.loginPlayers[websocket].state['screen'] == 'in_lobby':
                    index = self.lobbyManager.getLobbyIndexById(
                        self.playerManager.loginPlayers[websocket].state['screen_id'])
                    if index != -1 and self.lobbyManager.lobbyList[index].host_socket == websocket:
                        self.lobbyManager.gameStart(index, messageQueue)
                    else:
                        print('Error state')
                else:
                    print('Error state')
        else:
            print('Error socket no authorised')

    def gameAction(self, websocket, data, messageQueue):
        if data["action"] == "reqestHints":
            self.gameManager.sendHits(websocket, data, messageQueue)
        elif data["action"] == "newAnswer":
            if self.playerManager.loginPlayers[websocket].state['screen'] == 'in_lobby':
                self.lobbyManager.lobbyList[self.lobbyManager.getLobbyIndexById(
                    self.playerManager.loginPlayers[websocket].state['screen_id'])].setAnswer(websocket, data['data'])

    def disconnect(self, websocket, messageQueue):
        if websocket in self.playerManager.loginPlayers.keys():
            if (self.playerManager.loginPlayers[websocket].state['screen'] == 'lobby' or
                    self.playerManager.loginPlayers[websocket].state['screen'] == 'game'):

                index = self.lobbyManager.getLobbyIndexById(
                    self.playerManager.loginPlayers[websocket].state['screen_id'])
                if index != -1:
                    self.lobbyManager.disconnect(index, websocket,
                                                 self.get_sockets_by_state({'screen': 'lobby_list', 'screen_id': -1}),
                                                 messageQueue)

            del self.playerManager.loginPlayers[websocket]

    def get_sockets_by_state(self, state):
        result = []
        for socket in list(self.playerManager.loginPlayers.keys()):
            if self.playerManager.loginPlayers[socket].state == state:
                result.append(socket)
        return result

    async def checkMessage(self, websocket, message, messageQueue):
        data = json.loads(message)
        if data["type"] == "login":
            await self.login(websocket, data, messageQueue)
        elif data["type"] == "lobby":
            self.lobbyAction(websocket, data, messageQueue)
        elif data["type"] == "game":
            self.gameAction(websocket, data, messageQueue)
