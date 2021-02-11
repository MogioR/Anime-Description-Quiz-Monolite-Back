import asyncio
import datetime
import random
import re
import psycopg2
import websockets
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
        loginPlayers[websocket] = Player(websocket, data["nickname"])
        await getLobbyList(websocket)
    else:
        req = ""
    await websocket.send(req)

async def createLobby(websocket):
    print("Player " + loginPlayers.get(websocket).nickname + " create lobby!")
    lobbyList.append(Lobby(loginPlayers.get(websocket).nickname, websocket, 8))
    req = "{\"type\": \"lobby\", \"action\": \"enter\"}"
    await websocket.send(req)
    await getPlayerList(websocket, lobbyList[-1])

async def connectLobby(websocket, message):
    data = json.loads(message)
    print("Player " + loginPlayers.get(websocket).nickname + ' connect to lobby ' + str(data["id"])+'!')
    lobbyList[data["id"]].connect(loginPlayers.get(websocket).nickname, websocket)
    req = "{\"type\": \"lobby\", \"action\": \"enter\"}"
    await websocket.send(req)
    await notifyNewPlayerList(lobbyList[data["id"]])

async def notifyNewPlayerList(lobby):
    for socket in lobby.sockets:
        await getPlayerList(socket, lobby)

async def getLobbyList(websocket):
    print("Player " + loginPlayers.get(websocket).nickname + " get lobbyes!")
    req = "{\"type\": \"lobbyList\", \"lobbyes\": ["
    i = 0
    for lobby in lobbyList:
        req+="{\"host\": \"" + lobby.host + "\",\"size\": "+ str(lobby.size) + ",\"occupancy\":" + str(lobby.occupancy) + ",\"id\":" + str(i) + " } "
        i+=1
        if(i < len(lobbyList)):
            req += ','
    req+="]}"
    await websocket.send(req)

async def getPlayerList(websocket, lobby):
    print("Player " + loginPlayers.get(websocket).nickname + " get lobby players!")
    req = "{\"type\": \"lobby\", \"action\": \"getPlayerList\", \"players\": ["
    i = 0
    for player in lobby.players:
        req += "\"" + player +"\""
        i += 1
        if (i < len(lobby.players)):
            req += ','
    req += "]}"
    await websocket.send(req)

async def lobbyAction(websocket, message):
    data = json.loads(message)
    if(data["action"] == "create"):
        await createLobby(websocket)
    elif (data["action"] == "connect"):
        await connectLobby(websocket, message)
    elif (data["action"] == "start"):
        #await asyncio.gather(asyncio.create_task(game(lobbyList[0])))
        await websocket.send("")
    else:
        await websocket.send("")

async def sendHits(websocket, data):
    print("Player " + loginPlayers.get(websocket).nickname + " try hint!" + str(len(data["data"])))
    if(len(data["data"]) >= minHintMaskSize):
        print("Player " + loginPlayers.get(websocket).nickname + " get hint!")
        req = "{\"type\": \"game\", \"action\": \"newHints\", \"hints\": ["
        hints = getAnimeBySubName(data["data"])
        i = 0
        for h in hints:
            req += "\"" + str(hints[i].f_name) + "\""
            i += 1
            if (i < len(hints)):
                req += ','
        req += "]}"
        await websocket.send(req)
    else:
        await websocket.send("")

async def gameAction(websocket, data):
    print("gameMessage")
    if(data["action"] == "reqestHints"):
        await sendHits(websocket, data)
    else:
        await websocket.send("")

async def chackMessage(websocket, message):
    print("message")
    data = json.loads(message)
    if(data["type"] == "login"):
        await login(websocket, message)
    elif(data["type"] == "lobby"):
        await lobbyAction(websocket, message)
    elif (data["type"] == "game"):
        await gameAction(websocket, data)
    else:
        await websocket.send("")

async def lobbyUpdate():
    print(1)
    await asyncio.sleep(1)

async def time(websocket, path):
    while True:
        async for message in websocket:
            await chackMessage(websocket, message)


async def consumer(websocket, message):
    await chackMessage(websocket, message)

async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(websocket, message)

async def game_loop():
    await asyncio.sleep(1)
    return ""

async def producer_handler(websocket, path):
    while True:
        message = await game_loop()
        if len(message) != 0:
            await websocket.send(message)

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
