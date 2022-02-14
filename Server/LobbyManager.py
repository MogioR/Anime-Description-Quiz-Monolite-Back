import json
from Lobby import Lobby
from Package import Package
from serverUtilites import *

class LobbyManager:
    def __init__(self):
        self.lobbyList = []
        self.counter = 0

    def create(self, websocket, playerManager, messageQueue):
        self.lobbyList.append(Lobby(playerManager.loginPlayers.get(websocket).nickname, websocket, 8, self.counter))
        self.connectToLobby(websocket, self.counter, playerManager, messageQueue)
        self.counter = self.counter+1

    def connectToLobby(self, websocket, id, playerManager, messageQueue):
        index = self.getLobbyIndexById(id)

        if index != -1 and self.lobbyList[index].size > self.lobbyList[index].occupancy:
            self.lobbyList[index].connect(playerManager.loginPlayers.get(websocket).nickname, websocket)
            playerManager.loginPlayers[websocket].state = "inLobby"
            messageQueue.append(Package(websocket, json.dumps({'action': 'lobby', 'type': 'enter'})))
            message = json.dumps({'action': 'lobby', 'type': 'setPlayerList', 'players': self.lobbyList[index].players})
            notifySockets(self.lobbyList[index].sockets, message, messageQueue)
            playerManager.notifyByState("lobbyList", self.getLobbyListMessage(), messageQueue)

    def disconnect(self, socket, nickname, messageQueue):
        for lobby in self.lobbyList:
            lobby.disconnect(socket, nickname, messageQueue)

    def gameStart(self, lobbyId, messageQueue):
        self.lobbyList[lobbyId].start()
        notifySockets(self.lobbyList[lobbyId].sockets, json.dumps({'action': 'lobby', 'type': 'startGame'}), messageQueue)

    def getLobbyListMessage(self):
        buf_message = []
        for lobby in self.lobbyList:
            buf_message.append(json.dumps({'host': lobby.host, 'size': str(lobby.size), 'occupancy': lobby.occupancy, 'id': lobby.id}))
        message = json.dumps({'action': 'lobbyList', 'type': 'setLobbyList', 'lobbies': buf_message})
        message = message.replace("\\", "")
        message = message.replace("[\"", "[")
        message = message.replace("\"]", "]")
        message = message.replace('}", "{', "},{")
        return message

    def getLobbyIndexById(self, id):
        i = 0
        for lobby in self.lobbyList:
            if lobby.id == id:
                return i
            i = i + 1
        return -1

    async def update(self, messageQueue):
        for lobby in self.lobbyList:
            await lobby.update(messageQueue)