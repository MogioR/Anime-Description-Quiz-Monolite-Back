import json
from Lobby import Lobby
from Package import Package
from serverUtilites import *


class LobbyManager:
    def __init__(self):
        self.lobbyList = []
        self.counter = 0

    def create(self, websocket, playerManager, lobby_list_sockets, messageQueue):
        self.lobbyList.append(Lobby(playerManager.loginPlayers.get(websocket).nickname, websocket, 8, self.counter))
        self.connectToLobby(websocket, self.counter, playerManager, lobby_list_sockets, messageQueue)
        self.counter = self.counter+1

    def connectToLobby(self, websocket, id, playerManager, lobby_list_sockets, messageQueue):
        index = self.getLobbyIndexById(id)

        if index != -1 and self.lobbyList[index].size > len(self.lobbyList[index].players):
            self.lobbyList[index].connect(playerManager.loginPlayers.get(websocket), websocket, messageQueue)

            playerManager.notifyByState("lobbyList", self.getLobbyListMessage(), messageQueue)
            notifySockets(lobby_list_sockets, self.getLobbyListMessage(), messageQueue)

    def disconnect(self, index, websocket, lobby_list_sockets, messageQueue):
        self.lobbyList[index].disconnect(websocket, messageQueue)
        message = json.dumps({'action': 'lobby', 'type': 'setPlayerList', 'players': self.lobbyList[index].players})
        notifySockets(self.lobbyList[index].sockets, message, messageQueue)
        len_ = len(self.lobbyList)
        self.lobbyList = [lobby for lobby in self.lobbyList if len(lobby.players) > 0]

        if len_ != len(self.lobbyList):
            notifySockets(lobby_list_sockets, self.getLobbyListMessage(), messageQueue)

    def gameStart(self, lobbyIndex, messageQueue):
        self.lobbyList[lobbyIndex].start()
        notifySockets(self.lobbyList[lobbyIndex].sockets, json.dumps({'action': 'lobby', 'type': 'startGame'}),
                      messageQueue)

    def getLobbyListMessage(self):
        buf_message = []
        for lobby in self.lobbyList:
            buf_message.append(json.dumps({'host': lobby.host, 'size': str(lobby.size), 'occupancy': len(lobby.players), 'id': lobby.id}))
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