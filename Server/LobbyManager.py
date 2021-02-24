import json
from Server.Lobby import Lobby
from Server.Package import Package
from Server.serverUtilites import *

class LobbyManager:
    def __init__(self):
        self.lobbyList = []

    def create(self, websocket, playerManager, messageQueues):
        self.lobbyList.append(Lobby(playerManager.onlinePlayers.get(websocket).nickname, websocket, 8))
        req = json.dumps({'type': 'lobby', 'action': 'enter'})
        messageQueues.append(Package(websocket, req))
        self.getPlayerList(websocket, self.lobbyList[-1], messageQueues)
        #notifySockets(playerManager.onlinePlayers.keys(), )

    async def update(self):
        for lobby in self.lobbyList:
            await lobby.update()

    def getPlayerList(self, websocket, lobby, messageQueues):
        req = json.dumps({'type': 'lobby', 'action': 'getPlayerList', 'players' : lobby.players})
        print(req)
        messageQueues.append(Package(websocket, req))

    def connectLobby(self, websocket, id, playerManager, messageQueues):
        self.lobbyList[id].connect(playerManager.onlinePlayers.get(websocket).nickname, websocket)
        req = json.dumps({'type': 'lobby', 'action': 'enter'})
        messageQueues.append(Package(websocket, req))
        self.notifyNewPlayerList(self.lobbyList[id], messageQueues)

    def notifyNewPlayerList(self, lobby, messageQueues):
        for socket in lobby.sockets:
            self.getPlayerList(socket, lobby, messageQueues)

    def notifyPlayers(self, lobby, message, messageQueues):
        for socket in lobby.sockets:
            messageQueues.append(Package(socket, message))

    def notifyGameStart(self, lobby, messageQueues):
        req = json.dumps({'type': 'lobby', 'action': 'startGame'})
        self.notifyPlayers(lobby, req, messageQueues)

    def gameStart(self, lobbyId, messageQueues):
        self.lobbyList[lobbyId].start()
        self.notifyGameStart(self.lobbyList[lobbyId], messageQueues)

    def getLobbyListReqest(self):
        req = "{\"type\": \"lobbyList\", \"lobbyes\": ["
        i = 0
        for lobby in self.lobbyList:
            req += "{\"host\": \"" + lobby.host + "\",\"size\": " + str(lobby.size) + ",\"occupancy\":" + str(
                lobby.occupancy) + ",\"id\":" + str(i) + " } "
            i += 1
            if (i < len(self.lobbyList)):
                req += ','
        req += "]}"
        return req

    def disconnect(self, socket, nickname, messageQueue):
        for lobby in self.lobbyList:
            lobby.disconnect(socket, nickname, messageQueue)
