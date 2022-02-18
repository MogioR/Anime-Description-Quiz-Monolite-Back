import asyncio
import websockets
from models import *
from collections import deque
import json
import threading

from ActionManager import ActionManager

from bs4 import BeautifulSoup
import requests
import re

actionManager = ActionManager()
messageQueue = deque()
gameLoopAlive = 0


async def consumer(websocket, message):
    await actionManager.checkMessage(websocket, message, messageQueue)


async def consumer_handler(websocket, path):
    async for message in websocket:
        print(websocket, message)
        try:
            await consumer(websocket, message)
        except Exception as e:
            print("disconnect", e)
            actionManager.disconnect(websocket, messageQueue)

        if websocket.closed:
            print("DISCONNECT1")
            actionManager.disconnect(websocket, messageQueue)


async def game_loop():
    global gameLoopAlive
    if gameLoopAlive == 0:
        gameLoopAlive = 1
        await actionManager.lobbyManager.update(messageQueue)
        await asyncio.sleep(1)
        gameLoopAlive = 0
    else:
        await asyncio.sleep(1)


async def producer_handler():
    global gameLoopAlive
    while True:
        await game_loop()
        while len(messageQueue) != 0:
            package = messageQueue.popleft()
            print(package.socket, package.message)
            try:
                await package.socket.send(package.message)
            except Exception as e:
                print("Error", e)


async def close_handler(websocket):
    await websocket.wait_closed()
    print(websocket, 'DISCONNECTED')
    actionManager.disconnect(websocket, messageQueue)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path)
    )
    producer_task = asyncio.ensure_future(
        producer_handler()
    )
    wait_close_task = asyncio.ensure_future(
        close_handler(websocket)
    )
    done, pending = await asyncio.wait(
        [consumer_task, producer_task, wait_close_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


def filldb(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')


start_server = websockets.serve(handler, "192.168.1.122", 5678)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()


# def getUnspoilerDescription(str):
#     i=0
#     end = len(str)-3
#     ret = ""
#     spoil = False
#
#     while i < end:
#         if str[i] == '<' and str[i+1] == 's' and str[i+2] == 'p' and str[i+3] == '>':
#             i+=4
#             spoil = not spoil
#             continue
#
#         if not spoil:
#             ret += str[i]
#         else:
#             ret += '*'
#
#         i+=1
#
#     return ret
#
#
