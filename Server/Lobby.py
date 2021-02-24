import asyncio
from Server.Question import Qestion
from Server.serverUtilites import *

class Lobby:
    def __init__(self, host_name,  host_socket, size, id):
        self.host = host_name
        self.size = size
        self.occupancy = 1
        self.players = []
        self.sockets = []
        self.timer = 0
        self.phase = 0
        self.question = Qestion()
        self.id = id

    def connect(self, player, socket):
        self.players.append(player)
        self.occupancy += 1
        self.sockets.append(socket)

    def start(self):
        self.phase = 1
        self.timer = 0

    def stop(self):
        self.phase = 0
        self.timer = 0

    async def update(self, messageQueue):
        self.timer = self.timer - 1
        if self.timer <= 0:
            if self.phase == 0:
                self.timer = 0
            elif self.phase == 1:
                self.timer = 0
                await self.question.getNewQestion()
                self.phase = self.phase + 1
            elif self.phase == 2:
                self.timer = 5
                self.phase = self.phase + 1
                notifySockets(self.sockets, self.question.getQestionMessage(), messageQueue)
            elif self.phase == 3:
                self.timer = 5
                self.phase = self.phase + 1
                notifySockets(self.sockets, self.question.getAnswerMessage(), messageQueue)
            else:
                self.phase = 1