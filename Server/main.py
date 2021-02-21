import asyncio
import websockets
import json
import time

from collections import deque

from Server.PlayerManager import PlayerManager
from Server.LobbyManager import LobbyManager
from Server.GameManager import GameManager
from Server.Package import Package
from Server.models import *


lobbyManager = LobbyManager()
playerManager = PlayerManager()
gameManager = GameManager()

messageQueues = deque()
gameLoopAlive = 0

def registrationInDB(login,pas):
    try:
        p = PlayerModel(p_name = login, p_pas_hash = pas, is_relative=True)
        p.save()
    except Exception as error:
        print('A New Exception occured: ', str(error))

async def login(websocket, data):
    await playerManager.login(websocket, data["nickname"], data["password"], lobbyManager, messageQueues)

def lobbyAction(websocket, data):
    if(data["action"] == "create"):
        lobbyManager.create(websocket, playerManager, messageQueues)
    elif (data["action"] == "connect"):
        lobbyManager.connectLobby(websocket, data["id"], playerManager, messageQueues)
    elif (data["action"] == "start"):
        lobbyManager.gameStart(0, messageQueues)

async def gameAction(websocket, data):
    if(data["action"] == "reqestHints"):
        await gameManager.sendHits(websocket, data)
    else:
        await websocket.send("")

async def chackMessage(websocket, message):
    data = json.loads(message)
    if(data["type"] == "login"):
        await login(websocket, data)
    elif(data["type"] == "lobby"):
        lobbyAction(websocket, data)
    elif (data["type"] == "game"):
        await gameAction(websocket, data)
    else:
        await websocket.send("")

async def lobbyUpdate():
    print(1)
    await asyncio.sleep(1)

async def consumer(websocket, message):
    await chackMessage(websocket, message)

async def consumer_handler(websocket, path):
    async for message in websocket:
        print("Consume")
        await consumer(websocket, message)

async def game_loop():
    global gameLoopAlive
    if(gameLoopAlive == 0):
        gameLoopAlive = 1
        await lobbyManager.update()
        await asyncio.sleep(1)
        gameLoopAlive = 0
        print(time.time())
    else:
        await asyncio.sleep(1)

async def producer_handler(websocket, path):
    global gameLoopAlive
    while True:
        await game_loop()

        while(len(messageQueues) != 0):
            package = messageQueues.popleft()
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
