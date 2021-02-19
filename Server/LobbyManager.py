from Server.Question import Qestion
from Server.Lobby import Lobby

class LobbyManager:
    def __init__(self):
        self.lobbyList = []

    async def create(self, websocket, playerManager):
        self.lobbyList.append(Lobby(playerManager.loginPlayers.get(websocket).nickname, websocket, 8))
        req = "{\"type\": \"lobby\", \"action\": \"enter\"}"
        await websocket.send(req)
        await self.getPlayerList(websocket, self.lobbyList[-1], playerManager)

    async def update(self):
        for lobby in self.lobbyList:
            await lobby.update()

    async def getPlayerList(self, websocket, lobby, playerManager):
        print("Player " + playerManager.loginPlayers.get(websocket).nickname + " get lobby players!")
        req = "{\"type\": \"lobby\", \"action\": \"getPlayerList\", \"players\": ["
        i = 0
        for player in lobby.players:
            req += "\"" + player + "\""
            i += 1
            if (i < len(lobby.players)):
                req += ','
        req += "]}"
        await websocket.send(req)

    async def connectLobby(self, websocket, id, playerManager):
        self.lobbyList[id].connect(playerManager.loginPlayers.get(websocket).nickname, websocket)
        req = "{\"type\": \"lobby\", \"action\": \"enter\"}"
        await websocket.send(req)
        await self.notifyNewPlayerList(self.lobbyList[id])

    async def notifyNewPlayerList(self, lobby):
        for socket in lobby.sockets:
            await self.getPlayerList(socket, lobby)

    async def getLobbyList(self, websocket, playerManager):
        print("Player " + playerManager.loginPlayers.get(websocket).nickname + " get lobbyes!")
        req = "{\"type\": \"lobbyList\", \"lobbyes\": ["
        i = 0
        for lobby in self.lobbyList:
            req += "{\"host\": \"" + lobby.host + "\",\"size\": " + str(lobby.size) + ",\"occupancy\":" + str(
                lobby.occupancy) + ",\"id\":" + str(i) + " } "
            i += 1
            if (i < len(self.lobbyList)):
                req += ','
        req += "]}"
        await websocket.send(req)
