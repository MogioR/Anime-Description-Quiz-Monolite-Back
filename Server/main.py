import asyncio
import websockets
<<<<<<< HEAD
import requests
import json
from Server.Lobby import Lobby
from Server.models import *
from Server.Player import Player
from bs4 import BeautifulSoup
import urllib3

loginPlayers = {}
lobbyList = []
games = []
Players = []

minHintMaskSize = 1

class Qestion:
    def __init__(self):
        self.answers = []
        self.answers.append(getFilm())
        self.answers.append(getFilm())
        while (self.answers[0] == self.answers[1]):
            self.answers[1] = getFilm()
        self.answers.append(getFilm())
        while (self.answers[0] == self.answers[2] or self.answers[1] == self.answers[2]):
            self.answers[2] = getFilm()
        self.answers.append(getFilm())
        while (self.answers[0] == self.answers[3] or self.answers[1] == self.answers[3] or self.answers[2] == self.answers[3]):
            self.answers[3] = getFilm()
        self.true = random.randint(0,3)

        f_url = FilmModel.select().where(FilmModel.id == int(self.answers[self.true])).get().f_url
        r = requests.get(f_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.discription = str(soup.find("p", {"itemprop": "description"}))
        self.discription = self.discription.replace("<p itemprop=\"description\">","")
        self.discription = self.discription.replace("[Written by MAL Rewrite]</p>", "")
        self.discription = self.discription.replace("<i/>", " ")
        self.discription = self.discription.replace("<i>", " ")
        self.discription = self.discription.replace("</i>", " ")
        self.discription = self.discription.replace("<br/>", " ")
        self.discription = self.discription.replace("\"", " \\\"")
        self.discription = re.sub("^\s+|\n|\r|\s+$", ' ', self.discription)

    def getQestion(self):
        f0 = FilmNameModel.select().where(FilmNameModel.film_id == int(self.answers[0])).get().f_name
        f1 = FilmNameModel.select().where(FilmNameModel.film_id == int(self.answers[1])).get().f_name
        f2 = FilmNameModel.select().where(FilmNameModel.film_id == int(self.answers[2])).get().f_name
        f3 = FilmNameModel.select().where(FilmNameModel.film_id == int(self.answers[3])).get().f_name

        print(self.discription)
        return "{\"type\": \"game\", \"action\": \"newAnswer\", \"discription\": \"" + self.discription + \
               "\", \"answers\": [\"" + str(f0) + "\", \"" + str(f1) + "\", \"" + str(f2) + "\", \"" + str(f3) + "\"]}"

    def getAnswer(self):
        return "{\"type\": \"game\", \"action\": \"trueAnswer\", \"trueAnswer\": " + str(self.true) + "}"

def getAnimeBySubName(SubName):
    return FilmNameModel.select().where(FilmNameModel.f_name.contains(SubName))

def registrationInDB(login,pas):
    try:
        p = PlayerModel(p_name = login, p_pas_hash = pas, is_relative=True)
        p.save()
    except Exception as error:
        print('A New Exception occured: ', str(error))


def loginByBD(login,pas):
    try:
        p = PlayerModel.select().where(PlayerModel.p_name == login and PlayerModel.p_pass_hash == pas).get()
        return 1
    except Exception as error:
        return 0

async def sendQuestion(lobby, qestion):
    for socket in lobby.sockets:
        await socket.send(qestion.getQestion())

async def sendAnswer(lobby, qestion):
    for socket in lobby.sockets:
        await socket.send(qestion.getAnswer())

async def game(lobby):
    game = Game.create(is_relative=True)
    q = Qestion()
    await sendQuestion(lobby, q)

    loop = asyncio.get_running_loop()
    end_time = loop.time() + 15.0
    round = 0
    i = 1
    while True:
        if (loop.time() + 1.0) >= end_time:
            if(i == 0):
                q = Qestion()
                await sendQuestion(lobby, q)
                i=1
            elif (i == 1):
                await sendAnswer(lobby, q)
                round+=1
                i=0
            if (round == 5):
                break
        await asyncio.sleep(15)

def getFilm():
    f = FilmModel.select().order_by(fn.Random()).get()
    ret = FilmNameModel.select().where(FilmNameModel.film_id == int(f.id)).get()
    return f.id

async def login(websocket, message):
    data = json.loads(message)
    print("Join " + data["nickname"] + '!')
    if(loginByBD(data["nickname"], data["password"]) == 1):
        req = "{\"type\": \"login\", \"login\": 1}"
        loginPlayers[websocket] = data["nickname"]
        print(len(loginPlayers))
        p = Player(websocket, data["nickname"])
        print(str(p.round_played))
        await getLobbyList(websocket)
=======
from collections import deque

from Server.ActionManager import ActionManager

actionManager = ActionManager()
messageQueue = deque()
gameLoopAlive = 0

async def consumer(websocket, message):
    await actionManager.chackMessage(websocket, message, messageQueue)

async def consumer_handler(websocket, path):
    async for message in websocket:
        try:
            await consumer(websocket, message)
        finally:
            actionManager.playerManager.disconnect(websocket, actionManager.lobbyManager, messageQueue)

async def game_loop():
    global gameLoopAlive
    if(gameLoopAlive == 0):
        gameLoopAlive = 1
        await actionManager.lobbyManager.update()
        await asyncio.sleep(1)
        gameLoopAlive = 0
>>>>>>> working
    else:
        await asyncio.sleep(1)

async def producer_handler(websocket, path):
    global gameLoopAlive
    while True:
        await game_loop()
        while(len(messageQueue) != 0):
            package = messageQueue.popleft()
            await package.socket.send(package.message)

async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

start_server = websockets.serve(handler, "127.0.0.1", 5678)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
