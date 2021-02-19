import asyncio
import websockets
import json

from Server.PlayerManager import PlayerManager
from Server.LobbyManager import LobbyManager
from Server.GameManager import GameManager
from Server.models import *
from Server.Player import Player
from Server.Question import Qestion

lobbyManager = LobbyManager()
playerManager = PlayerManager()
gameManager = GameManager()

def registrationInDB(login,pas):
    try:
        p = PlayerModel(p_name = login, p_pas_hash = pas, is_relative=True)
        p.save()
    except Exception as error:
        print('A New Exception occured: ', str(error))

async def login(websocket, data):
    await playerManager.login(websocket, data["nickname"], data["password"], lobbyManager)

async def lobbyAction(websocket, data):
    if(data["action"] == "create"):
        await lobbyManager.create(websocket, playerManager)
    elif (data["action"] == "connect"):
        await lobbyManager.connectLobby(websocket, data["id"], playerManager)
    elif (data["action"] == "start"):
        await lobbyManager.lobbyList[data["id"]].start()
    else:
        await websocket.send("")

async def gameAction(websocket, data):
    if(data["action"] == "reqestHints"):
        await gameManager.sendHits(websocket, data)
    else:
        await websocket.send("")

async def chackMessage(websocket, data):
    if(data["type"] == "login"):
        await login(websocket, data)
    elif(data["type"] == "lobby"):
        await lobbyAction(websocket, data)
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
    await lobbyManager.update()
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
