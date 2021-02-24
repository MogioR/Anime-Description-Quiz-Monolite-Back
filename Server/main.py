import asyncio
import websockets
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
        actionManager.lobbyManager.update(messageQueue)
        await asyncio.sleep(1)
        gameLoopAlive = 0
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
