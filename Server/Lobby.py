import asyncio
from Server.Question import Qestion

class Lobby:
    def __init__(self, host_name,  host_socket, size):
        self.host = host_name
        self.size = size
        self.occupancy = 1
        self.players = [host_name]
        self.sockets = [host_socket]
        self.timer = 0
        self.phase = 0
        self.question = Qestion()

    def connect(self, player, socket):
        self.players.append(player)
        self.occupancy += 1
        self.sockets.append(socket)

    def disconnect(self, player):
        self.players = [x for ind, x in enumerate(self.players) if x!=player]
        self.occupancy -= 1

    async def sendQuestion(self):
        for socket in self.sockets:
            await socket.send(self.question.getQestion())

    async def sendAnswer(self):
        for socket in self.sockets:
            await socket.send(self.question.getAnswer())

    def start(self):
        self.phase = 1
        self.timer = 0

    def stop(self):
        self.phase = 0
        self.timer = 0

    async def update(self):
        self.timer = self.timer - 1;
        if(self.timer <= 0):
            if(self.phase == 0):
                self.timer = 0
            elif (self.phase == 1):
                self.timer = 0
                self.question = Qestion()
                self.phase = self.phase + 1
            elif(self.phase == 2):
                self.timer = 5
                self.phase = self.phase + 1
                await self.sendQuestion()
            elif(self.phase == 3):
                self.timer = 5
                self.phase = self.phase + 1
                await self.sendAnswer()
            else:
                self.phase = 1