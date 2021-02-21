from Server.Question import Qestion
from Server.Lobby import Lobby
from Server.Package import Package

class LobbyManager:
    def __init__(self):
        self.lobbyList = []

    def create(self, websocket, playerManager, messageQueues):
        self.lobbyList.append(Lobby(playerManager.onlinePlayers.get(websocket).nickname, websocket, 8))
        req = "{\"type\": \"lobby\", \"action\": \"enter\"}"
        messageQueues.append(Package(websocket, req))
        self.getPlayerList(websocket, self.lobbyList[-1], messageQueues)

    async def update(self):
        for lobby in self.lobbyList:
            await lobby.update()

    def getPlayerList(self, websocket, lobby, messageQueues):
        req = "{\"type\": \"lobby\", \"action\": \"getPlayerList\", \"players\": ["
        i = 0
        for player in lobby.players:
            req += "\"" + player + "\""
            i += 1
            if (i < len(lobby.players)):
                req += ','
        req += "]}"
        messageQueues.append(Package(websocket, req))

    def connectLobby(self, websocket, id, playerManager, messageQueues):
        self.lobbyList[id].connect(playerManager.onlinePlayers.get(websocket).nickname, websocket)
        req = "{\"type\": \"lobby\", \"action\": \"enter\"}"
        messageQueues.append(Package(websocket, req))
        self.notifyNewPlayerList(self.lobbyList[id], messageQueues)

    def notifyNewPlayerList(self, lobby, messageQueues):
        for socket in lobby.sockets:
            self.getPlayerList(socket, lobby, messageQueues)

    def notifyPlayers(self, lobby, message, messageQueues):
        for socket in lobby.sockets:
            messageQueues.append(Package(socket, message))

    def notifyGameStart(self, lobby, messageQueues):
        self.notifyPlayers(lobby, "{\"type\": \"lobby\", \"action\": \"startGame\"}", messageQueues)

    def gameStart(self, lobbyId, messageQueues):
        self.lobbyList[lobbyId].start()
        self.notifyGameStart(self.lobbyList[lobbyId], messageQueues)

    def getLobbyList(self, websocket, messageQueues):
        req = "{\"type\": \"lobbyList\", \"lobbyes\": ["
        i = 0
        for lobby in self.lobbyList:
            req += "{\"host\": \"" + lobby.host + "\",\"size\": " + str(lobby.size) + ",\"occupancy\":" + str(
                lobby.occupancy) + ",\"id\":" + str(i) + " } "
            i += 1
            if (i < len(self.lobbyList)):
                req += ','
        req += "]}"
        messageQueues.append(Package(websocket, req))
